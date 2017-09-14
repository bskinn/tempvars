# ------------------------------------------------------------------------------
# Name:        tests
# Purpose:     Master script for tempvars testing suite
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     11 Sep 2017
# Copyright:   (c) Brian Skinn 2017
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#           http://www.github.com/bskinn/tempvars
#
# ------------------------------------------------------------------------------


class AP(object):
    """ Container for arguments for selecting test suites.

    Also includes PFX, a helper string for substitution/formatting.

    """
    ALL = 'all'
    GOOD = 'good'
    FAIL = 'fail'

    PFX = "--{0}"


def get_parser():
    import argparse

    # Create the parser
    prs = argparse.ArgumentParser(description="Run tests for tempvars")

    # Verbosity argument
    prs.add_argument('-v', action='store_true',
                     help="Show verbose output")

    # Argument to keep temp files around
    prs.add_argument('-k', action='store_true',
                     help="Keep temporary files")

    # Groups without subgroups
    prs.add_argument(AP.PFX.format(AP.ALL), '-a',
                     action='store_true',
                     help="Run all tests (overrides any other selections)")
    prs.add_argument(AP.PFX.format(AP.GOOD), '-g',
                     action='store_true',
                     help="Run all expect-good tests")
    prs.add_argument(AP.PFX.format(AP.FAIL), '-f',
                     action='store_true',
                     help="Run all expect-fail tests")

    # Return the parser
    return prs


def main():
    import tempvars.test
    from tempvars.test.consts import scratch_dir

    import os
    import os.path as osp
    import sys
    import unittest as ut

    # Retrieve the parser
    prs = get_parser()

    # Pull the dict of stored flags, saving the un-consumed args, and
    # update sys.argv
    ns, args_left = prs.parse_known_args()
    params = vars(ns)
    sys.argv = sys.argv[:1] + args_left

    # Create the empty test suite
    ts = ut.TestSuite()

    # Helper function for adding test suites. Just uses ts and params from
    # the main() function scope
    def addsuiteif(suite, flags):
        if any(params[k] for k in flags):
            ts.addTest(suite)

    # Commandline tests per-group
    # Expect-good tests
    addsuiteif(tempvars.test.tempvars_base.suite_expect_good(),
               [AP.ALL, AP.GOOD])
    # Expect-fail tests
    addsuiteif(tempvars.test.tempvars_base.suite_expect_fail(),
               [AP.ALL, AP.FAIL])

    # Create the test runner and execute
    ttr = ut.TextTestRunner(buffer=True,
                            verbosity=(2 if params['v'] else 1))
    success = ttr.run(ts).wasSuccessful()

    # Delete the temp files unless specified
    if not params['k'] and osp.isdir(scratch_dir):
        list(map(os.remove, (osp.join(scratch_dir, _)
                 for _ in os.listdir(scratch_dir) if _.startswith('scratch'))))

    # Return based on success result (enables tox)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

