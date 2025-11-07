from ._anvil_designer import rule_has_tag_oldTemplate
from anvil import *
import m3.components as m3
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class rule_has_tag_old(rule_has_tag_oldTemplate):
  def __init__(self, lastTag=False, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    self.tag = {
      "type": "Has Tag",
      "key": "",
      "not": False,
    }
    if lastTag:
      self.key.text = lastTag["key"]
      self.notSwitch.checked = lastTag["not"]
      self.key_change()
      self.notSwitch_change()

  def key_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.tag["key"] = self.key.text.lstrip()
    self.key.text = self.tag["key"] #Prevent white space

  def notSwitch_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.tag["not"] = self.notSwitch.checked
 