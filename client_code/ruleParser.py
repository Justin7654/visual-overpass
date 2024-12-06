import anvil.server
import _ruleParserParseTypes as parseTypeModule
from collections import defaultdict


# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

def tag_has_key(tag, key):
  return hasattr(tag, '__iter__') and key in tag

def is_rule_group(component):
  return tag_has_key(component.tag, "rule_group")

def is_rule(component):
  return tag_has_key(component.tag, "type")

def get_structure(form):
  def customException(text, focusTo):
    anvil.alert(text)
    
    if hasattr(focusTo, "scroll_into_view"):
      focusTo.scroll_into_view()
    return NameError(text)
  
  def try_expand_search(component):
    #If the given component has children, it will scan the children
    try:
      component.get_components()
      return scan(component)
    except AttributeError:
      return
  
  def scan(form):
    is_group = is_rule_group(form)
    structure = []
    children = form.get_components()
    for child in children:      
      #If we are in a rule group, and the current component is a rule form
      if is_group and is_rule(child):
        tag = child.tag
        structureItem = tag #Copy that we can modify

        #Check if its not deleted
        if child.layout.tag.deleted:
          print("Skipping deleted rule")
          continue
        
        #Check its group tags and if it has a groupx tag, scan it and replace the tag
        for i in range(5):
          key = "group"+str(i)
          if tag_has_key(tag, key) and tag[key] is not None:
            #Add a new key to the tag to keep its tags accessible
            print("Searching for: "+key)
            print("Inside: "+str(child))
            structureItem[key+"tag"] = tag[key].tag
            structureItem[key] = scan(tag[key])
            if len(structureItem[key]) == 0:
              #Group was left empty
              raise customException("Group was left empty", structureItem[key])
              
        #Make sure all required text inputs are filled
        if tag_has_key(tag, "key") and len(tag["key"]) == 0:
          raise customException("Key input was left blank", child)
        if tag_has_key(tag, "value") and len(tag["value"]) == 0:
          raise customException("Value input was left blank", child)
            

        #Final
        structure.append(structureItem)
      else:
        try_expand_search(child)

    return structure

  if is_rule_group(form):
    try:
      result = scan(form)
      return result
    except NameError as e:
      print(e)
      return []
  else:
    print("WARNING: Attempted to get structure of a non rule group")
    return

'''
Parsing the structure and turning it into text.
'''

'''
Type parsing functions
Each rule type gets a different handler that turns it into text
'''

typeParsers = {
  "Match Tag": parseTypeModule.match_tag,
  "Has Tag": parseTypeModule.has_tag,
  "Intersects": parseTypeModule.intersects,
  "OR": parseTypeModule.OR,
}

groupTypes = ["OR","Intersects"]

'''
Helper Functions
'''
def filterParentStructList(data):
  blackList = ["OR","Intersects"]
  return [item for item in data if item.get("type") not in blackList]

def group_by_type(ruleGroupList):
  #All the items are AND in each ruleGroup, so combine them by type for easier processing
  grouped = defaultdict(list)
  for item in ruleGroupList:
      item_type = item.get("type") #item.get wont make a error if "type" doesn't exist
      if item_type is not None:
        grouped[item_type].append(item)
  return dict(grouped)


'''
Main Function
'''

def parse(structure, includeTypes, parentStructLists):
  parentStructLists += filterParentStructList(structure)
  grouped = group_by_type(structure)
  output = ""
  for key, list in grouped.items():
    handler = typeParsers.get(key)
    if handler is None:
      print(f'WARNING: No handler found for the rule type "{key}". It will be not included in the final output')
      continue
    result = handler(list, includeTypes, parentStructLists)
    output += result
  return output