from ._anvil_designer import OutModeSelectorTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class OutModeSelector(OutModeSelectorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    INCLUDES_TYPE = "Includes the objects type"
    INCLUDES_ID = "Includes the objects ID"
    INCLUDES_LOCATION = "Includes the objects location"
    INCLUDES_TAGS = "Includes the objects tags"
    INCLUDES_META = "Includes the objects current version number and information on the last changeset that edited it"
    
    DOES_NOT_INCLUDE_TYPE = "Does not include the objects type"
    DOES_NOT_INCLUDE_ID = "Does not include the objects ID"
    DOES_NOT_INCLUDE_LOCATION = "Does not include the objects location"
    DOES_NOT_INCLUDE_TAGS = "Does not include the objects tags"
    DOES_NOT_INCLUDE_META = "Does not include the objects current version number and information on the last changeset that edited it"
    
    
    
    # Any code you write here will run before the form opens.
    self.textData = {
      "id": {
        "pros": [INCLUDES_TYPE, INCLUDES_ID, "Fastest processing time"],
        "cons": [DOES_NOT_INCLUDE_LOCATION, DOES_NOT_INCLUDE_TAGS, DOES_NOT_INCLUDE_META]
      },
      "skel": {
        "pros": [INCLUDES_TYPE, INCLUDES_ID, INCLUDES_LOCATION],
        "cons": [DOES_NOT_INCLUDE_TAGS, DOES_NOT_INCLUDE_META]
      },
      "body": {
        "pros": [INCLUDES_TYPE, INCLUDES_ID, INCLUDES_LOCATION, INCLUDES_TAGS],
        "cons": [DOES_NOT_INCLUDE_META]
      },
      "tags": {
        "pros": [INCLUDES_TYPE, INCLUDES_ID, INCLUDES_TAGS],
        "cons": [DOES_NOT_INCLUDE_LOCATION, DOES_NOT_INCLUDE_META]
      },
      "meta": {
        "pros": [INCLUDES_TYPE, INCLUDES_ID, INCLUDES_LOCATION, INCLUDES_TAGS, INCLUDES_META],
        "cons": ["Large amount of data", "Long processing time"]
      }
    }
    
  def setContents(self, pros, cons):
    proText = ""
    conText = ""
    for pro in pros:
      proText += "+ "+pro+"\n"
    for con in cons:
      conText += "- "+con+"\n"
      
    self.pros.text = proText
    self.cons.text = conText
  
  def mode_change(self, **event_args):
    """This method is called when an item is selected"""
    mode = self.mode.selected_value
    if mode in self.textData:
      self.setContents(self.textData[mode]["pros"], self.textData[mode]["cons"])

  def mode_show(self, **event_args):
    """This method is called when the component is shown on the screen."""
    self.mode.selected_value = "body"
    self.mode_change()
