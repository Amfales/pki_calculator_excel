import typing

import openpyxl

from .data_manager import DataManager

class PluginProtocol(typing.Protocol):
  def start(self, data_manager: DataManager) -> typing.Callable[[openpyxl.Workbook], typing.Awaitable[None]]:
    pass