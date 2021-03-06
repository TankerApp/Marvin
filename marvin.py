#/bin/python
import sqlite3
import sys
from random import random, randint, choice

QUOTESFILE = "quotes.sqlite"

# Set PROD to 0 to enable command line debug interface 
PROD=1


# Init db
conn = sqlite3.connect(QUOTESFILE)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS quotes (id integer PRIMARY KEY, date text, answer boolean, who text, keyword text, value text)")
conn.commit()
conn.close()
  

def Speak(phenny, value):
  if PROD:
    phenny.say(value)
  else:
    print value

def AddString(phenny, nick, value, answer):
  args = value[2:100]
  
  keyword = "";
  req = ""
  if (len(args) >1) and (args[1] == ":"):
    keyword = args[0]
    args = args[2:100]
    
  value = " ".join(args)

  conn = sqlite3.connect(QUOTESFILE)
  c = conn.cursor()
  req = "SELECT MAX(id) + 1 FROM quotes"
  c.execute(req)
  idx = c.fetchone()[0]
  if (idx == None):
    idx = 0

  value   = value.replace("'", "''");
  keyword = keyword.replace("'", "''");
  
  req = "INSERT INTO quotes (id, date, answer, who, keyword, value) VALUES (" + str(idx) + ", CURRENT_TIMESTAMP, " + str(answer) + ", '" + nick + "', '" + keyword + "', '" + value + "')"
  
  c.execute(req)
  conn.commit()
  conn.close()

  if (len(keyword)):
    Speak(phenny, "Added quote #" + str(idx)+ " : \"" + value + "\" for keyword " + keyword);
  else:
    Speak(phenny, "Added quote #" + str(idx)+ " : \"" + value + "\"");


def DumpAll(phenny):
  conn = sqlite3.connect(QUOTESFILE)
  c = conn.cursor()
  req = "SELECT MAX(id) + 1 FROM quotes"
  c.execute(req)
  idx = c.fetchone()[0]
  req = "SELECT id, date, who, keyword, value FROM quotes ORDER BY id DESC"
  for row in c.execute(req):
    if (len(row[3])):
      d = "#" + str(row[0]) + " - " + row[1] + " @" + row[2] + " [Keyword \"" + row[3] + "\"] \"" + row[4] + "\""
    else:
      d = "#" + str(row[0]) + " - " + row[1] + " @" + row[2] + " \"" + row[4] +"\""
    Speak(phenny, d)
  conn.close()

def Erase(id):
  conn = sqlite3.connect(QUOTESFILE)
  c = conn.cursor()
  req = "DELETE FROM quotes WHERE id=" + id
  c.execute(req)
  conn.commit()
  conn.close()


def PickAny(answer):
  req = "SELECT value FROM quotes WHERE answer = " + str(answer) + " AND keyword = \"\" ORDER BY RANDOM() LIMIT 1"
  conn = sqlite3.connect(QUOTESFILE)
  c = conn.cursor()
  c.execute(req)
  reply = c.fetchone()
  
  if (reply == None):
    reply = "..."
  else:
    reply = reply[0]
  return reply
  
   
def HasKnownKeywords(phenny, nick, input):
  # Test if keywords
  req = "SELECT value FROM quotes WHERE answer = 0 AND keyword IN (";
  for i in range(0, len(input)):
    if (i != 0):
      req += ", "
    inp   = input[i].replace("'", "''");
    req += "'" + inp + "'"
  req += ")"
  conn = sqlite3.connect(QUOTESFILE)
  c = conn.cursor()
  all = c.execute(req)

  ret = False
  reply = c.fetchone()
  if (reply != None):
    ret = True
  conn.commit()
  conn.close()
  return ret

def Generate(phenny, nick, input, answer):
  
  # Test if keywords
  req = "SELECT value FROM quotes WHERE answer = " + str(answer) + " AND keyword IN (";
  for i in range(0, len(input)):
    if (i != 0):
      req += ", "
    inp   = input[i].replace("'", "''");
    req += "'" + inp + "'"
  req += ")"
  
  conn = sqlite3.connect(QUOTESFILE)
  c = conn.cursor()
  all = c.execute(req)
  
  reply = c.fetchone()
  if (reply != None):
    reply = reply[0]      
  else:
    reply = PickAny(answer)
  conn.commit()
  conn.close()
  
  reply = reply.replace("$nick", nick)
  Speak(phenny, reply)
  
  

 
def talk(phenny, input):
  willspeak = False
  spontaneous = randint(0, 20)
  
  if PROD:
    nick = input.nick
    input = input.split()
  else:
    nick = "Bob"
    
  # Marvin invoked, Marvin will reply
  if (("Marvin" in input) or ("Marvin," in input) or ("Marvin;" in input) or ("Marvin." in input) or ("Marvin!" in input) or ("Marvin?" in input)):
    willspeak = True

  # Spontaneous intervention
  if (spontaneous == 0):
    willspeak = True

  # If Marvin knows something about current topic, Marvin may talk
  if ( (willspeak == False)  and (spontaneous < 7) and (HasKnownKeywords(phenny, nick, input)) ):
    willspeak = True;

  if (".die" in input):
    Speak(phenny, ".die")
    return

  if willspeak == False:
    return


  if (input[0] == "Marvin") and (input[1] == "help"):
    Speak(phenny, "To register a new string, type : \"Marvin ADD This is my new string\"")
    Speak(phenny,"To register a new answer, type : \"Marvin ADD? This is my answer\"")
    Speak(phenny,"To register a new string for a keyword, type : \"Marvin ADD keyword : This is my new string\"")
    return
    
  # ADD quote
  if (len(input) >= 2) and (input[0] == "Marvin") and (input[1] == "ADD"):
    AddString(phenny, nick, input, 0)
    return

  # ADD reply
  if (len(input) >= 2) and (input[0] == "Marvin") and (input[1] == "ADD?"):
    AddString(phenny, nick, input, 1)
    return
    
  # DUMP keyword
  if (len(input) == 2) and (input[0] == "Marvin") and (input[1] == "DUMP"):
    DumpAll(phenny)
    return

  # DEL keyword
  if (len(input) == 3) and (input[0] == "Marvin") and (input[1] == "DEL"):
    Erase(input[2])
    return


  # Generate marvin reply
  if "?" in input:
    Generate(phenny, nick, input, 1)
  else:
    Generate(phenny, nick, input, 0)

if (PROD == 0):
  talk(0, sys.argv[1:100]);
else:
  talk.rule  = r'.*'
