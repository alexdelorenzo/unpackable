from __future__ import annotations
from typing import Final, Iterator, Iterable, Any, \
  Sequence


PRIVATE: Final[str] = '_'
ITER: Final[str] = '__iter__'
DICT: Final[str] = '__dict__'


class Unpackable:
  def __iter__(self) -> Iterator[Any]:
    if hasattr(super(), ITER):
      yield from super().__iter__()

    yield from iter_vals(self)


def iter_vals(obj: Any) -> Iterable[Any]:
  if not hasattr(obj, DICT):
    return

  for attr, val in obj.__dict__.items():
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
