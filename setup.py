# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright (C) 2013-2019 British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------

from importlib.util import spec_from_file_location, module_from_spec
import os
from pathlib import Path
# overriding setuptools command
# https://stackoverflow.com/a/51294311
from setuptools.command.bdist_rpm import bdist_rpm as bdist_rpm_original
# to parse pytest command arguments
# https://docs.pytest.org/en/2.8.7/goodpractices.html#manual-integration
from setuptools.command.test import test as TestCommand
from setuptools import setup, find_namespace_packages
import sys


try:
    os.chdir(os.path.dirname(__file__))
except FileNotFoundError:
    pass


def get_version(module, path):
    """Return the __version__ attr from a module sourced by FS path."""
    spec = spec_from_file_location(module, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__


__version__ = get_version(
    'metomi.isodatetime',
    Path('metomi/isodatetime/__init__.py')
)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


class bdist_rpm(bdist_rpm_original):

    def run(self):
        """Before calling the original run method, let's change the
        distribution name to create an RPM for python-isodatetime."""
        self.distribution.metadata.name = "python-isodatetime"
        self.distribution.metadata.version = __version__
        super().run()


setup(
    name="metomi-isodatetime",
    version='1!' + __version__,
    author="Met Office",
    author_email="metomi@metoffice.gov.uk",
    cmdclass={
        "bdist_rpm": bdist_rpm,
        "pytest": PyTest
    },
    description=("Python ISO 8601 date time parser" +
                 " and data model/manipulation utilities"),
    license="LGPLv3",
    keywords="isodatetime datetime iso8601 date time parser",
    url="https://github.com/metomi/isodatetime",
    packages=find_namespace_packages(include=['metomi.*']),
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    platforms='any',
    setup_requires=['pytest-runner'],
    tests_require=['coverage', 'pytest>=5', 'pytest-cov', 'pytest-env'],
    install_requires=[],
    python_requires='>=3.4, <3.8',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        ("License :: OSI Approved" +
         " :: GNU Lesser General Public License v3 (LGPLv3)"),
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': ['isodatetime=isodatetime.main:main'],
    },
)
