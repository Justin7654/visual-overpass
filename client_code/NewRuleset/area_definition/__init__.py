from ._anvil_designer import area_definitionTemplate
from anvil import *
import m3.components as m3
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class area_definition(area_definitionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.tag = {
      "area_definition":  True,
      "group1": self.rule_group
    }

  def key_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass
