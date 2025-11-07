from ._anvil_designer import RulesetResultTemplate
from anvil import *
import m3.components as m3
import anvil.server
import anvil.users
import anvil.js

class RulesetResult(RulesetResultTemplate):
  def __init__(self, json=None, geojson=None, jsonMedia=None, geojsonMedia=None,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.json = json
    self.jsonMedia = jsonMedia
    self.geojson = geojson
    self.geojsonMedia = geojsonMedia
    self.kml = None
    self.export_menu.visible = False
    self.export_menu.raise_event("x-hook", otherSelf=self)
    self.set_event_handler("x-export-geojson", self.export_geojson)
    self.set_event_handler("x-export-json", self.export_json)
    self.set_event_handler("x-export-kml", self.export_kml)

  def export_geojson(self, **args):
    import json
    if self.geojson is None:
      return Notification(
        "GeoJSON exporting not supported with current output mode (requires location data)", style="warning").show()
    
    file = BlobMedia("application/geo+json", self.geojsonMedia.get_bytes(), name="exported.geojson")
    anvil.download(file)


  def export_json(self, **args):
    import json
    if self.json is None:
      return Notification("JSON exporting not supported with current information", style="warning").show()

    file = BlobMedia("application/json", json.dumps(self.json).encode(), name="exported.json")
    anvil.download(file)

  def export_kml(self, **args):
    if self.geojson is None:
      return Notification("KML exporting not supported with current output mode (requires location data)", style="warning").show()
    if self.kml is None:
      self.kml = anvil.server.call("generateKmlMediafromGeoJson", self.geojsonMedia, "exported.kml")
    anvil.download(self.kml)
  
  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    MAX_SIZE = 2_000_000 #2mb
    if not self.geojson or len(self.geojsonMedia.get_bytes()) < MAX_SIZE:
      self.load_map(self.map_placeholder)
    elif self.geojson:
      size = str(len(self.geojsonMedia.get_bytes())/1_000_000)
      buttons = [("Render Anyways",True), ("Continue without map",False)]
      confirmed = confirm(content="Result is too big to automatically render on the map for performance reasons. ("+size+"mb)", buttons=buttons,large=True)
      if confirmed and confirm("Are you sure? If theres enough data, this may freeze the tab.",dismissible=False):
        self.load_map(self.map_placeholder)
  def load_map(self, renderAt):
    renderAt = anvil.js.get_dom_node(renderAt)
    leaf = anvil.js.window.leaflet
    map = leaf.map(renderAt).setView([0, 0], 1)
    leaf.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      "maxZoom": 19,
      "attribution": '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map)
    if self.geojson:      
      def onClick(e):
        '''
        type: 
        id: 
        tags: {
          dict with key being key and value being value
        }
        '''
        #https://runebook.dev/en/articles/leaflet/index/geojson-click
        clickedFeature = e.layer.feature["properties"]
        htmlContent = '<h3>Tags</h3><h5>'
        for key in clickedFeature["tags"].keys():
          value = clickedFeature["tags"][key]
          htmlContent += f'<br>{key+": "+value}'
        htmlContent += "</h5>"
        leaf.popup(e.latlng, {"content":htmlContent}).openOn(map)

      self.geoLayer = leaf.geoJSON(self.geojson)
      self.geoLayer.on("click", onClick)
      self.geoLayer.addTo(map)

      try:
        map.fitBounds(self.geoLayer.getBounds())
      except:
        pass
        '''Uncaught TypeError: Cannot read properties of undefined (reading '_leaflet_pos')
    at getPosition (leaflet:2563:14)
    at NewClass._getMapPanePos (leaflet:4601:12)
    at NewClass._getNewPixelOrigin (leaflet:4618:69)
    at NewClass._move (leaflet:4337:30)
    at NewClass._onZoomTransitionEnd (leaflet:4839:10)
      '''
    else:
      Notification("Map will not show previews because the current output mode does not include object locations", title="Locations unavailable", style="warning")
    
    self.map = map
  
  def reset_map(self):
    self.map.off()
    self.map.remove()
    self.load_map(self.map_placeholder)
    
  
  def return_click(self, **event_args):
    open_form("Home")

  def tabs_tab_click(self, tab_index, tab_title, **event_args):
    """This method is called when a tab is clicked"""
    self.export_menu.visible = False
    self.map_placeholder.visible = False
    self.map_reset.visible = False
    if tab_index == 1:
      self.export_menu.visible = True
    else:
      self.map_placeholder.visible = True
      self.map_reset.visible = True

  def map_reset_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.map_reset.enabled = False
    self.reset_map_cooldown.interval = 1
    self.reset_map()

  def reset_map_cooldown_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.reset_map_cooldown.interval = 0
    self.map_reset.enabled = True


    
