# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

import json
import jmespath
import re

from datetime import datetime

from c7n.exceptions import PolicyValidationError
from c7n.utils import local_session, type_schema

from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo

from c7n.filters.offhours import OffHour, OnHour
from c7n.filters import ValueFilter

from google.cloud.storage import client


@resources.register('instance')
class Instance(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'instances'
        enum_spec = ('aggregatedList', 'items.*.instances[]', None)
        scope = 'project'
        name = id = 'name'
        labels = True
        default_report_fields = ['name', 'status', 'creationTimestamp', 'machineType', 'zone']
        asset_type = "compute.googleapis.com/Instance"

        @staticmethod
        def get(client, resource_info):
            # The api docs for compute instance get are wrong,
            # they spell instance as resourceId
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'zone': resource_info['zone'],
                        'instance': resource_info[
                            'resourceName'].rsplit('/', 1)[-1]})

        @staticmethod
        def get_label_params(resource, all_labels):
            path_param_re = re.compile('.*?/projects/(.*?)/zones/(.*?)/instances/(.*)')
            project, zone, instance = path_param_re.match(
                resource['selfLink']).groups()
            return {'project': project, 'zone': zone, 'instance': instance,
                    'body': {
                        'labels': all_labels,
                        'labelFingerprint': resource['labelFingerprint']
                    }}


@Instance.filter_registry.register('offhour')
class InstanceOffHour(OffHour):

    def get_tag_value(self, instance):
        return instance.get('labels', {}).get(self.tag_key, False)


@Instance.filter_registry.register('onhour')
class InstanceOnHour(OnHour):

    def get_tag_value(self, instance):
        return instance.get('labels', {}).get(self.tag_key, False)


@Instance.filter_registry.register('invalid-network')
class InvalidNetworkFilter(ValueFilter):
    """
    Instance's attached network interfaces short names are compared to the target
    that is stored at the specified jmespath in a file in a bucket.
    The filter returns the ones that do not match the target ('invalid' networks).
    Usage example:
      filters:
      - type: invalid-network
        bucket-name: bucket-id
        config-path: some/path/to.json
        valid-network-jmespath: path.to.network.key
    """
    bucket_name_key = 'bucket-name'
    config_path_key = 'config-path'
    valid_network_jmespath_key = 'valid-network-jmespath'
    schema = type_schema('invalid-network', rinherit={
        'type': 'object',
        'additionalProperties': False,
        'required': ['type'],
        'properties': {
            bucket_name_key: {'$ref': '#/definitions/filters_common/value'},
            config_path_key: {'$ref': '#/definitions/filters_common/value'},
            valid_network_jmespath_key: {'$ref': '#/definitions/filters_common/value'},
        },
    })
    required_keys = [bucket_name_key, config_path_key, valid_network_jmespath_key]

    def validate(self):
        for required_key in InvalidNetworkFilter.required_keys:
            if required_key not in self.data:
                raise PolicyValidationError("missing required key: %s" % required_key)

    def process(self, resources, event=None):
        valid_network = self.get_valid_network()
        invalid_network_instances = []
        for resource in resources:
            is_invalid_network_instance = False
            if 'networkInterfaces' in resource:
                for network_interface in resource['networkInterfaces']:
                    actual_network = re.match('.*/(.*?)$', network_interface['network']).group(1)
                    if actual_network != valid_network:
                        is_invalid_network_instance = True
                        break
            if is_invalid_network_instance:
                invalid_network_instances.append(resource)
        return invalid_network_instances

    def get_valid_network(self):
        storage_client = client.Client()
        bucket_object_text = storage_client.bucket(
            self.data[InvalidNetworkFilter.bucket_name_key]
        ).get_blob(self.data[InvalidNetworkFilter.config_path_key]).download_as_text()
        bucket_object_json = json.loads(bucket_object_text)
        valid_network = jmespath.search(
            self.data[InvalidNetworkFilter.valid_network_jmespath_key], bucket_object_json)
        return valid_network


class InstanceAction(MethodAction):

    def get_resource_params(self, model, resource):
        path_param_re = re.compile('.*?/projects/(.*?)/zones/(.*?)/instances/(.*)')
        project, zone, instance = path_param_re.match(resource['selfLink']).groups()
        return {'project': project, 'zone': zone, 'instance': instance}


