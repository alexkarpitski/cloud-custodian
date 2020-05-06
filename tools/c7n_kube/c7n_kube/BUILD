package(default_visibility = [
    "//:__pkg__",
    "//tests:__pkg__",
    "//tools/c7n_kube/tests:__pkg__",
    "//tools/c7n_sphinxext/c7n_sphinxext:__pkg__",
])

load("@rules_python//python:defs.bzl", "py_library")
load("@kube_py_deps//:requirements.bzl", "all_requirements", "requirement")
load("@rules_python//experimental/python:wheel.bzl", "py_package")

pip_deps = [i for i in all_requirements]

KUBE_PKG_DEPS = [
    "actions_core",
    "actions_labels",
    "actions_shared",
    "client",
    "entry",
    "filters",
    "provider",
    "query",
    "resources_apps",
    "resources_core",
    "resources_crd",
]

py_package(
    name = "c7n_kube_pkg",
    deps = KUBE_PKG_DEPS,
)

py_library(
    name = "kube_lib",
    deps = KUBE_PKG_DEPS,
)

py_library(
    name = "resource_lib",
    deps = [
        "resources_apps",
        "resources_core",
        "resources_crd",
    ],
)

py_library(
    name = "actions_core",
    srcs = [
        "actions/core.py",
    ],
    deps = [
        "//c7n:actions",
        "//c7n:exceptions",
        "//c7n:utils",
    ],
)

py_library(
    name = "actions_labels",
    srcs = [
        "actions/labels.py",
    ],
    deps = [
        ":actions_core",
        "//c7n:utils",
    ],
)

py_library(
    name = "actions_shared",
    srcs = [
        "actions/shared.py",
    ],
    deps = [
        ":actions_core",
        ":actions_labels",
        "//tools/c7n_kube/c7n_kube:provider",
    ],
)

py_library(
    name = "resources_apps",
    srcs = [
        "resources/apps/daemonset.py",
        "resources/apps/deployment.py",
        "resources/apps/replicaset.py",
        "resources/apps/statefulset.py",
    ],
    deps = [
        ":provider",
        ":query",
    ],
)

py_library(
    name = "resources_core",
    srcs = [
        "resources/core/configmap.py",
        "resources/core/namespace.py",
        "resources/core/node.py",
        "resources/core/pod.py",
        "resources/core/replicationcontroller.py",
        "resources/core/secret.py",
        "resources/core/service.py",
        "resources/core/serviceaccount.py",
        "resources/core/volume.py",
    ],
    deps = [
        ":provider",
        ":query",
    ],
)

py_library(
    name = "resources_crd",
    srcs = [
        "resources/crd.py",
        "resources/resource_map.py",
    ],
    deps = [
        ":provider",
        ":query",
    ],
)

py_library(
    name = "client",
    srcs = ["client.py"],
    deps = [
        requirement("kubernetes"),
    ],
)

py_library(
    name = "entry",
    srcs = ["entry.py"],
    deps = [
        ":actions_shared",
        ":resources_apps",
        ":resources_core",
        ":resources_crd",
    ] + pip_deps,
)

py_library(
    name = "filters",
    srcs = ["filters.py"],
)

py_library(
    name = "provider",
    srcs = ["provider.py"],
    deps = [
        ":client",
        "//c7n:provider",
        "//c7n:registry",
    ],
)

py_library(
    name = "query",
    srcs = ["query.py"],
    deps = [
        "//c7n:actions",
        "//c7n:exceptions",
        "//c7n:filters",
        "//c7n:manager",
        "//c7n:query",
        "//c7n:utils",
    ],
)
