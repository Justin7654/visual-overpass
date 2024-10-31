import anvil.server

# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

def is_rule_group(component):
  return hasattr(component.tag, '__iter__') and "rule_group" in component.tag

def get_structure(form, loadingBarParent):
  def try_expand_search(component):
    #If the given component has children, it will scan the children
    component.get_components()
    scan(component)
  
  def scan(form):
    form.get_components()
    for child in form:
      print(child)
      
    
    

  scan(form)

def parse():
  pass