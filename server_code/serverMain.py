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

def getSafeRulesetName(name):
  def nameFree(name): return all([x["name"] != name for x in existingRulesets])
  def getNewName(num): return name+f' ({num})'
  existingRulesets = getUserRulesets()
  if not nameFree(name):
    num = 1
    while not nameFree(getNewName(num)):
      num += 1
    return getNewName(num)
  else:
    return name
  

@anvil.server.callable(require_user=True)
def saveRuleset(name, structure, topLayerIncludes):
  from datetime import datetime
  if name == "":
    name = "Unnamed Ruleset"
  name = getSafeRulesetName(name)
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
  #row = app_tables.user_rulesets.get_by_id(rowID)
  row["name"] = name
  row["savedStructure"] = structure
  row["topLayerIncludeTypes"] = topLayerIncludes
  

@anvil.server.callable(require_user=True)
def deleteRuleset(ruleset):
  ruleset.delete()

@anvil.server.callable(require_user=True)
def runQuary(quaryText):
  task = anvil.server.launch_background_task("runQuaryTask", quaryText)
  return task

@anvil.server.callable(require_user=True)
def cancelQuary(task):
  task.kill()

@anvil.server.background_task()
def runQuaryTask(quaryText):
  from OSMPythonTools.overpass import Overpass
  import logging
  logging.getLogger('OSMPythonTools').setLevel(logging.ERROR)
  print("Running task")
  overpass = Overpass(useragent="Visualized Overpass 2024-2025 Senior Mastery Project")
  result = overpass.query(quaryText, timeout=500) #the result is a number of objects, which can be accessed by result.elements()
  jsonVersion = result.toJSON()
  return jsonVersion

@anvil.server.callable
def generateGeoJson(data):
  import osm2geojson
  #from inspect import getmembers, isfunction
  #print(getmembers(osmtogeojson, isfunction))
  return osm2geojson.json2geojson(data, log_level="ERROR")

@anvil.server.callable
def renew_session(): #Cliant can call this every once in a while to prevent the session from expiring
  return True