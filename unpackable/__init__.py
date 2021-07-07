from __future__ import annotations
from typing import Iterator, Iterable, Any, \
  Sequence, Iterable
from dataclasses import is_dataclass, astuple

from .obj import get_members
from .types import HasIter, HasDict, Final


__all__: Final[list[str]] = [
  'Unpackable',
  'can_unpack',
  'unpack',
  'iter_vals',
]


PRIVATE: Final[str] = '_'
DICT: Final[str] = '__dict__'


class Unpackable:
  def __iter__(self) -> Iterator[Any]:
    return iter(self.__unpack())

  def __unpack(self) -> Iterable[Any]:
    if has_iter(super()):
      yield from super().__iter__()

    else:
      yield from unpack_obj(self)


def iter_vals(obj: Any) -> Iterable[Any]:
  attrs_vals = get_members(obj)

  for attr, val in attrs_vals:
    if is_val(attr, val):
      yield val


def unpack_obj(obj: Any) -> Iterable[Any]:
  if is_dataclass(obj):
    yield from astuple(obj)
    return

  elif has_dict(obj):
    yield from iter_vals(obj)
    return

  # try the built-in iter()
  try:
    yield from iter(obj)

  except TypeError as e:
    msg = f"{type(obj).__name__} isn't iterable and can't be unpacked."
    raise TypeError(msg) from e


def unpack(obj: Any) -> Iterable[Any]:
  if has_iter(obj):
    yield from obj.__iter__()

  else:
    yield from unpack_obj(obj)


def is_val(name: str, obj: Any) -> bool:
  return not name.startswith(PRIVATE) \
    and not callable(obj)


def has_dict(obj: Any) -> bool:
  return hasattr(obj, DICT)


def has_iter(obj: Any) -> bool:
  return isinstance(obj, HasIter)


def can_unpack(obj: Any) -> bool:
  if has_dict(obj) or has_iter(obj):
    return True

  try:
    iter(obj)
    return True

  except TypeError:
    return False

  return False
