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
    self.add_new_plus(self.content_panel)

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
    copy = foundRule['form']()
    self.add_component(copy)
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
