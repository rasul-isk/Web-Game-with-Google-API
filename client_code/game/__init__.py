from ._anvil_designer import gameTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import time


class game(gameTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.
    self.item['word'] = anvil.server.call('getWord')    
    self.refresh_data_bindings()
    

  def refresh_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item['word'] = anvil.server.call('getWord')    
    self.refresh_data_bindings()
    

  def finish_click(self, **event_args):
    """This method is called when the button is clicked""" 
    answer = self.answer_area.text 
    if answer:
      sourceword = self.item['word']  
      seven_words = answer.lower().strip().split(" ") 
      reasons = anvil.server.call("collect_reasons", seven_words, sourceword)
      
      winner = True if not reasons else False
             
      if winner:
        anvil.server.call('submit_log',"")
        open_form('winner',sourceword, ', '.join(seven_words))
      else:
        anvil.server.call('submit_log',"fail")
        open_form('fail', reasons)
        
    else:
      alert("Please, enter your answer")

        




