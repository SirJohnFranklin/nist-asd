import setuptools
from setuptools import setup

setup(name='nist-asd',
      version='1.0',
      description='Basically a class which parses the NIST Atomic Spectra Database and saves the data to a dictionary on HDD. Also includes a traits representation to set the parameters within a gui and plot or print them. As an object, you can pass an matplotlib.axis, and the emissions lines will be plotted with an optional normalization factor. ',
      url='https://github.com/SirJohnFranklin/nist-asd',
      author='SirJohnFranklin',
      author_email='sirjfu@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False,
      use_2to3_on_doctests=False,
      classifiers=(
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 2",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ),
      install_requires=[
        'HTMLParser',
        'traits',
        'traitsui',
        'pyside',
        'numpy',
        'matplotlib',
        'mpldatacursor',
       ],
)