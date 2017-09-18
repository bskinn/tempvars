tempvars
--------

*A context manager for handling temporary variables in Jupyter Notebook,
IPython, etc.*

There's little worse than debugging a worksheet for half an hour
and discovering a typo or carried-over variable name was causing
the misbehavior. The ``TempVars`` context manager clears selected
identifiers from the namespace for the duration of the ``with``
suite, then puts things back the way it found them afterwards
(or not, if desired). New variables created within the ``with``
suite that match the criteria passed to ``TempVars`` are all deleted
upon exiting the suite::

    test code here

Due to the way Python handles non-global variable scopes, ``TempVars``
can only be used at the global scope. Such contexts include Jupyter notebooks,
the IPython and basic Python REPLs, and at the base scope of executed and
imported modules. Attempts to use ``TempVars`` in non-global contexts will
result in a ``RuntimeError``.


**Administrative**

Branches named with the prefix `v.` are volatile. The history there
may be rewritten dramatically, without warning.

Eventually will be available on PyPI.

Source on `GitHub <https://github.com/bskinn/tempvars>`__.

Documentation at Read the Docs (pending).

Copyright (c) Brian Skinn 2017

License: The MIT License. See `LICENSE.txt <https://github.com/bskinn/tempvars/blob/master/LICENSE.txt>`__
for full license terms.
