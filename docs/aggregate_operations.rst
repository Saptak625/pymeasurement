Aggregate Operations
=======================

The following operations are available for iterable collections of measurements:

* ``sum``: Sum a collection of measurements.
* ``min``: Find the minimum of a collection of measurements.
* ``max``: Find the maximum of a collection of measurements.
* ``average``: Find the average of a collection of measurements (Uncertainty = :math:`\Delta x = \frac{x_{max}-x_{min}}{2\sqrt{n}}`).

All of these operations return a new measurement object.

.. testsetup:: *

    from pymeasurement import Measurement as M

.. doctest:: python

    >>> collection = [M.fromStr('20.23d g'), M.fromStr('13.86d g'), M.fromStr('46.37d g')]
    >>> M.sum(collection)
    80.46 +/- 0.03 g
    >>> M.min(collection)
    13.86 +/- 0.01 g
    >>> M.max(collection)
    46.37 +/- 0.01 g
    >>> M.average(collection)
    26.82 +/- 9.38 g
