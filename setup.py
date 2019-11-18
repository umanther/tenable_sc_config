from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    __long_description__ = f.read()

__name__ = 'tenable_sc_config'
__version__ = '1.0.2'
__author__ = 'Geoff Hellstrand'
__desc__ = 'A simple tool to create & load an .ini file for logging into an instance of Tenable.SC'
__author_email__ = 'ubil@hotmail.com'
__license__ = 'GPLv3'
__url__ = 'https://github.com/umanther/tenable_sc_config'
__keywords__ = ['python', 'tenable', 'security', 'center', 'SC', 'login', 'configuration', 'ini']
__packages__ = find_packages()
__python_requires__ = '>=3.6'
__install_requires__ = ['configparser>=4.0.2']
__classifiers__ = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
    'Natural Language :: English',
    'Topic :: Utilities',
]

setup(
    name=__name__,
    packages=__packages__,
    version=__version__,
    description=__desc__,
    long_description=__long_description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    keywords=__keywords__,
    license=__license__,
    classifiers=__classifiers__,
    install_requires=__install_requires__,
    python_requires=__python_requires__,
)
