from ._anvil_designer import NewRulesetTemplate
from anvil import *
import anvil.users
import anvil.server
from datetime import datetime
from anvil_extras.non_blocking import call_async
from anvil_extras import augment
from . import hoverTracking
from .. import ruleParser
from .area_definition import area_definition

#UI
from .new_rule_button import new_rule_button
from .operation_text import operation_text

#Rules
from .rules import get_all_rule_data

class NewRuleset(NewRulesetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    #Find the rules    
    self.ruleData = get_all_rule_data()
    
    self.rule_group.tag = {
      "rule_group": True,
      "include": {
        "node":True,
        "way":True,
        "relation":True,
      }
    }
    self.dirty = False
    
    self.initRuleGroups(self)
    self.initRuleGroups(self.area_definition_1.layout.slots['content'])
    
    self.saveRow = None
    if properties["preset"]:
      self.loadSet(properties["preset"])
    

  def initRuleGroups(self, form):
    #Loops through all descendents of the given form and adds plus icons to each rule group
    children = form.get_components()
    for child in children:
      try:
        child.get_components()
      except AttributeError:
        pass
      else:
        self.initRuleGroups(child)
        
      try:
        if ruleParser.is_rule_group(child):
          #check if its already setup, if so dont setup again
          if "RuleGroupSetup" not in child.tag:
            child.tag["RuleGroupSetup"] = True
            self.add_new_plus(child)
      except TypeError as e:
        print(child,"was compatible but failed because:",e)
         
  def add_new_plus(self, form):
    # Adds a new plus button to the bottom of the specified form which can be used to add new rules to its parent
    newRuleButton = new_rule_button()
    newRuleButton.raise_event("x-hookClick", func=self.new_rule_click)
    form.add_component(newRuleButton)
  
  def add_new_rule(self, name, form, preset=False):
    # Adds a new rule form in the specified location. Name is the user-friendly name of the target rule.
    foundRule = None
    for rule in self.ruleData:
      if rule["name"] == name:
        foundRule = rule
        break
    else:
      Notification("No rule found with the name '"+name+"'. Loading halted", title="Unexpected error while initializing", style="warning").show()
      exit("No rule found with the name '"+name+"'")

    #Make the and/or text
    currentSize = len(form.get_components()) #Use custom index to keep the plus at the bottom
    operationText = False
    if currentSize > 1:
      operationText = operation_text()
      form.add_component(operationText, index=currentSize-1)
      currentSize += 1
    
    #Make the UI
    copy = foundRule["form"](lastTag=preset)
    copySlot = copy.layout.slots['content']
    self.initRuleGroups(copySlot)
    form.add_component(copy, index=currentSize-1)
    self.dirty = True

    def onDelete(**event_args):
      copy.remove_from_parent()
      if operation_text:
        operationText.remove_from_parent()

    copy.layout.tag.onDeleteCallback = onDelete
    
    return copy

  def runSet(self):
    if self.dirty:
      if not confirm("All unsaved changes will be lost. Are you sure?"):
        return
    print("-------------- GETTING STRUCTURE ----------------")
    struct = ruleParser.get_structure(self.rule_group)
    print(struct)
    if len(struct) == 0:
      return None
    open_form("RunRuleset", structure=struct, topIncludes=self.rule_group.tag["include"])
  
  def saveSet(self):
    #Check if to overwrite or do a new set
    mode = "new"
    if self.saveRow is not None:
      buttons = [("Overwrite", "overwrite"),("Create New", "new"),("Cancel",None)]
      mode = confirm("Would you like to overwrite the existing set?", buttons=buttons, dismissible=True, large=True)
    #
    structure = ruleParser.get_structure(self.rule_group)
    name = self.ruleset_name.text.strip()
    if len(structure) == 0:
      return False
    if not anvil.server.is_app_online():
      alert("Connect to the internet and try again later", title="No Internet")
      return False

    if mode == "new":
      anvil.server.call("saveRuleset", name, structure, self.rule_group.tag["include"])
      Notification("Saved").show()
      self.dirty = False
    elif mode == "overwrite":
      anvil.server.call("updateRuleset", self.saveRow, name, structure, self.rule_group.tag["include"])
      Notification("Overwritten").show()
      self.dirty = False
  def loadSet(self, data):
    self.saveRow = data
    savedStructure = data["savedStructure"]
    topIncludes = data["topLayerIncludeTypes"]
    #Check if this still uses the old structure format
    if savedStructure is not None:
      savedStructure = anvil.server.call("decompress_dict", savedStructure)
    elif data["savedStructure_legacy"] is not None:
      savedStructure = data["savedStructure_legacy"]
    #Check the top includes
    self.includeNodes.checked = topIncludes["node"]
    self.includeWays.checked = topIncludes["way"]
    self.includeRelations.checked = topIncludes["relation"]
    self.ruleset_name.text = data["name"]
    #Add the rules
    def parse(list, targetForm):
      for rule in list:
        #Add
        newRuleComponent = self.add_new_rule(rule["type"], targetForm, preset=rule)
        
        #Search for inner groups
        for i in range(5):
          key = "group"+str(i)
          if ruleParser.tag_has_key(rule, key) and rule[key] is not None:
            includes = rule[key+"tag"]["include"]
            groupComponent = newRuleComponent.tag[key]
            upperGroup = groupComponent.parent.parent
            upperGroup.includeNodes.checked = includes["node"]
            upperGroup.includeWays.checked = includes["way"]
            upperGroup.includeRelations.checked = includes["relation"]
            parse(rule[key], groupComponent)
        
    parse(savedStructure, self.rule_group)
    self.dirty = False
    

  def get_rule_selection(self):
    names = [item["name"] for item in self.ruleData]
    dropdown = DropDown(items=names)
    alert(content=dropdown,
      title="Please select a rule type",
      dismissible=False)
    return dropdown.selected_value
  
  def new_rule_click(self, otherSelf, **event_args):
    option = self.get_rule_selection()
    self.add_new_rule(option, otherSelf or self)
  
  def run_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.runSet()

  def includeNodes_change(self, **event_args):
    self.rule_group.tag["include"]["node"] = event_args["sender"].checked

  def includeWays_change(self, **event_args):
    self.rule_group.tag["include"]["way"] = event_args["sender"].checked

  def includeRelations_change(self, **event_args):
    self.rule_group.tag["include"]["relation"] = event_args["sender"].checked

  def save_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.saveSet()

  def return_click(self, **event_args):
    if self.dirty:
      if not confirm("All unsaved changes will be lost. Are you sure?"):
        return
    open_form("Home")

  def delete_rule_click(self, **event_args):
    newState = not hoverTracking.getState()
    hoverTracking.setEnabled(newState)
    if newState:
      self.delete_rule.icon = "fa:trash"
    else:
      self.delete_rule.icon = "fa:trash-o"

  def renew_ression_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    print("Renewing session...")
    with anvil.server.no_loading_indicator:
      call_async("renew_session").on_result(lambda a: print("Session renewed"))
