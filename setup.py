# -*- coding: utf-8 -*-
from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup

with open(join(dirname(__file__), 'httpbinx', 'VERSION'), 'r') as vf:
    version = vf.read().strip()

setup(
    name='httpbinx',
    version=version,
    description='HTTP Request & Response Service, '
                'written in Python + FastAPI.',
    long_description='',
    # The project URL
    url='https://github.com/imleowoo/httpbinx',

    # Author
    author='Leo',
    author_email='imleowoo@outlook.com',

    # license
    license='MIT',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages(
        include=['httpbinx'],
    ),
    requires=[
        'fastapi', 'pydantic', 'uvicorn', 'starlette'
    ],
    python_requires='>=3.6'
)
