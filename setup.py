#! /usr/bin/env python

import setuptools

from pycondor.version import __version__


setuptools.setup(
    name="pycondor",
    version=__version__,
    description="Clean up stale code",
    long_description="\n\n".join(
        [open("README.md").read(), open("CHANGELOG.md").read()]
    ),
    long_description_content_type="text/markdown",
    keywords=['stale', 'code', 'clean', 'techn', 'debt'],
    author="Cristian Moyano",
    author_email="cristianmoyano.mza@gmail.com",
    url="https://github.com/cristianemoyano/pycondor",
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
    entry_points={"console_scripts": ["pycondor = pycondor.main:init"]},
    python_requires="!=3.4.*",
    packages=setuptools.find_packages(exclude=["tests"]),
)
