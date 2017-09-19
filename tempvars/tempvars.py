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


import attr


@attr.s()
class TempVars(object):

    # ## Arguments indicating variables to treat as temporary vars
    names = attr.ib(default=attr.Factory(list))
    starts = attr.ib(default=None)
    ends = attr.ib(default=None)

    @names.validator
    @starts.validator
    @ends.validator
    def _must_be_None_or_iterable_of_string(self, at, val):
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

    # ## Flag for whether to restore the prior namespace contents
    restore = attr.ib(default=True,
                      validator=attr.validators.instance_of(bool))

    # ## Namespace for temp variable management.
    # Always the globals at the level of the invoker of the TempVars
    # instance (set below in _ns_default).
    ns = attr.ib(repr=False, init=False)

    @ns.default
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
        # the instantiation call.
        return inspect.currentframe().f_back.f_back.f_globals

    # ## Internal vars, not set via the attrs __init__
    # Bucket for preserving variables temporarily removed from
    # the namespace
    stored_nsvars = attr.ib(init=False, repr=False,
                            default=attr.Factory(dict))

    # Bucket for retaining the temporary variables after the context is exited
    retained_tempvars = attr.ib(init=False, repr=False,
                                default=attr.Factory(dict))

    # Bucket for documenting the initial vars passed to tempvars
    passed_names = attr.ib(init=False, repr=True,
                           default=attr.Factory(list))

    def __enter__(self):
        # Save the initial list of tempvars passed
        for _ in self.names:
            self.passed_names.append(_)

        # Search the namespace for anything matching the .starts or
        # .ends patterns
        for k in self.ns.keys():
            if self.starts is not None:
                for sw in self.starts:
                    if k.startswith(sw):
                        self.names.append(k)

            if self.ends is not None:
                for ew in self.ends:
                    if k.endswith(ew):
                        self.names.append(k)

        # Now that all of the variable names have been identified,
        # pop any values that exist from the namespace and store
        for k in self.names:
            if k in self.ns:
                self.stored_nsvars.update({k: self.ns.pop(k)})

        # Return instance so that users can inspect it if needed
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Pop any existing temp variables from the ns and into
        # the storage dict
        for k in self.names:
            if k in self.ns:
                self.retained_tempvars.update({k: self.ns.pop(k)})

        # Check for any new variables that match `starts` and/or
        # `ends` and pop them into the storage dict as well
        vars_to_pop = []
        for k in self.ns.keys():
            if self.starts is not None:
                for sw in self.starts:
                    if k.startswith(sw):
                        vars_to_pop.append(k)

            if self.ends is not None:
                for ew in self.ends:
                    if k.endswith(ew):
                        vars_to_pop.append(k)

        for k in vars_to_pop:
            if k not in self.retained_tempvars.keys():
                self.retained_tempvars.update({k: self.ns.pop(k)})

        # If restore is set, then repopulate the namespace with
        # the pre-existing values.  Otherwise, do nothing.
        if self.restore:
            self.ns.update(self.stored_nsvars)

        # Containing code should handle any exception raised
        return False


if __name__ == '__main__':  # pragma: no cover
    print("Module not executable.")
