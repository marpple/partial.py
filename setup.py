from setuptools import setup


with open('README.rst') as rm:
      long_description = rm.read()


setup_kwargs = {
      'name': 'partial.py',
      'version': '0.1.2',
      'description': 'Functional Python Library',
      'long_description': long_description,
      'url': 'https://github.com/marpple/partial.py',
      'author': 'Marpple',
      'author_email': 'dev@marpple.com',
      'license': 'MIT',
      'packages': ['partial'],
      'package_dir': {'partial': 'src'},
      'classifiers': [
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
}

setup(**setup_kwargs)