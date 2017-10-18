# ------------------------------------------------------------------------------
# Name:        tempvars.py
# Purpose:     Module defining the TempVars class
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     10 Sep 2017
# Copyright:   (c) Brian Skinn 2017
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#       https://www.github.com/bskinn/tempvars
#
# ------------------------------------------------------------------------------

"""Core module defining the TempVars class."""

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
            if at.name != 'names' and (s == '_' or s == '__'):
                raise ValueError("'_' and '__' are not permitted "
                                 "for '{0}'".format(at.name))
            if at.name == 'starts' and s.startswith('__'):
                raise ValueError("'starts' may not start with '__'")
            if at.name == 'ends' and s.endswith('__'):
                raise ValueError("'ends' may not end with '__'")

    # ## Flag for whether to restore the prior namespace contents
    #: |bool| flag indicating whether to restore the prior namespace
    #: contents. **Can** be changed within the |with| suite.
    restore = attr.ib(default=True,
                      validator=attr.validators.instance_of(bool))

    # ## Namespace for temp variable management.
    # Always the globals at the level of the invoker of the TempVars
    # instance (set below in _ns_default).
    _ns = attr.ib(repr=False, init=False)

    @_ns.default
    def _ns_default(self):
        import inspect

        # Need two f_back's since this call is inside a method that's
        # inside a class.
        fm = inspect.currentframe().f_back.f_back

        # Refuse to work if not in top-level scope, since it's *known*
        # to behave incorrectly
        if fm.f_locals is not fm.f_globals:
            raise RuntimeError("TempVars can only be used in the global scope")

        # This default needs to be crafted this way
        # because it's evaluated at run time, during instantiation.
        # Putting the globals() retrieval attempt directly in the attr.ib()
        # signature above would make the evaluation occur at
        # definition time(? at import?), which apparently changes
        # the relevant scope in a significant way (likely it makes
        # this module the accessed scope, rather than the scope of
        # the instantiation call).
        return inspect.currentframe().f_back.f_back.f_globals

    # ## Internal vars, not set via the attrs __init__
    #: |dict| container for preserving variables masked from
    #: the namespace, along with their associated values.
    stored_nsvars = attr.ib(init=False, repr=False,
                            default=attr.Factory(dict))

    #: |dict| container for storing the temporary variables discarded from
    #: the namespace after exiting the |with| block.
    retained_tempvars = attr.ib(init=False, repr=False,
                                default=attr.Factory(dict))

    def __attrs_post_init__(self):
        """Process arguments post-init in various ways."""
        import warnings

        def copy_if_not_none(v):
            """Return a copy of the input argument if it's not None."""
            # This relies on `v` being a finite-size iterable if isn't None
            return v if v is None else v[:]

        # Trigger a warning if no patterns were passed
        if all(map(lambda a: a is None, (self.names, self.starts, self.ends))):
            warnings.warn("No masking patterns provided for TempVars",
                          RuntimeWarning, stacklevel=2)

        # Copy any arguments that aren't None
        self.names = copy_if_not_none(self.names)
        self.starts = copy_if_not_none(self.starts)
        self.ends = copy_if_not_none(self.ends)

    def _pop_to(self, dest_dict, patterns, test_fxn):
        """Pop matching namespace members to a storage dict.

        Namespace variables are popped over to `dest_dict` if
        `test_fxn` is truthy when called with the variable
        name as the first argument and any member of `patterns`
        as the second argument.

        """
        for _ in list(self._ns.keys()):
            # Pop the variable over to the destination dictionary if
            # any ``map`` result is truthy.
            if any(map(lambda p, k=_, t=test_fxn: t(k, p),
                       patterns)):
                dest_dict.update({_: self._ns.pop(_)})

    def __enter__(self):
        """Context manager entry function.

        Removes from the namespace any variables indicated by the
        criteria provided in `names`/`starts`/`ends` and stores
        them in `self.stored_nsvars` for later reference.

        """
        # Pop variables if they match exactly anything in `names`
        if self.names is not None:
            self._pop_to(self.stored_nsvars, self.names, str.__eq__)

        # Pop variables if they match any starts-with pattern
        if self.starts is not None:
            self._pop_to(self.stored_nsvars, self.starts, str.startswith)

        # Pop variables if they match any ends-with pattern
        if self.ends is not None:
            self._pop_to(self.stored_nsvars, self.ends, str.endswith)

        # Return instance so that users can inspect it if desired
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit function.

        Removes from the namespace any variables matching the criteria
        provided in `names`/`starts`/`ends` and stores them in
        `self.retained_tempvars` for later reference.

        No use is made of any exception information passed in. Calling
        context must handle all errors.

        """
        # Pop variables if they match exactly anything in `names`
        if self.names is not None:
            self._pop_to(self.retained_tempvars, self.names, str.__eq__)

        # Pop variables if they match any starts-with pattern
        if self.starts is not None:
            self._pop_to(self.retained_tempvars, self.starts, str.startswith)

        # Pop variables if they match any ends-with pattern
        if self.ends is not None:
            self._pop_to(self.retained_tempvars, self.ends, str.endswith)

        # If restore is set, then repopulate the namespace with
        # the pre-existing values.  Otherwise, do nothing.
        if self.restore:
            self._ns.update(self.stored_nsvars)

        # Containing code should handle any exception raised
        return False


if __name__ == '__main__':  # pragma: no cover
    print("Module not executable.")
