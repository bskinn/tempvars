# ------------------------------------------------------------------------------
# Name:        tempvars_base
# Purpose:     Base module for tempvars tests
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     11 Sep 2017
# Copyright:   (c) Brian Skinn 2017
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#            https://www.github.com/bskinn/tempvars
#
# ------------------------------------------------------------------------------


import os
import os.path as osp
import unittest as ut


# Module-scope mutable object to be used as a closure in `runCode` method
keep = []

# Only want to clear the scratch folder once. Length-zero means it hasn't
# been cleared; length-one means it has
cleared = []


class SuperTestTempVars_ScratchMgr(object):
    """Superclass to handle scratch folder management."""

    @classmethod
    def setUpClass(cls):

        from tempvars.test.consts import scratch_dir

        # Ensure scratch directory exists
        if not osp.isdir(scratch_dir):
            os.mkdir(scratch_dir)

        # Clear its contents if it's the first ut.TestCase executed
        if len(cleared) == 0:
            cleared.append(None)
            for _ in os.listdir(scratch_dir):
                fn = osp.join(scratch_dir, _)
                if osp.isfile(fn):
                    os.remove(fn)

    @classmethod
    def tearDownClass(cls):

        from tempvars.test.consts import scratch_fn

        # Always delete the basic scratch file if it exists
        # If 'keep' is set, then it presumably won't exist
        if osp.isfile(scratch_fn):
            os.remove(scratch_fn)


    def runCode(self, code, name):

        import importlib

        from tempvars.test.consts import scratch_fn

        # Write the desired code to the temp file
        with open(scratch_fn, 'w') as f:
            f.write(code)

        # Must force a full recompile of scratch.py. Clearing
        # __pycache__ was not sufficient, nor was using
        # importlib.invalidate_caches()
        import tempvars.test.scratch.scratch as scratch
        importlib.reload(scratch)

        # Rename to augmented file if indicated to keep
        if keep[0]:
            base, ext = osp.splitext(scratch_fn)
            os.rename(scratch_fn, '{0}_{1}{2}'.format(base, name, ext))

        # `d` is a result accumulator dict that should be built up within
        # the code of each test
        return scratch.d


    def locals_subTest(self, id, locdict, val):
        with self.subTest(id):
            if val:
                self.assertTrue(locdict[id])
            else:
                self.assertFalse(locdict[id])


