from ._anvil_designer import NewRulesetTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import ruleParser

#UI
from .new_rule_button import new_rule_button

#Rules
from .rule_match_tag import rule_match_tag
from .rule_has_tag import rule_has_tag
from .rule_intersects import rule_intersects

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
      genRuleData(rule_intersects, "Intersects")
    ]
    
    self.rule_group.tag = {"rule_group": True}
    self.initRuleGroups(self)
    
    #self.add_new_plus(self.ruleset_group)

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
        #if its iterable (avoid error), has the rule_group key in its tag, and isn't already setup
        if hasattr(child.tag, '__iter__') and "rule_group" in child.tag:
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
  
  def add_new_rule(self, name, form):
    # Adds a new rule form in the specified location. Name is the user-friendly name of the target rule.
    foundRule = None
    for rule in self.ruleData:
      if rule["name"] == name:
        foundRule = rule
        break
    else:
      exit("No rule found with that name")

    #Make the UI
    currentSize = len(form.get_components()) #Use custom index to keep the plus at the bottom
    copy = foundRule["form"]()
    self.initRuleGroups(copy)
    form.add_component(copy, index=currentSize-1)
    return copy

  def get_rule_selection(self):
    names = [item["name"] for item in self.ruleData]
    dropdown = DropDown(items=names)
    alert(content=dropdown,
      title="Please select a rule type",
      dismissible=False)
    return dropdown.selected_value


  def new_rule_click(self, otherSelf, **event_args):
    option = self.get_rule_selection()
    print(otherSelf)
    self.add_new_rule(option, otherSelf or self)
  
  def run_click(self, **event_args):
    """This method is called when the button is clicked"""
    ruleParser.get_structure(self, self)
