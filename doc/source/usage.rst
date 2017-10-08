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
|arg_names|_ argument:

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

    |arg_names|_ must always be a list of strings, even when
    only one variable name is passed.

If a variable name passed to |arg_names|_ doesn't exist in the namespace,
|TempVars| silently ignores it when entering the |with| block. It **does**,
however, still remove any matching variables from the namespace upon exiting
the |with| block:

.. doctest::

    >>> with TempVars(names=['baz']):
    ...     print('foo' in dir())
    ...     print('bar' in dir())
    ...     print(2 * (foo + bar))
    ...     baz = 5
    ...     print(baz)
    ...
    True
    True
    6
    5
    >>> print(2 * foo + bar)
    4
    >>> 'baz' in dir()
    False

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

To avoid accidental masking of system variables, the |arg_starts|_
argument cannot start with a double underscore:

.. doctest::

    >>> try:
    ...     with TempVars(starts=['__foo']):
    ...         pass
    ... except ValueError:
    ...     print('Argument rejected')
    ...
    Argument rejected

Similarly, |arg_ends|_ cannot end with a double underscore:

.. doctest::

    >>> try:
    ...     with TempVars(ends=['foo__']):
    ...         pass
    ... except ValueError:
    ...     print('Argument rejected')
    ...
    Argument rejected

As well, neither |arg_starts|_ nor |arg_ends|_ can be a single
underscore, since this also would mask Python system
variables:

.. doctest::

    >>> try:
    ...     with TempVars(starts=['_']):
    ...         pass
    ... except ValueError:
    ...     print('Argument rejected')
    ...
    Argument rejected

|arg_starts|_ and |arg_ends|_ also discard any matching variables created
within the |with| block, whether they existed previously or not:

.. doctest::

    >>> with TempVars(starts=['t_'], ends=['_t']):
    ...     t_foo = 6
    ...     bar_t = 7
    ...     print(t_foo * bar_t)
    ...
    42
    >>> 't_foo' in dir()
    False
    >>> 'bar_t' in dir()
    False


Discarding Masked Variables
---------------------------

If desired, |TempVars| can be instructed not to restore any variables
it masks from the original namespace:

.. doctest::

    >>> with TempVars(names=['foo', 'bar'], restore=False):
    ...     pass
    ...
    >>> 'foo' in dir()
    False
    >>> 'bar' in dir()
    False

|TempVars| contexts can be freely nested to allow selective restore/
discard behavior:

.. doctest:: mixed_nest_restore

    >>> with TempVars(names=['foo'], restore=False):
    ...     with TempVars(names=['bar']):
    ...         foo = 3
    ...         bar = 5
    ...         print(foo * bar)
    ...     print(foo * bar)
    15
    6
    >>> print(bar)
    2
    >>> 'foo' in dir()
    False


Binding TempVars Instances
--------------------------

|TempVars| is constructed so that each instance can be bound for later
inspection as part of the |with| statement:



|br|


 * binding to `tv`
 * `stored_nsvars` (simple assignment, not copy!)
 * `retained_tempvars`
 * how `names` populates
 * `passed_names` holding only the original stuff
 * Nested contexts
