from ._anvil_designer import rule_has_tagTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class rule_has_tag(rule_has_tagTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.tag = {
      "type": "Has Tag",
      "key": "",
    }
    self.key.tag = {
      "required": True
    }

    # Any code you write here will run before the form opens.

  def key_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.tag["key"] = self.key.text
