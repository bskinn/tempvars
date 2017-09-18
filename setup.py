from setuptools import setup
from os import environ

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='tempvars',
    version='0.0',
    provides=['tempvars'],
    install_requires=['attrs>=17'],
    packages=['tempvars'],
    url='https://www.github.com/bskinn/tempvars',
    license='MIT License',
    author='Brian Skinn',
    author_email='bskinn@alum.mit.edu',
    description='Context Manager for Handling Temporary Variables',
    long_description=readme(),
    classifiers=['License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Environment :: Console',
                 'Intended Audience :: Science/Research',
		 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3 :: Only',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Software Development',
                 'Development Status :: 2 - Pre-Alpha']
    )
