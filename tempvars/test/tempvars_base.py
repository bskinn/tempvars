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


import unittest as ut


class TestTempVarsExpectGood(ut.TestCase):

    def locals_subTest(self, id, locdict, val):
        with self.subTest(id):
            if val:
                self.assertTrue(locdict[id])
            else:
                self.assertFalse(locdict[id])


    def test_Good_tempvarsPassed(self):

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "with TempVars(tempvars=['x']) as tv:\n"
             "    inside = 'x' in dir()\n"
             "outside = 'x' in dir()\n"
             , locals())

        self.locals_subTest('inside', locals(), False)
        self.locals_subTest('outside', locals(), True)


    def test_Good_tempvarsPassed_NoRestore(self):

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "with TempVars(tempvars=['x'], restore=False) as tv:\n"
             "    inside = 'x' in dir()\n"
             "outside = 'x' in dir()\n"
             , locals())

        self.locals_subTest('inside', locals(), False)
        self.locals_subTest('outside', locals(), False)


    def test_Good_startsPassed(self):

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(starts=['t_']) as tv:\n"
             "    inside_x = 't_x' in dir()\n"
             "    inside_y = 't_y' in dir()\n"
             "    inside_z = 'z_x' in dir()\n"
             "outside_x = 't_x' in dir()\n"
             "outside_y = 't_y' in dir()\n"
             "outside_z = 'z_x' in dir()\n"
             , locals())

        for _ in ['inside_x', 'inside_y']:
            self.locals_subTest(_, locals(), False)

        for _ in ['inside_z', 'outside_x', 'outside_y', 'outside_z']:
            self.locals_subTest(_, locals(), True)


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


# Replicate test_Good_checkStorage_startsNoRestore for 'ends'

# Confirming contents of tv.passed_tempvars, tv.starts, tv.ends and tv.tempvars after entering with starts/ends

# Examining if expected behavior of nested contexts occurs (goal to allow mixed restore=True|False)

# Examining behavior of other scopes enclosed within a TempVars with suite; for example:
#
#  with TempVars(tempvars=['var']):
#      def function(...):
#          thing = var  #Will this throw a NameError?




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

