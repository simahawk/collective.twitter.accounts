from setuptools import setup, find_packages
import os

version = '1.0.1'

setup(name='collective.twitter.accounts',
      version=version,
      description="Provide Twitter integration for a Plone Site",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Franco Pellegrini',
      author_email='frapell@gmail.com',
      url='https://github.com/collective/collective.twitter.accounts',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.twitter'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'python-twitter==0.8.2',
          'plone.app.registry',
          # -*- Extra requirements: -*-
      ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
