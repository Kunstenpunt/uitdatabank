from setuptools import setup

setup(name='uitdatabank',
      version='0.1',
      description='A light wrapper around the UiTdatabank API v2',
      url='https://github.com/ruettet/uitdatabank',
      author='Tom Ruette',
      author_email='tom@kunsten.be',
      license='Apache 2',
      packages=['uitdatabank'],
      zip_safe=False,
      install_requires=['requests'],
      test_suite='nose.collector',
      tests_require=['nose'])
