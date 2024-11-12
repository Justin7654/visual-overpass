import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

@anvil.server.callable(require_user=True)
def getUserRulesets():
  currentUser = anvil.users.get_user()
  if currentUser is None:
    return
  return app_tables.user_rulesets.search(
    tables.order_by("date", ascending=False),
    user = currentUser
  )
  

@anvil.server.callable(require_user=True)
def saveRuleset(name, structure, topLayerIncludes):
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
def deleteRuleset(record):
  pass

@anvil.server.callable(require_user=True)
def runQuary(quaryText):
  task = anvil.server.launch_background_task("runQuaryTask", quaryText)
  return task
  

@anvil.server.background_task()
def runQuaryTask(quaryText):
  from OSMPythonTools.overpass import Overpass
  import zlib
  print("Running task")
  overpass = Overpass()
  result = overpass.query(quaryText, timeout=999) #the result is a number of objects, which can be accessed by result.elements()
  jsonVersion = result.toJSON()
  return jsonVersion