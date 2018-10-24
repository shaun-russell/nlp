from setuptools import setup

setup(
  name='treefurcate',
  version='1.0',
  py_modules=['treefurcate'],
  install_requires=['Click', 'nltk', 'pycorenlp'],
  entry_points='''
    [console_scripts]
    treefurcate=treefurcate:cli
  '''
)