from setuptools import setup, find_packages

setup(
    name="consaulider",
    version="0.1.0",
    author="Aliaume Lopez",
    author_email="aliaume.lopez@ens-paris-saclay.fr",
    packages=find_packages(),
    # scripts=["bin/siance-backend"],
    # url="http://pypi.python.org/pypi/PackageName/",
    url="github.com",
    license="LICENSE.md",
    description="Safely compute data-completion using SAT solvers",
    long_description=open("README.md").read(),
    install_requires=[
        "click",
        "pydantic",
        "pytest",
        "python-sat",
	"py-aiger-cnf"
    ],
)
