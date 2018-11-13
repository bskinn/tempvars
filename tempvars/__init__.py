r"""*Core package definition module for* ``tempvars``.

Context manager for handling temporary variables in
Jupyter Notebook, IPython, etc.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    10 Sep 2017

**Copyright**
    \(c) Brian Skinn 2017-2018

**Source Repository**
    http://www.github.com/bskinn/tempvars

**Documentation**
    http://tempvars.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

"""

from __future__ import absolute_import

__all__ = ["TempVars"]

from .tempvars import TempVars

__version__ = "1.0.1.dev1"
