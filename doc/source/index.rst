.. Root file for tempvars documentation

tempvars
========

*Streamlined temporary variable management in Jupyter Notebook, IPython, etc.*

A frustrating aspect of working with Jupyter notebooks
is debugging a worksheet for half an hour
and discovering a carried-over variable name was hanging around
in the notebook namespace and causing
that cryptic misbehavior. Similarly, it's incredibly annoying to open
a broken notebook that "worked fine" the last
time it was used because of random variables lingering in the
namespace. 

The ``TempVars`` context manager helps to avoid these pitfalls by
masking selected identifiers from the namespace for the duration of
the ``with`` suite, then restoring them afterwards (or not, if desired).
Further, any variables created within the managed context
that match the criteria passed to ``TempVars`` are removed from
the namespace upon exiting, ensuring these values do not spuriously
contribute to following code. For convenience, all variables
that were removed from the namespace at both entry and exit
are stored with their values for later reference; see
:ref:`usage_stored_nsvars` and :ref:`usage_ret_tempvars`, respectively,
in the usage instructions.

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

Install with ``pip install tempvars``, import as
``from tempvars import TempVars``, and use as
``with TempVars({pattern args}):``.

The project source is hosted on `GitHub <https://github.com/bskinn/tempvars>`__.
Bug reports and feature requests are welcomed at the
`Issues <https://github.com/bskinn/tempvars/issues>`__ page there.
If you like the idea of an existing enhancement in the Issues list,
please comment to say so; it'll help prioritization.


.. toctree::
    :maxdepth: 1
    :caption: Contents:

    Usage <usage>
    API <api>


