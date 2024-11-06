import ruleParser

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
          quary += f'[!"{key}"="{value}"]'
        else:
          quary += f'["{key}"="{value}"]'
    
    #
    return addTypeFilter(includeTypes, quary+";")

def has_tag(list, includeTypes, parentStructLists):
  quary = ""
  for tag in list:
    key = tag.get("key")
    is_not = tag.get("not", False)
    if is_not:
      quary += f'[!{key}]'
    else:
      quary += f'[{key}]'
  return addTypeFilter(includeTypes, quary+";")

def intersects(list):
  pass

def OR(list, includeTypes, parentStructLists):
  for value in list:
    group1 = value["group1"]
    #group2 = value["group2"]
    result = ruleParser.parse(group1+parentStructLists, group1["include"], parentStructLists)
    print("OR Group 1 Parse:")
    print(result)
    