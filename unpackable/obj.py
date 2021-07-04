from typing import Any, Callable, Optional, Sized, Final
from inspect import isclass, getmro
from types import DynamicClassAttribute


DICT: Final[str] = '__dict__'


Key = str
Val = Any
KeyVal = tuple[Key, Val]
KeyVals = list[KeyVal]
Sort = Callable[[KeyVal], Sized]
Predicate = Callable[[Val], bool]


def sort_by_name(key_val: KeyVal) -> Key:
  key, _ = key_val
  return key


def sort_by_val(key_val: KeyVal) -> Val:
  _, val = key_val
  return val


def get_members(
  obj: Any,
  predicate: Optional[Predicate] = None,
  sort: Optional[Sort] = None,
) -> KeyVals:
  """Return all members of an obj as (name, value) pairs sorted by name.
  Optionally, only return members that satisfy a given predicate."""
  mro: tuple[type]

  if isclass(obj):
      mro = (obj,) + getmro(obj)
  else:
      mro = ()

  results: list[Key] = []
  processed: set[KeyVals] = set()
  names: list[Key]

  if hasattr(obj, DICT) and vars(obj):
    names = list(obj.__dict__.keys())

  else:
    names = dir(obj)

  # :dd any DynamicClassAttributes to the list of names if obj is a class;
  # this may result in duplicate entries if, for example, a virtual
  # attribute with the same name as a DynamicClassAttribute exists
  try:
    for base in obj.__bases__:
      for k, v in base.__dict__.items():
        if isinstance(v, DynamicClassAttribute):
          names.append(k)

  except AttributeError:
      pass

  for key in names:
    # First try to get the value via getattr.  Some descriptors don't
    # like calling their __get__ (see bug #1785), so fall back to
    # looking in the __dict__.
    try:
      value = getattr(obj, key)

      # handle the duplicate key
      if key in processed:
        raise AttributeError

    except AttributeError:
      for base in mro:
        if key in base.__dict__:
          value = base.__dict__[key]
          break
      else:
        # could be a (currently) missing slot member, or a buggy
        # __dir__; discard and move on
        continue

    if not predicate or predicate(value):
      results.append((key, value))

    processed.add(key)

  if callable(sort):
    results.sort(key=sort)

  return results
