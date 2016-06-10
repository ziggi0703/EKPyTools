#!/usr/bin/env python
import inspect
import os

__author__ = 'Michael Ziegler'

from setuptools import setup

__location__ = os.path.join(os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe())))


def get_install_requirements(path):
    content = open(os.path.join(__location__, path)).read()
    return [req for req in content.splitlines() if req != '']

install_reqs = get_install_requirements('requirements.txt')


console_scripts = ['ekpy = ekpytools.cli:ekpy']

setup(name='EKPyTools',
      version='0.1.4',
      description='Some helpers for the work at the EKP',
      author='Michael Ziegler',
      packages=['ekpytools', 'ekpytools.colors'],
      install_requires= install_reqs,
      test_suite='tests',
      tests_require=['pytest', 'pytest-cov'],
      entry_points={'console_scripts': console_scripts}
      )
