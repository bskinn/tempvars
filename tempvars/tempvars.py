r"""``TempVars`` *class definition*.

This module is part of ``tempvars``,
a context manager for handling temporary variables in
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

import attr


@attr.s(slots=True)
class TempVars(object):
    """Context manager for handling temporary variables at the global scope.

    **WILL NOT WORK PROPERLY unless used as a context manager!!**

    **CAN ONLY BE USED at global scopes (Python/IPython REPL, Jupyter notebook,
    etc.)**

    Parameters
    ----------
    names :
        |list| of |str| - Variables will be treated as temporary if their names
        test equal to any of these items.

    starts :
        |list| of |str| - Variables will be treated as temporary if their names
        *start* with any of these patterns (tested with
        :meth:`.startswith(starts[i]) <str.startswith>`).

    ends :
        |list| of |str| - Variables will be treated as temporary if their names
        *end* with any of these patterns (tested with
        :meth:`.endswith(ends[i]) <str.endswith>`).

    restore :
        |bool| - If |True|, any variables hidden from the namespace upon entry
        into the |with| suite are restored to the namespace upon exit. If
        |False|, no variables are restored.


    The :class:`TempVars` instance can be bound in the |with| statement for
    access to stored variables, etc.::

        >>> with TempVars(names=['abcd']) as tv:
        ...     pass

    See the :doc:`usage examples <usage>` page for more information.


    **Class Members**

    These objects are accessible via the instance bound as part of the
    |with| statement (``tv`` from the above snippet). All are constructed
    using :func:`attr.ib() <attrs:attr.ib>`.

    """

    # ## Arguments indicating variables to treat as temporary vars
    #: |list| of |str| - All variable names passed to |arg_names|_.
    names = attr.ib(default=None)

    #: |list| of |str| - All passed :meth:`.startswith <str.startswith>`
    #: matching patterns.
    starts = attr.ib(default=None)

    #: |list| of |str| - All passed :meth:`.endswith <str.endswith>`
    #: matching patterns.
    ends = attr.ib(default=None)

    @names.validator
    @starts.validator
    @ends.validator
    def _var_pattern_validator(self, at, val):
        # Standard error for failure return
        te = TypeError("'{0}' must be a list of str".format(at.name))

        if val is None:
            return

        if type(val) != list:
            raise te

        for s in val:
            if type(s) != str:
                raise te

            if at.name != "names" and (s == "_" or s == "__"):
                raise ValueError(
                    "'_' and '__' are not permitted "
                    "for '{0}'".format(at.name)
                )

            if at.name == "starts" and s.startswith("__"):
                raise ValueError("'starts' may not start with '__'")

            if at.name == "ends" and s.endswith("__"):
                raise ValueError("'ends' may not end with '__'")

    # ## Flag for whether to restore the prior namespace contents
    #: |bool| flag indicating whether to restore the prior namespace
    #: contents. **Can** be changed within the |with| suite.
    restore = attr.ib(
        default=True, validator=attr.validators.instance_of(bool)
    )

    # ## Namespace for temp variable management.
    # Always the globals at the level of the invoker of the TempVars
    # instance (set below in _ns_default).
    _ns = attr.ib(repr=False, init=False)

    @_ns.default
    def _ns_default(self):
        """Assign the globals() namespace of the instantiating scope.

        This "default value" needs to be crafted this way
        because this way it's evaluated at run time, during instantiation.
        Putting the globals() retrieval attempt directly in the attr.ib()
        signature above would instead make the evaluation occur at
        import/definition, which changes the relevant scope in a
        significant way: it makes **this module** the scope of
        the invocation of globals(), rather than the scope of
        the instantiation call.

        """
        import inspect

        # Need two f_back's since this call is inside a method that's
        # inside a class.
        fm = inspect.currentframe().f_back.f_back

        # Refuse to work if not in top-level scope, since it's *known*
        # to behave incorrectly
        if fm.f_locals is not fm.f_globals:
            raise RuntimeError("TempVars can only be used in the global scope")

        return fm.f_globals

    # ## Internal vars, not set via the attrs __init__
    #: |dict| container for preserving variables masked from
    #: the namespace, along with their associated values.
    stored_nsvars = attr.ib(init=False, repr=False, default=attr.Factory(dict))

    #: |dict| container for storing the temporary variables discarded from
    #: the namespace after exiting the |with| block.
    retained_tempvars = attr.ib(
        init=False, repr=False, default=attr.Factory(dict)
    )

    def __attrs_post_init__(self):
        """Proofread identifier-matching arguments and copy for safety."""
        from copy import copy
        import warnings

        # Raise a warning if no patterns were passed
        if all(
            map(
                lambda a: a is None or len(a) == 0,
                (self.names, self.starts, self.ends),
            )
        ):
            warnings.warn(
                "No masking patterns provided for TempVars",
                RuntimeWarning,
                stacklevel=2,
            )

        # Copy any arguments that aren't None
        self.names = copy(self.names)
        self.starts = copy(self.starts)
        self.ends = copy(self.ends)

    def _pop_to(self, dest_dict, patterns, test_fxn):
        """Pop matching namespace members to a storage dict.

        Namespace variables are popped over to `dest_dict` if
        `test_fxn` is truthy when called with the variable
        name as the first argument and any member of `patterns`
        as the second argument.

        """
        for key in list(self._ns.keys()):
            if any(map(lambda p, k=key, t=test_fxn: t(k, p), patterns)):
                dest_dict.update({key: self._ns.pop(key)})

    def __enter__(self):
        """Context manager entry function.

        Removes from the namespace any variables indicated by the
        criteria provided in `names`/`starts`/`ends` and stores
        them in `self.stored_nsvars` for later reference.

        """
        patterns = (self.names, self.starts, self.ends)
        funcs = (str.__eq__, str.startswith, str.endswith)

        for p, f in zip(patterns, funcs):
            if p is not None:
                self._pop_to(self.stored_nsvars, p, f)

        # Return instance so that users can inspect/modify it if desired
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit function.

        Removes from the namespace any variables matching the criteria
        provided in `names`/`starts`/`ends` and stores them in
        `self.retained_tempvars` for later reference.

        No use is made of any exception information passed in. Calling
        context must handle all errors.

        """
        patterns = (self.names, self.starts, self.ends)
        funcs = (str.__eq__, str.startswith, str.endswith)

        for p, f in zip(patterns, funcs):
            if p is not None:
                self._pop_to(self.retained_tempvars, p, f)

        if self.restore:
            self._ns.update(self.stored_nsvars)

        # Containing code should handle any exception raised
        return False


if __name__ == "__main__":  # pragma: no cover
    print("Module not executable.")
