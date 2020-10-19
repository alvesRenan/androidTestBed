import sqlite3

from utils.queries import *

class DBManager:

  def __init__(self):
    self.conn = sqlite3.connect( 'DB/testbed.db' )
    self.cur = self.conn.cursor()

    self.create_dbs()
  
  def create_dbs(self):
    """Create the tables if they don't exist"""
    with self.conn:
      self.cur.execute( CREATE_DB_SCENARIOS )
      self.cur.execute( CREATE_DB_CONTAINERS )
  
  def scenario_exists(self, scenario_name):
    """Checks if a scenario with a given name already exists

      Args:
        scneario_name (str): Name of the scenario

      Returns:
        list if scenario exists or None if dosn't exists 
    """
    self.cur.execute( SCENARIO_EXISTS, {'name': scenario_name} )

    return self.cur.fetchone()
  
  def inset_scenario(self, scenario_name):
    """Inserts scenario_name into scenarios table"""
    with self.conn:
      self.cur.execute( INSET_SCENARIO, {'name': scenario_name} )
    
  def list_all_scenarios(self):
    """Returns a list of all scenarios and their states"""
    self.cur.execute( LIST_ALL_SCENARIOS )
    
    return self.cur.fetchall()
  
  def list_containers(self, scenario_name):
    """Returns a list of all containers in a scenario"""
    self.cur.execute( LIST_CONTAINERS, {'name': scenario_name} )

    return self.cur.fetchall()
  
  def delete_scenario(self, scenario_name):
    """Deletes a scenario and the containers associated with it"""
    with self.conn:
      self.cur.execute( DELETE_SCENARIO, {'name': scenario_name} )
      self.cur.execute( DELETE_CONTAINERS_FROM_SCENARIO, {'name': scenario_name} )
  
  def container_exists(self, container_name):
    """Checks if a container with a given name already exists

      Args:
        container_name (str): Name of the container

      Returns:
        list if container exists or None if dosn't exists
    """
    self.cur.execute( CONTAINER_EXISTS, {'name': container_name} )

    return self.cur.fetchone()

  def insert_container(
    self,
    scenario_name,
    container_name,
    memory,
    network=None,
    is_server=0,
    cpus=None,
    adb_connection=None
  ):
    """Inserts a container specs into containers table"""
    with self.conn:
      self.cur.execute( INSET_CONTAINER, (
        scenario_name, container_name, memory, network, is_server, cpus, adb_connection) )
    

db_mgr = DBManager()
