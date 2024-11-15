from ._anvil_designer import rule_match_tagTemplate
from anvil import *


class rule_match_tag(rule_match_tagTemplate):
  def __init__(self, lastTag=False, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.tag = {
      "type": "Match Tag",
      "key": "",
      "value": "",
      "not": False,
    }
    if lastTag:
      self.key.text = lastTag["key"]
      self.value.text = lastTag["value"]
      self.notSwitch.checked = lastTag["not"]
      self.key_change()
      self.value_change()
      self.notSwitch_change()
    # Any code you write here will run before the form opens.

  def key_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.key.text = self.key.text.lstrip()
    self.tag["key"] = self.key.text

  def value_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.value.text = self.value.text.lstrip()
    self.tag["value"] = self.value.text

  def notSwitch_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.tag["not"] = self.notSwitch.checked
