from ._anvil_designer import AreaSelectorTemplate
from anvil import *
import anvil.server
import anvil.js

class AreaSelector(AreaSelectorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print(self.leaflet.leafmap)

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
    south = bounds.getSouth()
    west = bounds.getWest()
    north = bounds.getNorth()
    east = bounds.getEast()
    return f'({south},{west},{north},{east})'
  
  def radio_global_select(self, **event_args):
    """This method is called when the radio button is selected."""
    self.leaflet.visible = False

  def radio_bbox_select(self, **event_args):
    """This method is called when the radio button is selected."""
    self.leaflet.visible = True

  def update_bounds_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.item["mapBounds"] = self.getBoundingArea()

  def radio_geocode_select(self, **event_args):
    """This method is called when the radio button is selected."""
    self.leaflet.visible = False
