from ._anvil_designer import AreaSelectorTemplate
from anvil import *
import anvil.server
import anvil.js

class AreaSelector(AreaSelectorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.leaflet.visible = self.radio_bbox.selected

  def getBoundingArea(self):
    '''
    nwr(51.477,-0.001,51.478,0.001);
    Here (51.477,-0.001,51.478,0.001) represents the bounding box. The order of the edges is always the same:

    51.477 is the latitude of the southern edge.
    -0.001 is the longitude of the western edge.
    51.478 is the latitude of the norther edge.
    0.001 is the longitude of the eastern edge.
    '''
    bounds = self.leaflet.leafmap.getBounds()
    south = min(max(bounds.getSouth(),-90),90) #Returns the south latitude of the bounds
    west = min(max(bounds.getWest(),-180),180) #Returns the west longitude of the bounds
    north = min(max(bounds.getNorth(),-90),90) #Returns the north latitude of the bounds
    east = min(max(bounds.getEast(),-180),180) #Returns the east longitude of the bounds
    return f'{south},{west},{north},{east}'
  
  def radio_global_select(self, **event_args):
    """This method is called when the radio button is selected."""
    self.leaflet.visible = False
    self.map_hint.visible = False
    self.locationName.visible = False
    self.divider.visible = False

  def radio_bbox_select(self, **event_args):
    """This method is called when the radio button is selected."""
    self.leaflet.visible = True
    self.map_hint.visible = True
    self.locationName.visible = False
    self.divider.visible = True

  def update_bounds_tick(self, **event_args):
    if self.leaflet.visible:
      self.item["mapBounds"] = self.getBoundingArea()
      self.leaflet.map.invalidateSize() #Fixes a weird issue where you have to resize your browser window in order for all tiles to load

  def radio_area_select(self, **event_args):
    """This method is called when the radio button is selected."""
    self.leaflet.visible = False
    self.map_hint.visible = False
    self.locationName.visible = True
    self.divider.visible = True