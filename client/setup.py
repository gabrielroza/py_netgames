from setuptools import setup, find_namespace_packages

setup(name='Client',
      version='1.0',
      description='Model',
      author='Gabriel Machado',
      packages=find_namespace_packages(),
      install_requires=[
          'Model'
      ]
      )
