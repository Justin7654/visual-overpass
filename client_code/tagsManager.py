import anvil.server
from anvil_extras.non_blocking import call_async

keyList = {}
valueLists = {}

def tryGetKeyList():
  if len(keyList) > 0:
    return print("Attempt to get key list when its already loaded!")
  
  #Handlers
  def _ResultHandler(result):
    global keyList
    keyList = result
    print("Got keylist")
    
  def _ErrorHandler():
    print("Error getting key list")
  #Call the server function with non blocking
  call_async("getKeyList").on_result(_ResultHandler, _ErrorHandler)

def getKeyList():
  return keyList

def getValueList(key):
  if key not in keyList:
    print(f'Not requesting values since key "{key}" is not in keylist')
    return
  if valueLists.get(key) is None:
    valueLists[key] = anvil.server.call_s("getValueListForKey", key)
  return valueLists[key]

#Need to put inside a try statement or else designer wont work in forms where this is imported
if len(keyList) == 0:
  try:
    tryGetKeyList()
    #keyList = anvil.server.call_s("getKeyList")
  except anvil.server.SessionExpiredError:
    pass