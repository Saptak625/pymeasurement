Physics Example
================

Problem
--------
A ball is thrown vertically upward with an initial velocity of 20. +/- 1 m/s. Calculate the time it takes for the ball to reach its maximum height and the maximum height it reaches. Neglect air resistance and assume that the acceleration due to gravity is 9.81 m/s².


Solution
--------

Formulas:

.. math::
    
   \text{Time} = \frac{v_i}{a}

.. math::    

   \text{Max Height} = \frac{v_i^2}{2a}

.. testsetup:: python

    from pymeasurement import Measurement as M

.. doctest:: python

        >>> v_i = M.fromStr('20. +/- 1 m/s')
        >>> a = M.fromFloat(9.81, 'm/s^2')
        >>> t = v_i / a
        >>> h = v_i**2 / (2 * a)
        >>> t
        2.0 +/- 5% s
        >>> h
        20 +/- 1E+1% m

Thus, the time it takes to reach the maximum height is :math:`2.0 \pm 5\% \text{ s}` and the maximum height is :math:`101.5 \pm 1E+1\% \text{ m}`.