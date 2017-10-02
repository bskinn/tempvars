from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='tempvars',
    version='1.0b2',
    provides=['tempvars'],
    install_requires=['attrs>=17'],
    packages=['tempvars'],
    url='https://www.github.com/bskinn/tempvars',
    license='MIT License',
    author='Brian Skinn',
    author_email='bskinn@alum.mit.edu',
    description=('Context manager for handling temporary variables '
                 'in Jupyter Notebook, IPython, etc.'),
    long_description=readme(),
    classifiers=['License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3 :: Only',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Software Development',
                 'Development Status :: 4 - Beta']
    )
