Lab Example
=================

Pymeasurement's Measurement type can be used to perform precision-based calculations with uncertainty propagation in standard Python data structures such as Pandas DataFrames. This example shows how to use the Measurement type to evaluate the data from a calorimetry experiment.

Problem
--------

Calculate the relationship between the molar enthalpy of combustion and the carbon chain length of primary alcohol fuels.


**Data Table throughout Calorimetry Lab**

.. exceltable:: 
    :file: Combustion_Lab_1920_Student_Data.xls
    :selection: A1:F24
    :header: 1

Solution
--------

The data from the lab is imported into a Pandas DataFrame.

.. doctest:: python

    >>> import pandas as pd
    >>> df = pd.read_excel('Combustion_Lab_1920_Student_Data.xlsx')

The DataFrame columns are converted into pymeasurement Measurements.

.. doctest:: python

    >>> from pymeasurement import Measurement as M
    >>> decimals = [3, 3, 3, 1, 1]
    >>> units = ['g', 'g', 'g', 'ºC', 'ºC']
    >>> for i in range(5):
    ...     df.iloc[:, i + 3] = M.importColumn(df.iloc[:, i + 3], d=True, un=units[i], decimals=decimals[i])

Now using the below formulas, the enthalpy of combustion can be calculated for each trial.

.. math::

    Q = m c \Delta T = m c (T_f - T_i)

.. math::

    n = m / M

.. math::

    \Delta H = -\frac{Q}{n}

.. doctest:: python
    
    >>> heat_capacity = M.fromStr('4.18c J/g*ºC')
    >>> j_to_kj = M.fromStr('0.001c kJ/J')
    >>> results_df_1 = df.iloc[:, 0:3]
    >>> results_df_1['Q of H2O (kJ)'] = df['Mass of water (+/- 0.001 g)'] * heat_capacity * (df['Final temperature (+/- 0.1 ºC)'] - df['Initial temperature (+/- 0.1 ºC)']) * j_to_kj
    >>> results_df_1['Mass of Alcohol (g)'] = df['Initial mass of spirit burner (+/- 0.001 g)'] - df['Final mass of spirit burner (+/- 0.001 g)']
    >>> molar_masses = {'Ethanol': M.fromStr('46.08c g/mol'), 'Propan-1-ol': M.fromStr('60.11c g/mol'), 'Butan-1-ol': M.fromStr('74.14c g/mol'), 'Pentan-1-ol': M.fromStr('88.17c g/mol')}
    >>> results_df_1['Molar Mass of Alcohol (g/mol)'] = results_df_1.apply(lambda x: x['Mass of Alcohol (g)'] / molar_masses[x['Alcohol tested']], axis=1)
    >>> results_df_1['Molar Enthalpy of Combustion (kJ/mol)'] = - results_df_1['Q of H2O (kJ)'] / results_df_1['Molar Mass of Alcohol (g/mol)']

**Results Table 1: Individual Molar Enthalpy of Combustion**

.. exceltable:: 
    :file: output.xls
    :selection: A1:G24
    :header: 1

Now, to calculate the average molar enthalpy of combustion for each of the alcohols, the data is grouped by alcohol type and the average is taken.

.. doctest:: python

    >>> results_df_2 = pd.DataFrame()
    >>> results_df_2['Alcohol'] = results_df_1['Alcohol tested'].unique()
    >>> grouped_data = list(results_df_1.groupby('Alcohol tested')['Molar Enthalpy of Combustion (kJ/mol)'])
    >>> grouped_data_dict = {i[0]: i[1] for i in grouped_data}
    >>> results_df_2['Average Molar Enthalpy of Combustion (kJ/mol)'] = [M.average(list(grouped_data_dict[i])).percent() for i in results_df_2['Alcohol']]
    >>> results_df_2['Accepted Molar Enthalpy of Combustion (kJ/mol)'] = [M.fromStr('-1367c kJ/mol'), M.fromStr('-2021c kJ/mol'), M.fromStr('-2676c kJ/mol'), M.fromStr('-3329c kJ/mol')]
    >>> results_df_2['Percent Error (%)'] = results_df_2.apply(lambda x: ((x['Accepted Molar Enthalpy of Combustion (kJ/mol)'] - x['Average Molar Enthalpy of Combustion (kJ/mol)']) * 100 / x['Accepted Molar Enthalpy of Combustion (kJ/mol)']), axis=1)

**Results Table 2: Average Molar Enthalpy of Combustion**

.. exceltable:: 
    :file: output.xls
    :selection: J1:M5
    :header: 1


Finally, we can convert the Measurement columns back into standard numeric columns.

.. doctest:: python

    >>> final_results_df_1 = results_df_1.copy()
    >>> for i in range(4):
    ...     M.exportColumn(final_results_df_1, results_df_1.iloc[:, i + 3])
    >>> final_results_df_2 = results_df_2.copy()
    >>> final_results_df_2 = results_df_2.copy()
    >>> for i in range(3):
    ...     M.exportColumn(final_results_df_2, results_df_2.iloc[:, i + 1], addUncertainty=i==0)

**Final Results Table 1: Individual Molar Enthalpy of Combustion**

.. exceltable:: 
    :file: output.xls
    :selection: A31:K54
    :header: 1

**Final Results Table 2: Average Molar Enthalpy of Combustion**

.. exceltable:: 
    :file: output.xls
    :selection: P31:T35
    :header: 1