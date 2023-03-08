Create Measurements
===================

There are various ways to create measurements.

Every measurement has a sample and an uncertainty. If the uncertainty is not given, it is assumed to be zero and hence the measurement is infinitely precise.

**Using Constructor**

.. testsetup:: *

    from pymeasurement import Measurement

.. doctest:: python

        >>> Measurement("2.0", uncertainty="0.13", units="m")
        2.0 +/- 0.1 m

.. doctest:: python

        >>> Measurement("2.0", uncertainty="1.57", units="m", uncertaintyPercent=True)
        2.0 +/- 1.6% m

.. doctest:: python

        >>> Measurement("2.0", uncertainty="0.13", units="m", precision=3)
        2.00 +/- 0.13 m

**From String**

.. doctest:: python

        >>> Measurement.fromStr("2.0 +/- 0.13 m")
        2.0 +/- 0.1 m

.. doctest:: python

        >>> Measurement.fromStr("2.0 +/- 1.57% m")
        2.0 +/- 1.6% m

**From Float**

.. doctest:: python

        >>> Measurement.fromFloat(3.14)
        3.14
