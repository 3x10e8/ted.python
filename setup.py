#!/usr/bin/env python

import os

from numpy.distutils.core import setup

DISTNAME = 'bionet.utils'
DESCRIPTION = 'Bionet utilities'
VERSION = '0.01'
MAINTAINER = 'Lev Givon'
MAINTAINER_EMAIL = 'lev@columbia.edu'
URL = 'http://bionet.ee.columbia.edu/code'
DOWNLOAD_URL = URL
LICENSE = 'BSD'

def configuration(parent_package='', top_path=None,
                  package_name=DISTNAME):
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')
    from numpy.distutils.misc_util import Configuration
    config = Configuration(package_name, parent_package, top_path,
                           version = VERSION,
                           maintainer = MAINTAINER,
                           maintainer_email = MAINTAINER_EMAIL,
                           description = DESCRIPTION,
                           license = LICENSE,
                           url = URL,
                           download_url = DOWNLOAD_URL)
    return config
                           
if __name__=="__main__":
    setup(configuration = configuration,
          namespace_packages = ['bionet'],
          packages = ['bionet.utils'],
          package_dir = {'bionet.utils': '.'},
          install_requires = ['numpy','tables']
          classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
	'Operating System :: OS Independent',
	'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development'])
