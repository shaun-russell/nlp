from setuptools import setup

setup(
  name='isspatial',
  version='1.1.1',
  py_modules=['isspatial', 'core', 'geonouns', 'spatialgrammar', 'validator', 'placenames'],
  install_requires=['Click', 'nltk'],
  entry_points='''
    [console_scripts]
    isspatial=isspatial:cli
  '''
)