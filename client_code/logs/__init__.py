from ._anvil_designer import logsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

class logs(logsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    table = []
    logs = app_tables.logs.search(tables.order_by("id", ascending=False))
    
    for log in logs:
      row = { "logs":log['messages'] }
      table.append(row)
        
    self.repeating_panel_1.items = table
    

  def menu_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homepage')

  def game_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('game')


