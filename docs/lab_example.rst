Lab Example
=================

Pymeasurement's Measurement type can be used to perform precision-based calculations with uncertainty propagation in standard Python data structures such as NumPy arrays and Pandas DataFrames. This example shows how to use the Measurement type to evaluate the data from a calorimetry experiment.

Problem
--------

Calculate the relationship between the molar enthalpy of combustion and the carbon chain length of primary alcohol fuels.


**Data Table throughout Calorimetry Lab**

.. exceltable:: 
    :file: _static\Combustion_Lab_1920_Student_Data.xls
    :header: 1
    :selection: A1:F24

Solution
--------

The data from the lab is imported into a Pandas DataFrame.

.. doctest:: python

    >>> import pandas as pd
    >>> df = pd.read_excel('_static\Combustion_Lab_1920_Student_Data.xlsx')

The DataFrame columns are converted into pymeasurement Measurements.

.. doctest:: python

    >>> 
