#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# Extract central version information
with open(os.path.join(os.path.dirname(__file__), "ando", "VERSION")) as version_file:
    version = version_file.read().strip()


setup(
    name="AnDO",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    package_data={
            # If any package contains *.json or *.csv files, include them:
            "": ["*.json", '*.csv', '*.tsv'],
    },
    author="Jeremy Garcia, Sylvain Takerkart , Julia Sprenger",
    description="Checks the validity of a directory with respect to the ANimal Data Organization (ANDO) specifications ",
    license='MIT',
    install_requires=[],
    entry_points={

        'console_scripts': ['AnDOChecker=ando.AnDOChecker:main',
                            'AnDOGenerator=ando.tools.generator.AnDOGenerator:main',
                            'AnDOViewer=ando.tools.viewer.AnDOViewer:main'],
    },
    python_requires='>=3.6',
    extras_require={
        'tools': ['pandas'],
        'test': ['pytest']
    }
)
