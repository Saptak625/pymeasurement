Chemistry Example
=================

Problem
--------
In a calorimetry experiment, 50.0 mL of 0.200 ± 2% M hydrochloric acid (HCl) at an initial temperature of 25.0°C is added to 50.0 mL of 0.200 ± 2% M sodium hydroxide (NaOH) at an initial temperature of 25.0°C in a polystyrene foam cup calorimeter. The temperature of the solution increases to 31.2°C after the reaction is complete. The specific heat capacity of the solution is assumed to be 4.18 J/g°C. The density of the solution is 1.00 g/mL.

The volume of each of the solutions was measured using a graduated cylinder. The temperature of the solution was measured using a digital sensor probe.

Calculate the change in enthalpy of the reaction (ΔH) in kJ/mol with its uncertainty.


Solution
--------

**Balanced Chemical Equation:**

.. math::

    HCl + NaOH \rightarrow NaCl + H_{2}O



**Formulas:**

.. math::

    \Delta T = T_f - T_i

.. math::

    m = \rho V

.. math::

    Q = m c \Delta T

.. math::

    n = M V

.. math::

    \Delta H = -\frac{Q}{n}
    

.. testsetup:: python

    from pymeasurement import Measurement as M

.. doctest:: python

        >>> molarity = M.fromStr('0.200 +/- 2% mol/mL')
        >>> volume = M.fromStr('50.0a mL')
        >>> t_i = M.fromStr('25.0d °C')
        >>> t_f = M.fromStr('31.2d °C')
        >>> density = M.fromStr('1.00c g/mL')
        >>> t_change = t_f - t_i
        >>> mass = density * volume
        >>> q = mass * M.fromFloat(4.18, 'J/(g*°C)') * t_change
        >>> n = molarity * volume
        >>> delta_h = -q / n
        >>> delta_h
        -1.3E+2 +/- 7% J/mol

Thus, this reaction has a change in enthalpy of :math:`-1.3 \times 10^2 \pm 7\%` J/mol.