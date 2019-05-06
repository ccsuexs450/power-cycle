from setuptools import setup
import subprocess

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='power-cycle',
      version='0.1',
      description='bicycle application',
      url='https://github.com/nep67/power-cycle',
      author='KHEN',
      author_email='test@test.com',
      license='MIT',
      packages=['powercycle'],
      install_requires=[
          'pyserial',
          'Pillow',
          'py3dns',
          'validate_email',
          'email',
          'pyoo',
          'numpy',
          'scipy',
          'matplotlib==2.2.3',   
      ],
      include_package_data=True,
      zip_safe=False)
