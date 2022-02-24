from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.google.auth
from anvil.tables import app_tables
from ..game import game
from ..table import table
import time
  


time1 = time.clock()

class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    
    # Any code you write here will run when the form opens.
    anvil.server.call('load_words')
  def refresh_table(self):
    # Load existing articles from the Data Table, and display them in the RepeatingPanel
    self.articles_panel.items = anvil.server.call('get_scores')

  def play_game(self, **event_args):
    open_form('game')


  def score_table_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('table',"")

  def log_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('logs')






