from setuptools import setup

setup(name='nist-asd',
      version='1.0.1',
      description='Basically a class which parses the NIST Atomic Spectra Database and saves the data to a dictionary '
                  'on HDD. You can pass an matplotlib.axis, and the emissions lines will be plotted with an optional '
                  'normalization factor.',
      url='https://github.com/SirJohnFranklin/nist-asd',
      author='SirJohnFranklin',
      author_email='sirjfu@gmail.com',
      license='MIT',
      packages=['nist_asd'],
      zip_safe=False,
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
        'pprint',
        'logzero',
        'numpy',
        'matplotlib',
        'mpldatacursor',
        'pathlib'
       ],
)