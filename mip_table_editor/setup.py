# (C) British Crown Copyright 2022, Met Office.
# Please see LICENSE for license details.
"""
Setup script for the CDDS Template package.
"""
import imp
import os
import unittest

from setuptools import setup, find_packages


def extract_version():
    """
    Return the version number of mip_table_editor
    """
    filename = os.path.join('mip_table_editor', '__init__.py')
    imported_module = imp.load_source('__init__', filename)
    version = imported_module.__version__
    return version


def extract_readme():
    """
    Return the contents of the README.rst file in CDDS Template.
    """
    with open('README.rst') as readme_file:
        return readme_file.read()


def data_file_search(directory):
    """
    Return a list in the form [(p1, f1), (p2, f2), ...], where p<#> is
    a string containing the path to a directory (the root of the
    directory is provided by the 'directory' argument) and f<#> is a
    list containing the files in that directory.
    """
    search_dirs = [dirpath for (dirpath, _, _) in os.walk(directory)]
    # The 'search_dir' string will always start with the 'directory' string
    return [(search_dir, [os.path.join(search_dir, filename) for filename in
                          os.listdir(search_dir) if
                          os.path.isfile(os.path.join(search_dir, filename))])
            for search_dir in search_dirs]


def find_data_files():
    """
    Return a list to use as the value of 'data_files' in the call to
    'setup'.
    """
    data_files = [('', ['setup.py', 'setup.cfg'])]
    data_files.extend(data_file_search(directory='doc'))
    return data_files


def find_scripts(directories):
    """
    Find and return all the scripts in the directories given.
    The directories are assumed to contain just scripts.
    Directories need not exist: any that don't (or aren't directories)
    will be skipped.

    This returns a list of (dir [script ...]) tuples, for each dir in
    dirs.
    """
    scripts = []
    for directory in directories:
        if os.path.isdir(directory):
            scripts.extend([os.path.join(directory, entry)
                            for entry in os.listdir(directory)
                            if os.path.isfile(os.path.join(directory, entry))])
    return scripts


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('mip_table_editor/tests', pattern='test_*.py')
    return test_suite


setup(name='mip_table_editor',
      version=extract_version(),
      description=('The mip_table_editor can be used for modifying and creating CMIP like mip_tables and cvs.'),
      keywords='mip_table_editor',
      url='https://github.com/MetOffice/gcmodeldev-cmor-tables',
      author='Jared Drayton',
      author_email='jared.drayton@metoffice.gov.uk',
      maintainer='Jared Drayton',
      maintainer_email='jared.drayton@metoffice.gov.uk',
      platforms=['Linux', 'Unix'],
      packages=find_packages(),
      data_files=find_data_files(),
      test_suite='setup.my_test_suite',
      scripts=find_scripts(['bin']),
      include_package_data=True,
      zip_safe=False)
