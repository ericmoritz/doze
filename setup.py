from setuptools import setup, find_packages
import doze
import sys, os

version = doze.__version__

setup(name='doze',
      version=version,
      description="Lazy URL construction",
      long_description="""\
""",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Eric Moritz',
      author_email='eric@themoritzfamily.com',
      url='https://github.com/ericmoritz/doze',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      test_suite="doze.tests",
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
