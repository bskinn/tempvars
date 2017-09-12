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
import inspect


@attr.s()
class TempVars(object):

    ### Arguments indicating variables to treat as temporary vars
    tempvars = attr.ib(default=[])
    starts = attr.ib(default=None, repr=False)
    ends = attr.ib(default=None, repr=False)

    @tempvars.validator
    @starts.validator
    @ends.validator
    def must_be_None_or_iterable_of_string(self, at, val):
        # Standard error for failure return
        te = TypeError("'{0}' must be a list of str".format(at.name))

        if val is None:
            return

        if type(val) != list:
            raise te

        for s in val:
            if type(s) != str:
                raise te
            if at.name != 'tempvars' and (s == '_' or s == '__'):
                raise ValueError("'_' and '__' are not permitted "
                                 "for '{0}'".format(at.name))
        else:
            # Reached the end of the list, so everything's fine
            return

        # Fall-through to this point means it's something other than
        # a list of strings
        raise te

    ### Flag for whether to restore the prior namespace contents
    restore = attr.ib(default=True, validator=attr.validators.instance_of(bool))

    ### Namespace for temp variable management. Defaults to the local variables of the
    # scope at which the TempVars instance was created. Python library docs
    # frown at this, apparently:
    #
    #    https://docs.python.org/3/library/functions.html#locals
    #
    # If a different namespace is desired for some reason, it can be passed here
    # Regardless, definitely don't want this in the `repr`, because it's a big
    # honking mess of stuff.
    ns = attr.ib(repr=False, init=False)

    @ns.default
    def ns_default(self):
        import inspect
        # Need two f_back's since this call is inside a method that's
        # inside a class. This default needs to be crafted this way
        # because it's evaluated at run time, during instantiation.
        # Putting the globals() retrieval directly in the attr.ib()
        # signature above would make the evaluation occur at
        # definition time(? at import?), which apparently changes
        # the relevant scope in a significant way.
        return inspect.currentframe().f_back.f_back.f_globals

    ### Internal vars, not set via the attrs __init__
    # Bucket for preserving variables temporarily removed from
    # the namespace
    stored_nsvars = attr.ib(init=False, repr=False,
                            default=attr.Factory(dict))

    # Bucket for retaining the temporary variables after the context is exited
    stored_tempvars = attr.ib(init=False, repr=False,
                              default=attr.Factory(dict))


    def __enter__(self):
        # Search the namespace for anything matching the .starts or
        # .ends patterns
        for k in self.ns.keys():
            if self.starts is not None:
                for sw in self.starts:
                    if k.startswith(sw):
                        self.tempvars.append(k)

            if self.ends is not None:
                for ew in self.ends:
                    if k.endswith(ew):
                        self.tempvars.append(k)

        # Now that all of the variables have been identified,
        # pop any values that exist from the namespace and store
        for k in self.tempvars:
            if k in self.ns:
                self.stored_nsvars.update({k: self.ns.pop(k)})

        # Return instance so that users can inspect it if needed
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Pop any existing temp variables from the ns and into
        # the storage dict
        for k in self.tempvars:
            if k in self.ns:
                self.stored_tempvars.update({k: self.ns.pop(k)})

        # If restore is set, then repopulate the namespace with
        # the pre-existing values.  Otherwise, do nothing.
        if self.restore:
            self.ns.update(self.stored_nsvars)

        # Containing code should handle any exception raised
        return False
