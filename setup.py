"""
Sanic-JWT-Extended
"""
import io
import re
import os
from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()


with open(os.path.join("sanic_jwt_extended", "__init__.py"), "r") as f:
    try:
        version = re.findall(
            r"^__version__ = \"([^']+)\"\r?$", f.read(), re.M
        )[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")


setup(name='Sanic-JWT-Extended',
      version=version,
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