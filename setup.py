from setuptools import setup

def readme():
      with open('README.md') as f:
            return f.read()

setup(name='partial.py',
      version='1.0.0',
      description='Functional Python Library',
      url='https://github.com/marpple/partial.py',
      author='Marpple',
      author_email='dev@marpple.com',
      license='MIT',
      packages=['parital'],
      package_dir={'parital': 'src'}
      )