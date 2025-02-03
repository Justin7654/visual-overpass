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

@anvil.server.callable
def runQuary(quaryText, outMode, user):
  user = anvil.users.get_user()
  task = anvil.server.launch_background_task("runQuaryTask", quaryText, outMode, user)
  return task

@anvil.server.callable
def cancelQuary(task):
  task.kill()

@anvil.server.background_task()
def runQuaryTask(quaryText, outMode, user):
  import overpass

  quaryText += f'out {outMode};'
  api = overpass.API(timeout=999, debug=True)
  response = api.get(quaryText, verbosity=outMode, responseformat="json", build=False)

  return uploudQueryDataOutput(response, user)

@anvil.server.callable()
def uploudQueryDataOutput(response, user):
  contentFile = compress_dict(response) #anvil.BlobMedia("application/json", encode_dict_to_byte(response))
  size = len(contentFile.get_bytes())/1_000_000
  newRow = app_tables.data_output.add_row(data=contentFile, user=user, size=size)
  return newRow.get_id()
  

@anvil.server.callable
def getDataOutput(row_id):
  row = app_tables.data_output.get_by_id(row_id)
  if row and row['user'] == anvil.users.get_user():
    print("(getDataOutput) Found row and it is owned by the user")
    newFile = anvil.BlobMedia("application/json", decompress_to_bytes(row['data']))
    print("(GetDataOutput) Decompressed and packaged into application")
    #row.delete()
    return newFile

@anvil.server.callable
def generateGeoJson(data):
  import osm2geojson
  print("Decoding data")
  data = decode_byte_to_dict(data.get_bytes())
  print("Converting to GeoJSON")
  try:
    result = osm2geojson.json2geojson(data, log_level='ERROR')
    print("Packaging to BlobMedia")
    return anvil.BlobMedia("application/geo+json", encode_dict_to_byte(result))
  except KeyError as err:
    #KeyError: 'lon' at /home/anvil/.env/lib/python3.10/site-packages/osm2geojson/main.py, line 186
    # ^ This means the json doesn't contain location data
    print("Error converting to geojson:",str(err))
    return None

@anvil.server.callable
def generateKmlMediafromGeoJson(geojson, filename):
  from geo2kml import to_kml
  geojson = decode_byte_to_dict(geojson.get_bytes())
  data = to_kml(geojson)
  return anvil.BlobMedia("application/vnd.google-earth.kml+xml", data.encode(), name=filename)

@anvil.server.callable
def renew_session(): #Cliant can call this every once in a while to prevent the session from expiring
  return True

#Input: Uncompressed bytestring
#Output: BlobMedia of compressed bytes (application/zstd)
def compress_bytes(byteData):
  import pyzstd
  startTime = time.time()
  compressed = pyzstd.compress(byteData) #Eligable for training?
  totalTime = (time.time() - startTime)*1000
  print(f'Compress took {totalTime:.0f}ms')
  #Calculate saved amount
  prev, after = calculate_mb(byteData), calculate_mb(compressed)
  print(f'Saved {prev-after:.2f}mb from compression ({prev:.2f} -> {after:.2f})')
  return anvil.BlobMedia("application/zstd", compressed)

#Input: BlobMedia of compressed bytes (application/zstd)
#Output: Uncompressed bytestring
def decompress_to_bytes(blobMedia):
  import pyzstd
  original = pyzstd.decompress(blobMedia.get_bytes())
  return original

def compress_dict(data):
  byteData = encode_dict_to_byte(data)
  return compress_bytes(byteData)

@anvil.server.callable
def decompress_dict(data):
  return decode_byte_to_dict(decompress_to_bytes(data))

def encode_dict_to_byte(dict):
  import json
  #print("Ecoding: ",dict)
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

def calculate_mb(bytestring):
  return len(bytestring)/1_000_000