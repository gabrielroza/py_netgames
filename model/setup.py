from setuptools import setup, find_namespace_packages

setup(name='py_netgames_model',
      version='1.0',
      license_files='LICENSE.txt',
      author='Gabriel Machado da Roza',
      author_email='gabrielmachadodaroza@outlook.com',
      description='Py-NetGames Internal Model package. Shared between server and client implementations.',
      packages=find_namespace_packages(),
      install_requires=[
          'dataclasses-json'
      ]
      )
