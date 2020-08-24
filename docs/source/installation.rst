.. include:: ./substitutions.rst

Installation
============

.. todo::

    Include a link to the pypi page in the very next sentence.

mannkendall will be available on pypi, which should make its installation straighforward.
In a terminal, type:

.. code-block:: python

   pip install mannkendall

And that will take care of things. mannkendall uses `semantic versioning <https://semver.org/>`_.
The latest stable version is |version|.

The most recent release of mannkendall is also available for download from its
`Github repository <https://github.com/MeteoSwiss-MDA/mannkendall/releases/latest/>`_.

.. Caution::
    The mannkendall Github repository will remain private until the code is being released.
    If you want to know more about the current status of the code, feel free to
    `get in touch <frederic.vogt@meteoswiss.ch>`_.

Requirements
------------
mannkendall is compatible with the following python versions:

.. literalinclude:: ../../setup.py
    :language: python
    :lines: 39

Furthermore, mannkendall relies on a few external modules, which will be automatically installed by
``pip`` if required:

.. literalinclude:: ../../setup.py
    :language: python
    :lines: 40-41

Testing the installation
------------------------

.. todo::

    Describe how to test that mannkendall was properly installed.
