tempvars: A context manager for handling temporary variables
============================================================

**Current Development Version:**

.. image:: https://travis-ci.org/bskinn/tempvars.svg?branch=master
    :target: https://travis-ci.org/bskinn/tempvars

.. image:: https://codecov.io/gh/bskinn/tempvars/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bskinn/tempvars

**Most Recent Stable Release:**

.. image:: https://img.shields.io/pypi/v/tempvars.svg
    :target: https://pypi.org/project/tempvars

.. image:: https://img.shields.io/pypi/pyversions/tempvars.svg

**Info:**

.. image:: https://img.shields.io/readthedocs/tempvars/latest.svg
    :target: http://tempvars.readthedocs.io/en/latest/

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/bskinn/tempvars/blob/stable/LICENSE.txt

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

----

**Use Jupyter Notebook?**

**Constantly run into problems from obsolete variables hanging around
in the namespace?**

``tempvars`` *can help.*

Developing in Jupyter notebooks can sometimes be frustrating.
For example, it's aggravating to debug a worksheet for half an hour,
only to discover that a carried-over variable name was hanging around
in the notebook namespace and causing problems.
Or, to open a notebook that "worked fine" the last
time it was used, but only because of random, obsolete variables that happened
to be lingering in the namespace.
Wrapping notebook code in functions/classes is an effective way of avoiding
these sorts of problems, but it's rarely effective or efficient to
do this in the initial exploratory phase of in-notebook development.

``TempVars`` is a context manager that helps to avoid these pitfalls by
clearing selected identifiers from the namespace for the duration of
its scope, then restoring them afterwards (or not, if desired).
Further, any variables created within the managed context
that match the ``TempVars`` filtering criteria are removed from
the namespace upon exiting, ensuring these values do not spuriously
contribute to following code. For convenience, all variables
removed from the namespace at entry and exit
are stored for later reference (see example code below).

Due to the way Python handles non-global scopes, ``TempVars``
can only be used at the global scope. *Any attempt
to use* ``TempVars`` *in non-global contexts will
result in a* ``RuntimeError``. Viable use-cases include Jupyter notebooks,
the IPython and basic Python REPLs, and the outermost scope of executed and
imported modules. Preliminary testing indicates it also works with
`cauldron-notebook <https://github.com/sernst/cauldron>`__, though
it may be less helpful there due to its step-local scoping paradigm
(shared values must be passed around via ``cauldron.shared``).

----

After installing with ``pip install tempvars``, import as:

.. code:: python

    >>> from tempvars import TempVars

For typical use in a Jupyter notebook cell, the recommended approach
is to pick a marker to use on all variables that are to be temporary,
and enclose the entire cell in a ``TempVars`` context. For example,
one could prefix all temporary variables with `t_` and make use
of the `starts` argument:

.. code:: python

    >>> foo = 5
    >>> with TempVars(starts=['t_']):
    ...     print(foo)
    ...     t_bar = 8
    ...     print(foo + t_bar)
    5
    13
    >>> 't_bar' in dir()
    False

A similar effect can be achieved with a suffix such as `_t` and
the `ends` argument.

Temporary variable masking can also be introduced to existing
code in a more selective fashion via the `names` argument:

.. code:: python

    >>> foo = 5
    >>> bar = 7
    >>> with TempVars(names=['bar']):
    ...     print(foo)
    ...     print('bar' in dir())
    5
    False
    >>> foo * bar
    35

Setting the `restore` argument to ``False`` instructs ``TempVars``
not to restore any masked variables to the namespace after its
context exits. This is potentially useful to avoid carryover of
common helper variables (`arr`, `df`, `i`, etc.) to downstream cells
that may have been created earlier in a notebook:

.. code:: python

    >>> for k in ['foo', 'bar']:
    ...     pass
    >>> k
    bar
    >>> with TempVars(names=['k'], restore=False):
    ...     print('k' in dir())
    False
    >>> 'k' in dir()
    False

``TempVars`` stores the values of variables it removes from the namespace,
should they need to be accessed. A bound `with`/`as` statement must be
used in order to enable this:

.. code:: python

    >>> foo = 5
    >>> with TempVars(names=['foo']) as tv:
    ...     print('foo' in dir())
    ...     print(tv.stored_nsvars['foo'])
    ...     foo = 8
    ...     print(foo)
    False
    5
    8
    >>> foo
    5
    >>> tv.retained_tempvars['foo']
    8

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

