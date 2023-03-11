Table Operations
================

pymeasurement can be used with Pandas DataFrames to perform precision-based uncertainty calculations on tables of data.

**Original Data Table**

.. exceltable:: 
    :file: example.xls
    :selection: A1:C7
    :header: 1

In order to acheive this, the DataFrame is converted into Measurement objects for calculations using the below. 

All data can be normalized in this step as well.

.. doctest:: python

    >>> import pandas as pd
    >>> df = pd.read_excel('example.xlsx')
    >>> from pymeasurement import Measurement as M
    >>> converted = pd.DataFrame()
    >>> converted['Mass (± 0.001 kg)'] = M.importColumn(df['Mass (± 0.001 kg)'], d=True, un='kg', decimals=3)
    >>> converted['Average Acceleration (m/s^2)'] = M.importColumn(df['Average Acceleration (m/s^2)'], uncertaintyColumn=df['Average Acceleration Percent Uncertainty (%)'], df=df, up=True, un='m/s^2', decimals=2)

**Converted Data Table**

.. exceltable:: 
    :file: example.xls
    :selection: F1:G7
    :header: 1

Now calculations can easily be performed on the DataFrame using the Measurement objects.

.. doctest:: python

    >>> converted['Force (N)'] = converted['Mass (± 0.001 kg)'] * converted['Average Acceleration (m/s^2)']

**Calculated Data Table**

.. exceltable:: 
    :file: example.xls
    :selection: J1:L7
    :header: 1

Once the calculations are complete, the DataFrame can be converted back into a numeric types using the below.

.. doctest:: python

    >>> final_table = converted.copy()
    >>> M.exportColumn(final_table, converted['Mass (± 0.001 kg)'], addUncertainty=False)
    >>> M.exportColumn(final_table, converted['Average Acceleration (m/s^2)'])
    >>> M.exportColumn(final_table, converted['Force (N)'], asPercent=False)

.. exceltable:: 
    :file: example.xls
    :selection: O1:S7
    :header: 1
