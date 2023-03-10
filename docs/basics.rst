Measurement Basics
==================

Every measurement has a sample, uncertainty, and units.

The uncertainty can be expressed as an absolute value or as a relative percentage.


**In-Place Mutation**

The below method mutates the measurement uncertainty style in-place.

.. testsetup:: *

    from pymeasurement import Measurement

.. doctest:: python

        >>> m = Measurement.fromStr("2.00 +/- 0.03 m")

        >>> m.toAbsolute()
        2.00 +/- 0.03 m

        >>> m
        2.00 +/- 0.03 m

.. doctest:: python

        >>> m.toPercent()
        2.00 +/- 1.5% m

        >>> m
        2.00 +/- 1.5% m

**Immutable**

The below method creates a new measurement object with the given uncertainty style.

.. doctest:: python

        >>> m.absolute()
        2.00 +/- 0.03 m

.. doctest:: python

        >>> m.percent()
        2.00 +/- 1.5% m