package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_library")
load("@pip_deps//:requirements.bzl", "all_requirements", "requirement")
load("@rules_python//experimental/python:wheel.bzl", "py_package")

c7n_core_requirements = [i for i in all_requirements]

py_library(
    name = "c7n_core_lib",
    deps = c7n_core_requirements,
)

py_package(
    name = "core_pkg",
    deps = [
        ":c7n",
        ":c7n_core_lib",
    ],
)

py_library(
    name = "c7n",
    srcs = [
        "__init__.py",
        "cache.py",
        "cli.py",
        "commands.py",
        "config.py",
        "credentials.py",
        "ctx.py",
        "cwe.py",
        "exceptions.py",
        "executor.py",
        "handler.py",
        "ipaddress.py",
        "loader.py",
        "log.py",
        "logs_support.py",
        "lookup.py",
        "manager.py",
        "mu.py",
        "output.py",
        "policy.py",
        "provider.py",
        "query.py",
        "registry.py",
        "resolver.py",
        "schema.py",
        "sqsexec.py",
        "structure.py",
        "tags.py",
        "testing.py",
        "utils.py",
        "version.py",
    ],
    deps = [
        "//c7n/actions",
        "//c7n/filters",
        "//c7n/reports",
        "//c7n/resources",
        "//c7n/ufuncs",
        requirement("argcomplete"),
        requirement("boto3"),
        requirement("botocore"),
        requirement("jsonschema"),
        requirement("PyYAML"),
        requirement("tabulate"),
        requirement("jsonpatch"),
        requirement("futures"),
        requirement("python-dateutil"),
        requirement("urllib3"),
        requirement("certifi"),
    ],
)

py_library(
    name = "cli",
    srcs = [
        "cli.py",
    ],
    deps = [
        ":commands",
        ":config",
        requirement("argcomplete"),
    ],
)

py_library(
    name = "commands",
    srcs = [
        "commands.py",
    ],
    deps = [
        ":config",
        ":exceptions",
        ":policy",
        ":provider",
        ":resources",
        ":schema",
        ":utils",
        requirement("six"),
        requirement("PyYAML"),
    ],
)

py_library(
    name = "sqsexec",
    srcs = [
        "sqsexec.py",
    ],
    deps = [
        ":utils",
    ],
)

py_library(
    name = "exceptions",
    srcs = [
        "exceptions.py",
    ],
)

py_library(
    name = "actions",
    deps = [
        "//c7n/actions",
    ],
)

py_library(
    name = "ufuncs",
    deps = [
        "//c7n/ufuncs",
    ],
)

py_library(
    name = "reports",
    deps = [
        "//c7n/reports",
    ],
)

py_library(
    name = "handler",
    srcs = [
        "handler.py",
    ],
    deps = [
        ":config",
        ":policy",
        ":resources",
        ":utils",
        requirement("boto3"),
    ],
)

py_library(
    name = "resources",
    deps = [
        ":actions",
        ":credentials",
        ":log",
        ":query",
        "//c7n/resources:resource_map",
        "//c7n/resources",
        requirement("botocore"),
        requirement("boto3"),
        requirement("aws_xray_sdk"),
        # transitive: aws_xray_sdk
        requirement("jsonpickle"),
    ],
)

py_library(
    name = "log",
    srcs = ["log.py"],
)

py_library(
    name = "tags",
    srcs = ["tags.py"],
)

py_library(
    name = "credentials",
    srcs = ["credentials.py"],
)

py_library(
    name = "query",
    srcs = ["query.py"],
    deps = [
        ":tags",
    ],
)

py_library(
    name = "filters",
    deps = [
        ":executor",
        ":manager",
        "//c7n/filters",
        # transitive: revisions.py
        requirement("jsonpatch"),
    ],
)

py_library(
    name = "manager",
    srcs = [
        "manager.py",
    ],
    deps = [
        ":cache",
    ],
)

py_library(
    name = "cache",
    srcs = [
        "cache.py",
    ],
)

py_library(
    name = "utils",
    srcs = [
        "utils.py",
    ],
    deps = [
        ":config",
        ":ipaddress",
    ],
)

py_library(
    name = "registry",
    srcs = [
        "registry.py",
    ],
)

py_library(
    name = "ipaddress",
    srcs = [
        "ipaddress.py",
    ],
)

py_library(
    name = "config",
    srcs = [
        "config.py",
    ],
)

py_library(
    name = "output",
    srcs = [
        "output.py",
    ],
    deps = [
        ":exceptions",
        ":registry",
        ":utils",
    ],
)

py_library(
    name = "version",
    srcs = [
        "version.py",
    ],
)

py_library(
    name = "ctx",
    srcs = [
        "ctx.py",
    ],
    deps = [
        ":output",
        ":utils",
        ":version",
    ],
)

py_library(
    name = "cwe",
    srcs = [
        "cwe.py",
    ],
    deps = [
        ":ctx",
    ],
)

py_library(
    name = "provider",
    srcs = [
        "provider.py",
    ],
    deps = [
        ":registry",
    ],
)

py_library(
    name = "policy",
    srcs = [
        "policy.py",
    ],
    deps = [
        ":cwe",
        ":mu",
        ":provider",
        ":resources",
        requirement("python-dateutil"),
    ],
)

py_library(
    name = "logs_support",
    srcs = [
        "logs_support.py",
    ],
)

py_library(
    name = "mu",
    srcs = [
        "mu.py",
    ],
    deps = [
        ":logs_support",
    ],
)

py_library(
    name = "executor",
    srcs = [
        "executor.py",
    ],
)

py_library(
    name = "loader",
    srcs = [
        "loader.py",
    ],
)

py_library(
    name = "lookup",
    srcs = [
        "lookup.py",
    ],
)

py_library(
    name = "schema",
    srcs = [
        "schema.py",
    ],
    deps = [
        ":filters",
        ":resolver",
        ":structure",
        requirement("jsonschema"),
        # transitive: jsonschema
        requirement("pyrsistent"),
    ],
)

py_library(
    name = "resolver",
    srcs = [
        "resolver.py",
    ],
)

py_library(
    name = "structure",
    srcs = [
        "structure.py",
    ],
)

py_library(
    name = "testing",
    testonly = True,
    srcs = [
        "testing.py",
    ],
    deps = [
        ":loader",
        ":policy",
        ":schema",
        ":lookup",
        requirement("mock"),
        requirement("pytest"),
        requirement("jmespath"),
        requirement("pyyaml"),
        # transitive: py_test
        requirement("packaging"),
        requirement("pluggy"),
        requirement("py"),
        requirement("attrs"),
        requirement("more_itertools"),
        requirement("importlib_metadata"),
        requirement("zipp"),
        requirement("uritemplate"),
    ],
)
