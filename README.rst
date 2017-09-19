tempvars
--------

*A context manager for handling temporary variables in Jupyter Notebook,
IPython, etc.*

There's little worse than debugging a worksheet for half an hour
and discovering a typo or carried-over variable name was causing
the misbehavior. The ``TempVars`` context manager clears selected
identifiers from the namespace for the duration of the ``with``
suite, then restores them afterwards (or not, if desired). Any pre-existing
variables as well as variables created within the managed context
that match the criteria passed to ``TempVars`` are removed from
the namespace upon exiting. For convenience, all variables
removed from the namespace at both entry and exit to the context manager
are stored for later reference (see example code below).

**NOTE:** Due to the way Python handles non-global variable scopes, ``TempVars``
can only be used at the global scope. Such contexts include Jupyter notebooks,
the IPython and basic Python REPLs, and at the base scope of executed and
imported modules. Attempts to use ``TempVars`` in non-global contexts will
result in a ``RuntimeError``.

**NOTE ALSO** that ``tempvars`` is *Python 3 only*.

After installing, import as:

.. code:: python

    from tempvars import TempVars

Example Jupyter notebook input:

.. code:: python

    t_var1 = 5
    t_var2 = 7
    x = 15
    y = 20
    with TempVars(names=['x']) as tv1:
        with TempVars(starts=['t_'], restore=False) as tv2:
            print('      x present inside:  ' + str('x' in dir()))
            print(' t_var1 present inside:  ' + str('t_var1' in dir()))
            print(' t_var2 present inside:  ' + str('t_var2' in dir()))
            print('        y value inside:  ' + str(y))
            print('     tv1.stored_nsvars:  ' + str(tv1.stored_nsvars))
            print('     tv2.stored_nsvars:  ' + str(tv2.stored_nsvars))
            x = -3
            t_var3 = -7
            print(' (x, t_var3, y) inside:  ' + str((x, t_var3, y)))
    print('   -------------------------------')
    print('        (x, y) outside:  ' + str((x, y)))
    print('t_var1 present outside:  ' + str('t_var1' in dir()))
    print('t_var2 present outside:  ' + str('t_var2' in dir()))
    print('t_var3 present outside:  ' + str('t_var3' in dir()))
    print(' tv1.retained_tempvars:  ' + str(tv1.retained_tempvars))
    print(' tv2.retained_tempvars:  ' + str(tv2.retained_tempvars))

Output::

          x present inside:  False
     t_var1 present inside:  False
     t_var2 present inside:  False
            y value inside:  20
         tv1.stored_nsvars:  {'x': 15}
         tv2.stored_nsvars:  {'t_var1': 5, 't_var2': 7}
     (x, t_var3, y) inside:  (-3, -7, 20)
       -------------------------------
            (x, y) outside:  (15, 20)
    t_var1 present outside:  False
    t_var2 present outside:  False
    t_var3 present outside:  False
     tv1.retained_tempvars:  {'x': -3}
     tv2.retained_tempvars:  {'t_var3': -7}


Administrative
--------------

Branches named with the prefix `v.` are volatile. The history there
may be rewritten dramatically, without warning.

Available (soon) on PyPI: ``pip install tempvars``.

Source on `GitHub <https://github.com/bskinn/tempvars>`__.

Full documentation (pending) at `Read the Docs <http://tempvars.readthedocs.io>`__.

Copyright (c) Brian Skinn 2017

License: The MIT License. See `LICENSE.txt <https://github.com/bskinn/tempvars/blob/master/LICENSE.txt>`__
for full license terms.
