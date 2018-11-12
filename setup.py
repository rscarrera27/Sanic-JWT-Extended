"""
Sanic-JWT-Extended
"""
import io
import re
from setuptools import setup

from sanic_jwt_extended import __version__


with open("README.md", "r") as f:
    long_description = f.read()


setup(name='Sanic-JWT-Extended',
      version=__version__,
      url='https://github.com/devArtoria/Sanic-JWT-Extended',
      license='MIT',
      author='Lewis "devArtoria" Kim',
      author_email='artoria@artoria.us',
      description='Extended JWT integration with Sanic',
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords=['sanic', 'jwt', 'json web token'],
      packages=['sanic_jwt_extended'],
      zip_safe=False,
      platforms='any',
      install_requires=[
          'Sanic',
          'PyJWT',
      ],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ])