tempvars
--------

*A context manager for handling temporary variables in Jupyter Notebook,
IPython, etc.*

A frustrating aspect of working with Jupyter notebooks
is debugging a worksheet for half an hour
and discovering a carried-over variable name was hanging around
in the notebook namespace and causing
the misbehavior, or opening a notebook that "worked fine" the last
time it was used because of random variables lingering in the
namespace. The ``TempVars`` context manager avoids these pitfalls by
clearing selected identifiers from the namespace for the duration of
the ``with`` suite, then restoring them afterwards (or not, if desired).
Further, any variables created within the managed context
that match the criteria passed to ``TempVars`` are removed from
the namespace upon exiting, ensuring these values do not spuriously
contribute to following code. For convenience, all variables
that were removed from the namespace at both entry and exit
are stored with their values for later reference (see example code below).

**NOTE:** Due to the way Python handles non-global variable scopes, ``TempVars``
can only be used at the global scope. *Any attempt
to use* ``TempVars`` *in non-global contexts will
result in a* ``RuntimeError``. Viable use-cases include Jupyter notebooks,
the IPython and basic Python REPLs, and the outermost scope of executed and
imported modules. Preliminary testing indicates it also works with
`cauldron-notebook <https://github.com/sernst/cauldron>`__, though
it may be less helpful there due to the step-local scoping paradigm used
(shared values must be passed around via ``cauldron.shared``).

**NOTE ALSO** that ``tempvars`` is *Python 3 only*.

After installing with ``pip install tempvars``, import as:

.. code:: python

    >>> from tempvars import TempVars

Example usage:

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


Administrative
--------------

Branches named with the prefix ``v.`` are volatile. The history there
may be rewritten dramatically, without warning.

Available on PyPI: ``pip install tempvars``.

Source on `GitHub <https://github.com/bskinn/tempvars>`__. Bug reports
and feature requests are welcomed at the
`Issues <https://github.com/bskinn/tempvars/issues>`__ page there.
If you like the idea of an enhancement already in the Issues list,
please comment to say so; it'll help with prioritization.

Full documentation at
`Read the Docs <http://tempvars.readthedocs.io>`__.

Copyright (c) Brian Skinn 2017

License: The MIT License. See `LICENSE.txt <https://github.com/bskinn/tempvars/blob/master/LICENSE.txt>`__
for full license terms.

