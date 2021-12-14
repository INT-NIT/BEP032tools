#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# Extract central version information
with open(os.path.join(os.path.dirname(__file__), "bep032tools", "VERSION")) as version_file:
    version = version_file.read().strip()


setup(
    name="BEP032tools",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    package_data={
            # If any package contains *.json or *.csv files, include them:
            "": ["*.json", '*.csv', '*.tsv'],
    },
    author="Jeremy Garcia, Sylvain Takerkart , Julia Sprenger",
    description="Checks the validity of a directory with respect to the BEP032 specifications ",
    license='MIT',
    install_requires=[],
    entry_points={
        'console_scripts': ['BEP032Validator=bep032tools.BEP032Validator:main',
                            'BEP032Generator=bep032tools.tools.generator.BEP032Generator:main',
                            'BEP032Templater=bep032tools.tools.generator.BEP032Templater:main',
                            'BEP032Viewer=bep032tools.tools.viewer.BEP032Viewer:main'],
    },
    python_requires='>=3.6',
    extras_require={
        'tools': ['pandas', 'pynwb'],
        'test': ['pytest', 'datalad']
    }
)
