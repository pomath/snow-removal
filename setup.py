'''
Setup for snowy package.
'''

from distutils.core import setup

setup(name='snowy',
      version='0.2',
      author='Peter Matheny',
      packages=['snowy'],
      data_files = [('bin', ['utils/teqc',
                          'utils/CRX2RNX',
                          'utils/get_data.sh']
                    )]
     )
