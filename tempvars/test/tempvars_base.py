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

"""Base module for tempvars tests."""


import unittest as ut


class SuperTestTempVars(object):
    """Superclass for temp vars testing."""

    def setUp(self):
        """Init/clear the working dict."""
        # Init work dict
        self.d = {}

    def locals_subTest(self, id, locdict, val):
        """Wrap and test previously run True/False checks."""
        with self.subTest(id):    # pragma: no cover
            if val:
                self.assertTrue(locdict[id])
            else:
                self.assertFalse(locdict[id])


class TestTempVarsExpectGood(SuperTestTempVars, ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_Good_namesPassed(self):
        """Confirm names passed to `names` get masked."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "with TempVars(names=['x']) as tv:\n"
             "    inside_absent = 'x' not in dir()\n"
             "outside_present = 'x' in dir()\n",
             self.d)

        for _ in ['inside_absent', 'outside_present']:
            self.locals_subTest(_, self.d, True)

    def test_Good_namesPassed_ToggleWorks(self):
        """Confirm in-suite toggle of `.restore` changes behavior."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "with TempVars(names=['x']) as tv:\n"
             "    inside_absent = 'x' not in dir()\n"
             "    tv.restore = False\n"
             "outside_absent = 'x' not in dir()\n",
             self.d)

        for _ in ['inside_absent', 'outside_absent']:
            self.locals_subTest(_, self.d, True)

    def test_Good_namesPassed_NoRestore(self):
        """Confirm vars passed to `names` w/Restore=False aren't restored."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "with TempVars(names=['x'], restore=False) as tv:\n"
             "    inside_absent = 'x' not in dir()\n"
             "outside_absent = 'x' not in dir()\n",
             self.d)

        for _ in ['inside_absent', 'outside_absent']:
            self.locals_subTest(_, self.d, True)

    def test_Good_namesPassedButNotPresent(self):
        """Confirm vars not matching `names` aren't masked.

        Also checks that matching vars created in the context are
        properly scrubbed.
        """
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "with TempVars(names=['y']) as tv:\n"
             "    y = 12\n"
             "    inside_x_present = 'x' in dir()\n"
             "    inside_y_present = 'y' in dir()\n"
             "outside_x_present = 'x' in dir()\n"
             "outside_y_absent = 'y' not in dir()\n"
             "outside_y_retained = tv.retained_tempvars['y'] == 12\n",
             self.d)

        for _ in ['inside_x_present', 'outside_x_present',
                  'inside_y_present', 'outside_y_absent',
                  'outside_y_retained']:
            self.locals_subTest(_, self.d, True)

    def test_Good_startsPassed(self):
        """Confirm vars starting with `starts` are masked."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(starts=['t_']) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_absent = 't_y' not in dir()\n"
             "    inside_z_x_present = 'z_x' in dir()\n"
             "outside_t_x_present = 't_x' in dir()\n"
             "outside_t_y_present = 't_y' in dir()\n"
             "outside_z_x_present = 'z_x' in dir()\n",
             self.d)

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_present', 'outside_t_x_present',
                  'outside_t_y_present', 'outside_z_x_present']:
            self.locals_subTest(_, self.d, True)

    def test_Good_endsPassed(self):
        """Confirm vars ending with `ends` are masked."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(ends=['_x']) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_present = 't_y' in dir()\n"
             "    inside_z_x_absent = 'z_x' not in dir()\n"
             "outside_t_x_present = 't_x' in dir()\n"
             "outside_t_y_present = 't_y' in dir()\n"
             "outside_z_x_present = 'z_x' in dir()\n",
             self.d)

        for _ in ['inside_t_x_absent', 'inside_t_y_present',
                  'inside_z_x_absent', 'outside_t_x_present',
                  'outside_t_y_present', 'outside_z_x_present']:
            self.locals_subTest(_, self.d, True)

    def test_Good_startsPassed_NoRestore(self):
        """Confirm vars matching `starts` aren't restored w/restore=False."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(starts=['t_'], restore=False) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_absent = 't_y' not in dir()\n"
             "    inside_z_x_present = 'z_x' in dir()\n"
             "outside_t_x_absent = 't_x' not in dir()\n"
             "outside_t_y_absent = 't_y' not in dir()\n"
             "outside_z_x_present = 'z_x' in dir()\n",
             self.d)

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_present', 'outside_t_x_absent',
                  'outside_t_y_absent', 'outside_z_x_present']:
            self.locals_subTest(_, self.d, True)

    def test_Good_endsPassed_NoRestore(self):
        """Confirm vars matching `ends` aren't restored w/restore=False."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "with TempVars(ends=['_x'], restore=False) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_present = 't_y' in dir()\n"
             "    inside_z_x_absent = 'z_x' not in dir()\n"
             "outside_t_x_absent = 't_x' not in dir()\n"
             "outside_t_y_present = 't_y' in dir()\n"
             "outside_z_x_absent = 'z_x' not in dir()\n",
             self.d)

        for _ in ['inside_t_x_absent', 'inside_t_y_present',
                  'inside_z_x_absent', 'outside_t_x_absent',
                  'outside_t_y_present', 'outside_z_x_absent']:
            self.locals_subTest(_, self.d, True)

    def test_Good_checkStorage_namesNoRestore(self):
        """Confirm storage dictionaries populate correctly.

        Specifically, checking `.stored_nsvars` and `.retained_tempvars`
        when vars are passed to `names`.
        """
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "before_val = x == 5\n"
             "with TempVars(names=['x'], restore=False) as tv:\n"
             "    inside_initial_absent = 'x' not in dir()\n"
             "    inside_stored_nsvar = tv.stored_nsvars.get('x') == 5\n"
             "    x = 18\n"
             "    inside_final_exist = 'x' in dir()\n"
             "    inside_final_val = x == 18\n"
             "    inside_retained_tempvars_empty =\\\n"
             "                    len(tv.retained_tempvars) == 0\n"
             "outside_stored_nsvar = tv.stored_nsvars.get('x') == 5\n"
             "outside_retained_tempvar = tv.retained_tempvars.get('x') == 18\n"
             "outside_final_absent = 'x' not in dir()\n",
             self.d)

        for _ in ['before_val', 'inside_initial_absent',
                  'inside_stored_nsvar', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_retained_tempvar',
                  'outside_final_absent']:
            self.locals_subTest(_, self.d, True)

    def test_Good_checkStorage_startsNoRestore(self):
        """Confirm storage dictionaries populate correctly.

        Specifically, checking `.stored_nsvars` and `.retained_tempvars`
        when patterns are passed to `starts`.
        """
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "before_var_present = t_x == 5\n"
             "before_newvar_absent = 't_y' not in dir()\n"
             "with TempVars(starts=['t_'], restore=False) as tv:\n"
             "    inside_initial_absent = 't_x' not in dir()\n"
             "    inside_initial_newvar_absent = 't_y' not in dir()\n"
             "    inside_stored_nsvar = tv.stored_nsvars.get('t_x') == 5\n"
             "    inside_newvar_notin_nsvars = 't_y' not in tv.stored_nsvars\n"
             "    t_x = 18\n"
             "    t_y = 43\n"
             "    inside_final_exist = 't_x' in dir()\n"
             "    inside_final_val = t_x == 18\n"
             "    inside_retained_tempvars_empty =\\\n"
             "                        len(tv.retained_tempvars) == 0\n"
             "outside_stored_nsvar = tv.stored_nsvars.get('t_x') == 5\n"
             "outside_newvar_absent = 't_y' not in dir()\n"
             "outside_newvar_notin_nsvars = 't_y' not in tv.stored_nsvars\n"
             "outside_retained_tempvar =\\\n"
             "                tv.retained_tempvars.get('t_x'\n) == 18\n"
             "outside_newvar_in_retained_tempvars =\\\n"
             "                           't_y' in tv.retained_tempvars\n"
             "outside_final_absent = 't_x' not in dir()\n",
             self.d)

        for _ in ['before_var_present', 'before_newvar_absent',
                  'inside_initial_absent',
                  'inside_initial_newvar_absent',
                  'inside_stored_nsvar', 'inside_newvar_notin_nsvars',
                  'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_newvar_absent',
                  'outside_newvar_notin_nsvars',
                  'outside_newvar_in_retained_tempvars',
                  'outside_retained_tempvar', 'outside_final_absent']:
            self.locals_subTest(_, self.d, True)

    def test_Good_checkStorage_endsNoRestore(self):
        """Confirm storage dictionaries populate correctly.

        Specifically, checking `.stored_nsvars` and `.retained_tempvars`
        when patterns are passed to `ends`.
        """
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "before_val = t_x == 5\n"
             "before_newvar_absent = 'r_x' not in dir()\n"
             "with TempVars(ends=['_x'], restore=False) as tv:\n"
             "    inside_initial_absent = 't_x' not in dir()\n"
             "    inside_initial_newvar_absent = 'r_x' not in dir()\n"
             "    inside_stored_nsvar = tv.stored_nsvars.get('t_x') is 5\n"
             "    inside_newvar_not_in_nsvars =\\\n"
             "                         'r_x' not in tv.stored_nsvars\n"
             "    t_x = 18\n"
             "    r_x = 43\n"
             "    inside_final_exist = 't_x' in dir()\n"
             "    inside_final_val = t_x == 18\n"
             "    inside_retained_tempvars_empty =\\\n"
             "                    len(tv.retained_tempvars) == 0\n"
             "outside_stored_nsvar = tv.stored_nsvars.get('t_x') == 5\n"
             "outside_newvar_absent = 'r_x' not in dir()\n"
             "outside_newvar_not_in_nsvars = 'r_x' not in tv.stored_nsvars\n"
             "outside_retained_tempvar =\\\n"
             "                    tv.retained_tempvars.get('t_x') == 18\n"
             "outside_newvar_in_retained_tempvars =\\\n"
             "                    'r_x' in tv.retained_tempvars\n"
             "outside_final_absent = 't_x' not in dir()\n",
             self.d)

        for _ in ['before_val', 'before_newvar_absent',
                  'inside_initial_absent',
                  'inside_initial_newvar_absent',
                  'inside_newvar_not_in_nsvars',
                  'inside_stored_nsvar', 'inside_final_exist',
                  'inside_final_val', 'inside_retained_tempvars_empty',
                  'outside_stored_nsvar', 'outside_newvar_absent',
                  'outside_newvar_not_in_nsvars',
                  'outside_newvar_in_retained_tempvars',
                  'outside_retained_tempvar', 'outside_final_absent']:
            self.locals_subTest(_, self.d, True)

    def test_Good_checkArgs(self):
        """Confirm that no collisions occur when all arguments used.

        Probing to ensure no cross-talk if all of `names`, `starts`, and
        `ends` are passed arguments.
        """
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "r_x = 12\n"
             "f_z = 59\n"
             "d_z = 12\n"
             "g_r = 43\n"
             "with TempVars(names=['g_r'], starts=['t_'],\n"
             "              ends=['_z']) as tv:\n"
             "    g_r_absent = 'g_r' not in dir()\n"
             "    _t_x_absent = 't_x' not in dir()\n"
             "    _t_y_absent = 't_y' not in dir()\n"
             "    r_x_present = 'r_x' in dir()\n"
             "    f_z_absent = 'f_z' not in dir()\n"
             "    d_z_absent = 'd_z' not in dir()\n"
             "    g_r_in_names = 'g_r' in tv.names\n"
             "    _t_x_in_names = 't_x' in tv.names\n"
             "    _t_y_in_names = 't_y' in tv.names\n"
             "    r_x_not_in_names = 'r_x' not in tv.names\n"
             "    f_z_in_names = 'f_z' in tv.names\n"
             "    d_z_in_names = 'd_z' in tv.names\n"
             "    g_r_in_passed_names = 'g_r' in tv.passed_names\n"
             "    _t_x_not_in_passed_names = 't_x' not in tv.passed_names\n"
             "    _t_y_not_in_passed_names = 't_y' not in tv.passed_names\n"
             "    r_x_not_in_passed_names = 'r_x' not in tv.passed_names\n"
             "    f_z_not_in_passed_names = 'f_z' not in tv.passed_names\n"
             "    d_z_not_in_passed_names = 'd_z' not in tv.passed_names\n",
             self.d)

        for _ in ['g_r_absent', '_t_x_absent', '_t_y_absent',
                  'r_x_present', 'f_z_absent', 'd_z_absent',
                  'g_r_in_names', '_t_x_in_names', '_t_y_in_names',
                  'r_x_not_in_names', 'f_z_in_names', 'd_z_in_names',
                  'g_r_in_passed_names', '_t_x_not_in_passed_names',
                  '_t_y_not_in_passed_names', 'r_x_not_in_passed_names',
                  'f_z_not_in_passed_names', 'd_z_not_in_passed_names']:
            self.locals_subTest(_, self.d, True)

    def test_Good_namesMultiPassed(self):
        """Confirm proper function with multiple `names`."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "t_x = 5\n"
             "t_y = 8\n"
             "z_x = 14\n"
             "z_m = 24\n"
             "r_x = 44\n"
             "with TempVars(names=['t_x', 'z_m']) as tv:\n"
             "    inside_t_x_absent = 't_x' not in dir()\n"
             "    inside_t_y_present = 't_y' in dir()\n"
             "    inside_z_x_present = 'z_x' in dir()\n"
             "    inside_z_m_absent = 'z_m' not in dir()\n"
             "    inside_r_x_present = 'r_x' in dir()\n"
             "outside_t_x_present = 't_x' in dir()\n"
             "outside_t_y_present = 't_y' in dir()\n"
             "outside_z_x_present = 'z_x' in dir()\n"
             "outside_z_m_present = 'z_m' in dir()\n"
             "outside_r_x_present = 'r_x' in dir()\n",
             self.d)

        for _ in ['inside_t_x_absent', 'inside_t_y_present',
                  'inside_z_x_present', 'inside_z_m_absent',
                  'inside_r_x_present',
                  'outside_t_x_present', 'outside_t_y_present',
                  'outside_z_x_present', 'outside_z_m_present',
                  'outside_r_x_present']:
            self.locals_subTest(_, self.d, True)

    def test_Good_startsMultiPassed(self):
        """Confirm ok w/multiple `starts` patterns."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

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
             "outside_r_x_present = 'r_x' in dir()\n",
             self.d)

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_absent', 'inside_z_m_absent',
                  'inside_r_x_present',
                  'outside_t_x_present', 'outside_t_y_present',
                  'outside_z_x_present', 'outside_z_m_present',
                  'outside_r_x_present']:
            self.locals_subTest(_, self.d, True)

    def test_Good_endsMultiPassed(self):
        """Confirm ok w/multiple `ends` patterns."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

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
             "outside_r_x_present = 'r_x' in dir()\n",
             self.d)

        for _ in ['inside_t_x_absent', 'inside_t_y_absent',
                  'inside_z_x_absent', 'inside_z_m_present',
                  'inside_r_x_absent',
                  'outside_t_x_present', 'outside_t_y_present',
                  'outside_z_x_present', 'outside_z_m_present',
                  'outside_r_x_present']:
            self.locals_subTest(_, self.d, True)

    def test_Good_nestedVarsRestoreOuterOnly(self):
        """Confirm outer-restore nested contexts restore correctly."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "y = 8\n"
             "z = 14\n"
             "with TempVars(names=['x'], restore=True) as tv_outer:\n"
             "    in_1_before_2_x_absent = 'x' not in dir()\n"
             "    in_1_before_2_y_present = 'y' in dir()\n"
             "    in_1_before_2_z_present = 'z' in dir()\n"
             "    with TempVars(names=['y'], restore=False) as tv_inner:\n"
             "        in_12_x_absent = 'x' not in dir()\n"
             "        in_12_y_absent = 'y' not in dir()\n"
             "        in_12_z_present = 'z' in dir()\n"
             "    in_1_after_2_x_absent = 'x' not in dir()\n"
             "    in_1_after_2_y_absent = 'y' not in dir()\n"
             "    in_1_after_2_z_present = 'z' in dir()\n"
             "after_12_x_present = 'x' in dir()\n"
             "after_12_y_absent= 'y' not in dir()\n"
             "after_12_z_present = 'z' in dir()\n",
             self.d)

        for _ in ['in_1_before_2_x_absent', 'in_1_before_2_y_present',
                  'in_1_before_2_z_present',
                  'in_12_x_absent', 'in_12_y_absent', 'in_12_z_present',
                  'in_1_after_2_x_absent', 'in_1_after_2_y_absent',
                  'in_1_after_2_z_present',
                  'after_12_x_present', 'after_12_y_absent',
                  'after_12_z_present']:
            self.locals_subTest(_, self.d, True)

    def test_Good_nestedVarsRestoreInnerOnly(self):
        """Confirm inner-restore nested contexts restore correctly."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "x = 5\n"
             "y = 8\n"
             "z = 14\n"
             "with TempVars(names=['x'], restore=False) as tv_outer:\n"
             "    in_1_before_2_x_absent = 'x' not in dir()\n"
             "    in_1_before_2_y_present = 'y' in dir()\n"
             "    in_1_before_2_z_present = 'z' in dir()\n"
             "    with TempVars(names=['y'], restore=True) as tv_inner:\n"
             "        in_12_x_absent = 'x' not in dir()\n"
             "        in_12_y_absent = 'y' not in dir()\n"
             "        in_12_z_present = 'z' in dir()\n"
             "    in_1_after_2_x_absent = 'x' not in dir()\n"
             "    in_1_after_2_y_present = 'y' in dir()\n"
             "    in_1_after_2_z_present = 'z' in dir()\n"
             "after_12_x_absent = 'x' not in dir()\n"
             "after_12_y_present= 'y' in dir()\n"
             "after_12_z_present = 'z' in dir()\n",
             self.d)

        for _ in ['in_1_before_2_x_absent', 'in_1_before_2_y_present',
                  'in_1_before_2_z_present',
                  'in_12_x_absent', 'in_12_y_absent', 'in_12_z_present',
                  'in_1_after_2_x_absent', 'in_1_after_2_y_present',
                  'in_1_after_2_z_present',
                  'after_12_x_absent', 'after_12_y_present',
                  'after_12_z_present']:
            self.locals_subTest(_, self.d, True)

    def test_Good_NonMutableNamesStartsEndsArgs(self):
        """Confirm external lists passed as args aren't being modified."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec("from tempvars import TempVars\n"
             "n = ['xyz', 'fnq']\n"
             "s = ['abc_', 'qrs_']\n"
             "e = ['_mnp', '_fzr']\n"
             "before_n_len = len(n) == 2\n"
             "before_s_len = len(s) == 2\n"
             "before_e_len = len(e) == 2\n"
             "t_fzr = 6\n"
             "xyz = 12\n"
             "abc_x = 35\n"
             "with TempVars(names=n, starts=s, ends=e) as tv:\n"
             "    inside_n_len = len(n) == 2\n"
             "    inside_s_len = len(s) == 2\n"
             "    inside_e_len = len(e) == 2\n"
             "outside_n_len = len(n) == 2\n"
             "outside_s_len = len(s) == 2\n"
             "outside_e_len = len(e) == 2\n",
             self.d)

        for _ in ['before_n_len', 'inside_n_len', 'outside_n_len',
                  'before_s_len', 'inside_s_len', 'outside_s_len',
                  'before_e_len', 'inside_e_len', 'outside_e_len']:
            self.locals_subTest(_, self.d, True)

    def runtest_Good_NoNamesDupes(self, code):
        """Perform subTest-ed name duplication check on indicated code."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(code, self.d)

        for _ in ['names_len_one', 'nsvars_len_one', 'ret_tempvars_len_one']:
            self.locals_subTest(_, self.d, True)

    def test_Good_NoNamesDupes_NamesDuplicatesPassed(self):
        """Confirm no duplicate vars stored if `names` holds dupes."""
        self.runtest_Good_NoNamesDupes(
            "from tempvars import TempVars\n"
            "t_y = 15\n"
            "with TempVars(names=['t_y', 't_y']) as tv:\n"
            "    names_len_one = len(tv.names) == 1\n"
            "    nsvars_len_one = len(tv.stored_nsvars) == 1\n"
            "    t_y = 35\n"
            "ret_tempvars_len_one = len(tv.retained_tempvars) == 1\n"
            )

    def test_Good_NoNamesDupes_StartsMultiMatch(self):
        """Confirm no dupe var names stored if `starts` matches repeatedly."""
        self.runtest_Good_NoNamesDupes(
            "from tempvars import TempVars\n"
            "t_y_f = 15\n"
            "with TempVars(starts=['t_', 't_y']) as tv:\n"
            "    names_len_one = len(tv.names) == 1\n"
            "    nsvars_len_one = len(tv.stored_nsvars) == 1\n"
            "    t_y_f = 35\n"
            "ret_tempvars_len_one = len(tv.retained_tempvars) == 1\n"
            )

    def test_Good_NoNamesDupes_EndsMultiMatch(self):
        """Confirm no dupe var names stored if `ends` matches repeatedly."""
        self.runtest_Good_NoNamesDupes(
            "from tempvars import TempVars\n"
            "t_y_f = 15\n"
            "with TempVars(ends=['_f', 'y_f']) as tv:\n"
            "    names_len_one = len(tv.names) == 1\n"
            "    nsvars_len_one = len(tv.stored_nsvars) == 1\n"
            "    t_y_f = 35\n"
            "ret_tempvars_len_one = len(tv.retained_tempvars) == 1\n"
            )

    def test_Good_NoNamesDupes_StartsEndsBothMatch(self):
        """Confirm no dupe var names stored if `starts` & `ends` both match."""
        self.runtest_Good_NoNamesDupes(
            "from tempvars import TempVars\n"
            "t_y = 15\n"
            "with TempVars(starts=['t_'], ends=['_y']) as tv:\n"
            "    names_len_one = len(tv.names) == 1\n"
            "    nsvars_len_one = len(tv.stored_nsvars) == 1\n"
            "    t_y = 35\n"
            "ret_tempvars_len_one = len(tv.retained_tempvars) == 1\n"
            )

    def test_Good_NoNamesDupes_NamesStartsBothMatch(self):
        """Confirm no dupe varnames stored if `starts` & `names` both match."""
        self.runtest_Good_NoNamesDupes(
            "from tempvars import TempVars\n"
            "t_y = 15\n"
            "with TempVars(names=['t_y'], starts=['t_']) as tv:\n"
            "    names_len_one = len(tv.names) == 1\n"
            "    nsvars_len_one = len(tv.stored_nsvars) == 1\n"
            "    t_y = 35\n"
            "ret_tempvars_len_one = len(tv.retained_tempvars) == 1\n"
            )

    def test_Good_NoNamesDupes_NamesEndsBothMatch(self):
        """Confirm no dupe var names stored if `names` & `ends` both match."""
        self.runtest_Good_NoNamesDupes(
            "from tempvars import TempVars\n"
            "t_y = 15\n"
            "with TempVars(names=['t_y'], ends=['_y']) as tv:\n"
            "    names_len_one = len(tv.names) == 1\n"
            "    nsvars_len_one = len(tv.stored_nsvars) == 1\n"
            "    t_y = 35\n"
            "ret_tempvars_len_one = len(tv.retained_tempvars) == 1\n"
            )

    def test_Good_NoNamesDupes_NamesStartsEndsAllMatch(self):
        """Confirm no dupe var names if `names`/`starts`/`ends` all match."""
        self.runtest_Good_NoNamesDupes(
            "from tempvars import TempVars\n"
            "t_y_f = 15\n"
            "with TempVars(names=['t_y_f'], starts=['t_'],\n"
            "              ends=['_f']) as tv:\n"
            "    names_len_one = len(tv.names) == 1\n"
            "    nsvars_len_one = len(tv.stored_nsvars) == 1\n"
            "    t_y_f = 35\n"
            "ret_tempvars_len_one = len(tv.retained_tempvars) == 1\n"
            )


