# Contributing to mannkendall

If you want to report a bug with mannkendall, [jump here](#reporting-a-bug).

If you are still reading this, you may actually be considering contributing to the development of
mannkendall. :heart_eyes: :tada:

There are many ways that you can do so, including by:
- [reporting a bug](#reporting-a-bug)
- fixing a [known issue](https://github.com/MeteoSwiss-MDA/mannkendall/issues?q=is%3Aissue+),
- implementing a new functionality,
- adding more functional tests, and/or
- improving the documentation:
  * in the code, with better docstrings,
  * in this repository (for example this very file !), and/or
  * in the website, via the docs `.rst` files

All these contributions are welcome, and what follows should help you get started. Note that
contributing to mannkendall does *not* necessarily require an advanced knowledge of python and/or
Github. Helping us fix typos in the docs, for example, could be an excellent first contribution.
Plus, :anger: typos :anger: are the worst !

## Table of contents

- [Code of conduct](#code-of-conduct)
- [Reporting a bug](#reporting-a-bug)
- [Essential things to know about mannkendall](#essential-things-to-know-about-mannkendall)
- [Styles](#styles)
- [Step-by-step guide to contributing](#step-by-step-guide-to-contributing)

## Code of conduct

This project and everyone participating in it is governed by the
[mannkendall Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold
this code. Please report unacceptable behavior to
[frederic.vogt@meteoswiss.ch](mailto:frederic.vogt@meteoswiss.ch).

## Reporting a bug

If you find something odd with mannkendall, first check if it is a
[known issue](https://github.com/MeteoSwiss-MDA/mannkendall/issues?q=is%3Aissue+). If not, please
create a new [Github Issue](https://github.com/MeteoSwiss-MDA/mannkendall/issues). This is the best
way for everyone to keep track of new problems and past solutions.

## Essential things to know about mannkendall
mannkendall is first-and-foremost a Python module - but not only. It also includes a series of
parameter and utilitarian files related to its Github repository, and a dedicated documentation
hosted using Github pages.

For the sake of clarity, and to facilitate the maintenance, we list here (succinctly) a series of
key facts about the mannkendall code and its repository:

1. **Source code:**
   * mannbkendall is distributed under the terms of the BSD 3-Clause License. The mannkendall
    copyright is owned by MeteoSwiss, with the following [authors](AUTHORS).
   * mannkendall adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
   * The adopted styles are described [here](#styles).
   * mannkendall dependencies are specified in `setup.py`.
   * There is a human-readable [Changelog](CHANGELOG).

2. **Github repository:**
   * Contributions to mannkendall get typically merged into the `develop` branch. Pull requests to
     the `master` branch should only originate from the `develop` branch.
   * Any successful pull request to the `master` branch should trigger a new code release.
   * A series of Github Actions are implemented for CI purposes. These include the execution of
     the mannkendall tests on Windows, macOS and Linux, a linting of the code, a validation
     of the docs, and a check of the `CHANGELOG`.
   * A `.pylintrc` refines the behavior of pylint for mannkendall.

3. **Documentation:**
   * The mannkendall documentation is generated using Sphinx, with the Read-the-docs theme. The
     compiled documentation is hosted on the `gh-pages` branch of the mannkendall repositiory.

## Styles

- **linting:**
  * The following [pylint](https://www.pylint.org/) error codes are forbidden in mannkendall:
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

We are currently in the early stages of development of mannkendall. If you would like to contribute to the code, please contact [frederic.vogt@meteoswiss.ch](mailto:frederic.vogt@meteoswiss.ch).

Until its release, the mannkendall repository will remain private: branching will thus remain the
only way to contribute to the code. To get a local copy of mannkendall and contribute to its
improvement, follow these steps:

0. Make sure you have git installed. Check that the setup is correct:

       git config --list

   If `user.name` and `user.email` are missing or do not match those of your github account account,
   change them:

       git config --local user.name "your_github_id"
       git config --local user.email "your_github_id@users.noreply.github.com"

1. Clone the develop branch locally:

       git clone -b develop https://github.com/MeteoSwiss-MDA/mannkendall.git your_branch_name

2. Actually create your new branch locally:

       cd your_branch_name
       git checkout -b your_branch_name

3. Check that it all went as expected:

       git branch -a
       git config --list
       git status

4. Install the package in development mode from the local source. Attention - if you already
   have mannkendall installed, you should remove it first:

       pip uninstall mannkendall
       pip install -e .

5. Modify the code locally. This could be the source code, or the docs `.rst` source files.

   :warning: Please read carefully (and adhere to!) the mannkendall [style conventions](#styles)
             below.

6. Commit changes regularly, trying to bundle them in a meaningful manner.

       git add a_modified_file (OR possibly: git rm a_file_to_delete)
       git commit -m "Some useful, clear, and concise message. Use present tense."

   You can/should also push your branch to the mannkendall repository, if you want others to see
   what you are up to:

       git push origin your_branch_name

7. Lint your contributions using the command `pylint some_modified_file.py`. If you want to run the
   checks that will be executed automatically at the pull request stage, you can run the following
   commands from the mannkendall repository:

       python ./.github/workflows/pylinter.py --restrict E C0303 C0304 C0112 C0114 C0115 C0116 C0411 W0611 W0612
       python ./.github/workflows/pylinter.py --min_score 8

    Note that this may pick-up linting problems outside of your contribution(s) as well.

8. If warranted, make sure that the docs still compile without errors/warnings:

       cd docs
       sh build_docs.sh

7. Once ready with the modifications, push your branch to the mannkendall repository. If warranted
   (it most likely will be!), remember to update the `CHANGELOG` and add your name to the `AUTHORS`
   before doing so.

       git push origin your_branch_name

9. Next, go to `your_branch_name` on the mannkendall Github repository, and draft a new pull
   request. By default, the pull request should go from `your_branch_name` to the `develop` branch.
   Do not forget to link the pull request to a specific issue if warranted. Once the
   pull request is issued, automated checks will be run (pytest, pylint, changelog, ...), which
   should all succeed (if not, there might be something wrong with your changes).

   The code devs will then come and take a look and review the pull request.
