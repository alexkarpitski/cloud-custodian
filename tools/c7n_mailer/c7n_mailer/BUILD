package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_library")
load("@mailer_py_deps//:requirements.bzl", "requirement")
load("@rules_python//experimental/python:wheel.bzl", "py_package")

py_package(
    name = "c7n_mailer_pkg",
    deps = [
        "c7n_mailer_cli",
    ],
)

py_library(
    name = "c7n_mailer_requirements",
    deps = [
        requirement("boto3"),
        requirement("botocore"),
        requirement("docutils"),
        requirement("jmespath"),
        requirement("vcversioner"),
        requirement("Jinja2"),
        requirement("jsonschema"),
        requirement("ruamel.yaml"),
        requirement("six"),
        requirement("pyasn1"),
        requirement("python_http_client"),
        requirement("markupsafe"),
        requirement("datadog"),
        requirement("sendgrid"),
        requirement("redis"),
        requirement("ldap3"),
    ],
)

py_library(
    name = "c7n_mailer_core_deps",
    srcs = [
        "__init__.py",
        "datadog_delivery.py",
        "deploy.py",
        "email_delivery.py",
        "handle.py",
        "ldap_lookup.py",
        "replay.py",
        "slack_delivery.py",
        "smtp_delivery.py",
        "sns_delivery.py",
        "splunk_delivery.py",
        "sqs_queue_processor.py",
        "utils.py",
        "utils_email.py",
    ],
    deps = [
        ":c7n_mailer_requirements",
    ],
)

py_library(
    name = "c7n_mailer_azure",
    deps = [
        "//tools/c7n_mailer/c7n_mailer/azure_mailer",
        requirement("azure-common"),  # azure.profiles
        requirement("azure-keyvault"),
    ],
)

py_library(
    name = "c7n_mailer_cli",
    srcs = ["cli.py"],
    data = glob(["msg-templates/*.j2"]),
    deps = [
        ":c7n_mailer_azure",
        ":c7n_mailer_core_deps",
    ],
)
