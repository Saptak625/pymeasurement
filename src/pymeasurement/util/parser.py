from pymeasurement.util.typecheck import typecheck

class Parser:
  """A class to parse strings.

  :param string: The string to parse.
  :type string: str
  :raises TypeError: If string is not a string.
  """
  def __init__(self, string):
    """Parser Constructor
    """
    typecheck(string, str)
    self.string = string
  
  def readByCharacter(self, string, startSetup = None, endSetup = None, checks = None):
    """Read a string by character.

    :param string: The string to read.
    :type string: str
    :param startSetup: A function to run before reading the string.
    :type startSetup: function
    :param endSetup: A function to run after reading the string.
    :type endSetup: function
    :param checks: A function to run on each character.
    :type checks: function
    """
    if startSetup:
      startSetup()
    for i, char in enumerate(string):
      if checks:
        checks(i, char)
    if endSetup:
      endSetup()

  def splitString(self, string, checks = None):
    """Split a string.

	  :param string: The string to split.
    :type string: str
    :param checks: A function to run on each string.
    :type checks: function
	"""
    if checks:
      checks(string)
  
  def __str__(self):
    """Get the string representation of the parser.

    :returns: The string representation of the parser.
    :rtype: str
	"""
    return self.string

  def __repr__(self):
    """Get the string representation of the parser.
    
    :returns: The string representation of the parser.
    :rtype: str
	"""
    return str(self)