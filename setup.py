from setuptools import setup
import subprocess

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='power-cycle',
      version='1.1',
      description='bicycle application',
      url='https://github.com/nep67/power-cycle',
      author='KHEN',
      author_email='nickpipino67@gmail.com',
      license='MIT',
      packages=['powercycle'],
      install_requires=[
          'Pillow',
          'py3dns',
          'pyserial',
          'validate_email',
          'email',
          'pyoo',
          'numpy',
          'scipy',
          'matplotlib==2.2.3',   
      ],
      include_package_data=True,
      zip_safe=False)
