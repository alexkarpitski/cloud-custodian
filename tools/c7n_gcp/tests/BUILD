load("@rules_python//python:defs.bzl", "py_library")
load("//:c7n_py_test.bzl", "c7n_py_test")

package(default_visibility = ["//visibility:private"])

py_library(
    name = "gcp_common",
    testonly = True,
    srcs = [
        "gcp_common.py",
        "recorder.py",
    ],
    imports = [".."],
    deps = [
        "//c7n:testing",
        "//tools/c7n_azure/tests_azure:azure_common",  # registering c7n_azure as an available provider
        "//tools/c7n_gcp/c7n_gcp:client",
        "//tools/c7n_gcp/c7n_gcp:handler",  # for test_mu_gcp.py only
        "//tools/c7n_kube/tests:common_kube",  # registering c7n_kube as an available provider
    ],
)

[c7n_py_test(
    name = test_file[:-3],
    srcs = [test_file],
    data = glob(["data/**"]) + ["//:.bazel-coveragerc"],
    imports = ["."],
    deps = [":gcp_common"],
) for test_file in glob(["test_*.py"])]

# bazel test //tools/c7n_gcp/tests
test_suite(
    name = "tests",
)
