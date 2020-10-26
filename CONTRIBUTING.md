# Contributing to mannkendall (Python)

If you want to report a bug with mannkendall (Python), [jump here](#reporting-a-bug).

Or perhaps you may actually be considering contributing to the development of
mannkendall (Python) ? :heart_eyes: :tada:

There are many ways that you can do so, including by:
- [reporting a bug](#reporting-a-bug)
- fixing a [known issue](https://github.com/mannkendall/Python/issues?q=is%3Aissue+),
- implementing a new functionality,
- adding more functional tests, and/or
- improving the documentation:
  * in the code, with better docstrings,
  * in this repository (for example this very file !), and/or
  * in the website, via the docs `.rst` files

All these contributions are welcome, and what follows should help you get started. Note that
contributing to mannkendall (Python) does *not* necessarily require an advanced knowledge of Python
and/or Github. Helping us fix typos in the docs, for example, could be an excellent first
contribution. Plus, :anger: typos :anger: are the worst !

## Table of contents

- [Code of conduct](#code-of-conduct)
- [Reporting a bug](#reporting-a-bug)
- [Essential things to know about mannkendall (Python)](#essential-things-to-know-about-mannkendall-python)
- [Styles](#styles)
- [Step-by-step guide to contributing](#step-by-step-guide-to-contributing)

## Code of conduct

This project and everyone participating in it is governed by the
[mannkendall Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold
this code. Please report unacceptable behavior to
[frederic.vogt@meteoswiss.ch](mailto:frederic.vogt@meteoswiss.ch).

## Reporting a bug

If you find something odd with mannkendall (Python), first check if it is a
[known issue](https://github.com/mannkendall/Python/issues?q=is%3Aissue+). If not, please
create a new [Github Issue](https://github.com/mannkendall/Python/issues). This is the best
way for everyone to keep track of new problems and past solutions.

## Essential things to know about mannkendall (Python)
mannkendall (Python) is first-and-foremost a Python module - but not only. It also includes a series
of parameter and utilitarian files related to its Github repository, and a dedicated documentation
hosted using Github pages.

For the sake of clarity, and to facilitate the maintenance, we list here (succinctly) a series of
key facts about the mannkendall (Python) code and its repository:

1. **Source code:**
   * mannkendall (Python) is distributed under the terms of the BSD 3-Clause License. The mannkendall
    copyright is owned by MeteoSwiss, with the following [authors](AUTHORS).
   * mannkendall (Python) adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
   * The adopted styles are described [here](#styles).
   * mannkendall (Python) dependencies are specified in `setup.py`.
   * There is a human-readable [Changelog](CHANGELOG).

2. **Github repository:**
   * Contributions to mannkendall (Python) get typically merged into the `develop` branch.
     Pull requests to the `master` branch should only originate from the `develop` branch.
   * Any successful pull request to the `master` branch should trigger a new code release.
   * A series of Github Actions are implemented for CI purposes. These include the execution of
     the mannkendall (Python) tests on Windows, macOS and Linux, a linting of the code, a validation
     of the docs, and a check of the `CHANGELOG`.
   * A `.pylintrc` refines the behavior of pylint for mannkendall (Python).

3. **Documentation:**
   * The mannkendall documentation is generated using Sphinx, with the Read-the-docs theme. The
     compiled documentation is hosted on the `gh-pages` branch of the mannkendall Python repositiory.
   * Two docs-related Github Actions are implemented:
     - `CI_docs_check`: triggered on pull requests, compiles the docs and look for errors.
     - `CI_docs_publish`: triggered on push to master if the docs is changed, compiles the docs and
        pushes it to the branch `gh-pages`, thus automatically publisihing it live. 

## Styles

- **linting:**
  * The following [pylint](https://www.pylint.org/) error codes are forbidden in mannkendall (Python):
    ``E, C0303, C0304, C0112, C0114, C0115, C0116, C0411, W0611, W0612.`` Any pull request will be automatically linted, and these will be flagged accordingly.
  * We encourage contributors to follow PEP8 as closely as possible/reasonable. You should check
    often how well you are doing using the command `pylint some_modified_file.py`.

- **doctrings:** Google Style. Please try to stick to the following MWE:
```
    """ A brief one-liner description, that finishes with a dot.

    Use some
    multi-line space for
    more detailed info.

    Args:
        x (float, int): variable x could be of 2 types ...

           - *float*: x could be a float
           - *int*: x could also be an int

        y (list[str]; optional): variable y info

    Returns:
        bool: some grand Truth about the World.

    Example:
        If needed, you can specify chunks of code using code blocks::

            def some_function():
                print('hurray!')

    Note:
        `Source <https://github.com/sphinx-doc/sphinx/issues/3921>`__
        Please note the double _ _ after the link !

    Caution:
        Something to be careful about.

    """
```
You should feel free to use more of the tools offered by
[sphinx](https://www.sphinx-doc.org/en/master/),
[napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html), and
[Google Doc Strings](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google). But if you do, **please make sure that there are no errors upon generating the docs !**

## Step-by-step guide to contributing

WIP.
