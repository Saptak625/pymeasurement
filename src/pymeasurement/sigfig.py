from decimal import Decimal, Context

class SigFig:
  """A class for representing numbers with significant figures. SigFig objects are immutable. Internally, all numbers are stored as Decimal objects (fixed point numbers) for extra accuracy and precision. The central paradigm of this class is that the decimal value is the true value of the number, and the sigfigs and decimals are the precision of the number. The sigfigs and decimals are used to determine the precision of the number when it is printed.

  :param value: The value of the number as a string.
  :type value: str
  :param sigfigs: The number of significant figures to use when printing the number. If None, the number of significant figures will be automatically determined.
  :type sigfigs: int or None
  :param decimals: The number of decimal places to use when printing the number. If None, the number of decimal places will be automatically determined.
  :type decimals: int or None
  :param constant: If True, the number will be assumed to be perfectly accurate for all calculations. If False, the number will be assumed to have some precision that must be followed.
  :type constant: bool
  """
  def __init__(self, value, sigfigs=None, decimals=None, constant=False):
    """SigFig Constructor
    """
    self.value = value
    try:
      self.decimalValue = Decimal(value) #True Value of Decimal including extra calculation precision.
    except:
      raise Exception(f'Sig Fig Error: Could not convert "{self.value}" into sig fig.')
    sign, digits, exponent = self.decimalValue.as_tuple()
    self.sigfigs = len(digits)
    self.decimal = Decimal((sign, digits, exponent)) #Sig Fig Decimal Representation
    if constant:
      #Constants are assumed to be perfectly accurate for all calculations.
      self.sigfigs = float('inf')
      self.decimals = float('-inf')
    else:
      #Value has some precision that must be followed.
      #Automatic Override
      if '.' in self.value: #Decimal Value
        #Force override to maintain sig fig precision
        self.decimal = SigFig.changeSigFigs(value, self.sigfigs)
        self.decimals = exponent
      else:
        newSigfigs = len([int(i) for i in ''.join([str(i) for i in digits]).rstrip('0')])
        if newSigfigs != self.sigfigs and newSigfigs > 0:
          self.decimal = SigFig.changeSigFigs(value, newSigfigs)
          self.sigfigs = newSigfigs
        self.decimals = len(digits) - self.sigfigs
  
      #Manual override for sigfig or decimal precision.
      if sigfigs != None and sigfigs != float("inf"):
        self.sigfigs = sigfigs
        self.decimal = SigFig.changeSigFigs(value, sigfigs)
        sign, digits, exponent = self.decimal.as_tuple()
        if exponent < 0: #Decimal Value
          self.decimals = exponent
        else:
          self.decimals = len(digits) - self.sigfigs
      elif decimals != None:
        self.decimals = decimals
        self.decimal = self.decimal.quantize(Decimal(f"1E{self.decimals}"))
        sign, digits, exponent = self.decimal.as_tuple()
        self.sigfigs = len(digits) - self.decimals + exponent

  def changeSigFigs(value, sigfigs):
    """Changes the number of significant figures of a number.

    :param value: The value of the number as a string.
    :type value: str
    :param sigfigs: The number of significant figures to use.
    :type sigfigs: int
    :return: The number with the new number of significant figures.
    :rtype: Decimal
    """
    sign, digits, exponent = Context(prec=sigfigs).create_decimal(value).as_tuple()
    if len(digits) < sigfigs:
      missing = sigfigs - len(digits)
      digits = digits + (0,) * missing
      exponent -= missing
    return Decimal((sign, digits, exponent))

  def deepCopy(self):
    """Returns a deep copy of the SigFig object.
    
    :return: A deep copy of the SigFig object.
    :rtype: SigFig
    """
    new = SigFig('0')
    new.value = self.value
    new.decimalValue = self.decimalValue
    new.decimal = self.decimal
    new.sigfigs = self.sigfigs
    new.decimals = self.decimals
    return new
  
  def __str__(self):
    """Returns the string representation of the SigFig object.

    :return: The string representation of the SigFig object.
    :rtype: str
    """
    return str(self.decimal)

  def __repr__(self):
    """Returns the string representation of the SigFig object.

    :return: The string representation of the SigFig object.
    :rtype: str
    """
    return str(self)

  def __eq__(self, other):
    """Checks if the two SigFig objects are equal.

    :param other: The other SigFig object to compare to this one.
    :type other: SigFig
    :return: True if the two SigFig objects are equal.
    :rtype: bool
    """
    return self.decimal == other.decimal

  def __lt__(self, other):
    """Checks if the SigFig object is less than the other SigFig object.

    :param other: The other SigFig object to compare to this one.
    :type other: SigFig
    :return: True if the SigFig object is less than the other SigFig object.
    :rtype: bool
    """
    return self.decimal < other.decimal

  def __gt__(self, other):
    """Checks if the SigFig object is greater than the other SigFig object.

    :param other: The other SigFig object to compare to this one.
    :type other: SigFig
    :return: True if the SigFig object is greater than the other SigFig object.
    :rtype: bool
    """
    return self.decimal > other.decimal

  def __le__(self, other):
    """Checks if the SigFig object is less than or equal to the other SigFig object.

    :param other: The other SigFig object to compare to this one.
    :type other: SigFig
    :return: True if the SigFig object is less than or equal to the other SigFig object.
    :rtype: bool
    """
    return self < other or self == other

  def __ge__(self, other):
    """Checks if the SigFig object is greater than or equal to the other SigFig object.

    :param other: The other SigFig object to compare to this one.
    :type other: SigFig
    :return: True if the SigFig object is greater than or equal to the other SigFig object.
    :rtype: bool
    """
    return self > other or self == other
  
  def __neg__(self):
    """Returns the negative of the SigFig object.

    :return: The negative of the SigFig object.
    :rtype: SigFig
    """
    neg = self.deepCopy()
    neg.value = self.value.replace('-', '') if '-' in self.value else f'-{self.value}'
    neg.decimal = -self.decimal
    neg.decimalValue = -self.decimalValue
    return neg

  def __add__(self, other):
    """Returns the sum of the two SigFig objects as a new SigFig object, following the rules of significant figures.

    :param other: The other SigFig object to add to this one.
    :type other: SigFig
    :return: The sum of the two SigFig objects as a new SigFig object.
    :rtype: SigFig
    """
    if isinstance(other, float) or isinstance(other, int):
      other = SigFig(str(other), constant=True)
    decimals = max(self.decimals, other.decimals)
    return SigFig(str(self.decimalValue + other.decimalValue), decimals=decimals, constant=decimals == float('-inf'))
  
  def __radd__(self, other):
    """Returns the sum of the two SigFig objects as a new SigFig object, following the rules of significant figures.

    :param other: The other SigFig object to add to this one.
    :type other: SigFig
    :return: The sum of the two SigFig objects as a new SigFig object.
    :rtype: SigFig
    """
    return self + other
  
  def __sub__(self, other):
    """Returns the difference of the two SigFig objects as a new SigFig object, following the rules of significant figures.

    :param other: The other SigFig object to subtract from this one.
    :type other: SigFig
    :return: The difference of the two SigFig objects as a new SigFig object.
    :rtype: SigFig
    """
    if isinstance(other, float) or isinstance(other, int):
      other = SigFig(str(other), constant=True)
    return -other + self

  def __rsub__(self, other):
    """Returns the difference of the two SigFig objects as a new SigFig object, following the rules of significant figures.

    :param other: The other SigFig object to subtract from this one.
    :type other: SigFig
    :return: The difference of the two SigFig objects as a new SigFig object.
    :rtype: SigFig
    """
    return -self + other

  def __mul__(self, other):
    """Returns the product of the two SigFig objects as a new SigFig object, following the rules of significant figures.

    :param other: The other SigFig object to multiply by this one.
    :type other: SigFig
    :return: The product of the two SigFig objects as a new SigFig object.
    :rtype: SigFig
    """
    if isinstance(other, float) or isinstance(other, int):
      other = SigFig(str(other), constant=True)
    sigfigs = min(self.sigfigs, other.sigfigs)
    return SigFig(str(self.decimalValue * other.decimalValue), sigfigs=sigfigs, constant=sigfigs == float('inf'))

  def __rmul__(self, other):
    """Returns the product of the two SigFig objects as a new SigFig object, following the rules of significant figures.

    :param other: The other SigFig object to multiply by this one.
    :type other: SigFig
    :return: The product of the two SigFig objects as a new SigFig object.
    :rtype: SigFig
    """
    return self * other

  def __truediv__(self, other):
    """Returns the quotient of the two SigFig objects as a new SigFig object, following the rules of significant figures.

    :param other: The other SigFig object to divide by this one.
    :type other: SigFig
    :return: This SigFig object divided by the other SigFig object.
    :rtype: SigFig
    """
    if isinstance(other, float) or isinstance(other, int):
      other = SigFig(str(other), constant=True)
    sigfigs = min(self.sigfigs, other.sigfigs)
    return SigFig(str(self.decimalValue / other.decimalValue), sigfigs=sigfigs, constant=sigfigs == float('inf'))

  def __rtruediv__(self, other):
    """Returns the quotient of the two SigFig objects as a new SigFig object, following the rules of significant figures.

    :param other: The other SigFig object to divide by this one.
    :type other: SigFig
    :return: Other SigFig object divided by this one.
    :rtype: SigFig
    """
    return other / self

  def abs(self):
    """Returns the absolute value of the SigFig object.

    :return: The absolute value of the SigFig object.
    :rtype: SigFig
    """
    if self >= SigFig('0', constant=True):
      return self
    else:
      return -self