@Instance.action_registry.register('start')
class Start(InstanceAction):

    schema = type_schema('start')
    method_spec = {'op': 'start'}
    attr_filter = ('status', ('TERMINATED',))


@Instance.action_registry.register('stop')
class Stop(InstanceAction):

    schema = type_schema('stop')
    method_spec = {'op': 'stop'}
    attr_filter = ('status', ('RUNNING',))


@Instance.action_registry.register('delete')
class Delete(InstanceAction):

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}


@Instance.action_registry.register('detach-disks')
class DetachDisks(MethodAction):
    """
    `Detaches <https://cloud.google.com/compute/docs/reference/rest/v1/instances/detachDisk>`_
    all disks from instance. The action does not specify any parameters.

    It may be useful to be used before deleting instances to not delete disks
    that are set to auto delete.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-instance-detach-disks
            resource: gcp.instance
            filters:
              - type: value
                key: name
                value: instance-template-to-detahc
            actions:
              - type: detach-disks
    """
    schema = type_schema('detach-disks')
    attr_filter = ('status', ('TERMINATED',))
    method_spec = {'op': 'detachDisk'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/zones/(.*?)/instances/(.*)')

    def validate(self):
        pass

    def process_resource_set(self, client, model, resources):
        for resource in resources:
            self.process_resource(client, resource)

    def process_resource(self, client, resource):
        op_name = 'detachDisk'

        project, zone, instance = self.path_param_re.match(
            resource['selfLink']).groups()

        base_params = {'project': project, 'zone': zone, 'instance': instance}
        for disk in resource.get('disks', []):
            params = dict(base_params, deviceName=disk['deviceName'])
            self.invoke_api(client, op_name, params)


@Instance.action_registry.register('create-machine-image')
class CreateMachineImage(MethodAction):
    """
    `Creates <https://cloud.google.com/compute/docs/reference/rest/beta/machineImages/insert>`_
     Machine Image from instance.

    The `name_format` specifies name of image in python `format string <https://pyformat.info/>`

    Inside format string there are defined variables:
      - `now`: current time
      - `instance`: whole instance resource

    Default name format is `{instance[name]}`

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-create-machine-image
            resource: gcp.instance
            filters:
              - type: value
                key: name
                value: instance-create-to-make-image
            actions:
              - type: create-machine-image
                name_format: "{instance[name]:.50}-{now:%Y-%m-%d}"

    """
    schema = type_schema('create-machine-image', name_format={'type': 'string'})
    method_spec = {'op': 'insert'}
    permissions = ('compute.machineImages.create',)

    def get_resource_params(self, model, resource):
        path_param_re = re.compile('.*?/projects/(.*?)/zones/(.*?)/instances/(.*)')
        project, _, _ = path_param_re.match(resource['selfLink']).groups()
        name_format = self.data.get('name_format', '{instance[name]}')
        name = name_format.format(instance=resource, now=datetime.now())

        return {'project': project, 'sourceInstance': resource['selfLink'], 'body': {'name': name}}

    def get_client(self, session, model):
        return session.client(model.service, "beta", "machineImages")


@resources.register('image')
class Image(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'images'
        name = id = 'name'
        default_report_fields = [
            "name", "description", "sourceType", "status", "creationTimestamp",
            "storageLocation", "diskSizeGb", "family"]
        asset_type = "compute.googleapis.com/Image"

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'resourceId': resource_info['image_id']})


@Image.action_registry.register('delete')
class DeleteImage(MethodAction):

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    attr_filter = ('status', ('READY'))
    path_param_re = re.compile('.*?/projects/(.*?)/global/images/(.*)')

    def get_resource_params(self, m, r):
        project, image_id = self.path_param_re.match(r['selfLink']).groups()
        return {'project': project, 'image': image_id}


