.. include:: ./substitutions.rst

Installation
============

|name| is available on `pypi <https://pypi.org/project/mannkendall/>`__, which should make its
installation straighforward. In a terminal, type:

.. code-block:: python

   pip install mannkendall

And that will take care of things. |name| uses `semantic versioning <https://semver.org/>`_.

The most recent release of |name| (|github|) is also available for download from its
`Github repository <https://github.com/mannkendall/Python/releases/latest/>`_.

Requirements
------------
|name| is compatible with the following python versions:

.. literalinclude:: ../../setup.py
    :language: python
    :lines: 39

Furthermore, |name| relies on the following external modules, which will be automatically
installed by ``pip`` if required:

.. literalinclude:: ../../setup.py
    :language: python
    :lines: 40-42

Testing the installation
------------------------

The most basic test you can do, to see if the installation was successful, is to verify the version
of the package:

.. code-block:: python

    import mannkendall
    mannkendall.__version__
