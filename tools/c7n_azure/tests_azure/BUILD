load("@rules_python//python:defs.bzl", "py_library")
load("@azure_py_deps//:requirements.bzl", "requirement")
load("//:c7n_py_test.bzl", "c7n_py_test")
load("//:builddefs.bzl", "EXCLUDED_PKGS")

package(default_visibility = ["//visibility:private"])

py_library(
    name = "azure_common",
    testonly = True,
    srcs = [
        "azure_common.py",
    ],
    imports = [".."],
    srcs_version = "PY2AND3",
    visibility = ["//visibility:public"],
    deps = [
        ":azure_serializer",
        ":tools_tags",
        "//c7n:testing",
        "//tools/c7n_azure/c7n_azure:c7n_azure_lib",
        requirement("vcrpy-unittest"),
        requirement("coverage"),
    ],
)

py_library(
    name = "azure_serializer",
    testonly = True,
    srcs = ["azure_serializer.py"],
)

py_library(
    name = "tools_tags",
    srcs = ["tools_tags.py"],
    deps = [requirement("azure-mgmt-resourcegraph")],
)

[c7n_py_test(
    name = test_file[:-3],
    srcs = [test_file],
    data = glob([
        "cassettes/**",
        "data/**",
        "templates/**",
    ]) + ["//:.bazel-coveragerc"],
    excluded_pkgs = EXCLUDED_PKGS,
    imports = ["."],
    srcs_version = "PY2AND3",
    deps = [":azure_common"],
) for test_file in glob(["test_*.py"])]

# bazel test //tools/c7n_azure/tests_azure
test_suite(
    name = "tests_azure",
)
