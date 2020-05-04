load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//visibility:private"])

py_library(
    name = "provisioning",
    srcs = [
        "__init__.py",
        "app_insights.py",
        "app_service_plan.py",
        "autoscale.py",
        "deployment_unit.py",
        "function_app.py",
        "resource_group.py",
        "storage_account.py",
    ],
    visibility = ["//visibility:public"],
)
