from setuptools import setup

setup(
  name='nlputils',
  version='1.1.0',
  py_modules=['nlputils','dedupe', 'untrash', 'subset'],
  install_requires=['Click', 'ftfy'],
  entry_points='''
    [console_scripts]
    nlputils=nlputils:cli
  '''
)
