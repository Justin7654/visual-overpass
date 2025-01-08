import anvil.server

keyList = anvil.server.call_s("getKeyList")
valueLists = {}

def getKeyList():
  return keyList

def getValueList(key):
  if key not in keyList:
    print(f'Not requesting values since key "{key}" is not in keylist')
    return
  if valueLists.get(key) is None:
    valueLists[key] = anvil.server.call_s("getValueListForKey", key)
  return valueLists[key]
  