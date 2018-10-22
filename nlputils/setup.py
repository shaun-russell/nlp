from setuptools import setup

setup(
  name='nlputils',
  version='1.0',
  py_modules=['nlputils.py','dedupe.py', 'untrash.py'],
  install_requires=['Click'],
  entry_points='''
    [console_scripts]
    nlputils=nlputils:cli
  '''
)
