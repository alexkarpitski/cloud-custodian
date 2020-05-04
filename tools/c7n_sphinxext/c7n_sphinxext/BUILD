load("@sphinx_py_deps//:requirements.bzl", "requirement")
load(":sphinx.bzl", "docgen", "sphinx_generate_docs")
load("//:builddefs.bzl", "EXCLUDED_PKGS")

# it is main sphinx file to build html documentation
SPHINX_BUILD_SCRIPT = "{repo_path}:{build_script}".format(
    repo_path = requirement("Sphinx"),
    build_script = "sphinx/cmd/build.py",
)

py_binary(
    name = "c7n_sphinxext_docgen",
    srcs = ["docgen.py"],
    data = glob(["_templates/*.rst"]),
    imports = [
        "..",
        "../../c7n_azure",
        "../../c7n_gcp",
        "../../c7n_kube",
    ],
    main = "docgen.py",
    deps = [
        ":sphinxlib",
        "//c7n",
        "//tools/c7n_azure/c7n_azure:c7n_azure_lib",
        "//tools/c7n_gcp/c7n_gcp:entry",
        "//tools/c7n_kube/c7n_kube:kube_lib",
    ],
)

py_binary(
    name = "sphinx_build",
    srcs = [SPHINX_BUILD_SCRIPT],
    imports = [
        "..",
        "../../c7n_azure",
        "../../c7n_gcp",
        "../../c7n_kube",
    ],
    main = SPHINX_BUILD_SCRIPT,
    deps = [
        ":c7n_sphinxext",
        ":sphinxlib",
        "//c7n",
        "//tools/c7n_azure/c7n_azure:c7n_azure_lib",
        "//tools/c7n_gcp/c7n_gcp:entry",
        "//tools/c7n_kube/c7n_kube:kube_lib",
    ],
)

docgen(
    name = "aws_gen",
    provider = "aws",
    resource_type = "resource_type.service",
    tool = ":c7n_sphinxext_docgen",
)

docgen(
    name = "gcp_gen",
    provider = "gcp",
    resource_type = "resource_type.service",
    tool = ":c7n_sphinxext_docgen",
)

docgen(
    name = "azure_gen",
    provider = "azure",
    resource_type = "resource_type.doc_groups",
    tool = ":c7n_sphinxext_docgen",
)

# bazel build //tools/c7n_sphinxext/c7n_sphinxext:sphinx_gen
# then you can get generated docs from bazel-out/k8-fastbuild/bin/tools/c7n_sphinxext/c7n_sphinxext/build/html
sphinx_generate_docs(
    name = "sphinx_gen",
    srcs = ["//:doc_rst_files"],
    excluded_pkgs = EXCLUDED_PKGS,
    inputs = [
        ":aws_gen",
        ":gcp_gen",
        ":azure_gen",
    ],
    readme_files = ["//:readme_files"],
    tool = ":sphinx_build",
)

py_library(
    name = "sphinxlib",
    deps = [
        requirement("Sphinx"),
        requirement("click"),
        requirement("recommonmark"),
        requirement("sphinx_rtd_theme"),
        requirement("imagesize"),
        requirement("sphinx-markdown-tables"),
        requirement("alabaster"),
        requirement("commonmark"),
        requirement("markdown"),
        requirement("chardet"),
        requirement("requests"),
        requirement("idna"),
        requirement("python-dateutil"),
        requirement("futures"),
        requirement("jinja2"),
        requirement("markupsafe"),
        requirement("babel"),
        requirement("pytz"),
        requirement("attrs"),
        requirement("pyrsistent"),
        requirement("importlib_metadata"),
        requirement("zipp"),
        requirement("more_itertools"),
        requirement("docutils"),
        requirement("pygments"),
        requirement("packaging"),
    ],
)

py_library(
    name = "c7n_sphinxext",
    srcs = [
        "__init__.py",
        "docgen.py",
    ],
    data = glob(["_templates/*.rst"]),
)
