from pymeasurement.util.parser import Parser
from pymeasurement.util.chem.element import Element
from pymeasurement.measurement import Measurement
import re

class Compound(Parser):
  """A class to represent a chemical compound.

  :param string: The string to parse.
  :type string: str
  """

  latexPrint = False # Whether to print the compound in latex format.

  def setLatexPrint(value):
    """Set whether to print the compound in latex format.

    :param value: Whether to print the compound in latex format.
    :type value: bool
    """
    Element.setLatexPrint(value)
    Compound.latexPrint = value
  
  def __init__(self, string):
    """Compound Constructor
    """
    super().__init__(string)
    self.composition = {}
    self.element = ""
    self.number = ""
    self.parenthesesOn = False
    self.parentheses = ')'
    self.subString = ""
    self.compoundString = self.string
    self.stateString = ""
    self.splitString(self.string, checks = self.split)
    for i in range(len(self.compoundString)):
      if not self.compoundString[i].isdigit():
        self.compoundString = self.compoundString[i:].strip()
        break
    self.readByCharacter(self.compoundString, checks = self.checks, endSetup = self.save)
    self.mass = Measurement.sum([e.mass * Measurement.fromFloat(self.composition[e]) for e in self.composition])

  def split(self, string):
    """Split the string into a compound string and a state string.

    :param string: The string to split.
    :type string: str
    """
    if '(s)' in string or '(l)' in string or '(g)' in string or '(aq)' in string:
      if '(s)' in string:
        self.stateString = '(s)'
      elif '(l)' in string:
        self.stateString = '(l)'
      elif '(g)' in string:
        self.stateString = '(g)'
      else:
        self.stateString = '(aq)'
      self.compoundString = self.string.replace(self.stateString, '').strip()
  
  def checks(self, i, char):
    """Check the character.

    :param i: The index of the character.
    :type i: int
    :param char: The character to check.
    :type char: str
    """
    if char.isalpha():
      if self.parenthesesOn:
          self.subString += char
      else:
        if char.isupper():
          self.save()
          self.element += char
        else:
          self.element += char
    elif char.isdigit():
      if self.parenthesesOn:
        self.subString += char
      else:
        self.number += char
    else:
      if char == '(' or char == '[':
        if not self.parenthesesOn:
          self.save()
          self.parenthesesOn = True
          self.parentheses = ')' if char == '(' else ']'
        else:
          self.subString += char
      elif char == ')' or char == ']':
        if char == self.parentheses:
          self.parenthesesOn = False
        else:
          self.subString += char
      else:
        raise Exception(f"Compound Parser Exception: Unknown character '{char}'")

  def saveElement(self, element, number, multiple = 1):
    """Save the element to the composition.

    :param element: The element to save.
    :type element: str
    :param number: The number of the element.
    :type number: str
    :param multiple: The multiple of the element.
    :type multiple: int
    """
    if Element(element) not in self.composition:
      self.composition[Element(element)] = (int(number) if number else 1) * multiple
    else:
      self.composition[Element(element)] += (int(number) if number else 1) * multiple

  def saveSubcompound(self):
    """Save subcompound to the composition.
    """
    subCompound = Compound(self.subString)
    for element in subCompound.composition:
      self.saveElement(element.string, self.number, multiple = subCompound.composition[element])

  def save(self):
    """Save the element or subcompound to the composition.
    """
    if self.element or self.subString:
      if self.element:
        self.saveElement(self.element, self.number)
      if self.subString:
        self.saveSubcompound()
    self.element = ""
    self.number = ""
    self.subString = ""

  def __str__(self, textOverride = False):
    """Get the string representation of the compound.

    :param textOverride: Whether to override the latex print setting.
    :type textOverride: bool
    :return: The string representation of the compound.
    :rtype: str
    """
    if Compound.latexPrint and not textOverride:
      allCoefficients = re.findall("\d+", self.compoundString)
      finalString = ''
      currentIndex = 0
      for i in allCoefficients:
        ind = self.compoundString[currentIndex:].index(i)
        finalString += self.compoundString[currentIndex:currentIndex + ind]+f'_{{{i}}}'
        currentIndex = currentIndex + ind + len(i)
      if currentIndex < len(self.compoundString):
        finalString += self.compoundString[currentIndex:]
      return finalString + (self.stateString if self.stateString else '')
    return self.compoundString + (self.stateString if self.stateString else '')

  def __eq__(self, other):
    """Check if the compound is equal to another compound.
    
    :param other: The other compound to check.
    :type other: Compound
    :return: Whether the compounds are equal.
    :rtype: bool
    """
    return self.composition == other.composition

  def __ne__(self, other):
    """Check if the compound is not equal to another compound.
    
    :param other: The other compound to check.
    :type other: Compound
    :return: Whether the compounds are not equal.
    :rtype: bool
    """
    return self.composition != other.composition
  
  def massPercentComposition(self):
    """Get the mass percent composition of the compound.

    :return: The mass percent composition of the compound.
    :rtype: list
    """
    return [['Element', 'Mass']]+[[str(i), self.composition[i]*i.mass] for i in self.composition]

  def molePercentComposition(self):
    """Get the mole percent composition of the compound.

    :return: The mole percent composition of the compound.
    :rtype: list
    """
    return [['Element', 'Moles']]+[[str(i), self.composition[i]] for i in self.composition]