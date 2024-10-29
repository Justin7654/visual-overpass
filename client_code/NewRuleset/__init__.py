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

class NewRuleset(NewRulesetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.ruleStructure = {}

    def genRuleData(form, name):
      return {
        "form": rule_match_tag,
        "name": name
      }
    #Find the rules
    self.ruleData = [
      genRuleData(rule_match_tag, "Match Tag")
    ]

    #Add plus (TODO: Convert to function)
    newRuleButton = new_rule_button()
    newRuleButton.new_rule.handle_click = self.new_rule_click
    self.content_panel.add_component(newRuleButton)


  def add_new_rule(self, name):
    foundRule = None
    for rule in self.ruleData:
      if rule["name"] == name:
        foundRule = rule
        break
    else:
      exit("No rule found with that name")

    #Make the UI
    copy = foundRule['form']()
    self.add_component(copy)

    #Update the structure
    
  def get_rule_selection(self):
    dropdown = DropDown()
  
  def new_rule_click(self, **event_args):
    """This method is called when the button is clicked"""
    print(event_args)
    self.add_component("Match Tag")
    #self.add_new_rule("rule_match_tag")
