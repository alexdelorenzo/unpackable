from __future__ import annotations
from typing import Iterator, Iterable, Any, \
  Sequence, Iterable
from inspect import stack
from dataclasses import is_dataclass, astuple
import logging

from .obj import get_members
from .types import HasIter, Final, \
  UnorderedAttributes, has_iter, has_dict, \
  is_attr


__all__: Final[list[str]] = [
  'Unpackable',
  'can_unpack',
  'unpack',
  'iter_vals',
]


class Unpackable:
  def __iter__(self) -> Iterator[Any]:
    if has_iter(super()):
      yield from super().__iter__()
      return

    else:
      yield from unpack_obj(self, from_cls=True)
      return


def iter_vals(obj: Any) -> Iterable[Any]:
  attrs_vals = get_members(obj)

  for attr, val in attrs_vals:
    if is_attr(attr, val):
      yield val


def unpack_obj(obj: Any, from_cls: bool = False) -> Iterable[Any]:
  if is_dataclass(obj):
    yield from astuple(obj)
    return

  # try the built-in iter()
  try:
    if has_dict(obj):
      yield from iter_vals(obj)
      return

    yield from iter(obj)

  except TypeError as e:
    pass

  if from_cls:
    _, _, calling_frame, *_ = stack()

  else:
    _, _, _, calling_frame, *_ = stack()
    print(calling_frame)

  assignment_line, *_ = calling_frame.code_context

  if '=' not in assignment_line:
    raise UnorderedAttributes.from_obj(obj)

  names, *_ = assignment_line.split('=')
  names = (name.strip() for name in names.split(','))

  for name in names:
    yield getattr(obj, name)


def unpack_gen(obj: Any) -> Iterable[Any]:
  if has_iter(obj):
    yield from obj.__iter__()

  else:
    yield from unpack_obj(obj)


def unpack(obj: Any) -> Iterable[Any]:
  if can_unpack(obj):
    return unpack_gen(obj)

  raise UnorderedAttributes.from_obj(obj)


def can_unpack(obj: Any) -> bool:
  if has_dict(obj) or has_iter(obj):
    return True

  try:
    iter(obj)
    return True

  except TypeError:
    return False

  return False
