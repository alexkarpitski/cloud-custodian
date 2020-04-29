load("@rules_python//experimental/python:wheel.bzl", "py_package", "py_wheel")

_FILE_HASH_SCRIPT_NAME = "file_hash.py"

def _impl_a(ctx):
    inputs = ctx.attr.whl_file.data_runfiles.files.to_list()
    python_script_file = False
    for f in ctx.attr._add_ep_runner.data_runfiles.files.to_list():
        if f.basename == _FILE_HASH_SCRIPT_NAME:
            python_script_file = f
            break
    if not python_script_file:
        fail("Can't find 'file_hash.py' in data of the run-add-ep-script rule")
    inputs.append(python_script_file)
    out_file = ctx.outputs.output
    contents = []
    args = ctx.actions.args()
    for k, v in ctx.attr.entry_points.items():
        contents.append("[%s]" % k)
        for p in v:
            contents.append(p)
    contents = "\\n".join(contents)
    ctx.actions.run(
        inputs = inputs,
        outputs = [out_file],
        arguments = [ctx.attr.distr_info, inputs[0].path, contents, out_file.path],
        executable = ctx.executable._add_ep_runner,
        progress_message = "Building wheel",
    )

_add_entry_points = rule(
    implementation = _impl_a,
    attrs = {
        "entry_points": attr.string_list_dict(mandatory = True),
        "distr_info": attr.string(mandatory = True),
        "whl_file": attr.label(mandatory = True),
        "output": attr.output(doc = "The generated file"),
        "_add_ep_runner": attr.label(
            executable = True,
            cfg = "host",
            default = ":run-add-ep-script",
        ),
    },
    doc = """
TODO: fill.
Example rule documentation.

Example:
  Here is an example of how to use this rule.
"""
)

def py_wheel_entry_points_ext(**kwargs):
    if kwargs.get("entry_points"):
        entry_points = kwargs.pop("entry_points")
    else:
        fail("Entry points not specified")
    py_wheel_rule_name = kwargs["name"] + "_wheel"
    py_wheel(
        name = py_wheel_rule_name,
        distribution = kwargs["distribution"],
        strip_path_prefixes = kwargs["strip_path_prefixes"],
        version = kwargs["version"],
        deps = kwargs["deps"],
    )
    outfile = "out/" + "-".join(
        [
            kwargs["distribution"],
            kwargs["version"],
            "py3",
            "none",
            "any",
        ],
    ) + ".whl"
    _add_entry_points(
        name = kwargs["name"],
        entry_points = entry_points,
        distr_info = kwargs["distribution"] + "-" + kwargs["version"],
        whl_file = "//:" + py_wheel_rule_name,
        output = outfile,
    )
