import abc
from functools import reduce
from typing import Protocol, Any

class PKI(Protocol):
  def get_value(self) -> Any:
    pass


class LiteralPKI():
  def __init__(self, val):
    self.val = val

  def get_value(self):
    return self.val

  def __repr__(self):
    return str(self)

  def __str__(self):
    return f'<LiteralPKI value={self.val}>'

class SumPKI():
  def __init__(self, *vals: PKI):
    self.vals = vals

  def get_value(self):
    return sum([x.get_value() for x in self.vals])

  def __repr__(self):
    return str(self)

  def __str__(self):
    return f'<SumPKI value={self.get_value()}>'

class MinusPKI():
  def __init__(self, val1: PKI, val2: PKI):
    self.val1 = val1
    self.val2 = val2
    if (type(self.val1) == type('')):
      print('something bad', self.val1)

  def get_value(self):
    return self.val1.get_value() - self.val2.get_value()

  def __repr__(self):
    return str(self)

  def __str__(self):
    return f'<MinusPKI value={self.get_value()}>'

class TimesPKI():
  def __init__(self, *vals: PKI):
    self.vals = vals

  def get_value(self):
    return reduce(lambda a,b: a.get_value()*b.get_value(), self.vals)

  def __repr__(self):
    return str(self)

  def __str__(self):
    return f'<TimesPKI value={self.get_value()}>'

class DividePKI():
  def __init__(self, val1: PKI, val2: PKI):
    self.val1 = val1
    self.val2 = val2

  def get_value(self):
    return self.val1.get_value() / self.val2.get_value()

  def __repr__(self):
    return str(self)

  def __str__(self):
    return f'<DividePKI value={self.get_value()}>'