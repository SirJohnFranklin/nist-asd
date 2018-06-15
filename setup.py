from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='nist-asd',
      version='1.4',
      description='Basically a class which parses the NIST Atomic Spectra Database and saves the data to a dictionary '
                  'on HDD. You can pass an matplotlib.axis, and the emissions lines will be plotted with an optional '
                  'normalization factor. \n Parser for energy levels is also included.',
      long_description=read('README.md'),
      url='https://github.com/SirJohnFranklin/nist-asd',
      author='SirJohnFranklin',
      author_email='sirjfu@gmail.com',
      license='MIT',
      packages=['nist-asd'],
      zip_safe=False,
      classifiers=(
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ),
      install_requires=[
        'HTMLParser',
        'pprint',
        'logzero',
        'mpldatacursor',
        'pathlib'
       ],
)