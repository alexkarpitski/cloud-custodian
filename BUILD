package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_binary")
load("//:py_wheel_extension.bzl", "py_wheel_entry_points_ext")
load("@rules_python//experimental/python:wheel.bzl", "py_package", "py_wheel")
load("@setup_versions//:versions.bzl", "setup_version")

exports_files([
    ".bazel-coveragerc",
])

sh_binary(
    name = "run-add-ep-script",
    srcs = ["add-entry-points-to-wheel.sh"],
    data = ["file_hash.py"],
)

# bazel build c7n_wheel
# To install a generated whl-file into your env: pip install <WORKSPACE_directory>/bazel-bin/<file_name>.whl
py_wheel(
    name = "c7n_wheel",
    console_scripts = {
        "custodian": "c7n.cli:main",
    },
    distribution = "c7n",
    version = setup_version("//:setup.py"),
    deps = [
        "//c7n:core_pkg",
    ],
)

# bazel build c7n_azure_wheel
# To install a generated whl-file into your env: pip install <WORKSPACE_directory>/bazel-bin/<file_name>.whl
# Installing c7n first is required for Custodian to work.
py_wheel_entry_points_ext(
    name = "c7n_azure_wheel",
    distribution = "c7n_azure",
    entry_points = {
        "custodian.resources": [
            "azure = c7n_azure.entry:initialize_azure",
        ],
    },
    strip_path_prefixes = [
        "tools/c7n_azure/",
    ],
    version = setup_version("//tools/c7n_azure:setup.py"),
    deps = [
        "//tools/c7n_azure/c7n_azure:azure_pkg",
    ],
)

# bazel build c7n_gcp_wheel
# To install a generated whl-file into your env: pip install <WORKSPACE_directory>/bazel-bin/<file_name>.whl
# Installing c7n first is required for Custodian to work.
py_wheel_entry_points_ext(
    name = "c7n_gcp_wheel",
    distribution = "c7n_gcp",
    entry_points = {
        "custodian.resources": [
            "gcp = c7n_gcp.entry:initialize_gcp",
        ],
    },
    strip_path_prefixes = [
        "tools/c7n_gcp/",
    ],
    version = setup_version("//tools/c7n_gcp:setup.py"),
    deps = [
        "//tools/c7n_gcp/c7n_gcp:gcp_pkg",
    ],
)

# bazel build c7n_kube_wheel
# To install a generated whl-file into your env: pip install <WORKSPACE_directory>/bazel-bin/<file_name>.whl
py_wheel_entry_points_ext(
    name = "c7n_kube_wheel",
    distribution = "c7n-kube",
    entry_points = {
        "custodian.resources": [
            "kube = c7n_kube.entry:initialize_kube",
        ],
    },
    strip_path_prefixes = [
        "tools/c7n_kube/",
    ],
    version = setup_version("//tools/c7n_kube:setup.py"),
    deps = [
        "//tools/c7n_kube/c7n_kube:c7n_kube_pkg",
    ],
)

# bazel build c7n_mailer_wheel
# To install a generated whl-file into your env: pip install <WORKSPACE_directory>/bazel-bin/<file_name>.whl
py_wheel(
    name = "c7n_mailer_wheel",
    console_scripts = {
        "c7n-mailer": "c7n_mailer.cli:main",
        "c7n-mailer-replay": "c7n_mailer.replay:main",
    },
    distribution = "c7n-mailer",
    strip_path_prefixes = [
        "tools/c7n_mailer/",
    ],
    version = setup_version("//tools/c7n_mailer:setup.py"),
    deps = [
        "//tools/c7n_mailer/c7n_mailer:c7n_mailer_pkg",
    ],
)

filegroup(
    name = "doc_rst_files",
    srcs = glob(
        ["docs/**/*"],
    ),
)

filegroup(
    name = "readme_files",
    srcs = [
        "tools/c7n_guardian/readme.md",
        "tools/c7n_logexporter/README.md",
        "tools/c7n_org/README.md",
        "tools/c7n_policystream/README.md",
        "tools/c7n_salactus/README.md",
        "tools/c7n_trailcreator/readme.md",
        "tools/cask/readme.md",
        "tools/omnissm/README.md",
        "tools/omnissm/assets/omnissm.svg",
        # tools/c7n_mailer/README.md' is invalid because 'tools/c7n_mailer' is a subpackage;
        # that's why we have to put the colon here: '//tools/c7n_mailer:README.md
        "//tools/c7n_mailer:README.md",
    ],
)
