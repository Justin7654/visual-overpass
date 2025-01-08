from ._anvil_designer import RunRulesetTemplate
from .OutModeSelector import OutModeSelector
from anvil import *
import anvil.server
import time
import json
from .. import ruleParser


class RunRuleset(RunRulesetTemplate):
  def __init__(self, structure={}, topIncludes={"node":True,"way":True,"relation":True}, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.progress = []
    self.dots = 0
    self.structure = structure
    self.topIncludes = topIncludes

  def form_show(self, **event_args):
    #Get the output mode
    self.loading.visible = False
    options = {"mode":"body","recurse_down":True}
    promptForm = OutModeSelector(item=options)
    chooseDefault = alert(content=promptForm, large=True, dismissible=False, buttons=[("Select",False),("Choose for me",True)])
    if chooseDefault:
      options = {"mode":"body","recurse_down":True}

    
    #Start processing
    self.loading.visible = True
    #Decompress structure if needed
    if str(type(self.structure)) == "<class 'anvil.LazyMedia'>":
      self.addProgress("Decompressing")
      self.structure = anvil.server.call("decompress_dict", self.structure)
      self.appenedLastProgress("... done")
    print("------------- PARSING STRUCTURE ----------------")
    self.addProgress("Parsing structure")
    startTime = time.time()
    #Add a rescurse statement at the end to get nodes inside ways and then the out mode
    parsed =  ruleParser.parse(self.structure, self.topIncludes, [])
    totalTime = (time.time() - startTime)*1000
    self.appenedLastProgress(f'... done ({totalTime:.0f}ms)')
    print("Parse final result:", parsed, sep="\n")
    #Modify the parsed string to include a recurse down if selected
    if options["recurse_down"]:
      parsed += '(._;>;);'
    print("-------------- STARTING QUARY -----------------")
    print("Sending:\n"+str(parsed))
    self.addProgress("Connecting to server")
    try:
      with anvil.server.no_loading_indicator:
        self.task = anvil.server.call_s("runQuary", parsed, options["mode"])
    except anvil.server.RuntimeUnavailableError as err:
      self.progressDots.interval = 0
      self.appenedLastProgress("... "+str(err))
      print(err)
      self.loading.visible = False
      return
    #Set up a timer
    self.appenedLastProgress("... done")
    self.addProgress("Waiting for Overpass API")
    self.recheckTask.interval = 0.2
  
  def onTaskSuccess(self):
    self.appenedLastProgress("... done")
    self.addProgress("Receiving data")
    resultLocation = self.task.get_return_value()
    self.resultFile = anvil.server.call_s("getDataOutput", resultLocation)
    self.result = self.parse_file(self.resultFile)
    self.appenedLastProgress("... done")
    self.addProgress("Processing results")
    self.geojsonFile = anvil.server.call_s('generateGeoJson', self.resultFile)
    print("Received geojson")
    self.geojson = self.parse_file(self.geojsonFile)
    print("Parsed successfully")
    if not self.geojson:
      #Handle a potential error
      print("Error!")
      return self.start_error(errorText="Error occurred while converting to geojson")
    print("Opening RulesetResult form")
    open_form("RulesetResult", json=self.result, geojson=self.geojson)

  def onTaskFail(self):
    self.appenedLastProgress("... "+self.errMessage)
    self.loading.visible = False
    self.progressDots.interval = 0
    #self.addProgress("Attempting alternate method") #Use users browser to send request
  
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
    if not task.is_running():
      self.recheckTask.interval = 0
      state = task.get_termination_status()
      print("Finish state:",state)
      if state == "completed":
        #self.taskReturn = task.get_return_value()
        return self.onTaskSuccess()
      elif state == "failed":
        try:
          task.get_error()
        except Exception as err:
          msg = str(err)
          Notification("A error occured: "+msg,title="error",style="warning",timeout=10).show()
          self.errMessage = msg
          print(err)
      elif state == "killed":
        Notification("Quary task was killed",title="error",style="warning",timeout=4).show()
      elif state == "missing":
        Notification("Quary task went missing. This is most likely caused by an outage with our hosting provider",title="missing",timeout=4).show()
      self.onTaskFail()

  def progressDots_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    #Loop dot amount
    self.dots += 1
    if self.dots >= 4:
      self.dots = 1
    #Create a string with the amount of dots, and append it to the current progress text
    #Dont change self.progress
    dotsToAppend = "."*self.dots
    self.progressText.text = "\n".join(self.progress) + dotsToAppend

  def abort_click(self, **event_args):
    confirmed = confirm("Are you sure you would like to abort this quary?")
    if confirmed:
      #Cancel the background task if needed
      if hasattr(self, "task") and self.task is not None and self.task.is_running():
        print("Cancelling background task")
        anvil.server.call("cancelQuary", self.task)
      print("Exiting")
      self.recheckTask.interval = 0
      self.progressDots.interval = 0
      open_form("Home")

  def start_error(self, errorText="error"):
    print("Error:",errorText)
    self.appenedLastProgress("... "+errorText)
    self.progressDots.interval = 0
    self.abort.text = "Exit"

  def parse_file(self, file):
    return json.loads(file.get_bytes().decode('utf-8'))
