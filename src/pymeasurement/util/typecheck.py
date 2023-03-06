def typecheck(check, *args):
  """Check if the type of check is in args.

  :param check: The object to check the type of.
  :type check: object
  :param args: The types to check against.
  :type args: Iterable<type>
  :raises TypeError: If the type of check is not in args.
  """
  if not (any([isinstance(check, a) for a in args if a is not None]) or (None in args and check is None)):
    raise TypeError(f'Check type "{type(check)}" did not match type "{args}."')

def typecheckArray(checkArray, *args, dimension = 1):
  """Check if the type of each object in checkArray is in args.

  :param checkArray: The array of objects to check the type of.
  :type checkArray: Iterable<object>
  :param args: The types to check against.
  :type args: Iterable<type>
  :param dimension: The dimension of the array to check.
  :type dimension: int
  :raises TypeError: If the type of any object in checkArray is not in args.
  """
  for check in checkArray:
    if dimension == 1:
      typecheck(check, args)
    else:
      typecheckArray(check, args, dimension = dimension - 1)