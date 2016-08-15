from setuptools import setup

setup(name='uitdatabank',
      version='0.1',
      description='A light wrapper around the UiTdatabank API v2',
      download_url='https://github.com/ruettet/uitdatabank',
      url='http://uitdatabank.readthedocs.io/en/latest/',
      author='Tom Ruette',
      author_email='tom@kunsten.be',
      license='Apache 2',
      packages=['uitdatabank'],
      zip_safe=False,
      install_requires=['requests'],
      test_suite='nose.collector',
      tests_require=['nose'])
