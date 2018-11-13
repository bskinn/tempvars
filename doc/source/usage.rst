.. Usage info main page for tempvars

tempvars Usage Examples
=======================

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

.. note::

    The most common use case us anticipated to be via either
    |arg_starts| or |arg_ends|, where a common prefix or suffix,
    respectively (such as `t_` or `_t`), is used to mark all
    temporary variables within the managed context. See
    ":ref:`usage_pattern_masking`," below.


.. _usage_toc:

**Contents**

.. contents::
    :local:
    :backlinks: top


.. _recommended_standard_usage:

Recommended Standard Usage
--------------------------

This author's standard approach for using :class:`~tempvars.TempVars`
is to make use of the `starts` argument as follows:

.. doctest:: recommended

    >>> with TempVars(starts=['t_']):
    ...     t_foo = foo
    ...     t_baz = foo + bar
    >>> print('t_foo' in dir())
    False
    >>> print('t_baz' in dir())
    False

As shown, any variable desired to be temporary can just be prefixed with
`t_`, and it will not survive beyond the scope of the relevant
:class:`~tempvars.TempVars` suite.


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


.. _usage_pattern_masking:

Masking Variables by Pattern
----------------------------

As :ref:`noted above <recommended_standard_usage>`,
variables can also be masked by pattern matching. Currently,
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

As with |arg_names|_, |arg_starts|_ and |arg_ends|_ also discard at exit any
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
managed context. The masking pattern arguments are stored without
modification, but are duplicated from the input argument to avoid munging of
mutable arguments:

.. doctest:: basic_binding_demo

    >>> names_in = ['foo']
    >>> with TempVars(names=names_in, starts=['baz', 'quux'], ends=['ar']) as tv:
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

As shown above, these instance variables can also be examined after
the end of the managed context.


.. _usage_stored_nsvars:

Inspecting Masked Variables
---------------------------

|TempVars| provides a means to access the masked variables from within
the managed context, via the :data:`~tempvars.TempVars.stored_nsvars`
instance variable:

.. doctest:: examine_nsvars

    >>> with TempVars(names=['foo']) as tv:
    ...     print(list(tv.stored_nsvars.keys()))
    ...     print(tv.stored_nsvars['foo'])
    ...     print('foo' in dir())
    ['foo']
    1
    False

The masked variables remain available after the end of the managed
context, even if they are not restored when the context exits:

.. doctest:: examine_nsvars_norestore

    >>> with TempVars(names=['foo']) as tv:
    ...     pass
    >>> print(tv.stored_nsvars['foo'])
    1
    >>> with TempVars(names=['bar'], restore=False) as tv2:
    ...     pass
    >>> print('bar' in dir())
    False
    >>> print(tv2.stored_nsvars['bar'])
    2

A caveat: the masked variables are bound within
:data:`~tempvars.TempVars.stored_nsvars` by simple assignment,
which can have (possibly undesired) side effects when
mutable objects are modified after being masked:

.. doctest:: nsvars_mutable_munging

    >>> baz = [1, 2, 3]
    >>> with TempVars(names=['baz']) as tv:
    ...     tv.stored_nsvars['baz'].append(12)
    >>> print(baz)
    [1, 2, 3, 12]
    >>> baz.remove(2)
    >>> print(tv.stored_nsvars['baz'])
    [1, 3, 12]

If :func:`~copy.copy` or :func:`~copy.deepcopy` behavior is of interest,
please add a comment to that effect on the
`related GitHub issue <copy_deepcopy_>`_.


.. _usage_ret_tempvars:

Inspecting Discarded Temporary Variables
----------------------------------------

In an analogous fashion to :data:`~tempvars.TempVars.stored_nsvars`,
the temporary variables discarded from the namespace at the exit of
the managed context are stored in
:data:`~tempvars.TempVars.retained_tempvars`:

.. doctest:: examine_ret_tempvars

    >>> with TempVars(names=['foo']) as tv:
    ...     foo = 5
    ...     print(foo * bar)
    10
    >>> print(foo + tv.retained_tempvars['foo'])
    6

Also as with :data:`~tempvars.TempVars.stored_nsvars`, at this time
the values within :data:`~tempvars.TempVars.retained_tempvars` are
bound by simple assignment, leading to similar possible side effects:

.. doctest:: munging_ret_tempvars

    >>> baz = [1, 2]
    >>> with TempVars(names=['baz']) as tv:
    ...     tv.stored_nsvars['baz'].append(3)
    ...     baz = tv.stored_nsvars['baz']
    >>> tv.retained_tempvars['baz'].append(4)
    >>> print(baz)
    [1, 2, 3, 4]

As above, if :func:`~copy.copy` and/or :func:`~copy.deepcopy`
behavior is of interest, please comment on the
`relevant GitHub issue <copy_deepcopy_>`_.



.. _copy_deepcopy: https://github.com/bskinn/tempvars/issues/20


