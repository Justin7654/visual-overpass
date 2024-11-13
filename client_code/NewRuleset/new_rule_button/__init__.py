from ._anvil_designer import new_rule_buttonTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class new_rule_button(new_rule_buttonTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.clickHook = lambda: 1+1
    self.add_event_handler("x-hookClick", self.clickHooker)

  def clickHooker(self, sender, event_name, func):
    #print("Successfully received event x-hookClick. Hooking click event")
    self.clickHook = func

  def add_rule_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.clickHook(otherSelf=self.parent, **event_args)
