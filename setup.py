from os import chdir, pardir
from os.path import join, exists, dirname, normpath, abspath
from setuptools import find_packages, setup
from re import sub


def req_link(external_url):
    egg_link = sub(r'https://[^=]+=', '', external_url)
    return "==".join(egg_link.rsplit("-", 1))


reqs_default = join(dirname(__file__), "requirements.txt")
reqs_core = join(dirname(__file__), "requirements.core.txt")
required = []

if exists(reqs_default):
    with open(reqs_default) as f:
        required += f.read().splitlines()

if exists(reqs_core):
    with open(reqs_core) as f:
        required += f.read().splitlines()

with open(join(dirname(__file__), "README.rst")) as f:
    long_desc = f.read()

# Allow setup.py to be run from any path
chdir(normpath(join(abspath(__file__), pardir)))

dep_links = [r for r in required if r.startswith("https://")]
required = [req_link(r) if r.startswith("https://") else r for r in required]

setup(
    name="core_curate_app",
    version="1.0.0-beta4",
    description="Curation functionalities for the curator core project",
    long_description=long_desc,
    author="NIST IT Lab",
    author_email="itl_inquiries@nist.gov",
    url="https://github.com/usnistgov/core_curate_app",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    dependency_links=dep_links,
)
