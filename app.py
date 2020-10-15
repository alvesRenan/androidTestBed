import os
import re
from sys import exit

from Componentes.controller import Controller
from Componentes.manager import Manager
from utils.string_menus import *


class App:

  def __init__(self):
    self.ctrl = Controller()
    self.mgr = Manager()

    self.options = {
      '1': self.create_scenario,
      '2': self.ctrl.list_scenarios,
      '3': self.configure_scenario,
      '4': self.delete_scenario,
      '0': self.close_app
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
    option = input(">> ")

    self.execute_function( option )

  def create_scenario(self):
    name = input('Name of the new scenario: ')
    self.mgr.add_scenario( name )
  
  def configure_scenario(self):
    self.menu()
  
  def delete_scenario(self):
    scenario = input( 'Name of scenario to be deleted: ' )
    self.mgr.delete_scenario( scenario )

  def close_app(self):
    exit(0)


if __name__ == "__main__":
  App()
