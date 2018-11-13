tempvars: A context manager for handling temporary variables
============================================================

**Current Development Version:**

.. image:: https://travis-ci.org/bskinn/tempvars.svg?branch=dev
    :target: https://travis-ci.org/bskinn/tempvars

.. image:: https://codecov.io/gh/bskinn/tempvars/branch/dev/graph/badge.svg
    :target: https://codecov.io/gh/bskinn/tempvars

**Most Recent Stable Release:**

.. image:: https://img.shields.io/pypi/v/tempvars.svg
    :target: https://pypi.org/project/tempvars

.. image:: https://img.shields.io/pypi/pyversions/tempvars.svg

**Info:**

.. image:: https://img.shields.io/readthedocs/tempvars/latest.svg
    :target: http://tempvars.readthedocs.io/en/latest/

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/bskinn/tempvars/blob/master/LICENSE.txt

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

----

**Use Jupyter Notebook?**

**Constantly run into problems from obsolete variables hanging around
in the namespace?**

``tempvars`` *can help.*

Jupyter notebooks can be frustrating.
E.g., debugging a worksheet for half an hour, only to discover
that a carried-over variable name was hanging around
in the notebook namespace and causing problems.
Or, opening a notebook that only "worked fine" the last
time it was used because of random, obsolete variables that happened
to be lingering in the namespace.

``TempVars`` is a context manager that helps to avoid these pitfalls by
clearing selected identifiers from the namespace for the duration of
its scope, then restoring them afterwards (or not, if desired).
Further, any variables created within the managed context
that match the ``TempVars`` filtering criteria are removed from
the namespace upon exiting, ensuring these values do not spuriously
contribute to following code.

For convenience, all variables
that were removed from the namespace at both entry and exit
are stored with their values for later reference (see example code below).

Due to the way Python handles non-global scopes, ``TempVars``
can only be used at the global scope. *Any attempt
to use* ``TempVars`` *in non-global contexts will
result in a* ``RuntimeError``. Viable use-cases include Jupyter notebooks,
the IPython and basic Python REPLs, and the outermost scope of executed and
imported modules. Preliminary testing indicates it also works with
`cauldron-notebook <https://github.com/sernst/cauldron>`__, though
it may be less helpful there due to the step-local scoping paradigm used
(shared values must be passed around via ``cauldron.shared``).

----

After installing with ``pip install tempvars``, import as:

.. code:: python

    >>> from tempvars import TempVars

Example usage:

 * Screening pre-existing variables, that are restored afterward
 * Screening vars, then *not* restoring them
 * Clearing vars created in context that match, after exiting
 * Demonstrating how vars are stored either in ``.stored_nsvars``
   or in ``.retained_tempvars``

.. code:: python

    >>> t_var1 = 5
    >>> t_var2 = 7
    >>> x = 15
    >>> y = 20
    >>> with TempVars(names=['x']) as tv1:
    ...     with TempVars(starts=['t_'], restore=False) as tv2:
    ...         print('x' in dir())
    ...         print('t_var1' in dir())
    ...         print('t_var2' in dir())
    ...         print(y)
    ...         print(tv1.stored_nsvars)
    ...         print(sorted(tv2.stored_nsvars.keys()))
    ...         print(tv2.stored_nsvars['t_var1'])
    ...         print(tv2.stored_nsvars['t_var2'])
    ...         x = -3
    ...         t_var3 = -7
    ...         print((x, t_var3, y))
    False
    False
    False
    20
    {'x': 15}
    ['t_var1', 't_var2']
    5
    7
    (-3, -7, 20)
    >>> print((x, y))
    (15, 20)
    >>> print('t_var1' in dir())
    False
    >>> print('t_var2' in dir())
    False
    >>> print('t_var3' in dir())
    False
    >>> print(tv1.retained_tempvars)
    {'x': -3}
    >>> print(tv2.retained_tempvars)
    {'t_var3': -7}


----


Available on `PyPI <https://pypi.org/project/tempvars>`__: ``pip install tempvars``.

Full documentation at
`Read the Docs <http://tempvars.readthedocs.io/en/latest/>`__.

Source on `GitHub <https://github.com/bskinn/tempvars>`__.
Bug reports and feature requests are welcomed at the
`Issues <https://github.com/bskinn/tempvars/issues>`__ page there.
If you like the idea of an enhancement already in the Issues list,
please comment to say so; it'll help with prioritization.

Copyright (c) Brian Skinn 2017-2018

License: The MIT License. See `LICENSE.txt <https://github.com/bskinn/tempvars/blob/master/LICENSE.txt>`__
for full license terms.

