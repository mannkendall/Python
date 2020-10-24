.. include:: ./substitutions.rst

Installation
============

.. todo::

    Include a link to the pypi page in the very next sentence.

|name| will be available on pypi, which should make its installation straighforward.
In a terminal, type:

.. code-block:: python

   pip install mannkendall

And that will take care of things. |name| uses `semantic versioning <https://semver.org/>`_.
The latest stable version is |version|.

The most recent release of |name| is also available for download from its
`Github repository <https://github.com/mannkendall/Python/releases/latest/>`_.

Requirements
------------
|name| is compatible with the following python versions:

.. literalinclude:: ../../setup.py
    :language: python
    :lines: 39

Furthermore, |name| relies on a the following external modules, which will be automatically
installed by ``pip`` if required:

.. literalinclude:: ../../setup.py
    :language: python
    :lines: 40-43

Testing the installation
------------------------

The most basic check to see if the installation was successful consists in checking the version of
the package:

.. code-block:: python

    import mannkendall
    mannkendall.__version__
