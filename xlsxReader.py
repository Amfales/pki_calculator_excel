import openpyxl

from plugins.plugin_manager import PluginManager
from plugins.plugins.income_handler import IncomePluginFactory
from plugin_builder import register_plugins

book = openpyxl.load_workbook('IDVERDE Limited.xlsx', data_only=True)

pm = PluginManager()

register_plugins(pm, 'settings.toml')

pm.run(book)

import datetime
date = datetime.datetime(2019,12,31)

keys = pm.data_manager.data.keys()


for pki in sorted(keys):
  print(f"{pki} -> {pm.data_manager.data[pki][date].get_value()}")