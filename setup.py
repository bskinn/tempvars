import re
from setuptools import setup

from tempvars import __version__

NAME = "tempvars"


def readme():
    with open("README.rst", "r") as f:
        content = f.read()

    # Helper function
    def content_update(content, pattern, sub):
        return re.sub(pattern, sub, content, flags=re.M | re.I)

    # Docs reference updates to current release version, for PyPI
    # This one gets the badge image
    content = content_update(
        content,
        r"(?<=/readthedocs/{0}/)\S+?(?=\.svg$)".format(NAME),
        "v" + __version__,
    )

    # This one gets the RtD links
    content = content_update(
        content,
        r"(?<={0}\.readthedocs\.io/en/)\S+?(?=[/>])".format(NAME),
        "v" + __version__,
    )

    return content


setup(
    name="tempvars",
    version=__version__,
    description=(
        "Context manager for handling temporary variables "
        "in Jupyter Notebook, IPython, etc."
    ),
    long_description=readme(),
    url="https://www.github.com/bskinn/tempvars",
    license="MIT License",
    author="Brian Skinn",
    author_email="bskinn@alum.mit.edu",
    packages=["tempvars"],
    provides=["tempvars"],
    python_requires=">=3.4",
    requires=["attrs (>=17.1)"],
    install_requires=["attrs>=17"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Development Status :: 5 - Production/Stable",
    ],
)
