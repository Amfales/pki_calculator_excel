import asyncio
from asyncio.locks import Event
from collections import defaultdict as dd
from typing import Any

class DataManager():
  def __init__(self):
    self.data = {}
    self._data_events :dict[str,Event]= {}

  def register(self, var: str):
    self._data_events[var] = Event()

  async def block(self, vars: list[str]):
    if len(vars) != 0:
      await asyncio.gather(*[self._data_events[var].wait() for var in vars])
    return {var: self.data[var] for var in vars}

  def finalize(self, var: str, val: Any):
    self.data[var] = val
    self._data_events[var].set()

