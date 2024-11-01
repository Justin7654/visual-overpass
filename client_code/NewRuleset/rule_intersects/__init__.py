from ._anvil_designer import rule_intersectsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
#How it can work:
#area[name="London"]->.small;
#area[name="England"]->.big;
#nwr[shop=supermarket](area.small)(area.big);

class rule_intersects(rule_intersectsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.tag = {
      "type": "Intersects",
      "not": False,
      "group1": self.rule_group_1,
      "group2": self.rule_group_2
    }
    self.rule_group_1.tag = {"rule_group": True}
    self.rule_group_2.tag = {"rule_group": True}

    # Any code you write here will run before the form opens.

  def notSwitch_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.tag["not"] = self.notSwitch.checked
