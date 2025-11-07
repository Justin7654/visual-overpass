from ._anvil_designer import leafletMapTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

next_id = 1

class leafletMap(leafletMapTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    global next_id
    self.id = next_id
    next_id += 1
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    map_id = f"leafmap-{self.id}"
    self.mapDiv = self.dom_nodes["leaflet-div"]
    self.mapDiv.setAttribute("id", map_id)
    self.mapDiv.setAttribute("for", map_id)
    self.load_map()
    
  def load_map(self):
    renderAt = self.mapDiv
    leaf = anvil.js.window.leaflet
    map = leaf.map(renderAt).setView([0, 0], 1)
    leaf.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      "maxZoom": 19,
      "attribution": '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map)
    
    self.map = map
  
  def reset_map(self):
    self.map.off()
    self.map.remove()
    self.load_map(self.map_placeholder)

  @property
  def leafmap(self):
    return self.map