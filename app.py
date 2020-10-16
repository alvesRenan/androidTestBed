import re
from sys import exit

from Componentes.controller import Controller
from Componentes.db_manager import db_mgr
from Componentes.manager import Manager
from utils.string_menus import *


class FinishedExecution(Exception):
  pass


class App:

  def __init__(self):
    self.ctrl = Controller()
    self.mgr = Manager()

    self.options = {
      '0': self.close_app,
      '1': self.create_scenario,
      '2': self.ctrl.list_scenarios,
      '3': self.configure_scenario,
      '4': self.delete_scenario
    }

    self.menu()
  
  def execute_function(self, option):
    function = self.options.get( option )
    
    if function is None:
      print('Option not found')
    else:
      function()
    
    self.menu()
  
  def menu(self):
    print( MENU )
    option = input( '>> ' )

    self.execute_function( option )

  def create_scenario(self):
    name = input( 'Name of the new scenario: ' )
    self.mgr.add_scenario( name )
  
  def configure_scenario(self):
    scenario = input( 'Name of the scenario to be configured: ' )

    if db_mgr.scenario_exists( scenario ):
      "Wokaround to finish the class execution and go back to this menu"
      try:
        ConfigMenu( scenario, self.mgr, self.ctrl )
      except FinishedExecution:
        pass
    else:
      print( f'Scenario {scenario} not found.' )

    self.menu()
  
  def delete_scenario(self):
    scenario = input( 'Name of scenario to be deleted: ' )
    self.mgr.delete_scenario( scenario )
  
  def close_app(self):
    exit(0)


class ConfigMenu:

  def __init__(self, scenario_name, manager, controller):
    self.scenario_name = scenario_name
    self.mgr = manager
    self.ctrl = controller

    self.options = {
      '0': self.return_to_menu,
      '1': self.add_client,
      # '2': pass,
      # '3': pass,
      # '4': pass,
      # '5': pass,
      # '6': pass,
      # '7': pass,
      # '8': pass,
      # '9': pass,
      # '10': pass,
      # '11': pass,
      # '12': pass
    }

    self.show_menu()

  def execute_function(self, option):
    function = self.options.get( option )
    
    if function is None:
      print('Option not found')
    else:
      function()
    
    self.show_menu()

  def show_menu(self):
    print( CONFIG_MENU )
    option = input( '>> ' )

    self.execute_function( option )
  
  def add_client(self):
    container_name = input( 'Enter the container name: ' )
    
    """Check if name is not empty, a single number o letter"""
    if re.match( '[a-zA-Z0-9][a-zA-Z0-9_.-]', container_name ) is None:
      print( 'Name not allowed!' )
      return

    """Check if a container with that name already exists"""
    if db_mgr.container_exists( container_name ):
      print( 'Container already exists!' )
      return
    
    print( 'Available network configurations: umts, lte, full' )
    network = input( 'Entre the name of the network or define the value to be used in kbps (Ex: 620.0): ' )
    if re.match('lte|umts|full|[0-9]', network) is None:
      print( 'Network not supported! Using default network \'full\'' )
      network = 'full' 

    print('Memory value (in MB) of the device (defalt value 512 MB)')
    memory = input('Input the amount of memmory the device will have: ')
    try:
      if int(memory) < 512:
        memory = '512'
    except:
      print("Invalid value, using default value.")
      memory = '512'

    self.mgr.add_client( container_name, self.scenario_name, memory, network )

  def return_to_menu(self):
    raise FinishedExecution


if __name__ == "__main__":
  App()
