import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.server, anvil.http
import random, time, math, calendar
from datetime import date,datetime
from collections import Counter
from flask import request



@anvil.server.callable
def load_words():
    duplicate = ""
    big_words = ""
    all_words = ""
    
    text_file = app_files.words_txt.get_bytes().decode("UTF-8").replace("/n"," ").split()    
    
    for word in text_file:
      
      word = word.lower().strip()  # Remove pesky \n.
      word = word.replace(
          "'s", ""
      )  # Remove any trailing 's at end of word.
      if duplicate != word:
          duplicate = word
      else:
        continue;
        
      if len(word) > 7:
          big_words += f"{word} "
      if len(word) > 3:
          all_words += f"{word} "
      
    all_wordsFile = anvil.google.drive.app_files.all_words.set_bytes(all_words)    
    big_wordsFile = anvil.google.drive.app_files.big_words.set_bytes(big_words)
  
@anvil.server.callable
def getWord():
  big_words = anvil.google.drive.app_files.big_words.get_bytes().decode("UTF-8").split()
  anvil.server.session["startTime"] = time.time()
  return random.choice(big_words)

@anvil.server.callable
def collect_reasons(seven_words, sourceword):
  anvil.server.session["endTime"] =  round(time.time(),2)
  anvil.server.session["input"] = ', '.join(seven_words)
  anvil.server.session["source"] = sourceword
  anvil.server.session["timetaken"] = round(anvil.server.session["endTime"]-anvil.server.session["startTime"], 2)
  
  reason = ""
 
  reason += check_size(seven_words)
  reason += check_words_length(seven_words)
  reason += check_letters(sourceword, seven_words)
  reason += duplicates(seven_words)
  reason += check_spellings(seven_words)
  reason += check_not_sourceword(seven_words, sourceword)

  return reason


@anvil.server.callable
def submit_result(name):
  app_tables.score_table.add_row(name=name, timeTaken = anvil.server.session['timetaken'],sourceword=anvil.server.session["source"],guesses=anvil.server.session["input"],id=getID())                                          

@anvil.server.callable
def submit_log(result):
  seven_words = anvil.server.session["input"]
  sourceword = anvil.server.session["source"]
  if result == "fail":
    result = f"!!! ERRORS: {sourceword} - {seven_words}\n"
  else:
    result = f"SUCCESS: {sourceword} - {seven_words}\n"
    
  today = date.today()
  now = datetime.now()
  time =  now.strftime("%H:%M:%S")
  month = today.strftime("%B")
  monthDay = today.strftime("%d")
  year = today.strftime("%Y")
  weekDay = calendar.day_name[date.today().weekday()]
  finalDate = f"{weekDay[0:3]} {month[0:3]} {monthDay} {time} {year}" 
  
  ip = anvil.server.context.client.ip
  browser = anvil.server.context.client.type
  
  result += f"{finalDate} - {ip} - {browser}\n"
  
  app_tables.logs.add_row(id=getIDlog(),messages=result)                                          


@anvil.server.callable  
def getTimeTaken():
  return anvil.server.session["timetaken"]

def check_size(seven_words):                                                             
  """Checks a list of words to ensure they are of a certain size."""
  return f"\nYou have an incorrect number of words: {len(seven_words)}, not 7." if len(seven_words) != 7 else ""

def check_words_length(seven_words):                                                             
  small_words = []
  
  for word in seven_words:
    small_words.append(word) if len(word) < 4 else small_words
  
  return f"\nThese words are too small: {small_words}" if small_words else ""

def check_letters(sourceword, seven_word):                                          
    """Check one word (check_word) is "inside" another (source_word).

    By "inside" we mean that the number and value of the letters
    in the check_word must be in the sourceword as per the
    Word Game rules. A list of tuples is returned where
    each (letter, bool) tuple provides validity."""
    
    extra_letters = set()
    source_set = Counter(sourceword)
    for word in seven_word:
        word_set = set(word)
        word_extra = word_set.difference(source_set)
        if word_extra:
          for letter in word_extra: 
            extra_letters.add(letter)
    
    return f"\nExtra letter used: {extra_letters}." if extra_letters else ""

def duplicates(seven_word):                                                                             
    """Returns True if the list contains any duplicates."""
    duplicates = []
    for word in seven_word:
      duplicates.append(word) if seven_word.count(word) > 1 else duplicates
    return f"\nYou have duplicates in your list: {duplicates}" if duplicates else ""

def check_spellings(seven_word):                                                    
    """Check a list of words for spelling errors."""  
    all_words = anvil.google.drive.app_files.all_words.get_bytes().decode("UTF-8").split()
    spellings = []
    
    for word in seven_word:
        spellings.append(word) if word not in all_words else spellings
      
    return f"\nYou misspelt these words: {spellings}" if spellings else ""

def check_not_sourceword(seven_words, sourceword):                                                
    """Checks a list of words to ensure none are the sourceword."""
    return f"\nYou cannot use the source word: {sourceword}" if sourceword in seven_words else ""
  
def getID():  
  count = 1
  for user in app_tables.score_table.search():
    count += 1
  return count

def getIDlog():
  count = 1
  for user in app_tables.logs.search():
    count += 1
  return count
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

