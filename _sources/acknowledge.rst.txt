
.. include:: ./substitutions.rst

Acknowledging |name|
====================

1. Only use lower case letters when mentioning |name|. Always include the language and version
   number. Ideally, you should also include the Digital Object Identifier (DOI) associated to the
   specific release you have been using:

   |name| |version| (DOI:)

2. If |name| was useful for your research, please cite the dedicated article:

   `Collaud Coen et al., 2020, ... <http:....>`__

3. |name| relies on external Python libraries that require & deserve to be acknowledged in their own
   right. The following LaTeX blurb is one way to do so:

   .. code-block:: latex

        This research has made use of \textit{mannkendall v1.0.0} \citep[DOI:][]{CollaudCoen2020}
        Python package. \textit{mannkendall} relies on the following Python packages:
        \textit{numpy} \citep{Oliphant2006, Van2011}, \textit{scipy} \citep{Virtanen2020},
        and \textit{statsmodels} \citep{Seabold2010}.

        @book{Oliphant2006,
              title={A guide to NumPy},
              author={Oliphant, Travis E},
              volume={1},
              year={2006},
              publisher={Trelgol Publishing USA}
              }

        @article{Van2011,
                 title={The NumPy array: a structure for efficient numerical computation},
                 author={Van Der Walt, Stefan and Colbert, S Chris and Varoquaux, Gael},
                 journal={Computing in Science \& Engineering},
                 volume={13},
                 number={2},
                 pages={22},
                 year={2011},
                 publisher={IEEE Computer Society}
                 }

        @article{Virtanen2020,
                author = {{Virtanen}, Pauli and {Gommers}, Ralf and {Oliphant},
                  Travis E. and {Haberland}, Matt and {Reddy}, Tyler and
                  {Cournapeau}, David and {Burovski}, Evgeni and {Peterson}, Pearu
                  and {Weckesser}, Warren and {Bright}, Jonathan and {van der Walt},
                  St{\'e}fan J.  and {Brett}, Matthew and {Wilson}, Joshua and
                  {Jarrod Millman}, K.  and {Mayorov}, Nikolay and {Nelson}, Andrew
                  R.~J. and {Jones}, Eric and {Kern}, Robert and {Larson}, Eric and
                  {Carey}, CJ and {Polat}, {\.I}lhan and {Feng}, Yu and {Moore},
                  Eric W. and {Vand erPlas}, Jake and {Laxalde}, Denis and
                  {Perktold}, Josef and {Cimrman}, Robert and {Henriksen}, Ian and
                  {Quintero}, E.~A. and {Harris}, Charles R and {Archibald}, Anne M.
                  and {Ribeiro}, Ant{\^o}nio H. and {Pedregosa}, Fabian and
                  {van Mulbregt}, Paul and {SciPy 1.0 Contributors}},
                 title = "{{SciPy} 1.0: Fundamental Algorithms for Scientific
                           Computing in Python}",
               journal = {Nature Methods},
               year = {2020},
               volume={17},
               pages={261--272},
               adsurl = {https://rdcu.be/b08Wh},
               doi = {https://doi.org/10.1038/s41592-019-0686-2},
         }

        @inproceedings{Seabold2010,
                       title={statsmodels: Econometric and statistical modeling with python},
                       author={Seabold, Skipper and Perktold, Josef},
                       booktitle={9th Python in Science Conference},
                       year={2010},
                       }

.. todo::

    When the time comes, include here the link to the dedicated mannkendall article.
