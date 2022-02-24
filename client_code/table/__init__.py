from ._anvil_designer import tableTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

class table(tableTemplate):
  def __init__(self, name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    table = []
    winnerPlace = 0
    place = 1
    score_table = app_tables.score_table.search(tables.order_by("timeTaken", ascending=True))
    
    for player in score_table:
      row = {"place": place, "player_name":player['name'], "time":player['timeTaken'], "sourceword":player['sourceword'], "guesses":player['guesses']}
      table.append(row)
      
      place += 1
      
      if (place > 10):
        break
        
    self.repeating_panel_1.items = table
    
    
    winnerPlace = 0
    place = 1
    score_table = app_tables.score_table.search(tables.order_by("id", ascending=True))
    
    for player in score_table:
      if(name!= "" and (player['name'] == name) and winnerPlace < place):
          winnerPlace = place            
      place += 1
    
    if name != "":      
      winnerPlace = int(winnerPlace)
      
      if 11 <= (winnerPlace % 100) <= 13: 
          suffix = 'th'
      else:
          suffix = ['th', 'st', 'nd', 'rd', 'th'][min(winnerPlace % 10, 4)]
          
      place_string = str(winnerPlace) + suffix
      self.item['winnerText'] = f"Congratulation, {name}. You won!\nYou are on {place_string} Place!"
      self.refresh_data_bindings()    
      

  def menu_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homepage')

  def play_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('game')

  def logs_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('logs')




