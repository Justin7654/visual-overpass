from ._anvil_designer import NewRulesetTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#UI
from .new_rule_button import new_rule_button

#Rules
from .rule_match_tag import rule_match_tag
from .rule_has_tag import rule_has_tag

class NewRuleset(NewRulesetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.ruleStructure = {}

    def genRuleData(form, name):
      return {
        "form": form,
        "name": name
      }
    #Find the rules
    self.ruleData = [
      genRuleData(rule_match_tag, "Match Tag"),
      genRuleData(rule_has_tag, "Has Tag")
    ]
    
    #Add plus (TODO: Convert to function)
    self.rule_group.tag = {"rule_group": True}
    print(self.rule_group)
    self.initRuleGroups(self)
    
    #self.add_new_plus(self.ruleset_group)

  def initRuleGroups(self, form):
    #print("Starting")
    children = form.get_components()
    #print("Children: ",children)
    for child in children:
      print(child)
      try:
        child.get_components()
      except AttributeError:
        pass
      else:
        self.initRuleGroups(child)
        
      try:
        if hasattr(child.tag, '__iter__') and "rule_group" in child.tag:
          print("Child: ",child)
          print("1")
          child = form[child]
          print("2")
          self.add_new_plus(child)
      except TypeError as e: #TypeError: 'ColumnPanel' does not support indexing
        print(child,"was compatible but failed because:",e)
        
  
  
  def add_new_plus(self, form):
    newRuleButton = new_rule_button()
    newRuleButton.raise_event("x-hookClick", func=self.new_rule_click)
    form.add_component(newRuleButton)
  
  def add_new_rule(self, name):
    foundRule = None
    for rule in self.ruleData:
      if rule["name"] == name:
        foundRule = rule
        break
    else:
      exit("No rule found with that name")

    #Make the UI
    currentSize = len(self.ruleset_linear_panel.get_components()) #Use custom index to keep the plus at the bottom
    copy = foundRule["form"]()
    self.initRuleGroups(copy)
    self.ruleset_linear_panel.add_component(copy, index=currentSize-1)
    return copy

  def get_rule_selection(self):
    names = [item["name"] for item in self.ruleData]
    dropdown = DropDown(items=names)
    alert(content=dropdown,
      title="Please select a rule type",
      dismissible=False)
    return dropdown.selected_value


  def new_rule_click(self, **event_args):
    """This method is called when the button is clicked"""
    option = self.get_rule_selection()
    self.add_new_rule(option)
