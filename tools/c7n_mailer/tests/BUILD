load("//:c7n_py_test.bzl", "c7n_py_test")
load("@mailer_py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:private"])

py_library(
    name = "test_data",
    data = glob(["test-templates/*.j2"]),
)

py_library(
    name = "test_deps",
    srcs = ["common.py"],
    data = ["example.jinja"] + ["//:.bazel-coveragerc"],
    deps = [
        ":test_data",
        "//c7n",
        requirement("coverage"),
        requirement("mock"),
        requirement("fakeredis"),
        requirement("attrs"),
        requirement("pytest"),
        requirement("pyrsistent"),
        requirement("pluggy"),
        requirement("sortedcontainers"),
        requirement("pyasn1"),
        requirement("importlib_metadata"),
        requirement("zipp"),
        requirement("py"),
        requirement("packaging"),
        requirement("more_itertools"),
        requirement("jsonpointer"),
        requirement("jsonpatch"),
        requirement("python_http_client"),
        requirement("PyJWT"),
    ],
)

[c7n_py_test(
    name = test_file[:-3],
    srcs = [test_file],
    imports = [
        ".",
        "..",
        "../../c7n_azure/.",
    ],
    main = test_file,
    deps = [
        ":test_deps",
        "//tools/c7n_azure/c7n_azure:c7n_azure_lib",
        "//tools/c7n_mailer/c7n_mailer:c7n_mailer_cli",  # used instead of c7n_mailer_core_deps for testing cli as well
    ],
) for test_file in glob(
    include = ["test_*.py"],
)]

# bazel test //tools/c7n_mailer/tests
test_suite(
    name = "tests",
)
