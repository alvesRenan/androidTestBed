"""
  Novo criador
"""

import subprocess as sp

from Components.db_manager import db_mgr
from Components.docker_manager import docker_mgr


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
  
  def add_client(self, scenario_name, container_name, memory, network ):
    ip_ctnr = docker_mgr.create_client_container( container_name )

    if ip_ctnr is None:
      print( 'Something went wrong.' )
      return
    
    "The adb connection is the container ip and the default port 5555"
    db_mgr.insert_container( scenario_name, container_name, memory, adb_connection=ip_ctnr+':5555', network=network)
  
  def add_server(self, scenario_name, container_name, memory, cpus, bind_ports=True):
    ctnr = docker_mgr.create_server_container( container_name, memory, bind_ports )

    if ctnr is None:
      print( 'Something went wrong.' )
      return

    if cpus is not None:
      sp.call( f"docker update --cpus='{cpus}' {container_name}", shell=True, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
    
    db_mgr.insert_container( scenario_name, container_name, memory, is_server=1, cpus=cpus )
