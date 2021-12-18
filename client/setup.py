from setuptools import setup, find_namespace_packages

setup(name='client',
      version='1.0',
      description='Client',
      author='Gabriel Machado',
      packages=find_namespace_packages(),
      install_requires=[
          'model'
      ]
      )
