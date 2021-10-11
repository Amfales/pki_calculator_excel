import abc
import typing

import openpyxl

from plugins.data_manager import DataManager

class AbstractBasePlugin(abc.ABC):
  @property
  @abc.abstractmethod
  def datapoint_name(self) -> str:
    pass

  @property
  @abc.abstractmethod
  def dependencies(self) -> list[str]:
    pass

  def start(self, data_manager: DataManager):
    data_manager.register(self.datapoint_name)
    async def awaiter(workbook: openpyxl.Workbook):
      data = await data_manager.block(self.dependencies)
      val = self.do_work(workbook, data)
      data_manager.finalize(self.datapoint_name, val)
    return awaiter


  @abc.abstractmethod
  def do_work(self, workbook: openpyxl.Workbook, data: dict[str, typing.Any]) -> typing.Any:
    pass

  