class TestTempVarsExpectGood(SuperTestTempVars_ScratchMgr, ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_Good_tempvarsPassed(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "x = 5\n"
                         "with TempVars(tempvars=['x']) as tv:\n"
                         "    d['inside_absent'] = 'x' not in dir()\n"
                         "d['outside_present'] = 'x' in dir()\n"
                         , 'Good_tempvarsPassed')

        for _ in ['inside_absent', 'outside_present']:
            self.locals_subTest(_, d, True)


    def test_Good_tempvarsPassed_NoRestore(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "x = 5\n"
                         "with TempVars(tempvars=['x'], restore=False) as tv:\n"
                         "    d['inside_absent'] = 'x' not in dir()\n"
                         "d['outside_absent'] = 'x' not in dir()\n"
                         , 'Good_tempvarsPassed_NoRestore')

        for _ in ['inside_absent', 'outside_absent']:
            self.locals_subTest(_, d, True)



    def test_Good_tempvarsPassedButNotPresent(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "x = 5\n"
                         "with TempVars(tempvars=['y']) as tv:\n"
                         "    y = 12\n"
                         "    d['inside_x_present'] = 'x' in dir()\n"
                         "    d['inside_y_present'] = 'y' in dir()\n"
                         "d['outside_x_present'] = 'x' in dir()\n"
                         "d['outside_y_absent'] = 'y' not in dir()\n"
                         "d['outside_y_retained'] = tv.retained_tempvars['y'] == 12\n"
                         , 'Good_tempvarsPassedButNotPresent')

        for _ in ['inside_x_present', 'outside_x_present',
                  'inside_y_present', 'outside_y_absent',
                  'outside_y_retained']:
            self.locals_subTest(_, d, True)


    def test_Good_startsPassed(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "t_x = 5\n"
                         "t_y = 8\n"
                         "z_x = 14\n"
                         "with TempVars(starts=['t_']) as tv:\n"
                         "    d['inside_x_absent'] = 't_x' not in dir()\n"
                         "    d['inside_y_absent'] = 't_y' not in dir()\n"
                         "    d['inside_z_present'] = 'z_x' in dir()\n"
                         "d['outside_x_present'] = 't_x' in dir()\n"
                         "d['outside_y_present'] = 't_y' in dir()\n"
                         "d['outside_z_present'] = 'z_x' in dir()\n"
                         , 'Good_startsPassed')

        for _ in ['inside_x_absent', 'inside_y_absent',
                  'inside_z_present', 'outside_x_present',
                  'outside_y_present', 'outside_z_present']:
            self.locals_subTest(_, d, True)


    def test_Good_endsPassed(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(ends=['_x']) as tv:\n"
             "    inside_x = 't_x' in dir()\n"
             "    inside_y = 't_y' in dir()\n"
             "    inside_z = 'z_x' in dir()\n"
             "outside_x = 't_x' in dir()\n"
             "outside_y = 't_y' in dir()\n"
             "outside_z = 'z_x' in dir()\n"
             , locals())

        for _ in ['inside_x', 'inside_z']:
            self.locals_subTest(_, locals(), False)

        for _ in ['inside_y', 'outside_x', 'outside_y', 'outside_z']:
            self.locals_subTest(_, locals(), True)


    def test_Good_startsPassed_NoRestore(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(starts=['t_'], restore=False) as tv:\n"
             "    inside_x = 't_x' in dir()\n"
             "    inside_y = 't_y' in dir()\n"
             "    inside_z = 'z_x' in dir()\n"
             "outside_x = 't_x' in dir()\n"
             "outside_y = 't_y' in dir()\n"
             "outside_z = 'z_x' in dir()\n"
             , locals())

        for _ in ['inside_z', 'outside_z']:
            self.locals_subTest(_, locals(), True)

        for _ in ['inside_x', 'outside_x', 'inside_y', 'outside_y']:
            self.locals_subTest(_, locals(), False)


    def test_Good_endsPassed_NoRestore(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(ends=['_x'], restore=False) as tv:\n"
             "    inside_x = 't_x' in dir()\n"
             "    inside_y = 't_y' in dir()\n"
             "    inside_z = 'z_x' in dir()\n"
             "outside_x = 't_x' in dir()\n"
             "outside_y = 't_y' in dir()\n"
             "outside_z = 'z_x' in dir()\n"
             , locals())

        for _ in ['inside_y', 'outside_y']:
            self.locals_subTest(_, locals(), True)

        for _ in ['inside_x', 'outside_x', 'inside_z', 'outside_z']:
            self.locals_subTest(_, locals(), False)


    def test_Good_checkStorage_tempvarsNoRestore(self):

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "before_val = x == 5\n"
             "with TempVars(tempvars=['x'], restore=False) as tv:\n"
             "    inside_initial_exist = 'x' in dir()\n"
             "    inside_stored_nsvar = tv.stored_nsvars.get('x') is 5\n"
             "    x = 18\n"
             "    inside_final_exist = 'x' in dir()\n"
             "    inside_final_val = x == 18\n"
             "    inside_retained_tempvars_empty = len(tv.retained_tempvars) == 0\n"
             "outside_stored_nsvar = tv.stored_nsvars.get('x') == 5\n"
             "outside_retained_tempvar = tv.retained_tempvars.get('x') == 18\n"
             "outside_final_exist = 'x' in dir()\n"
             , locals())

        self.locals_subTest('before_val', locals(), True)
        self.locals_subTest('inside_initial_exist', locals(), False)
        for _ in ['inside_stored_nsvar', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_retained_tempvar']:
            self.locals_subTest(_, locals(), True)
        self.locals_subTest('outside_final_exist', locals(), False)


    def test_Good_checkStorage_startsNoRestore(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "before_val = t_x == 5\n"
             "with TempVars(starts=['t_'], restore=False) as tv:\n"
             "    inside_initial_exist = 't_x' in dir()\n"
             "    inside_stored_nsvar = tv.stored_nsvars.get('t_x') is 5\n"
             "    t_x = 18\n"
             "    t_y = 43\n"
             "    inside_final_exist = 't_x' in dir()\n"
             "    inside_final_val = t_x == 18\n"
             "    inside_retained_tempvars_empty = len(tv.retained_tempvars) == 0\n"
             "outside_stored_nsvar = tv.stored_nsvars.get('t_x') == 5\n"
             "outside_newvar_absent = 't_y' not in dir()\n"
             "outside_newvar_not_in_nsvars = 't_y' not in tv.stored_nsvars\n"
             "outside_retained_tempvar = tv.retained_tempvars.get('t_x') == 18\n"
             "outside_newvar_in_retained_tempvars = 't_y' in tv.retained_tempvars\n"
             "outside_final_exist = 't_x' in dir()\n"
             , locals())

        self.locals_subTest('before_val', locals(), True)
        self.locals_subTest('inside_initial_exist', locals(), False)
        for _ in ['inside_stored_nsvar', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_newvar_absent',
                  'outside_newvar_not_in_nsvars', 'outside_newvar_in_retained_tempvars',
                  'outside_retained_tempvar']:
            self.locals_subTest(_, locals(), True)
        self.locals_subTest('outside_final_exist', locals(), False)


    def test_Good_checkStorage_endsNoRestore(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "before_val = t_x == 5\n"
             "with TempVars(ends=['_x'], restore=False) as tv:\n"
             "    inside_initial_exist = 't_x' in dir()\n"
             "    inside_stored_nsvar = tv.stored_nsvars.get('t_x') is 5\n"
             "    t_x = 18\n"
             "    r_x = 43\n"
             "    inside_final_exist = 't_x' in dir()\n"
             "    inside_final_val = t_x == 18\n"
             "    inside_retained_tempvars_empty = len(tv.retained_tempvars) == 0\n"
             "outside_stored_nsvar = tv.stored_nsvars.get('t_x') == 5\n"
             "outside_newvar_absent = 'r_x' not in dir()\n"
             "outside_newvar_not_in_nsvars = 'r_x' not in tv.stored_nsvars\n"
             "outside_retained_tempvar = tv.retained_tempvars.get('t_x') == 18\n"
             "outside_newvar_in_retained_tempvars = 'r_x' in tv.retained_tempvars\n"
             "outside_final_exist = 't_x' in dir()\n"
             , locals())

        self.locals_subTest('before_val', locals(), True)
        self.locals_subTest('inside_initial_exist', locals(), False)
        for _ in ['inside_stored_nsvar', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_newvar_absent',
                  'outside_newvar_not_in_nsvars', 'outside_newvar_in_retained_tempvars',
                  'outside_retained_tempvar']:
            self.locals_subTest(_, locals(), True)
        self.locals_subTest('outside_final_exist', locals(), False)


    def test_Good_checkArgs(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "r_x = 12\n"
             "f_z = 59\n"
             "d_z = 12\n"
             "g_r = 43\n"
             "with TempVars(tempvars=['g_r'], starts=['t_'], ends=['_z']) as tv:\n"
             "    g_r_absent = 'g_r' not in dir()\n"
             "    t_x_absent = 't_x' not in dir()\n"
             "    t_y_absent = 't_y' not in dir()\n"
             "    r_x_present = 'r_x' in dir()\n"
             "    f_z_absent = 'f_z' not in dir()\n"
             "    d_z_absent = 'd_z' not in dir()\n"
             "    g_r_in_tempvars = 'g_r' in tv.tempvars\n"
             "    t_x_in_tempvars = 't_x' in tv.tempvars\n"
             "    t_y_in_tempvars = 't_y' in tv.tempvars\n"
             "    r_x_not_in_tempvars = 'r_x' not in tv.tempvars\n"
             "    f_z_in_tempvars = 'f_z' in tv.tempvars\n"
             "    d_z_in_tempvars = 'd_z' in tv.tempvars\n"
             "    g_r_in_passed_tempvars = 'g_r' in tv.passed_tempvars\n"
             "    t_x_not_in_passed_tempvars = 't_x' not in tv.passed_tempvars\n"
             "    t_y_not_in_passed_tempvars = 't_y' not in tv.passed_tempvars\n"
             "    r_x_not_in_passed_tempvars = 'r_x' not in tv.passed_tempvars\n"
             "    f_z_not_in_passed_tempvars = 'f_z' not in tv.passed_tempvars\n"
             "    d_z_not_in_passed_tempvars = 'd_z' not in tv.passed_tempvars\n"
             , locals())

        for _ in ['g_r_absent', 't_x_absent', 't_y_absent',
                  'r_x_present', 'f_z_absent', 'd_z_absent',
                  'g_r_in_tempvars', 't_x_in_tempvars', 't_y_in_tempvars',
                  'r_x_not_in_tempvars', 'f_z_in_tempvars', 'd_z_in_tempvars',
                  'g_r_in_passed_tempvars', 't_x_not_in_passed_tempvars',
                  't_y_not_in_passed_tempvars', 'r_x_not_in_passed_tempvars',
                  'f_z_not_in_passed_tempvars', 'd_z_not_in_passed_tempvars']:
            self.locals_subTest(_, locals(), True)


    def test_Good_tempvarsMultiPassed(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "z_m = 24\n"
             "r_x = 44\n"
             "with TempVars(tempvars=['t_x', 'z_m']) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_present = 't_y' in dir()\n"
             "    inside_z_x_present = 'z_x' in dir()\n"
             "    inside_z_m_absent = 'z_m' not in dir()\n"
             "    inside_r_x_present = 'r_x' in dir()\n"
             "outside_t_x_present = 't_x' in dir()\n"
             "outside_t_y_present = 't_y' in dir()\n"
             "outside_z_x_present = 'z_x' in dir()\n"
             "outside_z_m_present = 'z_m' in dir()\n"
             "outside_r_x_present = 'r_x' in dir()\n"
             , locals())

        for _ in ['inside_t_x_absent', 'inside_t_y_present',
                  'inside_z_x_present', 'inside_z_m_absent',
                  'inside_r_x_present',
                  'outside_t_x_present', 'outside_t_y_present',
                  'outside_z_x_present', 'outside_z_m_present',
                  'outside_r_x_present']:
            self.locals_subTest(_, locals(), True)


    def test_Good_startsMultiPassed(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "z_m = 24\n"
             "r_x = 44\n"
             "with TempVars(starts=['t_', 'z_']) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_absent = 't_y' not in dir()\n"
             "    inside_z_x_absent = 'z_x' not in dir()\n"
             "    inside_z_m_absent = 'z_m' not in dir()\n"
             "    inside_r_x_present = 'r_x' in dir()\n"
             "outside_t_x_present = 't_x' in dir()\n"
             "outside_t_y_present = 't_y' in dir()\n"
             "outside_z_x_present = 'z_x' in dir()\n"
             "outside_z_m_present = 'z_m' in dir()\n"
             "outside_r_x_present = 'r_x' in dir()\n"
             , locals())

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_absent', 'inside_z_m_absent',
                  'inside_r_x_present',
                  'outside_t_x_present', 'outside_t_y_present',
                  'outside_z_x_present', 'outside_z_m_present',
                  'outside_r_x_present']:
            self.locals_subTest(_, locals(), True)


    def test_Good_endsMultiPassed(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "z_m = 24\n"
             "r_x = 44\n"
             "with TempVars(ends=['_x', '_y']) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_absent = 't_y' not in dir()\n"
             "    inside_z_x_absent = 'z_x' not in dir()\n"
             "    inside_z_m_present = 'z_m' in dir()\n"
             "    inside_r_x_absent = 'r_x' not in dir()\n"
             "outside_t_x_present = 't_x' in dir()\n"
             "outside_t_y_present = 't_y' in dir()\n"
             "outside_z_x_present = 'z_x' in dir()\n"
             "outside_z_m_present = 'z_m' in dir()\n"
             "outside_r_x_present = 'r_x' in dir()\n"
             , locals())

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_absent', 'inside_z_m_present',
                  'inside_r_x_absent',
                  'outside_t_x_present', 'outside_t_y_present',
                  'outside_z_x_present', 'outside_z_m_present',
                  'outside_r_x_present']:
            self.locals_subTest(_, locals(), True)


# Examining if expected behavior of nested contexts occurs (goal to allow mixed restore=True|False)


def suite_expect_good(k):
    keep.append(k)
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestTempVarsExpectGood)])

    return s


def suite_expect_fail(k):
    keep.append(k)
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([])

    return s



if __name__ == '__main__':  # pragma: no cover
    print("Module not executable.")

