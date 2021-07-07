from __future__ import annotations
from typing import Any, Callable, Optional, Sized, \
  Iterable
from types import DynamicClassAttribute
from inspect import isclass, getmro

from .types import HasIter, HasDict, Final, \
  UnorderedAttributes


DICT: Final[str] = '__dict__'
SLOTS: Final[str] = '__slots__'


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


def gen_keys(
  obj: Any,
) -> Iterable[Key]:
  """Return all members of an obj as (name, value) pairs sorted by name.
  Optionally, only return members that satisfy a given predicate."""
  if hasattr(obj, DICT) and vars(obj):
    yield from obj.__dict__.keys()

  elif hasattr(obj, SLOTS):
    yield from obj.__slots__

  else:
    name = type(obj).__name__
    raise UnorderedAttributes(f"{name} attribute order can't be determined.")
    # yield from dir(obj)

  # Add any DynamicClassAttributes to the list of names if obj is a class;
  # this may result in duplicate entries if, for example, a virtual
  # attribute with the same name as a DynamicClassAttribute exists
  try:
    for base in obj.__bases__:
      for key, val in base.__dict__.items():
        if isinstance(key, DynamicClassAttribute):
          yield key

  except AttributeError:
      pass


def gen_results(
  obj: Any,
  predicate: Optional[Predicate] = None,
) -> Iterable[KeyVal]:
  mro: tuple[type] = ()

  if isclass(obj):
    mro = (obj,) + getmro(obj)

  processed: set[Key] = set()

  for key in gen_keys(obj):
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
      yield key, value

    processed.add(key)


def get_members(
  obj: Any,
  predicate: Optional[Predicate] = None,
  sort: Optional[Sort] = None,
) -> KeyVals:
  """Return all members of an obj as (name, value) pairs sorted by name.
  Optionally, only return members that satisfy a given predicate."""
  results_gen = gen_results(obj, predicate)
  results = list(results_gen)

  if callable(sort):
    results.sort(key=sort)

  return results
