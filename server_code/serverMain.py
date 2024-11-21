import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable(require_user=True)
def getUserRulesets():
  currentUser = anvil.users.get_user()
  return app_tables.user_rulesets.search(
    tables.order_by("date", ascending=False),
    user = currentUser
  )
  

@anvil.server.callable(require_user=True)
def saveRuleset(name, structure, topLayerIncludes):
  from datetime import datetime
  if name == "":
    name = "Unnamed Ruleset"
  user = anvil.users.get_user()
  date = datetime.now()
  app_tables.user_rulesets.add_row(
    user=user,
    date=date,
    name=name,
    savedStructure=structure,
    topLayerIncludeTypes=topLayerIncludes
  )

@anvil.server.callable(require_user=True)
def updateRuleset(row, name, structure, topLayerIncludes):
  pass
  

@anvil.server.callable(require_user=True)
def deleteRuleset(ruleset):
  ruleset.delete()

@anvil.server.callable(require_user=True)
def runQuary(quaryText):
  task = anvil.server.launch_background_task("runQuaryTask", quaryText)
  return task
  

@anvil.server.background_task()
def runQuaryTask(quaryText):
  from OSMPythonTools.overpass import Overpass
  import logging
  logging.getLogger('OSMPythonTools').setLevel(logging.ERROR)
  print("Running task")
  overpass = Overpass()
  result = overpass.query(quaryText, timeout=30) #the result is a number of objects, which can be accessed by result.elements()
  jsonVersion = result.toJSON()
  return jsonVersion

@anvil.server.callable
def renew_session(): #Cliant can call this every once in a while to prevent the session from expiring
  return True