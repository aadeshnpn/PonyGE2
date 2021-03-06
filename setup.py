#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from setuptools import setup, find_packages
from codecs import open

requires = [
    'numpy', 'scipy', 'scikit-learn', 'pandas', 'matplotlib'
]

version = ''
with open('__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)


setup(
    name='ponyge',
    version=version,
    description="Grammatical Evolution in Python 3+",
    long_description="testing",
    author='Project ponyge Team',
    author_email='aadeshnpn@byu.net',
    url='https://github.com/PonyGE/PonyGE2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    keywords='GE',
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Life',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
    ],
)
