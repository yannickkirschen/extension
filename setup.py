#!/usr/bin/env python3

# Copyright 2019 Yannick Kirschen. All rights reserved.
# Use of this source code is governed by the GNU-GPL
# license that can be found in the LICENSE file.

# Date created: May 21, 2018


from setuptools import setup, find_packages

from extension import __version__


with open('README.md', 'r') as file:
    long_description = file.read().replace(':.+: ', '')


with open('requirements.txt', 'r') as file:
    requirements = file.read().split('\n')


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
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ]
)
