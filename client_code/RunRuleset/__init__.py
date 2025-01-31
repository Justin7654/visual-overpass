from ._anvil_designer import RunRulesetTemplate
from .OutModeSelector import OutModeSelector
from .AreaSelector import AreaSelector
from anvil import *
import anvil.server
import anvil.users
import time
import json
from .. import ruleParser
from anvil_extras import non_blocking


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
    
    #Get the search area
    searchAreaItems = {"mode":"global", "locationName":"","mapBounds":""}
    promptForm = AreaSelector(item=searchAreaItems)
    alert(content=promptForm, large=True, dismissible=False, buttons=[("Continue")])
    areaMode = searchAreaItems["mode"]
    
    #Start processing
    self.loading.visible = True
    #Decompress structure if needed
    if str(type(self.structure)) == "<class 'anvil.LazyMedia'>":
      self.addProgress("Decompressing")
      self.structure = anvil.server.call("decompress_dict", self.structure)
      self.appendLastProgress("... done")
    print("------------- PARSING STRUCTURE ----------------")
    self.addProgress("Parsing structure")
    startTime = time.time()
    #Add a rescurse statement at the end to get nodes inside ways and then the out mode
    parsed =  ruleParser.parse(self.structure, self.topIncludes, [])
    totalTime = (time.time() - startTime)*1000
    self.appendLastProgress(f'... done ({totalTime:.0f}ms)')
    print("Parse final result:", parsed, sep="\n")
    #Modify the parsed string to include a recurse down if selected
    if options["recurse_down"]:
      parsed += '(._;>;);'
    if areaMode == "bbox":
      parsed = f'[out:json][bbox:{searchAreaItems["mapBounds"]}];'+parsed
    elif areaMode == "location":
      print("Location mode")
    else:
      parsed = '[out:json];'+parsed
    print("-------------- STARTING QUARY -----------------")
    print("Sending:\n"+str(parsed))
    self.addProgress("Connecting to server")
    def onResponse(response):
      if isinstance(response, str) or isinstance(response, int):
        self.onTaskSuccess(self.task)
      else:
        #Set up the timer to repeatedly check if its done
        self.appendLastProgress("... done")
        self.addProgress("Waiting for Overpass API")
        self.task = response
        self.recheckTask.interval = 0.2
    def onFailure(err):
      self.start_error(str(err))
    try:
      with anvil.server.no_loading_indicator:
        run_call = non_blocking.call_async("runQuary", parsed, options["mode"], anvil.users.get_user())
        run_call.on_result(onResponse, onFailure)
    except anvil.server.RuntimeUnavailableError as err:
      self.progressDots.interval = 0
      self.appendLastProgress("... "+str(err))
      print(err)
      self.loading.visible = False
      return
  def runOnAnvilServer(self):
    pass
  
  def onTaskSuccess(self, resultLocation):
    self.appendLastProgress("... done")
    self.addProgress("Receiving data")
    self.resultFile = anvil.server.call_s("getDataOutput", resultLocation)
    self.result = self.parse_file(self.resultFile)
    self.appendLastProgress("... done")
    self.addProgress("Processing results")
    self.geojsonFile = anvil.server.call_s('generateGeoJson', self.resultFile)
    print("Received geojson")
    self.geojson = self.parse_file(self.geojsonFile)
    open_form("RulesetResult", json=self.result, geojson=self.geojson, jsonMedia=self.resultFile, geojsonMedia=self.geojsonFile)

  def onTaskFail(self):
    self.appendLastProgress("... "+self.errMessage)
    self.loading.visible = False
    self.progressDots.interval = 0
    #self.addProgress("Attempting alternate method") #Use users browser to send request
  
  def addProgress(self, text):
    self.progress.append(text)
    self.progressText.text = "\n".join(self.progress)
  def appendLastProgress(self, text):
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
        return self.onTaskSuccess(task.get_return_value())
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
        self.errMessage = "Quary task was killed"
      elif state == "missing":
        Notification("Quary task went missing. This is most likely caused by an outage with our hosting provider",title="missing",timeout=4).show()
        self.errMessage = "Quary task went missing"
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
    self.appendLastProgress("... "+errorText)
    self.progressDots.interval = 0
    self.abort.text = "Exit"

  def parse_file(self, file):
    try:
      return json.loads(file.get_bytes().decode('utf-8'))
    except AttributeError as err: #If the file isn't a file and doesn't have get_bytes
      print("Could not parse file:",str(err))
      return None
