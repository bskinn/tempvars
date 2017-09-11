tempvars
--------

*A context manager for handling temporary variables.*

Jupyter notebooks and the like are the primary anticipated use case.
There's little worse than debugging a worksheet for half an hour
and discovering a typo or carried-over variable name was causing
the misbehavior. The ``TempVars`` context manager clears selected
identifiers from the local (or another) workspace
for the duration of the ``with`` suite, then puts things
back the way it found them afterwards (or not, if desired).

Branches named with the prefix `v.` are volatile. The history there
may be rewritten dramatically, without warning.

Eventually will be available on PyPI.

Source on `GitHub <https://github.com/bskinn/tempvars>`__.

Documentation at Read the Docs (pending).

Copyright (c) Brian Skinn 2017

License: The MIT License. See `LICENSE.txt <https://github.com/bskinn/tempvars/blob/master/LICENSE.txt>`__
for full license terms.