class TestTempVarsExpectFail(SuperTestTempVars, ut.TestCase):
    """Testing that code raises expected errors when invoked improperly."""

    list_args = ['names', 'starts', 'ends']

    def test_Fail_ArgIsNotListOrNone(self):
        """Confirm `TypeError` if non-list passed to var arg."""
        code = 'from tempvars import TempVars; TempVars({0}=1)'

        for arg in self.list_args:
            with self.subTest(arg):
                self.assertRaises(TypeError, exec, code.format(arg), {})

    def test_Fail_ArgListHasNonString(self):
        """Confirm `TypeError` if non-string passed in a var arg list."""
        code = 'from tempvars import TempVars; TempVars({0}=["abcde", 1])'

        for arg in self.list_args:
            with self.subTest(arg):
                self.assertRaises(TypeError, exec, code.format(arg), {})

    def test_Fail_UnderArgs(self):
        """Confirm `ValueError` on (d)under `starts`/`ends` patterns."""
        code = ('from tempvars import TempVars; '
                'TempVars({0}=["abc", "{1}", "pqr"])')

        for arg in ['starts', 'ends']:
            for val in ['_', '__']:
                with self.subTest('{0}-{1}'.format(arg, val)):
                    self.assertRaises(ValueError, exec,
                                      code.format(arg, val), {})

        with self.subTest('starts-any-dunder-start'):
            self.assertRaises(ValueError, exec,
                              code.format('starts', '__d'), {})

        with self.subTest('ends-any-dunder-end'):
            self.assertRaises(ValueError, exec,
                              code.format('ends', 's__'), {})

    def test_Fail_NonBooleanRestore(self):
        """Confirm `TypeError` if non-boolean `restore` is passed."""
        code = ('from tempvars import TempVars; '
                'TempVars(names=["abc"], restore=1)')

        self.assertRaises(TypeError, exec, code, {})

    def test_Fail_NonGlobalScope(self):
        """Confirm that a `RuntimeError` is raised in a non-global scope."""
        from tempvars import TempVars

        with self.assertRaises(RuntimeError):
            with TempVars(names=['abcd']):
                pass    # pragma: no cover


def suite_expect_good():
    """Create and return the test suite for expect-good cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestTempVarsExpectGood)])

    return s


def suite_expect_fail():
    """Create and return the test suite for expect-fail cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestTempVarsExpectFail)])

    return s


if __name__ == '__main__':  # pragma: no cover
    print("Module not executable.")