@resources.register('disk')
class Disk(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'disks'
        scope = 'zone'
        enum_spec = ('aggregatedList', 'items.*.disks[]', None)
        name = id = 'name'
        labels = True
        default_report_fields = ["name", "sizeGb", "status", "zone"]
        asset_type = "compute.googleapis.com/Disk"

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'zone': resource_info['zone'],
                        'resourceId': resource_info['disk_id']})

        @staticmethod
        def get_label_params(resource, all_labels):
            path_param_re = re.compile('.*?/projects/(.*?)/zones/(.*?)/disks/(.*)')
            project, zone, instance = path_param_re.match(
                resource['selfLink']).groups()
            return {'project': project, 'zone': zone, 'resource': instance,
                    'body': {
                        'labels': all_labels,
                        'labelFingerprint': resource['labelFingerprint']
                    }}


@Disk.action_registry.register('snapshot')
class DiskSnapshot(MethodAction):
    """
    `Snapshots <https://cloud.google.com/compute/docs/reference/rest/v1/disks/createSnapshot>`_
    disk.

    The `name_format` specifies name of snapshot in python `format string <https://pyformat.info/>`

    Inside format string there are defined variables:
      - `now`: current time
      - `disk`: whole disk resource

    Default name format is `{disk.name}`

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-disk-snapshot
            resource: gcp.disk
            filters:
              - type: value
                key: name
                value: disk-7
            actions:
              - type: snapshot
                name_format: "{disk[name]:.50}-{now:%Y-%m-%d}"
    """
    schema = type_schema('snapshot', name_format={'type': 'string'})
    method_spec = {'op': 'createSnapshot'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/zones/(.*?)/disks/(.*)')
    attr_filter = ('status', ('RUNNING', 'READY'))

    def get_resource_params(self, model, resource):
        project, zone, resourceId = self.path_param_re.match(resource['selfLink']).groups()
        name_format = self.data.get('name_format', '{disk[name]}')
        name = name_format.format(disk=resource, now=datetime.now())

        return {
            'project': project,
            'zone': zone,
            'disk': resourceId,
            'body': {
                'name': name,
                'labels': resource.get('labels', {}),
            }
        }


@Disk.action_registry.register('delete')
class DiskDelete(MethodAction):

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/zones/(.*?)/disks/(.*)')
    attr_filter = ('status', ('RUNNING', 'READY'))

    def get_resource_params(self, m, r):
        project, zone, resourceId = self.path_param_re.match(r['selfLink']).groups()
        return {
            'project': project,
            'zone': zone,
            'disk': resourceId,
        }


@resources.register('snapshot')
class Snapshot(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'snapshots'
        enum_spec = ('list', 'items[]', None)
        name = id = 'name'
        default_report_fields = ["name", "status", "diskSizeGb", "creationTimestamp"]
        asset_type = "compute.googleapis.com/Snapshot"

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'snapshot_id': resource_info['snapshot_id']})


@Snapshot.action_registry.register('delete')
class DeleteSnapshot(MethodAction):

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    attr_filter = ('status', ('READY', 'UPLOADING'))
    path_param_re = re.compile('.*?/projects/(.*?)/global/snapshots/(.*)')

    def get_resource_params(self, m, r):
        project, snapshot_id = self.path_param_re.match(r['selfLink']).groups()
        # Docs are wrong :-(
        # https://cloud.google.com/compute/docs/reference/rest/v1/snapshots/delete
        return {'project': project, 'snapshot': snapshot_id}


