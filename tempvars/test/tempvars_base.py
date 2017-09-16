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


class SuperTestTempVars(object):
    """Superclass for temp vars testing."""

    def locals_subTest(self, id, locdict, val):
        with self.subTest(id):
            if val:
                self.assertTrue(locdict[id])
            else:
                self.assertFalse(locdict[id])


class TestTempVarsExpectGood(SuperTestTempVars, ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_Good_tempvarsPassed(self):

        exec("from tempvars import TempVars\n"
             "d = {}\n"
             "x = 5\n"
             "with TempVars(tempvars=['x']) as tv:\n"
             "    inside_absent = 'x' not in dir()\n"
             "outside_present = 'x' in dir()\n"
             , locals())

        for _ in ['inside_absent', 'outside_present']:
            self.locals_subTest(_, locals(), True)


    def test_Good_tempvarsPassed_NoRestore(self):

        exec("from tempvars import TempVars\n"
             "d = {}\n"
             "x = 5\n"
             "with TempVars(tempvars=['x'], restore=False) as tv:\n"
             "    inside_absent = 'x' not in dir()\n"
             "outside_absent = 'x' not in dir()\n"
             , locals())

        for _ in ['inside_absent', 'outside_absent']:
            self.locals_subTest(_, locals(), True)


    def test_Good_tempvarsPassedButNotPresent(self):

        exec("from tempvars import TempVars\n"
             "d = {}\n"
             "x = 5\n"
             "with TempVars(tempvars=['y']) as tv:\n"
             "    y = 12\n"
             "    inside_x_present = 'x' in dir()\n"
             "    inside_y_present = 'y' in dir()\n"
             "outside_x_present = 'x' in dir()\n"
             "outside_y_absent = 'y' not in dir()\n"
             "outside_y_retained = tv.retained_tempvars['y'] == 12\n"
             , locals())

        for _ in ['inside_x_present', 'outside_x_present',
                  'inside_y_present', 'outside_y_absent',
                  'outside_y_retained']:
            self.locals_subTest(_, locals(), True)


    def test_Good_startsPassed(self):

        exec("from tempvars import TempVars\n"
             "d = {}\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(starts=['t_']) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_absent = 't_y' not in dir()\n"
             "    inside_z_x_present = 'z_x' in dir()\n"
             "outside_t_x_present = 't_x' in dir()\n"
             "outside_t_y_present = 't_y' in dir()\n"
             "outside_z_x_present = 'z_x' in dir()\n"
             , locals())

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_present', 'outside_t_x_present',
                  'outside_t_y_present', 'outside_z_x_present']:
            self.locals_subTest(_, locals(), True)


    def test_Good_endsPassed(self):

        exec("from tempvars import TempVars\n"
             "d = {}\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(ends=['_x']) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_present = 't_y' in dir()\n"
             "    inside_z_x_absent = 'z_x' not in dir()\n"
             "outside_t_x_present = 't_x' in dir()\n"
             "outside_t_y_present = 't_y' in dir()\n"
             "outside_z_x_present = 'z_x' in dir()\n"
             , locals())

        for _ in ['inside_t_x_absent', 'inside_t_y_present',
                  'inside_z_x_absent', 'outside_t_x_present',
                  'outside_t_y_present', 'outside_z_x_present']:
            self.locals_subTest(_, locals(), True)


    def test_Good_startsPassed_NoRestore(self):

        exec("from tempvars import TempVars\n"
             "d = {}\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(starts=['t_'], restore=False) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_absent = 't_y' not in dir()\n"
             "    inside_z_x_present = 'z_x' in dir()\n"
             "outside_t_x_absent = 't_x' not in dir()\n"
             "outside_t_y_absent = 't_y' not in dir()\n"
             "outside_z_x_present = 'z_x' in dir()\n"
             , locals())

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_present', 'outside_t_x_absent',
                  'outside_t_y_absent', 'outside_z_x_present']:
            self.locals_subTest(_, locals(), True)


    def test_Good_endsPassed_NoRestore(self):

        exec("from tempvars import TempVars\n"
             "d = {}\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(ends=['_x'], restore=False) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_present = 't_y' in dir()\n"
             "    inside_z_x_absent = 'z_x' not in dir()\n"
             "outside_t_x_absent = 't_x' not in dir()\n"
             "outside_t_y_present = 't_y' in dir()\n"
             "outside_z_x_absent = 'z_x' not in dir()\n"
             , locals())

        for _ in ['inside_t_x_absent', 'inside_t_y_present',
                  'inside_z_x_absent', 'outside_t_x_absent',
                  'outside_t_y_present', 'outside_z_x_absent']:
            self.locals_subTest(_, locals(), True)


    def test_Good_checkStorage_tempvarsNoRestore(self):

        exec("from tempvars import TempVars\n"
             "d = {}\n"
             "x = 5\n"
             "before_val = x == 5\n"
             "with TempVars(tempvars=['x'], restore=False) as tv:\n"
             "    inside_initial_absent = 'x' not in dir()\n"
             "    inside_stored_nsvar = tv.stored_nsvars.get('x') == 5\n"
             "    x = 18\n"
             "    inside_final_exist = 'x' in dir()\n"
             "    inside_final_val = x == 18\n"
             "    inside_retained_tempvars_empty = len(tv.retained_tempvars) == 0\n"
             "outside_stored_nsvar = tv.stored_nsvars.get('x') == 5\n"
             "outside_retained_tempvar = tv.retained_tempvars.get('x') == 18\n"
             "outside_final_absent = 'x' not in dir()\n"
             , locals())

        for _ in ['before_val', 'inside_initial_absent',
                  'inside_stored_nsvar', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_retained_tempvar',
                  'outside_final_absent']:
            self.locals_subTest(_, locals(), True)


    def test_Good_checkStorage_startsNoRestore(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "before_var_present = t_x == 5\n"
             "before_newvar_absent = 't_y' not in dir()\n"
             "with TempVars(starts=['t_'], restore=False) as tv:\n"
             "    inside_initial_absent = 't_x' not in dir()\n"
             "    inside_initial_newvar_absent = 't_y' not in dir()\n"
             "    inside_stored_nsvar = tv.stored_nsvars.get('t_x') == 5\n"
             "    inside_newvar_not_in_nsvars = 't_y' not in tv.stored_nsvars\n"
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
             "outside_final_absent = 't_x' not in dir()\n"
             , locals())

        for _ in ['before_var_present', 'before_newvar_absent', 'inside_initial_absent',
                  'inside_initial_newvar_absent',
                  'inside_stored_nsvar', 'inside_newvar_not_in_nsvars', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_newvar_absent',
                  'outside_newvar_not_in_nsvars', 'outside_newvar_in_retained_tempvars',
                  'outside_retained_tempvar', 'outside_final_absent']:
            self.locals_subTest(_, locals(), True)


    def test_Good_checkStorage_endsNoRestore(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "before_val = t_x == 5\n"
             "before_newvar_absent = 'r_x' not in dir()\n"
             "with TempVars(ends=['_x'], restore=False) as tv:\n"
             "    inside_initial_absent = 't_x' not in dir()\n"
             "    inside_initial_newvar_absent = 'r_x' not in dir()\n"
             "    inside_stored_nsvar = tv.stored_nsvars.get('t_x') is 5\n"
             "    inside_newvar_not_in_nsvars = 'r_x' not in tv.stored_nsvars\n"
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
             "outside_final_absent = 't_x' not in dir()\n"
             , locals())

        for _ in ['before_val', 'before_newvar_absent', 'inside_initial_absent',
                  'inside_initial_newvar_absent', 'inside_newvar_not_in_nsvars',
                  'inside_stored_nsvar', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_newvar_absent',
                  'outside_newvar_not_in_nsvars', 'outside_newvar_in_retained_tempvars',
                  'outside_retained_tempvar', 'outside_final_absent']:
            self.locals_subTest(_, locals(), True)


    def test_Good_checkArgs(self):

        exec("from tempvars import TempVars\n"
             "d = {}\n"
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
             "d = {}\n"
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
             "d = {}\n"
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


def suite_expect_good():
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestTempVarsExpectGood)])

    return s


def suite_expect_fail():
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([])

    return s



if __name__ == '__main__':  # pragma: no cover
    print("Module not executable.")

