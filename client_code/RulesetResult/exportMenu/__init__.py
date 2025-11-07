from ._anvil_designer import exportMenuTemplate
from anvil import *
import m3.components as m3
import anvil.server


class exportMenu(exportMenuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.set_event_handler("x-hook", self.hook)

  def hook(self, otherSelf=False, **event_args):
    self.otherSelf = otherSelf
    
  
  def export_geojson_click(self, **event_args):
    print("Export geojson click")
    print(self.parent)
    self.otherSelf.raise_event("x-export-geojson")
    

  def export_json_click(self, **event_args):
    self.otherSelf.raise_event("x-export-json")

  def export_kml_click(self, **event_args):
    self.otherSelf.raise_event("x-export-kml")
    
