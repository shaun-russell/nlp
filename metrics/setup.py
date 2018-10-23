from setuptools import setup

setup(
  name='metrics',
  version='1.0',
  py_modules=['metrics.py', 'tfidf.py'],
  install_requires=['Click'],
  entry_points='''
    [console_scripts]
    metrics=metrics:cli
  '''
)