@resources.register('instance-template')
class InstanceTemplate(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/instanceTemplates"""
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'instanceTemplates'
        scope = 'zone'
        enum_spec = ('list', 'items[]', None)
        name = id = 'name'
        default_report_fields = [
            name, "description", "creationTimestamp",
            "properties.machineType", "properties.description"]
        asset_type = "compute.googleapis.com/InstanceTemplate"

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'instanceTemplate': resource_info['instance_template_name']})


@InstanceTemplate.action_registry.register('delete')
class InstanceTemplateDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/compute/docs/reference/rest/v1/instanceTemplates/delete>`_
    an Instance Template. The action does not specify any parameters.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-instance-template-delete
            resource: gcp.instance-template
            filters:
              - type: value
                key: name
                value: instance-template-to-delete
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        project, instance_template = re.match('.*/projects/(.*?)/.*/instanceTemplates/(.*)',
                                              r['selfLink']).groups()
        return {'project': project,
                'instanceTemplate': instance_template}


@resources.register('autoscaler')
class Autoscaler(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/autoscalers"""
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'autoscalers'
        name = id = 'name'
        enum_spec = ('aggregatedList', 'items.*.autoscalers[]', None)
        default_report_fields = [
            "name", "description", "status", "target", "recommendedSize"]
        asset_type = "compute.googleapis.com/Autoscaler"

        @staticmethod
        def get(client, resource_info):
            project, zone, autoscaler = re.match(
                'projects/(.*?)/zones/(.*?)/autoscalers/(.*)',
                resource_info['resourceName']).groups()

            return client.execute_command(
                'get', {'project': project,
                        'zone': zone,
                        'autoscaler': autoscaler})


@Autoscaler.action_registry.register('set')
class AutoscalerSet(MethodAction):
    """
    `Patches <https://cloud.google.com/compute/docs/reference/rest/v1/autoscalers/patch>`_
    configuration parameters for the autoscaling algorithm.

    The `coolDownPeriodSec` specifies the number of seconds that the autoscaler
    should wait before it starts collecting information from a new instance.

    The `cpuUtilization.utilizationTarget` specifies the target CPU utilization that the
    autoscaler should maintain.

    The `loadBalancingUtilization.utilizationTarget` specifies fraction of backend capacity
    utilization (set in HTTP(S) load balancing configuration) that autoscaler should maintain.

    The `minNumReplicas` specifies the minimum number of replicas that the autoscaler can
    scale down to.

    The `maxNumReplicas` specifies the maximum number of instances that the autoscaler can
    scale up to.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-autoscaler-set
            resource: gcp.autoscaler
            filters:
              - type: value
                key: name
                value: instance-group-2
            actions:
              - type: set
                coolDownPeriodSec: 20
                cpuUtilization:
                  utilizationTarget: 0.7
                loadBalancingUtilization:
                  utilizationTarget: 0.7
                minNumReplicas: 1
                maxNumReplicas: 4
    """
    schema = type_schema('set',
                         **{
                             'coolDownPeriodSec': {
                                 'type': 'integer',
                                 'minimum': 15
                             },
                             'cpuUtilization': {
                                 'type': 'object',
                                 'required': ['utilizationTarget'],
                                 'properties': {
                                     'utilizationTarget': {
                                         'type': 'number',
                                         'exclusiveMinimum': 0,
                                         'maximum': 1
                                     }
                                 },
                             },
                             'loadBalancingUtilization': {
                                 'type': 'object',
                                 'required': ['utilizationTarget'],
                                 'properties': {
                                     'utilizationTarget': {
                                         'type': 'number',
                                         'exclusiveMinimum': 0,
                                         'maximum': 1
                                     }
                                 }
                             },
                             'maxNumReplicas': {
                                 'type': 'integer',
                                 'exclusiveMinimum': 0
                             },
                             'minNumReplicas': {
                                 'type': 'integer',
                                 'exclusiveMinimum': 0
                             }
                         })
    method_spec = {'op': 'patch'}
    path_param_re = re.compile('.*?/projects/(.*?)/zones/(.*?)/autoscalers/(.*)')
    method_perm = 'update'

    def get_resource_params(self, model, resource):
        project, zone, autoscaler = self.path_param_re.match(resource['selfLink']).groups()
        body = {}

        if 'coolDownPeriodSec' in self.data:
            body['coolDownPeriodSec'] = self.data['coolDownPeriodSec']

        if 'cpuUtilization' in self.data:
            body['cpuUtilization'] = self.data['cpuUtilization']

        if 'loadBalancingUtilization' in self.data:
            body['loadBalancingUtilization'] = self.data['loadBalancingUtilization']

        if 'maxNumReplicas' in self.data:
            body['maxNumReplicas'] = self.data['maxNumReplicas']

        if 'minNumReplicas' in self.data:
            body['minNumReplicas'] = self.data['minNumReplicas']

        result = {'project': project,
                  'zone': zone,
                  'autoscaler': autoscaler,
                  'body': {
                      'autoscalingPolicy': body
                  }}

        return result
