from ._anvil_designer import RulesetResultTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.js

class RulesetResult(RulesetResultTemplate):
  def __init__(self, json=None, geojson=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
   
    # Any code you write here will run before the form opens.
    self.json = json
    self.geojson = geojson
    self.export_menu.visible = False
    self.export_menu.raise_event("x-hook", otherSelf=self)
    self.set_event_handler("x-export-geojson", self.export_geojson)
    self.set_event_handler("x-export-json", self.export_json)
    self.set_event_handler("x-export-kml", self.export_kml)

  def export_geojson(self, **args):
    if self.geojson is None:
      return Notification("GeoJSON exporting not supported with current output", style="warning").show()
    
    file = BlobMedia("application/geo+json", self.geojson, name="exported.geojson")
    anvil.download(file)


  def export_json(self, **args):
    import json
    if self.json is None:
      return Notification("JSON exporting not supported with current information", style="warning").show()

    print(self.json)
    file = BlobMedia("application/json", json.dumps(self.json).encode(), name="exported.json")
    anvil.download(file)

  def export_kml(self, **args):
    from geo2kml import to_kml
    if self.geojson is None:
      return Notification("KML exporting not supported with current output", style="warning").show()
    file = BlobMedia("application/vnd.google-earth.kml+xml", to_kml(self.geojson), name="exported.kml")
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


    
