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

    def locals_subTestTrue(self, id, locdict):
        with self.subTest(id):
            self.assertTrue(locdict[id])

    def locals_subTestFalse(self, id, locdict):
        with self.subTest(id):
            self.assertFalse(locdict[id])


    def test_Good_tempvarsPassed(self):

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "with TempVars(tempvars=['x']) as tv:\n"
             "    inside = 'x' in dir()\n"
             "outside = 'x' in dir()\n", locals())

        self.locals_subTestFalse('inside', locals())
        self.locals_subTestTrue('outside', locals())


    def test_Good_tempvarsPassed_NoRestore(self):

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "with TempVars(tempvars=['x'], restore=False) as tv:\n"
             "    inside = 'x' in dir()\n"
             "outside = 'x' in dir()\n", locals())

        self.locals_subTestFalse('inside', locals())
        self.locals_subTestFalse('outside', locals())


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
             "outside_z = 'z_x' in dir()\n", locals())

        self.locals_subTestFalse('inside_x', locals())
        self.locals_subTestFalse('inside_y', locals())
        self.locals_subTestTrue('inside_z', locals())
        self.locals_subTestTrue('outside_x', locals())
        self.locals_subTestTrue('outside_y', locals())
        self.locals_subTestTrue('outside_z', locals())


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
             "outside_z = 'z_x' in dir()\n", locals())

        self.locals_subTestFalse('inside_x', locals())
        self.locals_subTestTrue('inside_y', locals())
        self.locals_subTestFalse('inside_z', locals())
        self.locals_subTestTrue('outside_x', locals())
        self.locals_subTestTrue('outside_y', locals())
        self.locals_subTestTrue('outside_z', locals())


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
             "outside_z = 'z_x' in dir()\n", locals())

        self.locals_subTestFalse('inside_x', locals())
        self.locals_subTestFalse('inside_y', locals())
        self.locals_subTestTrue('inside_z', locals())
        self.locals_subTestFalse('outside_x', locals())
        self.locals_subTestFalse('outside_y', locals())
        self.locals_subTestTrue('outside_z', locals())

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
             "outside_z = 'z_x' in dir()\n", locals())

        self.locals_subTestFalse('inside_x', locals())
        self.locals_subTestTrue('inside_y', locals())
        self.locals_subTestFalse('inside_z', locals())
        self.locals_subTestFalse('outside_x', locals())
        self.locals_subTestTrue('outside_y', locals())
        self.locals_subTestFalse('outside_z', locals())


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

