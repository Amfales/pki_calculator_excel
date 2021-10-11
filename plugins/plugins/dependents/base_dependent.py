from typing import Any, Callable

import openpyxl

from plugins.base_plugin import AbstractBasePlugin
from plugins.data_manager import DataManager
from pki_manager.pki import LiteralPKI, PKI

class DependentPluginFactory():
  @classmethod
  def create_plugin(cls, data_name: str, dependencies: list[str], evaluator: Callable[[dict[str, PKI]], PKI]):
    assert len(dependencies) > 0
    class DependentPlugin(AbstractBasePlugin):
      @property
      def datapoint_name(self) -> str:
          return data_name

      @property
      def dependencies(self) -> list[str]:
          return dependencies

      def do_work(self, workbook: openpyxl.Workbook, data: dict[str, Any]) -> Any:
        to_ret = {}
        first_dep_dates = data[dependencies[0]].keys()
        for date in first_dep_dates:
          date_data = {dep: data[dep][date] for dep in dependencies}
          to_ret[date] = evaluator(date_data)
        return to_ret

      def __repr__(self):
        return f'<DependentPlugin name={data_name}>'

      def __str__(self):
        return f'<DependentPlugin name={data_name}>'
    return DependentPlugin()