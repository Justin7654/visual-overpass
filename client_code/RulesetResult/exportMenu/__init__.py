from ._anvil_designer import exportMenuTemplate
from anvil import *


class exportMenu(exportMenuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def export_geojson_click(self, **event_args):
    self.parent.raise_event("x-export-geojson")

  def export_json_click(self, **event_args):
    self.parent.raise_event("x-export-json")

  def export_kml_click(self, **event_args):
    self.parent.raise_event("x-export-kml")
    
