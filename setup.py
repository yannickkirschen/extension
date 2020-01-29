#!/usr/bin/env python3

# Copyright 2019 Yannick Kirschen. All rights reserved.
# Use of this source code is governed by the GNU-GPL
# license that can be found in the LICENSE file.

# Date created: May 21, 2018


from setuptools import setup, find_packages

from extension import __version__


with open('README.md', 'r') as file:
    long_description = file.read()


setup(
    name='extension',
    version=__version__.__version__,
    author='Yannick Kirschen',
    author_email='github.yannickkirschen@protonmail.com',
    description='Utilities for python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        'extension': ['emojis.json', 'resources/*.svg']
    },
    install_requires=[
        'flask>=1.0.2',
        'markdown>=3.0.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ]
)
