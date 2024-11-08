from ._anvil_designer import RowRulesetTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import ruleParser


class RowRulesetTemplate(RowRulesetTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def ruleset_edit_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("NewRuleset")

  def ruleset_run_click(self, **event_args):
    """This method is called when the button is clicked"""
    data = self.item
    structure = data["savedStructure"]
    parsed = ruleParser.parse(structure, data["topLayerIncludeTypes"], [])
    print(parsed)
