import toml

from plugins.plugin_manager import PluginManager
from plugins.plugins.income_handler import IncomePluginFactory
from plugins.plugins.xlsx_plugin_factory import XLSXPluginFactory
from pki_manager.pki import PKI, LiteralPKI, SumPKI, MinusPKI, TimesPKI, DividePKI
from plugins.plugins.dependents.base_dependent import DependentPluginFactory


base_kpis = [
  ('revenue', [], 5),
  ('cost_of_sales', [], 6),
  ('distribution_costs',[], 9),
  ('administrative_expenses', [], 10),
  ('exceptional_administrative_expenses', [], 11),
  ('profit_on_disposal_of_subsidiary_undertaking', [],15),
  ('loss_on_disposal_of_joint_venture_investment', [], 17),
  ('provision_against_carrying_value_of_fixed_asset_investments', [], 19),
  ('interest_receivable', [], 23),
  ('interest_payable', [], 24)
]

def calc_gross_profit(data: dict[str, PKI]) -> PKI:
  return MinusPKI(
    data['revenue'],
    data['cost_of_sales']
  )

def calc_operating_profit(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['gross_profit'],
    data['distribution_costs'],
    data['administrative_expenses'],
    data['exceptional_administrative_expenses']
  )

def calc_earnings_before_interest_and_taxes(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['operating_profit'],
    data['profit_on_disposal_of_subsidiary_undertaking'],
    data['loss_on_disposal_of_joint_venture_investment'],
    data['provision_against_carrying_value_of_fixed_asset_investments']
  )

def calc_net_profit(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['earnings_before_interest_and_taxes'],
    data['interest_receivable'],
    data['interest_payable'],
    data['taxation']
  )

def calc_current_assets(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['cash'],
    data['current_assets_accounts_receivable'],
    data['inventory_stocks']
  )

def calc_long_term_assets(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['long_term_assets_accounts_receivable'],
    data['tangible_fixed_assets'],
    data['intangible_fixed_assets'],
    data['deferred_tax_assets']
  )

def calc_total_assets(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['current_assets'],
    data['long_term_assets']
  )

def calc_current_liabilities(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['accounts_payable'],
    data['current_loans_payable'],
    data['provisions_for_liabilities']
  )

def calc_long_term_liabilities(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['long_term_loans_payable'],
    data['employee_benefits']
  )

def calc_total_liabilities(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['current_liabilities'],
    data['long_term_liabilities']
  )

def calc_total_equity(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['capital_stock'],
    data['premium_on_capital_stock'],
    data['retained_earnings'],
    data['prior_year_adjustment'],
    TimesPKI(
      data['net_profit'],
      LiteralPKI(-1)
    )
  )

def calc_total_liabilities_and_equity(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['total_liabilities'],
    data['total_equity']
  )

def calc_variance(data: dict[str, PKI]) -> PKI:
  return SumPKI(
    data['total_assets'],
    data['total_liabilities_and_equity']
  )


def register_plugins(pm: PluginManager, filename: str):
  settings = toml.load(filename)
  for type in settings['sheets']:
    basic_kpis = settings['sheets'][type]['basic_kpis']
    basic_plugin_factory = XLSXPluginFactory(settings['num_years'], settings['row_base'], settings['col_base'])
    for basic_kpi in basic_kpis:
      pm.register(
        basic_plugin_factory.create_plugin(
          settings['sheets'][type]['sheetname'],
          basic_kpi['name'],
          basic_kpi['base_row']
        )
      )
      #pm.register(ipf.create_plugin(basic_kpi['name'], [], basic_kpi['base_row']))
    
    dependent_kpis = settings['sheets'][type]['dependent_kpis']
    for dependent_kpi in dependent_kpis:
      try:
        func_name = f'calc_{dependent_kpi["name"]}'
        func = eval(func_name)
        pm.register(DependentPluginFactory.create_plugin(
          dependent_kpi['name'],
          dependent_kpi['dependencies'],
          func
        ))
      except:
        pass
""""
def register_plugins(pm: PluginManager):
  ipf = IncomePluginFactory(5)
  for items in base_kpis:
    pm.register(ipf.create_plugin(*items))

  
  for items in dependent_plugin_data:
    pm.register(DependentPluginFactory.create_plugin(*items))
"""
  
