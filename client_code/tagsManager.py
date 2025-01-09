import anvil.server

keyList = {}
valueLists = {}

#Need to put inside a try statement or else designer wont work in forms where this is imported
if len(keyList) == 0:
  try:
    keyList = anvil.server.call_s("getKeyList")
  except anvil.server.SessionExpiredError:
    pass

def getKeyList():
  return keyList

def getValueList(key):
  if key not in keyList:
    print(f'Not requesting values since key "{key}" is not in keylist')
    return
  if valueLists.get(key) is None:
    valueLists[key] = anvil.server.call_s("getValueListForKey", key)
  return valueLists[key]
  