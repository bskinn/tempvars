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
        from test_scratch import scratch
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
                         "    d['inside_t_x_absent'] = 't_x' not in dir()\n"
                         "    d['inside_t_y_absent'] = 't_y' not in dir()\n"
                         "    d['inside_z_x_present'] = 'z_x' in dir()\n"
                         "d['outside_t_x_present'] = 't_x' in dir()\n"
                         "d['outside_t_y_present'] = 't_y' in dir()\n"
                         "d['outside_z_x_present'] = 'z_x' in dir()\n"
                         , 'Good_startsPassed')

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_present', 'outside_t_x_present',
                  'outside_t_y_present', 'outside_z_x_present']:
            self.locals_subTest(_, d, True)


    def test_Good_endsPassed(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "t_x = 5\n"
                         "t_y = 8\n"
                         "z_x = 14\n"
                         "with TempVars(ends=['_x']) as tv:\n"
                         "    d['inside_t_x_absent'] = 't_x' not in dir()\n"
                         "    d['inside_t_y_present'] = 't_y' in dir()\n"
                         "    d['inside_z_x_absent'] = 'z_x' not in dir()\n"
                         "d['outside_t_x_present'] = 't_x' in dir()\n"
                         "d['outside_t_y_present'] = 't_y' in dir()\n"
                         "d['outside_z_x_present'] = 'z_x' in dir()\n"
                         , 'Good_endsPassed')

        for _ in ['inside_t_x_absent', 'inside_t_y_present',
                  'inside_z_x_absent', 'outside_t_x_present',
                  'outside_t_y_present', 'outside_z_x_present']:
            self.locals_subTest(_, d, True)


    def test_Good_startsPassed_NoRestore(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "t_x = 5\n"
                         "t_y = 8\n"
                         "z_x = 14\n"
                         "with TempVars(starts=['t_'], restore=False) as tv:\n"
                         "    d['inside_t_x_absent'] = 't_x' not in dir()\n"
                         "    d['inside_t_y_absent'] = 't_y' not in dir()\n"
                         "    d['inside_z_x_present'] = 'z_x' in dir()\n"
                         "d['outside_t_x_absent'] = 't_x' not in dir()\n"
                         "d['outside_t_y_absent'] = 't_y' not in dir()\n"
                         "d['outside_z_x_present'] = 'z_x' in dir()\n"
                         , 'Good_startsPassed_NoRestore')

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_present', 'outside_t_x_absent',
                  'outside_t_y_absent', 'outside_z_x_present']:
            self.locals_subTest(_, d, True)


    def test_Good_endsPassed_NoRestore(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "t_x = 5\n"
                         "t_y = 8\n"
                         "z_x = 14\n"
                         "with TempVars(ends=['_x'], restore=False) as tv:\n"
                         "    d['inside_t_x_absent'] = 't_x' not in dir()\n"
                         "    d['inside_t_y_present'] = 't_y' in dir()\n"
                         "    d['inside_z_x_absent'] = 'z_x' not in dir()\n"
                         "d['outside_t_x_absent'] = 't_x' not in dir()\n"
                         "d['outside_t_y_present'] = 't_y' in dir()\n"
                         "d['outside_z_x_absent'] = 'z_x' not in dir()\n"
                         , 'Good_endsPassed_NoRestore')

        for _ in ['inside_t_x_absent', 'inside_t_y_present',
                  'inside_z_x_absent', 'outside_t_x_absent',
                  'outside_t_y_present', 'outside_z_x_absent']:
            self.locals_subTest(_, d, True)


    def test_Good_checkStorage_tempvarsNoRestore(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "x = 5\n"
                         "d['before_val'] = x == 5\n"
                         "with TempVars(tempvars=['x'], restore=False) as tv:\n"
                         "    d['inside_initial_absent'] = 'x' not in dir()\n"
                         "    d['inside_stored_nsvar'] = tv.stored_nsvars.get('x') == 5\n"
                         "    x = 18\n"
                         "    d['inside_final_exist'] = 'x' in dir()\n"
                         "    d['inside_final_val'] = x == 18\n"
                         "    d['inside_retained_tempvars_empty'] = len(tv.retained_tempvars) == 0\n"
                         "d['outside_stored_nsvar'] = tv.stored_nsvars.get('x') == 5\n"
                         "d['outside_retained_tempvar'] = tv.retained_tempvars.get('x') == 18\n"
                         "d['outside_final_absent'] = 'x' not in dir()\n"
                         , 'Good_checkStorage_tempvarsNoRestore')

        for _ in ['before_val', 'inside_initial_absent',
                  'inside_stored_nsvar', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_retained_tempvar',
                  'outside_final_absent']:
            self.locals_subTest(_, d, True)


    def test_Good_checkStorage_startsNoRestore(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "t_x = 5\n"
                         "d['before_var_present'] = t_x == 5\n"
                         "d['before_newvar_absent'] = 't_y' not in dir()\n"
                         "with TempVars(starts=['t_'], restore=False) as tv:\n"
                         "    d['inside_initial_absent'] = 't_x' not in dir()\n"
                         "    d['inside_initial_newvar_absent'] = 't_y' not in dir()\n"
                         "    d['inside_stored_nsvar'] = tv.stored_nsvars.get('t_x') == 5\n"
                         "    d['inside_newvar_not_in_nsvars'] = 't_y' not in tv.stored_nsvars\n"
                         "    t_x = 18\n"
                         "    t_y = 43\n"
                         "    d['inside_final_exist'] = 't_x' in dir()\n"
                         "    d['inside_final_val'] = t_x == 18\n"
                         "    d['inside_retained_tempvars_empty'] = len(tv.retained_tempvars) == 0\n"
                         "d['outside_stored_nsvar'] = tv.stored_nsvars.get('t_x') == 5\n"
                         "d['outside_newvar_absent'] = 't_y' not in dir()\n"
                         "d['outside_newvar_not_in_nsvars'] = 't_y' not in tv.stored_nsvars\n"
                         "d['outside_retained_tempvar'] = tv.retained_tempvars.get('t_x') == 18\n"
                         "d['outside_newvar_in_retained_tempvars'] = 't_y' in tv.retained_tempvars\n"
                         "d['outside_final_absent'] = 't_x' not in dir()\n"
                         , 'Good_checkStorage_startsNoRestore')

        for _ in ['before_var_present', 'before_newvar_absent', 'inside_initial_absent',
                  'inside_initial_newvar_absent',
                  'inside_stored_nsvar', 'inside_newvar_not_in_nsvars', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_newvar_absent',
                  'outside_newvar_not_in_nsvars', 'outside_newvar_in_retained_tempvars',
                  'outside_retained_tempvar', 'outside_final_absent']:
            self.locals_subTest(_, d, True)


    def test_Good_checkStorage_endsNoRestore(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "t_x = 5\n"
                         "d['before_val'] = t_x == 5\n"
                         "d['before_newvar_absent'] = 'r_x' not in dir()\n"
                         "with TempVars(ends=['_x'], restore=False) as tv:\n"
                         "    d['inside_initial_absent'] = 't_x' not in dir()\n"
                         "    d['inside_initial_newvar_absent'] = 'r_x' not in dir()\n"
                         "    d['inside_stored_nsvar'] = tv.stored_nsvars.get('t_x') is 5\n"
                         "    d['inside_newvar_not_in_nsvars'] = 'r_x' not in tv.stored_nsvars\n"
                         "    t_x = 18\n"
                         "    r_x = 43\n"
                         "    d['inside_final_exist'] = 't_x' in dir()\n"
                         "    d['inside_final_val'] = t_x == 18\n"
                         "    d['inside_retained_tempvars_empty'] = len(tv.retained_tempvars) == 0\n"
                         "d['outside_stored_nsvar'] = tv.stored_nsvars.get('t_x') == 5\n"
                         "d['outside_newvar_absent'] = 'r_x' not in dir()\n"
                         "d['outside_newvar_not_in_nsvars'] = 'r_x' not in tv.stored_nsvars\n"
                         "d['outside_retained_tempvar'] = tv.retained_tempvars.get('t_x') == 18\n"
                         "d['outside_newvar_in_retained_tempvars'] = 'r_x' in tv.retained_tempvars\n"
                         "d['outside_final_absent'] = 't_x' not in dir()\n"
                         , 'Good_checkStorage_endsNoRestore')

        for _ in ['before_val', 'before_newvar_absent', 'inside_initial_absent',
                  'inside_initial_newvar_absent', 'inside_newvar_not_in_nsvars',
                  'inside_stored_nsvar', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_newvar_absent',
                  'outside_newvar_not_in_nsvars', 'outside_newvar_in_retained_tempvars',
                  'outside_retained_tempvar', 'outside_final_absent']:
            self.locals_subTest(_, d, True)


    def test_Good_checkArgs(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "t_x = 5\n"
                         "t_y = 8\n"
                         "r_x = 12\n"
                         "f_z = 59\n"
                         "d_z = 12\n"
                         "g_r = 43\n"
                         "with TempVars(tempvars=['g_r'], starts=['t_'], ends=['_z']) as tv:\n"
                         "    d['g_r_absent'] = 'g_r' not in dir()\n"
                         "    d['t_x_absent'] = 't_x' not in dir()\n"
                         "    d['t_y_absent'] = 't_y' not in dir()\n"
                         "    d['r_x_present'] = 'r_x' in dir()\n"
                         "    d['f_z_absent'] = 'f_z' not in dir()\n"
                         "    d['d_z_absent'] = 'd_z' not in dir()\n"
                         "    d['g_r_in_tempvars'] = 'g_r' in tv.tempvars\n"
                         "    d['t_x_in_tempvars'] = 't_x' in tv.tempvars\n"
                         "    d['t_y_in_tempvars'] = 't_y' in tv.tempvars\n"
                         "    d['r_x_not_in_tempvars'] = 'r_x' not in tv.tempvars\n"
                         "    d['f_z_in_tempvars'] = 'f_z' in tv.tempvars\n"
                         "    d['d_z_in_tempvars'] = 'd_z' in tv.tempvars\n"
                         "    d['g_r_in_passed_tempvars'] = 'g_r' in tv.passed_tempvars\n"
                         "    d['t_x_not_in_passed_tempvars'] = 't_x' not in tv.passed_tempvars\n"
                         "    d['t_y_not_in_passed_tempvars'] = 't_y' not in tv.passed_tempvars\n"
                         "    d['r_x_not_in_passed_tempvars'] = 'r_x' not in tv.passed_tempvars\n"
                         "    d['f_z_not_in_passed_tempvars'] = 'f_z' not in tv.passed_tempvars\n"
                         "    d['d_z_not_in_passed_tempvars'] = 'd_z' not in tv.passed_tempvars\n"
                         , 'Good_checkArgs')

        for _ in ['g_r_absent', 't_x_absent', 't_y_absent',
                  'r_x_present', 'f_z_absent', 'd_z_absent',
                  'g_r_in_tempvars', 't_x_in_tempvars', 't_y_in_tempvars',
                  'r_x_not_in_tempvars', 'f_z_in_tempvars', 'd_z_in_tempvars',
                  'g_r_in_passed_tempvars', 't_x_not_in_passed_tempvars',
                  't_y_not_in_passed_tempvars', 'r_x_not_in_passed_tempvars',
                  'f_z_not_in_passed_tempvars', 'd_z_not_in_passed_tempvars']:
            self.locals_subTest(_, d, True)


    def test_Good_tempvarsMultiPassed(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "t_x = 5\n"
                         "t_y = 8\n"
                         "z_x = 14\n"
                         "z_m = 24\n"
                         "r_x = 44\n"
                         "with TempVars(tempvars=['t_x', 'z_m']) as tv:\n"
                         "    d['inside_t_x_absent'] = 't_x' not in dir()\n"
                         "    d['inside_t_y_present'] = 't_y' in dir()\n"
                         "    d['inside_z_x_present'] = 'z_x' in dir()\n"
                         "    d['inside_z_m_absent'] = 'z_m' not in dir()\n"
                         "    d['inside_r_x_present'] = 'r_x' in dir()\n"
                         "d['outside_t_x_present'] = 't_x' in dir()\n"
                         "d['outside_t_y_present'] = 't_y' in dir()\n"
                         "d['outside_z_x_present'] = 'z_x' in dir()\n"
                         "d['outside_z_m_present'] = 'z_m' in dir()\n"
                         "d['outside_r_x_present'] = 'r_x' in dir()\n"
                         , 'Good_tempvarsMultiPassed')

        for _ in ['inside_t_x_absent', 'inside_t_y_present',
                  'inside_z_x_present', 'inside_z_m_absent',
                  'inside_r_x_present',
                  'outside_t_x_present', 'outside_t_y_present',
                  'outside_z_x_present', 'outside_z_m_present',
                  'outside_r_x_present']:
            self.locals_subTest(_, d, True)


    def test_Good_startsMultiPassed(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "t_x = 5\n"
                         "t_y = 8\n"
                         "z_x = 14\n"
                         "z_m = 24\n"
                         "r_x = 44\n"
                         "with TempVars(starts=['t_', 'z_']) as tv:\n"
                         "    d['inside_t_x_absent'] = 't_x' not in dir()\n"
                         "    d['inside_t_y_absent'] = 't_y' not in dir()\n"
                         "    d['inside_z_x_absent'] = 'z_x' not in dir()\n"
                         "    d['inside_z_m_absent'] = 'z_m' not in dir()\n"
                         "    d['inside_r_x_present'] = 'r_x' in dir()\n"
                         "d['outside_t_x_present'] = 't_x' in dir()\n"
                         "d['outside_t_y_present'] = 't_y' in dir()\n"
                         "d['outside_z_x_present'] = 'z_x' in dir()\n"
                         "d['outside_z_m_present'] = 'z_m' in dir()\n"
                         "d['outside_r_x_present'] = 'r_x' in dir()\n"
                         , 'Good_startsMultiPassed')

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_absent', 'inside_z_m_absent',
                  'inside_r_x_present',
                  'outside_t_x_present', 'outside_t_y_present',
                  'outside_z_x_present', 'outside_z_m_present',
                  'outside_r_x_present']:
            self.locals_subTest(_, d, True)


    def test_Good_endsMultiPassed(self):

        d = self.runCode("from tempvars import TempVars\n"
                         "d = {}\n"
                         "t_x = 5\n"
                         "t_y = 8\n"
                         "z_x = 14\n"
                         "z_m = 24\n"
                         "r_x = 44\n"
                         "with TempVars(ends=['_x', '_y']) as tv:\n"
                         "    d['inside_t_x_absent'] = 't_x' not in dir()\n"
                         "    d['inside_t_y_absent'] = 't_y' not in dir()\n"
                         "    d['inside_z_x_absent'] = 'z_x' not in dir()\n"
                         "    d['inside_z_m_present'] = 'z_m' in dir()\n"
                         "    d['inside_r_x_absent'] = 'r_x' not in dir()\n"
                         "d['outside_t_x_present'] = 't_x' in dir()\n"
                         "d['outside_t_y_present'] = 't_y' in dir()\n"
                         "d['outside_z_x_present'] = 'z_x' in dir()\n"
                         "d['outside_z_m_present'] = 'z_m' in dir()\n"
                         "d['outside_r_x_present'] = 'r_x' in dir()\n"
                         , 'Good_endsMultiPassed')

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_absent', 'inside_z_m_present',
                  'inside_r_x_absent',
                  'outside_t_x_present', 'outside_t_y_present',
                  'outside_z_x_present', 'outside_z_m_present',
                  'outside_r_x_present']:
            self.locals_subTest(_, d, True)


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

