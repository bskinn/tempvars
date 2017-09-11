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

    # Arguments indicating variables to treat as temporary vars
    tempvars = attr.ib()
    starts = attr.ib(default=None)
    ends = attr.ib(default=None)

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

        for _ in val:
            if type(_) != str:
                raise te
        else:
            # Reached the end of the list, so everything's fine
            return

        # Fall-through to this point means it's something other than
        # a list of strings
        raise te

    # Flag for whether to restore the prior namespace contents
    restore = attr.ib(default=True, validator=attr.validators.instance_of(bool))

    # Namespace for temp variable management. Defaults to the locals() of the
    # scope at which the TempVars instance was created.
    # If a different namespace is desired for some reason, it can be passed here
    ns = attr.ib()

    @ns.default
    def ns_default(self):
        import inspect
        # Need two f_back's since this call is inside a method that's
        # inside a class.
        return inspect.currentframe().f_back.f_back.f_locals

    @ns.validator
    def ns_must_be_nsdict(self, _, val):
        if not (type(val) == dict and all(map(lambda s: type(s) == str, val.keys()))):
            raise ValueError("'ns' must be a namespace dict")

    ### Internal vars, not set via the attrs __init__
    # Bucket for preserving variables temporarily removed from 
    # the namespace
    stored_nsvars = attr.ib(init=False, default={})


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
        #  store the values and cull them from the namespace
        for k in self.tempvars:
            # Must account for the possibility that a temp var
            # won't already exist.
            try:
                self.stored_nsvars.update({k: self.ns.pop(k)})
            except KeyError:
                # No var found in namespace, do nothing
                pass

        # Return instance so that users can inspect it if needed
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clear the namespace of all temp variables, if they exist
        list(self.ns.pop(_) for _ in self.tempvars if _ in self.ns)

        # If restore is set, then repopulate the namespace with
        # the pre-existing values.  Otherwise, do nothing.
        if self.restore:
            self.ns.update(self.stored_nsvars)

        # Containing code should handle any exception raised
        return False
