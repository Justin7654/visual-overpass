from ._anvil_designer import RunRulesetTemplate
from anvil import *
import anvil.server
import time
from .. import ruleParser


class RunRuleset(RunRulesetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.progress = []
    self.structure = properties["structure"]
    self.topIncludes = properties["topIncludes"]

  def form_show(self, **event_args):
    print("---------------- PARSING MAIN -------------------")
    self.addProgress("Parsing structure... ")
    startTime = time.time()
    parsed = ruleParser.parse(self.structure, self.topIncludes, []) + "out body;"
    totalTime = (time.time() - startTime)*1000
    self.appenedLastProgress(f'done ({totalTime:.0f}ms)')
    print("----------------- PARSE RESULT ------------------")
    self.addProgress("Waiting for Overpass API... ")
    with anvil.server.no_loading_indicator:
      self.task = anvil.server.call("runQuary", parsed)
    #Set up a timer
    self.recheckTask.interval = 0.2
  
  def onTaskSuccess(self):
    self.appenedLastProgress("done")
    self.addProgress("Processing results... ")

  def onTaskFail(self):
    self.appenedLastProgress("error")
    self.addProgress("Attempting alternate method...") #Use users browser to send request
  
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
      state = task.get_termination_status()
      if state == "completed":
        self.taskReturn = task.get_return_value()
        return self.onTaskSuccess()
      elif state == "failed":
        Notification("A unknown error occured",title="error",style="warning",timeout=4).show()
      elif state == "killed":
        Notification("Quary task was unexpectedly killed",title="error",style="warning",timeout=4).show()
      elif state == "missing":
        Notification("Quary task went missing. This is most likely caused by issues with our hosting provider",title="missing",timeout=4).show()
      self.onTaskFail()