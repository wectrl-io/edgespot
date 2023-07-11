#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from setuptools import find_packages, setup

import edgespot

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = ""
"""Copyrighted"""

__credits__ = []
"""Credits"""

__license__ = ""
"""License
@see """

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = ["Orlin Dimitrov", "Martin Maslyankov", "Nikola Atanasov"]
"""Name of the maintainer."""

__email__ = ""
"""E-mail of the author."""

__class_name__ = ""
"""Class name."""

#endregion

def long_description():
    """Long description reader.

    Returns:
        str: Description content.
    """    
    with open('README.md', encoding='utf-8') as f:
        return f.read()

install_requires = ["backoff==2.2.1",
                    "certifi==2022.12.7",
                    "charset-normalizer==3.1.0",
                    "hassapi==0.1.1",
                    "huawei-solar==2.2.6",
                    "idna==3.4",
                    "paho-mqtt==1.6.1",
                    "pymodbus==3.1.3",
                    "pyserial==3.5",
                    "pyserial-asyncio==0.6",
                    "pytz==2023.3",
                    "PyYAML==6.0",
                    "requests==2.28.2",
                    "typing_extensions==4.7.1",
                    "urllib3==1.26.15"]

setup(
    name="edgespot",
    packages=find_packages(include=["edgespot", 'edgespot.*']),
    entry_points={
        'console_scripts': [
            'edgespot = edgespot.__main__:main'
        ]
    },
    version=__version__,
    description="Edgespot we-ctrl.io edge cloud software.",
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author=__author__,
    license=__license__,
    author_email=__email__,
    python_requires='>=3.7',
    install_requires=install_requires,
    setup_requires=[],
    tests_require=[],
    test_suite="",
    project_urls={
        'GitHub': 'https://github.com/wectrl-io/edgespot',
    },
    classifiers=[
        'Development Status :: 1 - Debug',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Home and Industrial automation'
    ],
    # package_data={'package.sub_1.sub_2': ['*.ext']}
)
