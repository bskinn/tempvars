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

Basic Usage
-----------

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

    >>> with TempVars(names=['bar']):
    ...    print('foo' in dir())
    ...    print('bar' in dir())
    ...    print(2 * foo)
    ...
    True
    False
    2
    >>> print(2 * foo + bar)
    4


 * `starts` and `ends`
 * binding to `tv`
 * `stored_nsvars` (simple assignment, not copy!)
 * `retained_tempvars`
 * how `names` populates
 * `passed_names` holding only the original stuff
 * Nested contexts
