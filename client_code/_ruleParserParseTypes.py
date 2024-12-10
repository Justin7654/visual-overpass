import anvil.server
import ruleParser

def filterParentStructList(data):
  blackList = ["OR","Intersects"]
  return [item for item in data if item.get("type") not in blackList]

def addTypeFilter(includeTypes, text):
  #If all of them are true, just use nwr since thats all of them combined
  if all(includeTypes.values()): #value for value in includeTypes.values()):
    return "nwr"+text
  #Make a new line for each of the types
  output = ""
  for key,value in includeTypes.items():
    if value:
      output += (key+text)
  return output
  

def match_tag(list, includeTypes, parentStructLists):
    quary = ""
    for tag in list:
        key = tag.get("key")
        value = tag.get("value")
        is_not = tag.get("not", False)
        
        if is_not:
          quary += f'["{key}"!="{value}"]'
        else:
          quary += f'["{key}"="{value}"]'
    
    #
    return quary#addTypeFilter(includeTypes, quary+";")

def has_tag(list, includeTypes, parentStructLists):
  quary = ""
  for tag in list:
    key = tag.get("key")
    is_not = tag.get("not", False)
    if is_not:
      quary += f'[!{key}]'
    else:
      quary += f'[{key}]'
  return quary#addTypeFilter(includeTypes, quary)

def newer_than(ruleList, includeTypes, parentStructLists):
  print("Newer than:")
  quary = ""
  for rule in ruleList:
    #quary += f'(newer:"{rule["year"]}-{rule["month"]:02d}-{rule["day"]:02d}T00:00:00Z")'
    quary += f'(changed:"{rule["start_year"]}-{rule["start_month"]:02d}-{rule["start_day"]:02d}T00:00:00Z","{rule["end_year"]}-{rule["end_month"]:02d}-{rule["end_day"]:02d}T00:00:00Z")'
  print(quary)
  return quary

def intersects(list):
  pass

def OR(ruleList, includeTypes, parentStructLists):
  '''
  Parse each side like normal, and put them in a OR format next to each other in a union
  Also give it the rules above it to be parsed so those ANDs also need to work
  '''
  #parentStructLists = filterParentStructList(parentStructLists)
  
  output = ""
  for value in ruleList:
    group1 = value["group1"]
    group1Tags = value["group1tag"]
    group2 = value["group2"]
    group2Tags = value["group2tag"]

    print("Parent struct:")
    print(parentStructLists)
    print("--- End parent struct")
    combined1 = group1+parentStructLists
    combined2 = group2+parentStructLists
    result1 = ruleParser.parse(combined1, group1Tags["include"], list(parentStructLists))
    result2 = ruleParser.parse(combined2, group2Tags["include"], list(parentStructLists))
    output += f'({result1}{result2});'
  return output