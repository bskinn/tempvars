.. Usage info main page for tempvars

tempvars - Usage Examples
=========================

In all of these examples, it is assumed that |TempVars|
has already been imported and that `foo` and `bar` have
been defined as:

.. code:: python

    from tempvars import TempVars

    foo = 1
    bar = 2

.. _usage_toc:

.. contents:: Table of Contents
    :local:
    :backlinks: top



.. _usage_basic:

Masking Specific Variables
--------------------------

The most basic usage is to supply individual variable names in the
|arg_names| argument:

.. doctest::

    >>> with TempVars(names=['foo', 'bar']):
    ...     print('foo' in dir())
    ...     print('bar' in dir())
    ...
    False
    False
    >>> print(foo + bar)
    3

.. note::

    |arg_names| must always be a list of strings, even when
    only one variable name is passed.

If a variable name passed to |arg_names| doesn't exist in the namespace,
|TempVars| silently ignores it:

.. doctest::

    >>> with TempVars(names=['baz']):
    ...    print('foo' in dir())
    ...    print('bar' in dir())
    ...    print(2 * (foo + bar))
    ...
    True
    True
    6
    >>> print(2 * foo + bar)
    4

Masking Variables by Pattern
----------------------------

Variables can also be masked by pattern matching. Currently,
only 'starts with' and 'ends with' matching styles are supported:

.. doctest::

    >>> with TempVars(starts=['fo'], ends=['ar']):
    ...     print('foo' in dir())
    ...     print('bar' in dir())
    ...
    False
    False
    >>> print(foo + bar)
    3

To avoid accidental masking of system variables, the |arg_starts|
argument cannot start with a double underscore:

.. doctest::

    >>> try:
    ...     with TempVars(starts=['__foo']):
    ...         pass
    ... except ValueError:
    ...     print('Argument rejected')
    ...
    Argument rejected

Similarly, |arg_ends| cannot end with a double underscore:

.. doctest::

    >>> try:
    ...     with TempVars(ends=['foo__']):
    ...         pass
    ... except ValueError:
    ...     print('Argument rejected')
    ...
    Argument rejected




 * `starts` and `ends`
 * binding to `tv`
 * `stored_nsvars` (simple assignment, not copy!)
 * `retained_tempvars`
 * how `names` populates
 * `passed_names` holding only the original stuff
 * Nested contexts
