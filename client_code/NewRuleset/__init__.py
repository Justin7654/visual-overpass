from ._anvil_designer import NewRulesetTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class NewRuleset(NewRulesetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.structure = {}

    #Find the rules
    ruleData = {
      
    }

  def add_new_rule(self, ruleTemplate):
    pass
  
  def new_rule_click(self, **event_args):
    """This method is called when the button is clicked"""
    NewRUle
    self.parent.add_component()
