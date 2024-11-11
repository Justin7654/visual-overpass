from ._anvil_designer import RunRulesetTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import ruleParser


class RunRuleset(RunRulesetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.progress = []
    self.structure = properties["structure"]
    self.topIncludes = properties["topIncludes"]
    print("---------------- PARSING MAIN -------------------")
    self.addProgress("Parsing structure... ")
    parsed = ruleParser.parse(self.structure, self.topIncludes, [])
    self.appenedLastProgress("done")
    print("----------------- PARSE RESULT ------------------")
    self.addProgress("Waiting for Overpass API... ")
    with anvil.server.no_loading_indicator:
      self.task = anvil.server.call("runQuary", parsed)
    #Set up a timer
    self.recheckTask.interval = 0.2
  def onTaskSuccess(self):
    self.appenedLastProgress("done")
    self.addProgress("Processing... ")
  
  def addProgress(self, text):
    self.progress.append(text)
    self.progressText.text = "\n".join(self.progress)
  def appenedLastProgress(self, text):
    self.progress[-1] += text
    self.progressText.text = "\n".join(self.progress)
  def editLastProgress(self, text):
    self.progress[-1] = text
    self.progressText.text = "\n".join(self.progress)

  def recheckTask_tick(self, **event_args):
    if self.task is None:
      return
    task = self.task
    print("Task State:",task.get_termination_status())
    if task.is_completed():
      self.recheckTask.interval = 0
      task.get_error()
      self.taskReturn = task.get_return_value()
      print("Task complete detected")
      self.onTaskSuccess()
