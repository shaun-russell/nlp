from setuptools import setup

setup(
  name='isspatial',
  version='1.0',
  py_modules=['isspatial', 'core', 'geonouns', 'spatialgrammar', 'validator'],
  install_requires=['Click', 'nltk'],
  entry_points='''
    [console_scripts]
    isspatial=isspatial:cli
  '''
)