from ._anvil_designer import RunRulesetTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RunRuleset(RunRulesetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.progress = []
    self.structure = properties["structure"]
    self.topIncludes = properties["topIncludes"]

  def addProgress(self, text):
    self.progress.append(text)
    self.progressText.text = self.progress.join("\n")