import anvil.server

# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#
disable = False

def tag_has_key(tag, key):
  return hasattr(tag, '__iter__') and key in tag

def is_rule_group(component):
  return tag_has_key(component.tag, "rule_group")

def is_rule(component):
  return tag_has_key(component.tag, "type")

def get_structure(form, loadingBarParent):
  global disable
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
        print("Found rule")
        tag = child.tag
        structureItem = tag
        #Check its group tags and if it has a groupx tag, scan it and replace the tag
        for i in range(5):
          key = "group"+str(i)
          if tag_has_key(tag, key) and tag[key] is not None:
            print("Found group inside rule. Scanning too")
            structureItem[key] = scan(tag[key])
        
        #Make sure all required text inputs are filled
        if tag_has_key(tag, "key") and tag["key"] != "":
          anvil.alert("Key input was left blank on "+tag.type+" rule")
          child.scroll_into_view()
          return
        if tag_has_key(tag, "value") and tag["value"] != "":
          anvil.alert("Value input was left blank on "+tag.type+" rule")
          child.scroll_into_view()
          return
            

        #Final
        structure.append(structureItem)
      else:
        try_expand_search(child)

    return structure

  if is_rule_group(form):
    result = scan(form)
    if disable:
      disable = False
      result = []
      print("Cancelled result because it was cancelled at some point.")
    return result
  else:
    print("WARNING: Attempted to get structure of a non rule group")
    return
  

def parse():
  pass