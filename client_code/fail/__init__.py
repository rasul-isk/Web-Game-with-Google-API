from ._anvil_designer import failTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

class fail(failTemplate):
  def __init__(self, reason, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.item['reasons'] = reason;
    self.refresh_data_bindings()

  def menu_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homepage')

  def play_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('game')

  def log_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('logs')



