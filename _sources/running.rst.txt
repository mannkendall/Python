.. include:: ./substitutions.rst

Running |name|
==============

The main function to compute the Mann-Kendall test with the desired prewhitening method, temporal
segmentation and confidence limit is:

.. code-block:: python

     import mannkendall as mk

     result = mk.mk_temp_aggr(multi_obs_dts, multi_obs, 2, pw_method='TFPW_WS',
                              alpha_mk=99, alpha_ak=95, alpha_cl=95, alpha_xhomo=90)

For example, in a case without temporal aggregation:

.. code-block:: python

    from datetime import datetime, timedelta
    import numpy as np
    import mannkendall as mk

    # Create some pseudo data
    y0 = datetime(2000, 1, 1)
    multi_obs_dts = np.array([y0+timedelta(days=365*item) for item in range(11)])
    multi_obs = np.array([1.92, 2.28, 2.71, 2.89, 2.82, 4.02, 3.25, 3.49, 4.94, 3.75, 3.25])

    # Process it
    out = mk.mk_temp_aggr(multi_obs_dts, multi_obs, 0.001)

    # Print the results
    print(out[0])

returns the following:

.. code-block:: python

    {'p': 0.007746191168936489, 'ss': 95, 'slope': 0.18612739726027397, 'ucl': 0.3052099519128413, 'lcl': 0.13008275427637808}


In a case with 4 temporal aggregates:

.. code-block:: python

    from datetime import datetime, timedelta
    import numpy as np
    import mannkendall as mk

    # Create some pseudo data
    y0 = [datetime(2000, 1, 1), datetime(2000, 4, 1), datetime(2000, 7, 1), datetime(2000, 10, 1)]
    multi_obs_dts = [np.array([y+timedelta(days=365*item) for item in range(19)]) for y in y0]
    multi_obs = [np.array([3.20, 2.92, 3.95, 1.80, 2.45, 2.70, 2.22, 2.10, 2.08, 2.21, 1.93, 2.15, 2.03, 1.82, 1.94, 2.24, 1.67, 1.34, 1.61]),
                 np.array([3.92, 2.99, 4.37, 3.04, 3.12, 4.07, 3.91, 3.42, 2.94, 3.14, 2.53, 2.80, 2.98, 2.86, 3.22, 2.31, 2.03, 1.59, 2.14]),
                 np.array([4.56, 4.13, 4.31, 1.83, 3.22, 5.06, 4.39, 4.13, 4.06, 3.20, 4.01, 3.62, 3.78, 3.61, 3.42, 3.65, 2.39, 3.01, 3.03]),
                 np.array([4.22, 4.78, 2.96, 3.23, 2.82, 2.96, 3.12, 3.49, 2.73, 2.61, 3.00, 2.66, 3.49, 2.58, 2.32, 2.10, 2.38, 2.29, 2.07])]

    # Process it
    out = mk.mk_temp_aggr(multi_obs_dts, multi_obs, 0.001)

    # Print the results
    for n in range(n_season):
        print('Season {ind}:'.format(ind=n+1), out[n])

    print('Combined yearly trend:', out[n_season])


returns the following:

.. code-block:: python

    Season 1: {'p': 0.028027113444650142, 'ss': 95, 'slope': -0.0630904059761449, 'ucl': -0.027152547174821143, 'lcl': -0.0887932846452936}
    Season 2: {'p': 0.0051285636056994655, 'ss': 95, 'slope': -0.09468046359192483, 'ucl': -0.045202101587346694, 'lcl': -0.1599308367432063}
    Season 3: {'p': 0.06887334136057355, 'ss': -1, 'slope': -0.06263257905417707, 'ucl': -0.01684988685739472, 'lcl': -0.1166561558463804}
    Season 4: {'p': 0.006355087077525301, 'ss': 95, 'slope': -0.06263257905417677, 'ucl': -0.03371081893003645, 'lcl': -0.11701020151232315}
    Combined yearly trend: {'p': 1.3649646335434085e-06, 'ss': 95, 'slope': -0.06286149251516099, 'ucl': -0.030431683052428795, 'lcl': -0.11683317867935178}


The function docstring provides all the details regarding what the function does, the different
input parameters, as well as the output. It can be accessed using the usual Python way:

.. code-block:: python

    import mannkendall as mk
    help(mk.mk_temp_aggr)
