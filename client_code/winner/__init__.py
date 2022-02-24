from ._anvil_designer import winnerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

class winner(winnerTemplate):
  def __init__(self, sourceword, guesses, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    timetaken = anvil.server.call('getTimeTaken')
    
    self.item['winnerText'] = f"Your results \nSource Word: {sourceword}\nGuessed words: {guesses}\nTime taken: {timetaken} seconds\n"
    
    
  
  def menu_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homepage')

  def submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.item['name']
    if(name):
      anvil.server.call('submit_result', name)
      open_form('table',name)
    else:
      alert("Please, enter your name.")


