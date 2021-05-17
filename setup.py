#!/usr/bin/env python

import os
from setuptools import setup

setup(name='modify_dicom_t2',
      version='0.0.1',
      description='Fix header info for baseline Myomaps acquisitions',
      url='',
      maintainer='Sharon Portnoy',
      maintainer_email='shportnoy@gmail.com',
      license='BSD',
      keywords=[],
      packages=['modify_dicom_t2'],
      install_requires=[open('requirements.txt').read().strip().split('\n')],
      long_description=(open('README.md').read() if os.path.exists('README.md')
                        else ''),
      entry_points='''
        [gui_scripts]
        modify_dicom_t2=modify_dicom_t2.modify_dicom_t2:main
        [console_scripts]
        modify_dicom_cli=modify_dicom_t2.modify_dicom_t2:main
      ''',
      zip_safe=False)
