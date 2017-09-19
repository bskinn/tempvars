## CHANGELOG: tempvars Temporary Variables Context Manager

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


### [Unreleased]

*Nothing yet*


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




