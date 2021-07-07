from __future__ import annotations
from dataclasses import Field
from typing import Iterator

try:
  from typing import Protocol, runtime_checkable, Final

except ImportError:
  from typing_extensions import Protocol, runtime_checkable, Final


@runtime_checkable
class HasDict(Protocol):
  def __dict__(self) -> dict[str, Any]:
    ...


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


class AttributeOrderAmbiguous(UnpackableException):
  pass
