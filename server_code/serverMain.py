import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
import time

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
  #Modify input data
  if name == "":
    name = "Unnamed Ruleset"
  name = getSafeRulesetName(name)
  structure = compress_dict(structure)
  #Get new data
  user = anvil.users.get_user()
  date = datetime.now()
  #Uploud
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
  row["savedStructure"] = compress_dict(structure)
  row["topLayerIncludeTypes"] = topLayerIncludes
  

@anvil.server.callable(require_user=True)
def deleteRuleset(ruleset):
  ruleset.delete()

@anvil.server.callable(require_user=True)
def runQuary(quaryText, outMode):
  user = anvil.users.get_user()
  task = anvil.server.launch_background_task("runQuaryTask", quaryText, outMode, user)
  return task

@anvil.server.callable(require_user=True)
def cancelQuary(task):
  task.kill()

@anvil.server.background_task()
def runQuaryTask(quaryText, outMode, user):
  import overpass
  
  api = overpass.API(timeout=999, debug=True)
  response = api.get(quaryText, verbosity=outMode, responseformat="json")
  contentFile = anvil.BlobMedia("application/json", encode_dict_to_byte(response))
  newRow = app_tables.data_output.add_row(data=contentFile, user=user)

  return newRow.get_id()#response

@anvil.server.callable
def getDataOutput(row_id):
  row = app_tables.data_output.get_by_id(row_id)
  if row and row['user'] == anvil.users.get_user():
    return row['data']

@anvil.server.callable
def generateGeoJson(data):
  import osm2geojson
  data = decode_byte_to_dict(data.get_bytes())
  try:
    return osm2geojson.json2geojson(data, log_level="ERROR")
  except KeyError: #KeyError: 'lon' at /home/anvil/.env/lib/python3.10/site-packages/osm2geojson/main.py, line 186
    return False

@anvil.server.callable
def generateKmlMediafromGeoJson(geojson, filename):
  from geo2kml import to_kml
  data = to_kml(geojson)
  return anvil.BlobMedia("application/vnd.google-earth.kml+xml", data.encode(), name=filename)

@anvil.server.callable
def renew_session(): #Cliant can call this every once in a while to prevent the session from expiring
  return True

def compress_dict(data):
  import pyzstd #Compresses
  byteData = encode_dict_to_byte(data)
  startTime = time.time()
  compressed = pyzstd.compress(byteData) #Eligable for training?
  totalTime = (time.time() - startTime)*1000
  print(f'Compress took {totalTime:.0f}ms')
  return anvil.BlobMedia("application/zstd", compressed)

@anvil.server.callable
def decompress_dict(data):
  import pyzstd
  original = pyzstd.decompress(data.get_bytes())
  return decode_byte_to_dict(original)

def encode_dict_to_byte(dict):
  import json
  print("Ecoding: ",dict)
  return json.dumps(dict).encode('utf-8')

def decode_byte_to_dict(byte):
  import json
  return json.loads(byte.decode('utf-8'))

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