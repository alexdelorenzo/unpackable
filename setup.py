from __future__ import annotations
from typing import Final
from setuptools import setup
from pathlib import Path


REQS: list[str] = Path('requirements.txt') \
  .read_text() \
  .splitlines()

REQS: Final = [
  line
  for line in REQS
  if line and not line.startswith('#')
]

NAME: str = 'unpackable'


setup(
  name=NAME,
  install_requires=REQS,
  packages=[NAME]
)
