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
    self.export_menu.visible = False
    self.set_event_handler("x-export-geojson", self.export_geojson)
    self.set_event_handler("x-export-json", self.export_json)
    self.set_event_handler("x-export-geojson", self.export_kml)

  def export_geojson(self):
    file = BlobMedia("application/geo+json", None, name="exported.geojson")
    anvil.download(file)


  def export_json(self):
    file = BlobMedia("application/json", None, name="exported.json")
    anvil.download(file)

  def export_kml(self):
    file = BlobMedia("application/vnd.google-earth.kml+xml", None, name="exported.kml")
    anvil.download(file)
  
  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    renderAt = anvil.js.get_dom_node(self.map_placeholder)
    leaf = anvil.js.window.leaflet
    map = leaf.map(renderAt).setView([0, 0], 1)
    leaf.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      "maxZoom": 19,
      "attribution": '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map)
    if self.geojson:
      self.geoLayer = leaf.geoJSON(self.geojson)
      self.geoLayer.addTo(map)
      map.fitBounds(self.geoLayer.getBounds())
    else:
      Notification("Map will not show previews because the current output mode does not include object locations", title="Locations unavailable", style="warning")
    
    self.map = map

  def return_click(self, **event_args):
    open_form("Home")

  def tabs_tab_click(self, tab_index, tab_title, **event_args):
    """This method is called when a tab is clicked"""
    self.export_menu.visible = False
    self.map_placeholder.visible = False
    if tab_index == 1:
      self.export_menu.visible = True
    else:
      self.map_placeholder.visible = True


    
