"""
  Novo gerente
"""
from texttable import Texttable

from Componentes.db_manager import db_mgr


class Controller:

  def __init__(self):
    db_mgr.create_dbs()
  
  def list_scenarios(self):
    scenarios = db_mgr.list_all_scenarios()

    if scenarios:
      table = Texttable()
      table.add_row(['Scenario Name', 'Scenario State'])

      for row in scenarios:
        table.add_row([ row[0], row[1] ])
      
      print( table.draw() )
    