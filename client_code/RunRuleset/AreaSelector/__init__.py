from ._anvil_designer import AreaSelectorTemplate
from anvil import *
import anvil.server
import anvil.js

class AreaSelector(AreaSelectorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load_map(self.map_location)

  def load_map(self, renderAt):
    renderAt = anvil.js.get_dom_node(renderAt)
    leaf = anvil.js.window.leaflet
    map = leaf.map(renderAt).setView([0, 0], 1)
    leaf.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      "maxZoom": 19,
      "attribution": '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map)
    renderAt.height = 700
    
    self.map = map

  def reset_map(self):
    self.map.off()
    self.map.remove()
    self.load_map(self.map_placeholder)

  def mode_change(self, **event_args):
    """This method is called when an item is selected"""
    mode = self.mode.selected_value
    if mode in self.textData:
      self.setContents(self.textData[mode]["pros"], self.textData[mode]["cons"])

  def mode_show(self, **event_args):
    """This method is called when the component is shown on the screen."""
    self.mode.selected_value = "global"
    self.mode_change()
