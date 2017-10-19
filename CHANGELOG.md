## CHANGELOG: tempvars Temporary Variables Context Manager

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

All references below to the variable `tv` indicate an instance of
`TempVars` that has been bound as

```
with TempVars(...) as tv:
```

### [Unreleased]

#### Added

* `TempVars` now emits a warning if it is instantiated without
  masking pattern arguments.

#### Changed
	
* `TempVars().names` changed to be an exact copy of the `__init__` argument
  *names*. The actual variables masked can be retrieved as
  `tv.stored_nsvars.keys()`.
* Since, due to the above, initialization of `names` as a new, empty list
  is no longer needed, its default was changed to `None` 
* The `globals()` namespace stored as `TempVars.ns` has been renamed
  to `._ns` to discourage fiddling with it.
* `TempVars` changed to be an `@attr.s(slots=True)` class.

#### Removed

* `TempVars.passed_names` has been completely removed.


### [1.0.0b2] - 2017-10-01

#### Fixed

 * `starts` and `ends` no longer allow patterns that respectively
   start and end with `__`, to avoid munging the default dunder
   objects in the namespace
 * If a variable referencing a list, rather than a list literal, is
   passed as `names`, that passed reference is no longer erroneously
   updated with matches to the `starts` and `ends` patterns.
 * Fixed an erroneous duplication of variable names held in
   `names` due to variables in the namespace, e.g., matching multiple
   pattern entries in `starts` and/or `ends`.


### [1.0.0b1] - 2017-09-19

#### Added

 * Created the `TempVars` context manager
 * Implemented hard prevention of use in other than global scopes
   (raises `RuntimeError`) due to known improper behavior
 * Implemented masking of specific variables with `names` argument
 * Implemented `.startswith`/`.endswith` pattern-based masking
   via `starts` and `ends` arguments
 * Implemented option to restore or not masked namespace variables
   via `restore` argument
 * Implemented storage of pre-existing masked namespace variables
   for use within the managed context (`TempVars.stored_nsvars`)
 * Implemented storage of temporary variables and values assigned
   within the managed context (`TempVars.retained_tempvars`) for
   use after exiting the suite




