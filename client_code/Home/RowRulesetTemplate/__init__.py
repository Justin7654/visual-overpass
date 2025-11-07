from ._anvil_designer import RowRulesetTemplateTemplate
from anvil import *
import m3.components as m3
import anvil.users
import anvil.server
from ... import ruleParser


class RowRulesetTemplate(RowRulesetTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.blocked = False

  def ruleset_edit_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.blocked:
      self.blocked = True
      open_form("NewRuleset", preset=self.item)

  def ruleset_run_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.blocked:
      return
    self.blocked = True
    data = self.item
    print("Open")
    structure = data["savedStructure"]
    if structure is None:
      structure = data["savedStructure_legacy"]
    open_form("RunRuleset", structure=structure, topIncludes=data["topLayerIncludeTypes"])

  def ruleset_delete_click(self, **event_args):
    self.parent.raise_event("x-delete-ruleset",item=self.item)

