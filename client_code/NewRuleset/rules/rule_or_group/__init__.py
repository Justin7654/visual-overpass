from ._anvil_designer import rule_or_groupTemplate
from anvil import *
import m3.components as m3
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class rule_or_group(rule_or_groupTemplate):
  def __init__(self, lastTag=False, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.tag = {
      "type": "OR",
      "group1": self.rule_group_1.rule_group,
      "group2": self.rule_group_2.rule_group,
    }
    # Any code you write here will run before the form opens.
