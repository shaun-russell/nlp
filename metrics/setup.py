from setuptools import setup

setup(
  name='metrics',
  version='1.0.1',
  py_modules=['metrics', 'tfidf'],
  install_requires=['Click'],
  entry_points='''
    [console_scripts]
    metrics=metrics:cli
  '''
)
