from ._anvil_designer import NewRulesetTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from datetime import datetime
from anvil.tables import app_tables
from .. import ruleParser

#UI
from .new_rule_button import new_rule_button
from .operation_text import operation_text

#Rules
from .rule_match_tag import rule_match_tag
from .rule_has_tag import rule_has_tag
from .rule_intersects import rule_intersects
from .rule_or_group import rule_or_group

class NewRuleset(NewRulesetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.colorDepths = []
    
    def genRuleData(form, name):
      return {
        "form": form,
        "name": name
      }
    #Find the rules    
    self.ruleData = [
      genRuleData(rule_match_tag, "Match Tag"),
      genRuleData(rule_has_tag, "Has Tag"),
      genRuleData(rule_intersects, "Intersects"),
      genRuleData(rule_or_group, "OR")
    ]
    
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
      exit("No rule found with the name '"+name+"'")

    #Make the and/or text
    currentSize = len(form.get_components()) #Use custom index to keep the plus at the bottom
    if currentSize > 1:
      operationText = operation_text()
      form.add_component(operationText, index=currentSize-1)
      currentSize += 1
    
    #Make the UI
    copy = foundRule["form"](lastTag=preset)
    self.initRuleGroups(copy)
    form.add_component(copy, index=currentSize-1)
    self.dirty = True
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
    if self.saveRow != None:
      buttons = [("Overwrite", "overwrite"),("Create New", "new"),("Cancel",None)]
      mode = confirm("Would you like to overwrite the existing set?", buttons=buttons, dismissible=True)
    #
    structure = ruleParser.get_structure(self.rule_group)
    name = self.ruleset_name.text.strip()
    if len(structure) == 0:
      return False
    if not anvil.server.is_app_online():
      alert("Connect to the internet and try again later", title="No Internet")
      return False
    anvil.server.call("saveRuleset", name, structure, self.rule_group.tag["include"])
    Notification("Saved").show()
    self.dirty = False
    
  def loadSet(self, data):
    self.saveRow = data
    savedStructure = data["savedStructure"]
    topIncludes = data["topLayerIncludeTypes"]
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
    success = self.saveSet()
    #if success or success is None:
      #self.runSet()

  def return_click(self, **event_args):
    if self.dirty:
      if not confirm("All unsaved changes will be lost. Are you sure?"):
        return
    open_form("Home")
