from pymeasurement.sigfig import SigFig
import math

class Measurement:
  """
  Measurement
  A class to represent a SigFig sample with a SigFig uncertainty and corresponding units.
  This class can be used to perform calculations with uncertainty propagation.
  Units are also automatically derived through operations with other measurements.

  :param sample: The sample value as a SigFig object or a string.
  :type sample: SigFig or str
  :param precision: The number of significant figures to use when printing the number. If None, the number of significant figures will be automatically determined.
  :type precision: int
  :param uncertainty: The uncertainty of the sample as a SigFig object or a string.
  :type uncertainty: SigFig or str
  :param uncertaintyPercent: If True, the uncertainty will be interpreted as a percentage of the sample value.
  :type uncertaintyPercent: bool
  :param digital: If True, the uncertainty will be automatically determined based on the precision of the device.
  :type digital: bool
  :param analog: If True, the uncertainty will be automatically determined based on the precision of the device.
  :type analog: bool
  :param units: The units of the measurement as a string.
  :type units: str
  :param P: The number of significant figures to use when printing the number. If None, the number of significant figures will be automatically determined.
  :type P: int
  :param U: The uncertainty of the sample as a SigFig object or a string.
  :type U: SigFig or str
  :param UP: If True, the uncertainty will be interpreted as a percentage of the sample value.
  :type UP: bool
  :param D: If True, the uncertainty will be automatically determined based on the precision of the device.
  :type D: bool
  :param A: If True, the uncertainty will be automatically determined based on the precision of the device.
  :type A: bool
  :param UN: The units of the measurement as a string.
  :type UN: str
  """
  def __init__(self, sample, precision=None, uncertainty=None, uncertaintyPercent=False, digital=False, analog=False, units=None, P=None, U=None, UP=False, D=False, A=False, UN=None):
    """
    Measurement Constructor
    """
    if P is not None:
      precision = P
    if U is not None:
      uncertainty = U
    if UP:
      uncertaintyPercent = UP
    if D:
      digital = D
    if A:
      analog = A
    if UN is not None:
      units = UN
    
    if not isinstance(sample, SigFig):
      if '(' in sample or '[' in sample:
        sample, precision = sample.split()
        try:
          precision = int(precision[1:-1]) #Precision in Sig Figs
        except ValueError:
          raise Exception('Measurement Error: Invalid Literal for Sig Fig Precision.')
    if not isinstance(sample, SigFig):
      if precision == float('inf'):
        self.sample = SigFig(sample, constant=True)
      else:
        self.sample = SigFig(sample, sigfigs=precision) 
    else:
      self.sample = sample

    #Automatic Determination of Uncertainty based on Device
    self.uncertainty = None
    if analog:
      self.uncertainty = SigFig(f"5e{self.sample.decimals}", decimals=self.sample.decimals)
    elif digital:
      self.uncertainty = SigFig(f"1e{self.sample.decimals}", decimals=self.sample.decimals)
    
    #Main Override
    if uncertainty is not None:
      if not isinstance(uncertainty, SigFig):
        if '%' in uncertainty:
          uncertaintyPercent = True
          uncertainty = uncertainty.replace('%', '')
      self.uncertainty = SigFig(uncertainty, decimals=self.sample.decimals) if not isinstance(uncertainty, SigFig) else uncertainty
    self.uncertaintyPercent = uncertaintyPercent

    #Chemistry Percent Rules(if <2%, 2 sig figs. Else 1 sig fig)
    if self.uncertainty is not None and self.uncertaintyPercent:
      self.uncertainty = SigFig(str(self.uncertainty.decimalValue), sigfigs=(2 if self.uncertainty < SigFig('2', constant=True) else 1))

    #Determine Units
    #Will use units class to allow for conversions later.
    self.units = units
    self.nUnits = [i.strip('() ') for i in self.units.split('*')] if self.units is not None else []
    self.dUnits = []
    if self.units is not None:
      if '/' in units:
        nUnitsStr, dUnitsStr = self.units.split('/')
        nUnitsStr = nUnitsStr.strip('() ')
        dUnitsStr = dUnitsStr.strip('() ')
        self.nUnits = [i.strip('() ') for i in nUnitsStr.split('*')]
        self.dUnits = [i.strip('() ') for i in dUnitsStr.split('*')]
        if '^' in nUnitsStr:
          newNUnits = []
          for i in self.nUnits:
            if '^' in i:
              i, repeat = i.split('^')
              for n in range(int(repeat)-1):
                newNUnits.append(i)
            newNUnits.append(i)
          self.nUnits = newNUnits
        if '^' in dUnitsStr:
          newDUnits = []
          for i in self.dUnits:
            if '^' in i:
              i, repeat = i.split('^')
              for n in range(int(repeat)-1):
                newDUnits.append(i)
            newDUnits.append(i)
          self.dUnits = newDUnits
    newNUnits = self.nUnits
    newDUnits = self.dUnits
    for i in self.nUnits:
      if i in newDUnits:
        newNUnits.remove(i)
        newDUnits.remove(i)
    #Sort units alphabetically
    self.nUnits=sorted(newNUnits)
    self.dUnits=sorted(newDUnits)
    #Reformat units string
    self.units = Measurement.formatUnits(self.nUnits, self.dUnits)

  def fromStr(string):
    """Creates a Measurement object from a string.
    The string must be in the form of a number, uncertainty, and units.
    The uncertainty can be in the form of a percentage or a number.
    A 'a' or 'd' can be used to indicate an analog or digital device for automatic uncertainty determination.

    :param string: The string to create the Measurement object from.
    :type string: str
    :return: The Measurement object created from the string.
    :rtype: Measurement
    """
    sample = string.strip()
    uncertainty = None
    units = None
    values = sample.split()
    if '+/-' in sample or '+-' in sample:
      if len(values) == 3:
        if '+/-' in sample:
          sample, uncertainty = string.split('+/-')
        elif '+-' in sample:
          sample, uncertainty = string.split('+-')
      elif len(values) >= 4:
        sample, _, uncertainty, *units = values
        if len(units) == 2: # Assuming form will mol H2O
          if '_' not in units[1]:
            from pymeasurement.util.chem.compound import Compound
            units[1] = str(Compound(units[1])) # Format Compound String
        units = ' '.join(units)
    else:
      if len(values) >= 2:
        sample, *units = values
        if len(units) == 2: # Assuming form will mol H2O
          if '_' not in units[1]:
            from pymeasurement.util.chem.compound import Compound
            units[1] = str(Compound(units[1])) # Format Compound String
        units = ' '.join(units)
    precision = None
    digital = False
    analog = False
    if uncertainty is None:
      if 'c' in sample:
        precision = float('inf')
        sample = sample.replace('c', '')
      elif 'd' in sample:
        digital = True
        sample = sample.replace('d', '')
      elif 'a' in sample:
        analog = True
        sample = sample.replace('a', '')
    return Measurement(sample.strip(), precision=precision, uncertainty=(uncertainty.strip() if isinstance(uncertainty, str) else uncertainty), digital=digital, analog=analog, units=units)

  def fromFloat(f, units=''): #Assume float is a constant with infinite precision and no uncertainty.
    """
    Creates a Measurement constant from a float.

    :param f: The float to create the Measurement constant from.
    :type f: float
    :param units: The units of the Measurement constant.
    :type units: str
    :return: The Measurement constant created from the float.
    :rtype: Measurement
    """
    return Measurement.fromStr(f'{f}c {units}')
  
  def toAbsolute(self):
    """
    Converts the uncertainty to an absolute value. Note that this mutates the object.

    :return: The Measurement object with the uncertainty converted to an absolute value.
    :rtype: Measurement
    """
    if self.uncertaintyPercent and isinstance(self.uncertainty, SigFig):
      self.uncertaintyPercent = False
      self.uncertainty *= (self.sample / SigFig('100', constant=True)).abs()
      self.uncertainty = SigFig(str(self.uncertainty.decimalValue), decimals=self.sample.decimals)
    return self

  def toPercent(self):
    """
    Converts the uncertainty to a percentage. Note that this mutates the object.

    :return: The Measurement object with the uncertainty converted to a percentage.
    :rtype: Measurement
    """
    if not self.uncertaintyPercent and isinstance(self.uncertainty, SigFig):
      self.uncertaintyPercent = True
      self.uncertainty = SigFig(self.uncertainty.value, constant=True) * SigFig((SigFig('100', constant=True) / self.sample).abs().value, constant=True)
      self.uncertainty = SigFig(str(self.uncertainty.decimalValue), sigfigs=(2 if self.uncertainty < SigFig('2', constant=True) else 1))
    return self

  def absolute(m):
    """
    Returns a copy of the Measurement with the uncertainty converted to an absolute value.

    :return: A copy of the Measurement with the uncertainty converted to an absolute value.
    :rtype: Measurement
    """
    return m.deepCopy().toAbsolute()

  def percent(m):
    """
    Returns a copy of the Measurement with the uncertainty converted to a percentage.

    :return: A copy of the Measurement with the uncertainty converted to a percentage.
    :rtype: Measurement
    """
    return m.deepCopy().toPercent()
  
  def deepCopy(self):
    """
    Returns a deep copy of the Measurement object.

    :return: A deep copy of the Measurement object.
    :rtype: Measurement
    """
    return Measurement(self.sample.deepCopy(), uncertainty = self.uncertainty.deepCopy() if self.uncertainty is not None else None, uncertaintyPercent = self.uncertaintyPercent, units=self.units)

  def apply_func(func, **kwargs):
    """
    Applies a function to the sample and uncertainty of the Measurement object. Based on the Generalized Uncertainty Propagation Formula. Suggest the units of the result by passing a "units" kwarg.

    :param func: The function expression to apply.
    :type func: string
    :return: The Measurement object with the function applied.
    :rtype: Measurement
    """
    # Remove the units from the kwargs
    units = None
    if 'units' in kwargs:
      units = kwargs.pop('units')

    # Convert the measurement kwargs to absolute uncertainties
    for i in kwargs.keys():
      kwargs[i] = Measurement.absolute(kwargs[i])

    # Generalized Uncertainty Propagation Formula
    # \delta f = \sqrt{\sum_{i=1}^{n} \left(\frac{\partial f}{\partial x_i}\right)^2 \delta x_i^2}
    from sympy import Symbol, diff, sqrt, sympify
    
    # Define each of the kwargs as a symbol
    symbols = {i: Symbol(i) for i in kwargs.keys()}

    # Convert the function expression to a sympy expression
    func = sympify(func)

    # Evaluate the function with the given kwargs
    eval_func = func
    for i in kwargs.keys():
      eval_func = eval_func.subs(symbols[i], float(kwargs[i].sample.value))
    eval_func = SigFig(str(eval_func.evalf()), sigfigs=min((kwargs[i].sample.sigfigs for i in kwargs.keys())))

    # Calculate the partial derivative of the function with respect to each symbol
    partials = {i: diff(func, symbols[i]) for i in symbols}

    # Define each of the uncertainties as \delta x_i
    uncertainties = {f'δ{i}': Symbol(f'δ{i}') for i in kwargs.keys()}

    # Determine the general uncertainty propagation formula
    func_uncertainty = sqrt(sum([partials[i]**2 * uncertainties[f'δ{i}']**2 for i in partials]))

    # Evaluate the uncertainty with the given kwargs
    eval_uncertainty = func_uncertainty
    for i in kwargs.keys():
      eval_uncertainty = eval_uncertainty.subs(symbols[i], float(kwargs[i].sample.value))
      eval_uncertainty = eval_uncertainty.subs(uncertainties[f'δ{i}'], float(kwargs[i].uncertainty.value))
    eval_uncertainty = SigFig(str(eval_uncertainty.evalf()), decimals=eval_func.decimals)

    # Return the Measurement object with the function applied
    # If the function is log, exp, or trig, units will be dimensionless.
    # Otherwise, units will need to be determined based on the units of the input.
    # Check if the function is log, exp, or trig
    if func.func.__name__ not in ['log', 'exp', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']:
      # TODO: Derive the units of the function
      # For example if the function is f(x) = 2x, then the units of f(x) are the units of x.
      # If the function is f(x) = 1/x, then the units of f(x) are the inverse of the units of x.
      pass
    return Measurement(eval_func, uncertainty=eval_uncertainty, units=units)
  
  def __str__(self):
    """
    Returns a string representation of the Measurement object.

    :return: A string representation of the Measurement object.
    :rtype: str
    """
    return str(self.sample) + (f' +/- {self.uncertainty}' + ('%' if self.uncertaintyPercent else '') if isinstance(self.uncertainty, SigFig) else '') + (f' {Measurement.formatUnits(self.nUnits, self.dUnits)}' if self.units is not None else '')

  def __repr__(self):
    """
    Returns a string representation of the Measurement object.

    :return: A string representation of the Measurement object.
    :rtype: str
    """
    return str(self)

  def multUnits(nUnits1, dUnits1, nUnits2, dUnits2):
    """
    Multiplies two sets of units.

    :param nUnits1: The numerator units of the first set.
    :type nUnits1: list
    :param dUnits1: The denominator units of the first set.
    :type dUnits1: list
    :param nUnits2: The numerator units of the second set.
    :type nUnits2: list
    :param dUnits2: The denominator units of the second set.
    :type dUnits2: list
    :return: The multiplied units.
    :rtype: tuple
    """
    nUnits = nUnits1 + nUnits2
    dUnits = dUnits1 + dUnits2
    newNUnits = nUnits
    newDUnits = dUnits
    for i in nUnits:
      if i in newDUnits:
        newNUnits.remove(i)
        newDUnits.remove(i)
    return (sorted(newNUnits), sorted(newDUnits))

  def formatUnits(nUnits, dUnits):
    """
    Formats a set of units into a string.

    :param nUnits: The numerator units.
    :type nUnits: list
    :param dUnits: The denominator units.
    :type dUnits: list
    :return: The formatted units.
    :rtype: str
    """
    combinedNUnits = sorted([i if nUnits.count(i) == 1 else f'{i}^{nUnits.count(i)}' for i in set(nUnits)])
    combinedDUnits = sorted([i if dUnits.count(i) == 1 else f'{i}^{dUnits.count(i)}' for i in set(dUnits)])
    nUnitsStr = '1' if not nUnits else '*'.join(combinedNUnits)
    dUnitsStr = '' if not dUnits else '*'.join(combinedDUnits)
    if len(combinedNUnits) > 1:
      nUnitsStr = '(' + nUnitsStr + ')'
    if len(combinedDUnits) > 1:
      dUnitsStr = '(' + dUnitsStr + ')'
    return None if nUnitsStr == '1' and dUnitsStr == '' else nUnitsStr + (f'/{dUnitsStr}' if dUnitsStr else '')

  def __eq__(self, other):
    """
    Returns True if the two Measurement objects are equal.

    :param other: The Measurement object to compare.
    :type other: Measurement
    :returns: True if the two Measurement objects are equal.
    :rtype: bool
    """
    return self.sample == other.sample

  def __lt__(self, other):
    """
    Returns True if the first Measurement object is less than the second.

    :param other: The Measurement object to compare.
    :type other: Measurement
    :returns: True if the first Measurement object is less than the second.
    :rtype: bool
    """
    return self.sample < other.sample

  def __gt__(self, other):
    """
    Returns True if the first Measurement object is greater than the second.

    :param other: The Measurement object to compare.
    :type other: Measurement
    :returns: True if the first Measurement object is greater than the second.
    :rtype: bool
    """
    return self.sample > other.sample

  def __le__(self, other):
    """
    Returns True if the first Measurement object is less than or equal to the second.

    :param other: The Measurement object to compare.
    :type other: Measurement
    :returns: True if the first Measurement object is less than or equal to the second.
    :rtype: bool
    """
    return self < other or self == other

  def __ge__(self, other):
    """
    Returns True if the first Measurement object is greater than or equal to the second.

    :param other: The Measurement object to compare.
    :type other: Measurement
    :returns: True if the first Measurement object is greater than or equal to the second.
    :rtype: bool
    """
    return self > other or self == other
  
  def __neg__(self):
    """
    Returns the negation of the Measurement object.

    :returns: The negation of the Measurement object.
    :rtype: Measurement
    """
    neg = self.deepCopy()
    neg.sample = -self.sample
    return neg

  def __add__(self, other):
    """
    Returns the sum of the two Measurement objects.

    :param other: The Measurement object to add.
    :type other: Measurement
    :returns: The sum of the two Measurement objects.
    :rtype: Measurement
    """
    if self.nUnits != other.nUnits or self.dUnits != other.dUnits:
      raise Exception(f'Measurement Error: Cannot add {self} and {other} with different units.')
    uSum = SigFig('0', constant=True)
    uncertainties = [Measurement.absolute(i).uncertainty for i in [self, other] if i.uncertainty is not None]
    for u in uncertainties:
      uSum += u
    return Measurement(self.sample + other.sample, uncertainty=uSum if uncertainties else None, units=self.units)
  
  def __radd__(self, other):
    """
    Returns the sum of the two Measurement objects.

    :param other: The Measurement object to add to.
    :type other: Measurement
    :returns: The sum of the two Measurement objects.
    :rtype: Measurement
    """
    return self + other
  
  def __sub__(self, other):
    """
    Returns the difference of the two Measurement objects.

    :param other: The Measurement object to subtract.
    :type other: Measurement
    :returns: The difference of the two Measurement objects.
    :rtype: Measurement
    """
    return -other + self

  def __rsub__(self, other):
    """
    Returns the difference of the two Measurement objects.

    :param other: The Measurement object to subtract from.
    :type other: Measurement
    :returns: The difference of the two Measurement objects.
    :rtype: Measurement
    """
    return -self + other

  def __mul__(self, other):
    """
    Returns the product of the two Measurement objects.

    :param other: The Measurement object to multiply by.
    :type other: Measurement
    :returns: The product of the two Measurement objects.
    :rtype: Measurement
    """
    if isinstance(other, float) or isinstance(other, int):
      other = Measurement.fromFloat(other)
    uSum = SigFig('0', constant=True)
    uncertainties = [Measurement.percent(i).uncertainty for i in [self, other] if i.uncertainty is not None]
    for u in uncertainties:
      uSum += u
    nUnits, dUnits = Measurement.multUnits(self.nUnits, self.dUnits, other.nUnits, other.dUnits)
    return Measurement(self.sample * other.sample, uncertainty=uSum if uncertainties else None, uncertaintyPercent=True, units=Measurement.formatUnits(nUnits, dUnits))
  
  def __rmul__(self, other):
    """
    Returns the product of the two Measurement objects.

    :param other: The Measurement object to multiply by.
    :type other: Measurement
    :returns: The product of the two Measurement objects.
    :rtype: Measurement
    """
    return self * other

  def __truediv__(self, other):
    """
    Returns the quotient of the two Measurement objects.

    :param other: The Measurement object to divide by.
    :type other: Measurement
    :returns: The quotient of the two Measurement objects.
    :rtype: Measurement
    """
    if isinstance(other, float) or isinstance(other, int):
      other = Measurement.fromFloat(other)
    uSum = SigFig('0', constant=True)
    uncertainties = [Measurement.percent(i).uncertainty for i in [self, other] if i.uncertainty is not None]
    for u in uncertainties:
      uSum += u
    nUnits, dUnits = Measurement.multUnits(self.nUnits, self.dUnits, other.dUnits, other.nUnits)
    return Measurement(self.sample / other.sample, uncertainty=uSum if uncertainties else None, uncertaintyPercent=True, units=Measurement.formatUnits(nUnits, dUnits))
    
  def __rtruediv__(self, other):
    """
    Returns the quotient of the two Measurement objects.

    :param other: The Measurement object to divide by.
    :type other: Measurement
    :returns: The quotient of the two Measurement objects.
    :rtype: Measurement
    """
    if isinstance(other, float) or isinstance(other, int):
      other = Measurement.fromFloat(other)
    return other / self

  def __pow__(self, integer):
    """
    Returns the Measurement object raised to the given integer power.

    :param integer: The integer power to raise the Measurement object to.
    :type integer: int
    :returns: The Measurement object raised to the given integer power.
    :rtype: Measurement
    """
    product = Measurement('1', precision=float('inf'))
    for i in range(integer):
      product *= self
    return product

  def sum(measurements):
    """
    Returns the sum of the given list of Measurement objects.

    :param measurements: The list of Measurement objects.
    :type measurements: list
    :returns: The sum of the given list of Measurement objects.
    :rtype: Measurement
    """
    if not measurements:
      return Measurement.fromStr('0c')
    s = measurements[0]
    for i in measurements[1:]:
      s += i
    return s

  def max(measurements):
    """
    Returns the maximum of the given list of Measurement objects.

    :param measurements: The list of Measurement objects.
    :type measurements: list
    :returns: The maximum of the given list of Measurement objects.
    :rtype: Measurement
    """
    m = measurements[0]
    for i in measurements[1:]:
      if m < i:
        m = i
    return m

  def min(measurements):
    """
    Returns the minimum of the given list of Measurement objects.

    :param measurements: The list of Measurement objects.
    :type measurements: list
    :returns: The minimum of the given list of Measurement objects.
    :rtype: Measurement
    """
    m = measurements[0]
    for i in measurements[1:]:
      if m > i:
        m = i
    return m

  def average(measurements):
    """
    Returns the average of the given list of Measurement objects. Uses (max - min) / (2 * sqrt(n)) as the uncertainty.

    :param measurements: The list of Measurement objects.
    :type measurements: list
    :returns: The average of the given list of Measurement objects.
    :rtype: Measurement
    """
    avg_sample = Measurement.sum(measurements) / len(measurements)
    avg_uncertainty = (Measurement.max(measurements) - Measurement.min(measurements)).sample / (2 * math.sqrt(len(measurements)))
    return Measurement(avg_sample.sample, uncertainty=avg_uncertainty.value, units=avg_sample.units)

  def convert(sample, uncertainty=None, uncertaintyPercent=False, units='', analog=False, digital=False, constant=False, u=None, up=False, a=False, d=False, un='', decimals=None):
    """
    Returns a Measurement object with the given sample, uncertainty, and units.
    
    :param sample: The sample of the Measurement object.
    :type sample: float or str
    :param uncertainty: The uncertainty of the Measurement object.
    :type uncertainty: float or str
    :param uncertaintyPercent: Whether the uncertainty is a percent.
    :type uncertaintyPercent: bool
    :param units: The units of the Measurement object.
    :type units: str
    :param analog: Whether the Measurement object is analog.
    :type analog: bool
    :param digital: Whether the Measurement object is digital.
    :type digital: bool
    :param constant: Whether the Measurement object is constant.
    :type constant: bool
    :param u: The uncertainty of the Measurement object.
    :type u: float or str
    :param up: Whether the uncertainty is a percent.
    :type up: bool
    :param a: Whether the Measurement object is analog.
    :type a: bool
    :param d: Whether the Measurement object is digital.
    :type d: bool
    :param un: The units of the Measurement object.
    :type un: str
    :param decimals: The number of decimals to round to.
    :type decimals: int
    """
    if u is not None:
      uncertainty = u
    if up:
      uncertaintyPercent = up
    if a:
      analog = a
    if d:
      digital = d
    if un:
      units = un

    return Measurement(SigFig(str(sample), decimals=-decimals if decimals is not None else None), uncertaintyPercent=uncertaintyPercent, uncertainty=str(uncertainty) if uncertainty is not None else None, precision=float('inf') if constant else None, units=units, analog=analog, digital=digital)
  
  def importColumn(column, uncertaintyColumn=None, df=None, **kwargs):
    """
    Convert a numeric Pandas DataFrame column to Measurement objects.
    
    :param column: The numeric Pandas DataFrame column.
    :type column: pandas.core.series.Series
    :param kwargs: Keyword arguments to pass to Measurement.convert.
    :type kwargs: dict
    """
    if uncertaintyColumn is None:
      return column.apply(Measurement.convert, **kwargs)
    else:
      return df.apply(lambda x: Measurement.convert(x[column.name], u=x[uncertaintyColumn.name], **kwargs), axis=1)

  def exportColumn(savedf, column, addUncertainty=True, asPercent=True):
    """
    Convert a Measurement Pandas DataFrame column to numeric values.

    :param savedf: The Pandas DataFrame to save to.
    :type savedf: pandas.core.frame.DataFrame
    :param column: The Measurement Pandas DataFrame column.
    :type column: pandas.core.series.Series
    :param addUncertainty: Whether to add the uncertainty to the DataFrame.
    :type addUncertainty: bool
    :param asPercent: Whether to add the uncertainty as a percent.
    :type asPercent: bool
    """
    savedf[column.name] = column.apply(lambda x: x.sample)
    if addUncertainty:
      label, units = (' ('.join(column.name.split(' (')[:-1]), ' (' + column.name.split(' (')[-1]) if ' (' in column.name else (column.name, '')
      if asPercent:
        savedf.insert(savedf.columns.get_loc(column.name) + 1, f'{label} Percent Uncertainty (%)', column.apply(lambda x: x.percent().uncertainty))
      else:
        savedf.insert(savedf.columns.get_loc(column.name) + 1, f'{label} Absolute Uncertainty{units}', column.apply(lambda x: x.absolute().uncertainty))
