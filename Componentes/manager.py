"""
  Novo criador
"""

from Componentes.db_manager import db_mgr


class Manager:
  
  def __init__(self):
    db_mgr.create_dbs()
  
  def add_scenario(self, scenario_name):
    """
      Creates a new scenario and inserts into the db

      Args:
        scenario_name (str): Name of the scenario
    """
    if db_mgr.scenario_exists( scenario_name ):
      print( 'Scenario already exists' )
      
      return
    
    try:
      db_mgr.inset_scenario( scenario_name )
      print( f'Scenario {scenario_name} created' )
    except:
      print( 'Something went wrong.' )

  def delete_scenario(self, scenario_name):
    """
      Deletes a scenario from the db
      //TODO also delete containers within that scenario

      Args:
        scenario_name (str): Name of the scenario
    """

    if db_mgr.scenario_exists( scenario_name ):
      db_mgr.delete_scenario( scenario_name )
      print( f'Scenario {scenario_name} deleted.' )

      return
  
    print( 'Scenario not found.' )