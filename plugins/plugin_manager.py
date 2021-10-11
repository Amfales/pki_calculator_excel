import asyncio
import typing

import openpyxl

from plugins.data_manager import DataManager
from .plugin_protocol import PluginProtocol

class PluginManager():
  plugins: list[PluginProtocol] = []
  data_manager = DataManager()

  def register(self, plugin: PluginProtocol):
    self.plugins.append(plugin)

  def run(self, workbook: openpyxl.Workbook):
    async def handle_tasks():
      all_tasks = [task.start(self.data_manager) for task in self.plugins]
      tasks = list(map(lambda x: x(workbook), all_tasks))
      await asyncio.gather(*tasks)
    asyncio.run(handle_tasks())