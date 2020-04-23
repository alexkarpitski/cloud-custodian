load("@rules_python//python:defs.bzl", "py_library")
load("@pip_deps//:requirements.bzl", "requirement")
load("//:c7n_py_test.bzl", "c7n_py_test")
load("//:builddefs.bzl", "EXCLUDED_PKGS")
load("//:c7n_py_test.bzl", "get_chunk", "C7N_TESTS_CHUNKS")

package(default_visibility = ["//visibility:private"])

# TODO: get rid of excluded tests; remember to update bazel-test-excluded.yml
EXCLUDED_TESTS = [
    # 1) AssertionError: 'azure.vm' not found in 'resources:
    # c7n_azure is a stub with no resources available
    # 2) jsonschema.exceptions.SchemaError: {'anyOf': []} is not valid under any of the given schemas
    "test_cli.py",
    # 1) AssertionError: False is not true
    # self.assertTrue(content.endswith("hello world"))
    "test_output.py",
]

py_library(
    name = "c7n_tests_common",
    testonly = True,
    srcs = glob([
        "common.py",
        "zpill.py",
        "test_offhours.py",
        "test_s3.py",
    ]),
    data = glob(["data/**/*"]) + [":placebo_data.zip"] + ["//:.bazel-coveragerc"],
    imports = [
        "../tools/c7n_azure/.",
        "../tools/c7n_gcp/.",
        "../tools/c7n_kube/.",
    ],
    deps = [
        "//c7n:cli",
        "//c7n:commands",
        "//c7n:handler",
        "//c7n:reports",
        "//c7n:sqsexec",
        "//c7n:testing",
        "//c7n:ufuncs",
        "//tools/c7n_azure/c7n_azure:entry",
        "//tools/c7n_gcp/c7n_gcp:entry",
        "//tools/c7n_kube/c7n_kube:entry",
        requirement("coverage"),
        requirement("placebo"),
        requirement("flake8"),
        requirement("pytest-xdist"),
        requirement("pytest-cov"),
        requirement("twine"),
        requirement("tox"),
        requirement("toml"),
        requirement("six"),
        requirement("psutil"),
        requirement("jsonpointer"),
        requirement("fakeredis"),
        requirement("tabulate"),
        requirement("argcomplete"),
        requirement("vcrpy"),
        requirement("wrapt"),
    ],
)

[c7n_py_test(
    name = test_file[:-3],
    srcs = [test_file],
    excluded_pkgs = EXCLUDED_PKGS,
    tags = [get_chunk(test_file[:-3])],
    deps = [":c7n_tests_common"],
) for test_file in glob(
    include = ["test_*.py"],
    exclude = EXCLUDED_TESTS,
)]

# bazel test //tests
test_suite(
    name = "tests",
    tests = [c7n_chunk_name for c7n_chunk_name in C7N_TESTS_CHUNKS.keys()],
)

# bazel test //tests:{c7n_chunk_name}
[test_suite(
    name = c7n_chunk_name,
    tags = [c7n_chunk_name],
) for c7n_chunk_name in C7N_TESTS_CHUNKS.keys()]
