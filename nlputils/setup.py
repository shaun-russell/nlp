from setuptools import setup

setup(
  name='nlputils',
  version='1.0.1',
  py_modules=['nlputils','dedupe', 'untrash'],
  install_requires=['Click', 'ftfy'],
  entry_points='''
    [console_scripts]
    nlputils=nlputils:cli
  '''
)
