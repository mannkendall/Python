.. include:: ./substitutions.rst

Running |name|
==============

The main function to compute the Mann-Kendall test with the desired prewhitening method, temporal
segmentation and confidence limit is:

.. code-block:: python

     import mannkendall as mk
     result = mk.mk_temp_aggr(multi_obs_dts, multi_obs, resolution, **kwargs)

For example:

.. code-block:: python

    result = mk.mk_temp_aggr(multi_obs_dts, multi_obs, 0.01)
    result = mk.mk_temp_aggr(multi_obs_dts, multi_obs, 2, pw_method='TFPW_WS',
                             alpha_mk=99, alpha_ak=95, alpha_cl=95, alpha_xhomo=90)

The associated docstring provides all the details regarding what the function does, the different
input parameters, as well as the output. It can be accessed using the usual Python way:

.. code-block:: python

    import mannkendall as mk
    help(mk.mk_temp_aggr)
