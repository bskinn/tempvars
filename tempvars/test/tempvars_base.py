r"""Core tests module for ``tempvars``.

Context manager for handling temporary variables in
Jupyter Notebook, IPython, etc.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    11 Sep 2017

**Copyright**
    \(c) Brian Skinn 2017-2018

**Source Repository**
    http://www.github.com/bskinn/tempvars

**Documentation**
    http://tempvars.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

"""

import doctest as dt
import unittest as ut


class SuperTestTempVars(object):
    """Superclass for temp vars testing."""

    def setUp(self):
        """Init/clear the working dict."""
        # Init work dict
        self.d = {}

    def locals_subTest(self, testid, locdict, val):
        """Wrap and test previously run True/False checks."""
        # Strip leading test flag if present when constructing
        # subtest name
        testname = testid[3:] if testid.startswith("_t_") else testid

        with self.subTest(testname):  # pragma: no cover
            if val:
                self.assertTrue(locdict[testid])
            else:
                self.assertFalse(locdict[testid])


class TestTempVarsExpectGood(SuperTestTempVars, ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_Good_namesPassed(self):
        """Confirm names passed to `names` get masked."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "x = 5\n"
            "with TempVars(names=['x']) as tv:\n"
            "    _t_inside_absent = 'x' not in dir()\n"
            "_t_outside_present = 'x' in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_namesPassed_ToggleWorks(self):
        """Confirm in-suite toggle of `.restore` changes behavior."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "x = 5\n"
            "with TempVars(names=['x']) as tv:\n"
            "    _t_inside_absent = 'x' not in dir()\n"
            "    tv.restore = False\n"
            "_t_outside_absent = 'x' not in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_namesPassed_NoRestore(self):
        """Confirm vars passed to `names` w/Restore=False aren't restored."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "x = 5\n"
            "with TempVars(names=['x'], restore=False) as tv:\n"
            "    _t_inside_absent = 'x' not in dir()\n"
            "_t_outside_absent = 'x' not in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_namesPassedButNotPresent(self):
        """Confirm vars not matching `names` aren't masked.

        Also checks that matching vars created in the context are
        properly scrubbed.
        """
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "x = 5\n"
            "with TempVars(names=['y']) as tv:\n"
            "    y = 12\n"
            "    _t_inside_x_present = 'x' in dir()\n"
            "    _t_inside_y_present = 'y' in dir()\n"
            "_t_outside_x_present = 'x' in dir()\n"
            "_t_outside_y_absent = 'y' not in dir()\n"
            "_t_outside_y_retained = tv.retained_tempvars['y'] == 12\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_startsPassed(self):
        """Confirm vars starting with `starts` are masked."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "t_x = 5\n"
            "t_y = 8\n"
            "z_x = 14\n"
            "with TempVars(starts=['t_']) as tv:\n"
            "    _t_inside_t_x_absent = 't_x' not in dir()\n"
            "    _t_inside_t_y_absent = 't_y' not in dir()\n"
            "    _t_inside_z_x_present = 'z_x' in dir()\n"
            "_t_outside_t_x_present = 't_x' in dir()\n"
            "_t_outside_t_y_present = 't_y' in dir()\n"
            "_t_outside_z_x_present = 'z_x' in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_endsPassed(self):
        """Confirm vars ending with `ends` are masked."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "t_x = 5\n"
            "t_y = 8\n"
            "z_x = 14\n"
            "with TempVars(ends=['_x']) as tv:\n"
            "    _t_inside_t_x_absent = 't_x' not in dir()\n"
            "    _t_inside_t_y_present = 't_y' in dir()\n"
            "    _t_inside_z_x_absent = 'z_x' not in dir()\n"
            "_t_outside_t_x_present = 't_x' in dir()\n"
            "_t_outside_t_y_present = 't_y' in dir()\n"
            "_t_outside_z_x_present = 'z_x' in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_startsPassed_NoRestore(self):
        """Confirm vars matching `starts` aren't restored w/restore=False."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "t_x = 5\n"
            "t_y = 8\n"
            "z_x = 14\n"
            "with TempVars(starts=['t_'], restore=False) as tv:\n"
            "    _t_inside_t_x_absent = 't_x' not in dir()\n"
            "    _t_inside_t_y_absent = 't_y' not in dir()\n"
            "    _t_inside_z_x_present = 'z_x' in dir()\n"
            "_t_outside_t_x_absent = 't_x' not in dir()\n"
            "_t_outside_t_y_absent = 't_y' not in dir()\n"
            "_t_outside_z_x_present = 'z_x' in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_endsPassed_NoRestore(self):
        """Confirm vars matching `ends` aren't restored w/restore=False."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "t_x = 5\n"
            "t_y = 8\n"
            "z_x = 14\n"
            "with TempVars(ends=['_x'], restore=False) as tv:\n"
            "    _t_inside_t_x_absent = 't_x' not in dir()\n"
            "    _t_inside_t_y_present = 't_y' in dir()\n"
            "    _t_inside_z_x_absent = 'z_x' not in dir()\n"
            "_t_outside_t_x_absent = 't_x' not in dir()\n"
            "_t_outside_t_y_present = 't_y' in dir()\n"
            "_t_outside_z_x_absent = 'z_x' not in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_checkStorage_namesNoRestore(self):
        """Confirm storage dictionaries populate correctly.

        Specifically, checking `.stored_nsvars` and `.retained_tempvars`
        when vars are passed to `names`.
        """
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "x = 5\n"
            "before_val = x == 5\n"
            "with TempVars(names=['x'], restore=False) as tv:\n"
            "    _t_inside_initial_absent = 'x' not in dir()\n"
            "    _t_inside_stored_nsvar = tv.stored_nsvars.get('x') == 5\n"
            "    x = 18\n"
            "    _t_inside_final_exist = 'x' in dir()\n"
            "    _t_inside_final_val = x == 18\n"
            "    _t_inside_retained_tempvars_empty =\\\n"
            "                    len(tv.retained_tempvars) == 0\n"
            "_t_outside_stored_nsvar = tv.stored_nsvars.get('x') == 5\n"
            "_t_outside_retained_tempvar =\\\n"
            "                    tv.retained_tempvars.get('x') == 18\n"
            "_t_outside_final_absent = 'x' not in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_checkStorage_startsNoRestore(self):
        """Confirm storage dictionaries populate correctly.

        Specifically, checking `.stored_nsvars` and `.retained_tempvars`
        when patterns are passed to `starts`.
        """
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "t_x = 5\n"
            "_t_before_var_present = t_x == 5\n"
            "_t_before_newvar_absent = 't_y' not in dir()\n"
            "with TempVars(starts=['t_'], restore=False) as tv:\n"
            "    _t_inside_initial_absent = 't_x' not in dir()\n"
            "    _t_inside_initial_newvar_absent = 't_y' not in dir()\n"
            "    _t_inside_stored_nsvar = tv.stored_nsvars.get('t_x') == 5\n"
            "    _t_inside_newvar_notin_nsvars =\\\n"
            "                        't_y' not in tv.stored_nsvars\n"
            "    t_x = 18\n"
            "    t_y = 43\n"
            "    _t_inside_final_exist = 't_x' in dir()\n"
            "    _t_inside_final_val = t_x == 18\n"
            "    _t_inside_retained_tempvars_empty =\\\n"
            "                        len(tv.retained_tempvars) == 0\n"
            "_t_outside_stored_nsvar = tv.stored_nsvars.get('t_x') == 5\n"
            "_t_outside_newvar_absent = 't_y' not in dir()\n"
            "_t_outside_newvar_notin_nsvars = 't_y' not in tv.stored_nsvars\n"
            "_t_outside_retained_tempvar =\\\n"
            "                tv.retained_tempvars.get('t_x'\n) == 18\n"
            "_t_outside_newvar_in_retained_tempvars =\\\n"
            "                           't_y' in tv.retained_tempvars\n"
            "_t_outside_final_absent = 't_x' not in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_checkStorage_endsNoRestore(self):
        """Confirm storage dictionaries populate correctly.

        Specifically, checking `.stored_nsvars` and `.retained_tempvars`
        when patterns are passed to `ends`.
        """
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "t_x = 5\n"
            "_t_before_val = t_x == 5\n"
            "_t_before_newvar_absent = 'r_x' not in dir()\n"
            "with TempVars(ends=['_x'], restore=False) as tv:\n"
            "    _t_inside_initial_absent = 't_x' not in dir()\n"
            "    _t_inside_initial_newvar_absent = 'r_x' not in dir()\n"
            "    _t_inside_stored_nsvar = tv.stored_nsvars.get('t_x') is 5\n"
            "    _t_inside_newvar_not_in_nsvars =\\\n"
            "                         'r_x' not in tv.stored_nsvars\n"
            "    t_x = 18\n"
            "    r_x = 43\n"
            "    _t_inside_final_exist = 't_x' in dir()\n"
            "    _t_inside_final_val = t_x == 18\n"
            "    _t_inside_retained_tempvars_empty =\\\n"
            "                    len(tv.retained_tempvars) == 0\n"
            "_t_outside_stored_nsvar = tv.stored_nsvars.get('t_x') == 5\n"
            "_t_outside_newvar_absent = 'r_x' not in dir()\n"
            "_t_outside_newvar_not_in_nsvars =\\\n"
            "                        'r_x' not in tv.stored_nsvars\n"
            "_t_outside_retained_tempvar =\\\n"
            "                    tv.retained_tempvars.get('t_x') == 18\n"
            "_t_outside_newvar_in_retained_tempvars =\\\n"
            "                    'r_x' in tv.retained_tempvars\n"
            "_t_outside_final_absent = 't_x' not in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_checkArgs(self):
        """Confirm that no collisions occur when all arguments used.

        Probing to ensure no cross-talk if all of `names`, `starts`, and
        `ends` are passed arguments.
        """
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "t_x = 5\n"
            "t_y = 8\n"
            "r_x = 12\n"
            "f_z = 59\n"
            "d_z = 12\n"
            "g_r = 43\n"
            "with TempVars(names=['g_r', 'm_m'], starts=['t_'],\n"
            "              ends=['_z']) as tv:\n"
            "    nsvk = tv.stored_nsvars.keys()\n"
            "    _t_g_r_absent = 'g_r' not in dir()\n"
            "    _t_t_x_absent = 't_x' not in dir()\n"
            "    _t_t_y_absent = 't_y' not in dir()\n"
            "    _t_r_x_present = 'r_x' in dir()\n"
            "    _t_f_z_absent = 'f_z' not in dir()\n"
            "    _t_d_z_absent = 'd_z' not in dir()\n"
            "    _t_g_r_in_stored_names = 'g_r' in nsvk\n"
            "    _t_t_x_in_stored_names = 't_x' in nsvk\n"
            "    _t_t_y_in_stored_names = 't_y' in nsvk\n"
            "    _t_r_x_not_in_stored_names = 'r_x' not in nsvk\n"
            "    _t_m_m_not_in_stored_names = 'm_m' not in nsvk\n"
            "    _t_f_z_in_stored_names = 'f_z' in nsvk\n"
            "    _t_d_z_in_stored_names = 'd_z' in nsvk\n"
            "    _t_g_r_in_passed_names = 'g_r' in tv.names\n"
            "    _t_m_m_in_passed_names = 'm_m' in tv.names\n"
            "    _t_t_x_not_in_passed_names = 't_x' not in tv.names\n"
            "    _t_t_y_not_in_passed_names = 't_y' not in tv.names\n"
            "    _t_r_x_not_in_passed_names = 'r_x' not in tv.names\n"
            "    _t_f_z_not_in_passed_names = 'f_z' not in tv.names\n"
            "    _t_d_z_not_in_passed_names = 'd_z' not in tv.names\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_namesMultiPassed(self):
        """Confirm proper function with multiple `names`."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "t_x = 5\n"
            "t_y = 8\n"
            "z_x = 14\n"
            "z_m = 24\n"
            "r_x = 44\n"
            "with TempVars(names=['t_x', 'z_m']) as tv:\n"
            "    _t_inside_t_x_absent = 't_x' not in dir()\n"
            "    _t_inside_t_y_present = 't_y' in dir()\n"
            "    _t_inside_z_x_present = 'z_x' in dir()\n"
            "    _t_inside_z_m_absent = 'z_m' not in dir()\n"
            "    _t_inside_r_x_present = 'r_x' in dir()\n"
            "_t_outside_t_x_present = 't_x' in dir()\n"
            "_t_outside_t_y_present = 't_y' in dir()\n"
            "_t_outside_z_x_present = 'z_x' in dir()\n"
            "_t_outside_z_m_present = 'z_m' in dir()\n"
            "_t_outside_r_x_present = 'r_x' in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_startsMultiPassed(self):
        """Confirm ok w/multiple `starts` patterns."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "t_x = 5\n"
            "t_y = 8\n"
            "z_x = 14\n"
            "z_m = 24\n"
            "r_x = 44\n"
            "with TempVars(starts=['t_', 'z_']) as tv:\n"
            "    _t_inside_t_x_absent = 't_x' not in dir()\n"
            "    _t_inside_t_y_absent = 't_y' not in dir()\n"
            "    _t_inside_z_x_absent = 'z_x' not in dir()\n"
            "    _t_inside_z_m_absent = 'z_m' not in dir()\n"
            "    _t_inside_r_x_present = 'r_x' in dir()\n"
            "_t_outside_t_x_present = 't_x' in dir()\n"
            "_t_outside_t_y_present = 't_y' in dir()\n"
            "_t_outside_z_x_present = 'z_x' in dir()\n"
            "_t_outside_z_m_present = 'z_m' in dir()\n"
            "_t_outside_r_x_present = 'r_x' in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_endsMultiPassed(self):
        """Confirm ok w/multiple `ends` patterns."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "t_x = 5\n"
            "t_y = 8\n"
            "z_x = 14\n"
            "z_m = 24\n"
            "r_x = 44\n"
            "with TempVars(ends=['_x', '_y']) as tv:\n"
            "    _t_inside_t_x_absent = 't_x' not in dir()\n"
            "    _t_inside_t_y_absent = 't_y' not in dir()\n"
            "    _t_inside_z_x_absent = 'z_x' not in dir()\n"
            "    _t_inside_z_m_present = 'z_m' in dir()\n"
            "    _t_inside_r_x_absent = 'r_x' not in dir()\n"
            "_t_outside_t_x_present = 't_x' in dir()\n"
            "_t_outside_t_y_present = 't_y' in dir()\n"
            "_t_outside_z_x_present = 'z_x' in dir()\n"
            "_t_outside_z_m_present = 'z_m' in dir()\n"
            "_t_outside_r_x_present = 'r_x' in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_nestedVarsRestoreOuterOnly(self):
        """Confirm outer-restore nested contexts restore correctly."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "x = 5\n"
            "y = 8\n"
            "z = 14\n"
            "with TempVars(names=['x'], restore=True) as tv_outer:\n"
            "    _t_in_1_before_2_x_absent = 'x' not in dir()\n"
            "    _t_in_1_before_2_y_present = 'y' in dir()\n"
            "    _t_in_1_before_2_z_present = 'z' in dir()\n"
            "    with TempVars(names=['y'], restore=False) as tv_inner:\n"
            "        _t_in_12_x_absent = 'x' not in dir()\n"
            "        _t_in_12_y_absent = 'y' not in dir()\n"
            "        _t_in_12_z_present = 'z' in dir()\n"
            "    _t_in_1_after_2_x_absent = 'x' not in dir()\n"
            "    _t_in_1_after_2_y_absent = 'y' not in dir()\n"
            "    _t_in_1_after_2_z_present = 'z' in dir()\n"
            "_t_after_12_x_present = 'x' in dir()\n"
            "_t_after_12_y_absent= 'y' not in dir()\n"
            "_t_after_12_z_present = 'z' in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_nestedVarsRestoreInnerOnly(self):
        """Confirm inner-restore nested contexts restore correctly."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "x = 5\n"
            "y = 8\n"
            "z = 14\n"
            "with TempVars(names=['x'], restore=False) as tv_outer:\n"
            "    _t_in_1_before_2_x_absent = 'x' not in dir()\n"
            "    _t_in_1_before_2_y_present = 'y' in dir()\n"
            "    _t_in_1_before_2_z_present = 'z' in dir()\n"
            "    with TempVars(names=['y'], restore=True) as tv_inner:\n"
            "        _t_in_12_x_absent = 'x' not in dir()\n"
            "        _t_in_12_y_absent = 'y' not in dir()\n"
            "        _t_in_12_z_present = 'z' in dir()\n"
            "    _t_in_1_after_2_x_absent = 'x' not in dir()\n"
            "    _t_in_1_after_2_y_present = 'y' in dir()\n"
            "    _t_in_1_after_2_z_present = 'z' in dir()\n"
            "_t_after_12_x_absent = 'x' not in dir()\n"
            "_t_after_12_y_present= 'y' in dir()\n"
            "_t_after_12_z_present = 'z' in dir()\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def test_Good_NonMutableNamesStartsEndsArgs(self):
        """Confirm external lists passed as args aren't being modified."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(
            "from tempvars import TempVars\n"
            "n = ['xyz', 'fnq']\n"
            "s = ['abc_', 'qrs_']\n"
            "e = ['_mnp', '_fzr']\n"
            "_t_before_n_len = len(n) == 2\n"
            "_t_before_s_len = len(s) == 2\n"
            "_t_before_e_len = len(e) == 2\n"
            "t_fzr = 6\n"
            "xyz = 12\n"
            "abc_x = 35\n"
            "with TempVars(names=n, starts=s, ends=e) as tv:\n"
            "    _t_inside_n_len = len(n) == 2\n"
            "    _t_inside_s_len = len(s) == 2\n"
            "    _t_inside_e_len = len(e) == 2\n"
            "_t_outside_n_len = len(n) == 2\n"
            "_t_outside_s_len = len(s) == 2\n"
            "_t_outside_e_len = len(e) == 2\n",
            self.d,
        )

        for _ in [__ for __ in self.d if __.startswith("_t_")]:
            self.locals_subTest(_, self.d, True)

    def runtest_Good_NoNamesDupes(self, code):
        """Perform subTest-ed name duplication check on indicated code."""
        # Ensure self.d is actually getting cleared/reset
        assert len(self.d) == 0

        exec(code, self.d)

        for _ in ["nsvars_len_one", "ret_tempvars_len_one"]:
            self.locals_subTest(_, self.d, True)

    def test_Good_NoNamesDupes_NamesDuplicatesPassed(self):
        """Confirm no duplicate vars stored if `names` holds dupes."""
        self.runtest_Good_NoNamesDupes(
            "from tempvars import TempVars\n"
            "t_y = 15\n"
            "with TempVars(names=['t_y', 't_y']) as tv:\n"
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
            "    nsvars_len_one = len(tv.stored_nsvars) == 1\n"
            "    t_y_f = 35\n"
            "ret_tempvars_len_one = len(tv.retained_tempvars) == 1\n"
        )


class TestTempVarsExpectFail(SuperTestTempVars, ut.TestCase):
    """Testing that code raises expected errors when invoked improperly."""

    list_args = ["names", "starts", "ends"]

    def test_Fail_ArgIsNotListOrNone(self):
        """Confirm `TypeError` if non-list passed to var arg."""
        code = "from tempvars import TempVars; TempVars({0}=1)"

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
        code = (
            "from tempvars import TempVars; "
            'TempVars({0}=["abc", "{1}", "pqr"])'
        )

        for arg in ["starts", "ends"]:
            for val in ["_", "__"]:
                with self.subTest("{0}-{1}".format(arg, val)):
                    self.assertRaises(
                        ValueError, exec, code.format(arg, val), {}
                    )

        with self.subTest("starts-any-dunder-start"):
            self.assertRaises(
                ValueError, exec, code.format("starts", "__d"), {}
            )

        with self.subTest("ends-any-dunder-end"):
            self.assertRaises(ValueError, exec, code.format("ends", "s__"), {})

    def test_Fail_NonBooleanRestore(self):
        """Confirm `TypeError` if non-boolean `restore` is passed."""
        code = (
            "from tempvars import TempVars; "
            'TempVars(names=["abc"], restore=1)'
        )

        self.assertRaises(TypeError, exec, code, {})

    def test_Fail_NonGlobalScope(self):
        """Confirm that a `RuntimeError` is raised in a non-global scope."""
        from tempvars import TempVars

        with self.assertRaises(RuntimeError):
            with TempVars(names=["abcd"]):
                pass  # pragma: no cover

    def test_Fail_NoPatternArgsWarning(self):
        """Confirm `RuntimeWarning` if no pattern arguments are passed."""
        code = (
            "from tempvars import TempVars\n" "with TempVars():\n" "    pass\n"
        )

        with self.assertWarns(RuntimeWarning):
            exec(code, self.d)

    def test_Fail_EmptyListArgWarnings(self):
        """Confirm `RuntimeWarning` if empty list passed."""
        code = (
            "from tempvars import TempVars\n"
            "with TempVars(**{{'{0}': []}}):\n"
            "    pass\n"
        )
        for _ in ["names", "starts", "ends"]:
            self.d = {}
            with self.subTest(_):
                with self.assertWarns(RuntimeWarning):
                    exec(code.format(_), self.d)


# Doctest suite for testing README.rst example code
SuiteDoctestReadme = dt.DocFileSuite("README.rst", module_relative=False)


def suite_expect_good():
    """Create and return the test suite for expect-good cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests(
        [tl.loadTestsFromTestCase(TestTempVarsExpectGood), SuiteDoctestReadme]
    )

    return s


def suite_expect_fail():
    """Create and return the test suite for expect-fail cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestTempVarsExpectFail)])

    return s


if __name__ == "__main__":  # pragma: no cover
    print("Module not executable.")
