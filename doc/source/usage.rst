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

The removal of a pre-existing variable from the namespace for the
duration of a ``with TempVars`` context is termed **masking** here.
Temporary variables created within the managed context that match
one or more of |arg_names|_, |arg_starts|_, and/or |arg_ends|_ are
**discarded** (removed from the namespace) when exiting the context.


.. _usage_toc:

Table of Contents
~~~~~~~~~~~~~~~~~

.. contents::
    :local:
    :backlinks: top


Masking Specific Variables
--------------------------

The most basic usage is to supply individual variable names in the
|arg_names|_ argument:

.. doctest:: names_basic

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
however, still discard any matching variables from the namespace upon exiting
the |with| block:

.. doctest:: names_creatednew

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
    >>> print(2 * (foo + bar))
    6
    >>> 'baz' in dir()
    False

Masking Variables by Pattern
----------------------------

Variables can also be masked by pattern matching. Currently,
only 'starts with' and 'ends with' matching styles are supported:

.. doctest:: starts_ends_basic

    >>> with TempVars(starts=['fo'], ends=['ar']):
    ...     print('foo' in dir())
    ...     print('bar' in dir())
    ...
    False
    False
    >>> print(foo + bar)
    3

.. note::

    |arg_starts|_ and |arg_ends|_ must always be lists of strings, even when
    only one pattern is passed.

To avoid accidental masking of system variables, the |arg_starts|_
argument cannot start with a double underscore:

.. doctest:: starts_no_dunder

    >>> try:
    ...     with TempVars(starts=['__foo']):
    ...         pass
    ... except ValueError:
    ...     print('Argument rejected')
    ...
    Argument rejected

Similarly, |arg_ends|_ cannot end with a double underscore:

.. doctest:: ends_no_dunder

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

.. doctest:: starts_ends_not_underscore

    >>> try:
    ...     with TempVars(starts=['_']):
    ...         pass
    ... except ValueError:
    ...     print('Argument rejected')
    ...
    Argument rejected

As with |arg_names|_, |arg_starts|_ and |arg_ends|_ also discard any
matching variables created within the |with| block, whether they existed
previously or not:

.. doctest:: starts_ends_creatednew

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
it masks from the original namespace, effectively discarding them
permanently:

.. doctest:: restore_one_false

    >>> with TempVars(names=['foo', 'bar'], restore=False):
    ...     pass
    ...
    >>> 'foo' in dir()
    False
    >>> 'bar' in dir()
    False

|TempVars| contexts can be freely nested to allow selective
restore/discard behavior:

.. doctest:: restore_mixed_nested

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

|TempVars| is constructed so that each instance can be bound as part
of the |with| statement, for later inspection within *and* after the
managed context. The masking pattern arguments are stored as-is,
but are duplicated from the input argument to avoid munging of
mutable arguments:

.. doctest:: basic_binding_demo

    >>> names_in = ['foo']
    >>> with TempVars(names=names_in, starts=['baz', 'quux'],
    ...               ends=['ar']) as tv:
    ...     print(tv.starts)
    ...     print(tv.ends)
    ...     print(tv.names)
    ...     print('foo' in dir())
    ...     print('bar' in dir())
    ['baz', 'quux']
    ['ar']
    ['foo']
    False
    False
    >>> names_in.append('quorz')
    >>> print(tv.names)
    ['foo']

All of these instance variables can also be examined after
the end of the managed context:

.. doctest:: examine_instance_vars_after

    >>> with TempVars(names=['foo', 'baz'], starts=['ba']) as tv:
    ...     pass
    >>> print(tv.names)
    ['foo', 'baz']
    >>> print(tv.starts)
    ['ba']


Inspecting Masked Variables within the Managed Context
------------------------------------------------------

|TempVars| provides a means to access the masked variables from within
the managed context,


|br|


 * binding to `tv`
 * `stored_nsvars` (simple assignment, not copy!)
 * `retained_tempvars` (also simple assignment!)

