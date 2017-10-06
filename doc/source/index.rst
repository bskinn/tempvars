.. Root file for tempvars documentation

tempvars Documentation
======================

*Streamlined temporary variable management in Jupyter Notebook, IPython, etc.*

[texty text mctexterson]

Testing ``doctest``:

.. testsetup testing

..    from tempvars import TempVars

.. doctest:: testing

    >>> a = [1]
    >>> print(a)
    [1]
    >>> with TempVars(names=['a']) as tv:
    ...     print('a' in dir())
    ...     a = 3
    ...     print(a)
    False
    3
    >>> print(a)
    [1]
    >>> a.append(2)
    >>> print(a)
    [1, 2]
    >>> print(tv.stored_nsvars['a'])
    [1, 2]
    >>> with TempVars(starts=['t_']) as tv:
    ...     t_z = [5]
    ...     z = t_z
    ...     print(t_z)
    [5]
    >>> z.append(6)
    >>> print(z)
    [5, 6]
    >>> print(tv.retained_tempvars['t_z'])
    [5, 6]


.. toctree::
    :maxdepth: 2
    :caption: Contents:

    Usage <usage>
    API <api>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
