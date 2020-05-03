load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("//:builddefs.bzl", "add_exclude_pkgs_command")

def _impl(ctx):
    """
    TODO: fill.
    """
    old_runner = ctx.attr.test[DefaultInfo].files_to_run.executable
    new_runner = ctx.actions.declare_file(ctx.attr.name)
    excluded_pkgs_command = add_exclude_pkgs_command(ctx.attr.excluded_pkgs)
    test_name = ctx.attr.name
    test_pkg = ctx.label.package.replace("/", ".")
    command = ""

    if ctx.configuration.coverage_enabled:
        command = (
            #  save coverage data to /tmp/C7N-cov/[test.module]/
            "  cov_path = os.path.join(os.getenv(\"TMPDIR\"), \"C7N-cov\", \"%s\")\\\n" % (test_pkg) +
            "  os.system(\"mkdir -p \" + cov_path)\\\n" +
            #  target dir: /home/user/.cache/bazel/_bazel_user/hash of the workspace dir/execroot/__main__
            "  while not re.match(\"[a-zA-Z0-9]{32}\", os.path.basename(os.getcwd())):\\\n" +
            "    os.chdir(\"..\")\\\n" +
            "  os.chdir(os.path.join(\"execroot\", \"%s\"))\\\n" % (ctx.workspace_name) +
            "  os.environ[\"COVERAGE_FILE\"] = os.path.join(cov_path, \".coverage\")\\\n" +
            "  args = \\[python_program, \"-m\", \"coverage\", \"run\", \"--rcfile\", \".bazel-coveragerc\", \"-m\", \"unittest\", \"%s.%s\"\\] + args" % (test_pkg, test_name)
        )
    else:
        command = (
            "  os.chdir(os.path.join(module_space, \"%s\"))\\\n" % (ctx.workspace_name) +
            "  args = \\[python_program, \"-m\", \"unittest\", \"%s.%s\"\\] + args" % (test_pkg, test_name)
        )

    ctx.actions.run_shell(
        progress_message = "Patching file content - %s" % old_runner.short_path,
        # TODO: replace all *.inner mentions in file_to_run
        command =
            "sed $'s/" +
            "  args = \\[python_program, main_filename\\] + args/" + command +
            " /g' '%s' %s > '%s'" % (old_runner.path, excluded_pkgs_command, new_runner.path),
        inputs = [old_runner],
        outputs = [new_runner],
    )

    return [DefaultInfo(
        runfiles = ctx.attr.test.default_runfiles,
        executable = new_runner,
    )]

_py_test = rule(
    implementation = _impl,
    executable = True,
    attrs = {
        "test": attr.label(mandatory = True),
        "excluded_pkgs": attr.string_list(default = []),
    },
    test = True,
    doc = """
TODO: fill.
Example rule documentation.

Example:
  Here is an example of how to use this rule.
"""
)

def c7n_py_test(name, **kwargs):
    """
    TODO: fill.
    """
    inner_test_name = name + ".inner"
    tags = kwargs.pop("tags", default = [])
    main_name = kwargs.pop("name", default = name + ".py")
    excluded_pkgs = kwargs.pop("excluded_pkgs", default = [])
    kwargs.update(main = main_name, tags = tags + ["manual"])
    py_test(name = inner_test_name, **kwargs)
    _py_test(name = name, tags = tags, test = inner_test_name, excluded_pkgs = excluded_pkgs)

C7N_TESTS_CHUNKS = {
    "first_chunk": "test_doc_examples",
    "second_chunk": "test_hsm",
    "third_chunk": "test_report",
    "fourth_chunk": "test_workspaces",
}

def get_chunk(test_file_name):
    """
    TODO: fill.
    We have a lot of tests of AWS, and to fit GitHub Actions worker limits,
    it's splitted for chunks, which is rougly equal in processing time and
    resource consumption.
    This function just goes through the list and divide it by test name.
    """
    for chunk_name, last_test_in_chunk in C7N_TESTS_CHUNKS.items():
        if test_file_name <= last_test_in_chunk:
            return chunk_name
    return C7N_TESTS_CHUNKS.keys()[-1]
