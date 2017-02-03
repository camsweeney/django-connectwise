#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import djconnectwise

LONG_DESCRIPTION = open('README.rst').read()

setup(
    name="django-connectwise",
    version=djconnectwise.__version__,
    description='Django app for working with ConnectWise. Defines models (tickets, members, companies, etc.) '
    'and callbacks.',
    long_description=LONG_DESCRIPTION,
    keywords='django connectwise rest api python',
    packages=find_packages(),
    author='Kerkhoff Technologies Inc.',
    author_email='matt@kerkhofftech.ca',
    url="https://github.com/KerkhoffTechnologies/django-connectwise",
    include_package_data=True,
    test_suite='djconnectwise.tests.runtests.runtests',
    license='MIT',
    install_requires=[
        'requests',
        'django',
        'easy-thumbnails',
        'python-dateutil',
        'django-braces',
    ],
    zip_safe=False,  # Django likes to inspect apps for /migrations directories,
    # and can't if package is installed as a egg. zip_safe=False disables installation as an egg.
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Development Status :: 3 - Alpha',
    ],
)