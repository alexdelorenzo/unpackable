from __future__ import annotations
from typing import Final, Iterator, Iterable, Any, \
  Sequence
from dataclasses import is_dataclass, astuple

from .obj import get_members


__all__: Final[list[str]] = [
  'Unpackable',
  'unpack',
  'iter_vals',
]


PRIVATE: Final[str] = '_'
ITER: Final[str] = '__iter__'
DICT: Final[str] = '__dict__'


class Unpackable:
  def __iter__(self) -> Iterator[Any]:
    if hasattr(super(), ITER):
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

  else:
    yield from iter_vals(obj)


def unpack(obj: Any) -> Iterable[Any]:
  if hasattr(obj, ITER):
    yield from obj.__iter__()

  else:
    yield from unpack_obj(obj)


def is_val(name: str, obj: Any) -> bool:
  return not name.startswith(PRIVATE) \
    and not callable(obj)
