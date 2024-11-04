from ._anvil_designer import rule_or_groupTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class rule_or_group(rule_or_groupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.tag = {
      "type": "OR",
      "group1": self.rule_group_1,
      "group2": self.rule_group_2,
    }
    self.rule_group_1.tag = {"rule_group": True}
    self.rule_group_2.tag = {"rule_group": True}

    # Any code you write here will run before the form opens.
