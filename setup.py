#! /usr/bin/env python

import codecs
import os.path
import re

import setuptools


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), "r") as f:
        return f.read()


def find_version(*file_parts):
    version_file = read(*file_parts)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]$", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="condor",
    version=find_version("condor", "main.py"),
    description="Clean up stale code",
    long_description="\n\n".join(
        [open("README.md").read(), open("CHANGELOG.md").read()]
    ),
    long_description_content_type="text/markdown",
    keywords=['stale', 'code', 'clean', 'techn', 'debt'],
    author="Cristian Moyano",
    author_email="cristianmoyano.mza@gmail.com",
    url="https://github.com/cristianemoyano/condor",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Quality Assurance",
    ],
    entry_points={"console_scripts": ["condor = condor.main:init"]},
    python_requires="!=3.4.*",
    packages=setuptools.find_packages(exclude=["tests"]),
)
