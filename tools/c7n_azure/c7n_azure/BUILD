package(default_visibility = [
    "//:__pkg__",
    "//tests:__pkg__",
    "//tools/c7n_azure/c7n_azure/actions:__pkg__",
    "//tools/c7n_azure/c7n_azure/resources:__pkg__",
    "//tools/c7n_azure/tests_azure:__pkg__",
    "//tools/c7n_kube/tests:__pkg__",
    "//tools/c7n_mailer/tests:__pkg__",
    "//tools/c7n_sphinxext/c7n_sphinxext:__pkg__",
])

load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//experimental/python:wheel.bzl", "py_package")
load("@azure_py_deps//:requirements.bzl", "requirement")

py_library(
    name = "c7n_azure_lib",
    deps = [
        ":function",
        requirement("azure-mgmt-eventgrid"),
    ],
)

py_package(
    name = "azure_pkg",
    deps = [
        ":c7n_azure_lib",
        ":entry",
    ],
)

py_library(
    name = "actions",
    deps = ["//tools/c7n_azure/c7n_azure/actions"],
)

py_library(
    name = "container_host",
    deps = ["//tools/c7n_azure/c7n_azure/container_host"],
)

py_library(
    name = "provisioning",
    deps = ["//tools/c7n_azure/c7n_azure/provisioning"],
)

py_library(
    name = "resources",
    deps = ["//tools/c7n_azure/c7n_azure/resources"],
)

py_library(
    name = "azure_events",
    srcs = ["azure_events.py"],
    deps = [
        ":session",
    ],
)

py_library(
    name = "constants",
    srcs = ["constants.py"],
)

py_library(
    name = "entry",
    srcs = ["entry.py"],
    deps = [
        ":container_host",
        ":output",
        ":policy",
        ":provider",
    ],
)

py_library(
    name = "filters",
    srcs = ["filters.py"],
    deps = [
        ":tags",
        ":utils",
        requirement("azure-mgmt-costmanagement"),
        requirement("azure-mgmt-policyinsights"),
        requirement("python-dateutil"),
        requirement("msrest"),
    ],
)

py_library(
    name = "function",
    srcs = ["function.py"],
    deps = [
        ":entry",
        ":handler",
        ":utils",
        requirement("azure-functions"),
    ],
)

py_library(
    name = "function_package",
    srcs = ["function_package.py"],
    deps = [
        ":constants",
        ":session",
        requirement("requests"),
        "//c7n:mu",
        "//c7n:utils",
    ],
)

py_library(
    name = "functionapp_utils",
    srcs = ["functionapp_utils.py"],
    deps = [
        ":constants",
        ":provisioning",
        ":session",
        ":storage_utils",
        ":utils",
        "//c7n:utils",
    ],
)

py_library(
    name = "handler",
    srcs = ["handler.py"],
    deps = [
        ":provider",
        requirement("azure-common"),
        requirement("msrestazure"),
        "//c7n:config",
        "//c7n:policy",
        "//c7n:resources",
        "//c7n:structure",
        "//c7n:utils",
    ],
)

py_library(
    name = "output",
    srcs = ["output.py"],
    deps = [
        ":storage_utils",
        ":utils",
        "//c7n:output",
        "//c7n:utils",
        requirement("applicationinsights"),
        requirement("azure-common"),
    ],
)

py_library(
    name = "policy",
    srcs = ["policy.py"],
    deps = [
        ":azure_events",
        ":constants",
        ":function_package",
        ":functionapp_utils",
        ":resources",
        ":storage_utils",
        ":utils",
        requirement("azure-mgmt-eventgrid"),
        "//c7n:actions",
        "//c7n:exceptions",
        "//c7n:mu",
        "//c7n:policy",
        "//c7n:utils",
    ],
)

py_library(
    name = "provider",
    srcs = ["provider.py"],
    deps = [
        ":resources",
        ":session",
        "//c7n:provider",
        "//c7n:registry",
        "//c7n:utils",
    ],
)

py_library(
    name = "query",
    srcs = ["query.py"],
    deps = [
        ":actions",
        ":constants",
        ":filters",
        # ":provider", # avoiding cyclic dependency
        requirement("azure-mgmt-resourcegraph"),
        "//c7n:actions",
        "//c7n:exceptions",
        "//c7n:filters",
        "//c7n:manager",
        "//c7n:query",
        "//c7n:utils",
    ],
)

py_library(
    name = "session",
    srcs = ["session.py"],
    deps = [
        ":constants",
        # ":utils", # avoiding cyclic dependency
        requirement("azure"),
        requirement("azure-cli-core"),
        requirement("azure-common"),
        requirement("azure-keyvault"),
        requirement("msrest"),
        requirement("msrestazure"),
        requirement("requests"),
    ],
)

py_library(
    name = "storage_utils",
    srcs = ["storage_utils.py"],
    deps = [
        ":constants",
        requirement("azure-common"),
        requirement("azure-storage-common"),
        requirement("azure-storage-blob"),
        requirement("azure-storage-queue"),
    ],
)

py_library(
    name = "tags",
    srcs = ["tags.py"],
    deps = [
        ":utils",
        requirement("azure-mgmt-resource"),
    ],
)

py_library(
    name = "utils",
    srcs = ["utils.py"],
    deps = [
        ":constants",
        ":session",
        requirement("azure-graphrbac"),
        requirement("azure-keyvault"),
        requirement("azure-mgmt-managementgroups"),
        requirement("azure-mgmt-web"),
        requirement("msrestazure"),
        requirement("netaddr"),
        "//c7n:utils",
    ],
)
