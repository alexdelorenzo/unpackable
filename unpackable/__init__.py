from __future__ import annotations
from typing import Iterator, Any, Final, Iterable
from functools import partial


PRIVATE: Final[str] = '_'
ITER: Final[str] = '__iter__'


class Unpackable:
  def __iter__(self) -> Iterator[Any]:
    if hasattr(super(), ITER):
      yield from super().__iter__()

    yield from iter_vals(self)


def iter_vals(obj: Any) -> Iterable[Any]:
  attrs: set[str] = {
    *dir(obj),
    *obj.__dict__,
  }

  for attr in attrs:
    val = getattr(obj, attr)

    if is_val(attr, val):
      yield val


def unpack(obj: Any) -> Iterable[Any]:
  if hasattr(obj, ITER):
    yield from obj.__iter__()
    return

  yield from iter_vals(obj)


def is_val(name: str, obj: Any) -> bool:
  return not name.startswith(PRIVATE) \
    and not callable(obj)
