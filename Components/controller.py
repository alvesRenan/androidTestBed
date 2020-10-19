"""
  Novo gerente
"""

import re

from texttable import Texttable

from Components.db_manager import db_mgr


class Controller:

  def __init__(self):
    db_mgr.create_dbs()
  
  def show_table(self, header, rows, align=None, width=80):
    table = Texttable(max_width=width)
    
    table.header( header )

    if align:
      table.set_cols_align( align )

    for row in rows:
      table.add_row([ value for value in row ])
    
    print( table.draw() )
  
  def list_scenarios(self):
    scenarios = db_mgr.list_all_scenarios()

    if scenarios:
      header = ['Scenario Name', 'Scenario State']
      self.show_table( header, scenarios )
  
  def list_scneario_containers(self, scenario):
    """
      Lists all containers of a scenario

      Args:
        scenario (str): name of the scenario to look for
    """
    containers = db_mgr.list_containers( scenario )

    header = ['Container Name', 'ADB Connection', 'Network/Speed', 'Memory', 'CPUS', 'State']
    align = ['l', 'c', 'c', 'c', 'c', 'c']

    self.show_table( header, containers, align=align, width=0 )
  
  def validate_container_name(self, container_name):
    """
      Checks if the container is valid or if the name is already in use

      Args:
        container_name (str): name to validate
      
      Returns:
        False if fails any of the checks or 
        True if name is valid
    """

    """Check if name is not empty, a single number o letter"""
    if re.match( '[a-zA-Z0-9][a-zA-Z0-9_.-]', container_name ) is None:
      print( 'Name not allowed!' )
      return False

    """Check if a container with that name already exists"""
    if db_mgr.container_exists( container_name ):
      print( 'Container already exists!' )
      return False
    
    return True
