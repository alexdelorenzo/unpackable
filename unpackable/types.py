from __future__ import annotations
from dataclasses import Field
from typing import Iterator, Any

try:
  from typing import Protocol, runtime_checkable, Final

except ImportError:
  from typing_extensions import Protocol, runtime_checkable, \
    Final


PRIVATE: Final[str] = '_'
DICT: Final[str] = '__dict__'


@runtime_checkable
class HasIter(Protocol):
  def __iter__(self) -> Iterator[Any]:
    ...


@runtime_checkable
class Dataclass(Protocol):
  def __dataclass_fields__(self) -> dict[str, Field]:
    ...


class UnpackableException(Exception):
  pass


class UnorderedAttributes(UnpackableException, TypeError):
  @classmethod
  def from_obj(cls: type, obj: Any) -> UnorderedAttributes:
    msg = f"{type(obj).__name__} isn't iterable and can't be unpacked."
    return cls(msg)


def has_dict(obj: Any) -> bool:
  return hasattr(obj, DICT)


def has_iter(obj: Any) -> bool:
  return isinstance(obj, HasIter)


def is_attr(name: str, obj: Any) -> bool:
  return not name.startswith(PRIVATE) \
    and not callable(obj)
