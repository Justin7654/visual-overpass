from ._anvil_designer import rule_match_tagTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class rule_match_tag(rule_match_tagTemplate):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.tag = {
      "type": "Match Tag",
      "key": "",
      "value": "",
      "not": False,
      "requiredTextInputs": [self.key, self.value]
    }

    # Any code you write here will run before the form opens.

  def key_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.tag["key"] = self.key.text

  def value_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.tag["value"] = self.value.text

  def notSwitch_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.tag["not"] = self.notSwitch.checked
