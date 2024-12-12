from ._anvil_designer import rule_groupTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class rule_group(rule_groupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.rule_group.tag = {
      "rule_group": True,
      "include": {
        "node":self.allow_nodes,
        "way":self.allow_ways,
        "relation":self.allow_relations,
      }
    }      

  def includeNodes_change(self, **event_args):
    self.rule_group.tag["include"]["node"] = event_args["sender"].checked

  def includeWays_change(self, **event_args):
    self.rule_group.tag["include"]["way"] = event_args["sender"].checked

  def includeRelations_change(self, **event_args):
    self.rule_group.tag["include"]["relation"] = event_args["sender"].checked
    
