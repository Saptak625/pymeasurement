Measurement Operations
=======================

The following operations are available for measurements:

* ``+``: Add two measurements together.
* ``-``: Subtract two measurements.
* ``*``: Multiply two measurements or a measurement and a float together.
* ``/``: Divide two measurements or a measurement and a float.
* ``-``: Negate a measurement.
* ``**``: Raise a measurement to an integer power.
* ``abs()``: Return the absolute value of a measurement.

All of these operations return a new measurement object.

.. testsetup:: *

    from pymeasurement import Measurement as M

.. doctest:: python

        >>> a = M.fromStr('3.14d m/s')

        >>> b = M.fromStr('2.71d m/s')

        >>> a + b
        5.85 +/- 0.02 m/s

        >>> a - b
        0.43 +/- 0.02 m/s

        >>> a * b
        8.5 +/- 0.2 m^2/s^2

        >>> a / b
        1.15 +/- 0.02
        
        >>> a * 2
        6.28 +/- 0.02 m/s
        
        >>> a / 2
        1.57 +/- 0.01 m/s
        
        >>> -a
        -3.14 +/- 0.01 m/s
        
        >>> a ** 2
        9.9 +/- 0.1 m^2/s^2
        
        >>> abs(-a)
        3.14 +/- 0.01 m/s

