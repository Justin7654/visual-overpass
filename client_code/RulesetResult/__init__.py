from ._anvil_designer import RulesetResultTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.js

class RulesetResult(RulesetResultTemplate):
  def __init__(self, json={}, geojson={}, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
   
    # Any code you write here will run before the form opens.
    self.json = json
    self.geojson = geojson

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    renderAt = anvil.js.get_dom_node(self.map_placeholder)
    leaf = anvil.js.window.leaflet
    map = leaf.map(renderAt).setView([0, 0], 1)
    leaf.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      "maxZoom": 19,
      "attribution": '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map)
    self.geoLayer = leaf.geoJSON(self.geojson)
    self.geoLayer.addTo(map)
    #try:
    map.fitBounds(self.geoLayer.getBounds())
    #except:
    self.map = map


    
