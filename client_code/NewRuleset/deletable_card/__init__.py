import anvil.server
from ._anvil_designer import deletable_cardTemplate
import m3.components as m3
from anvil_extras import augment
from .. import hoverTracking


class deletable_card(deletable_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
  
    # Any code you write here will run before the form opens.
    augment.add_event_handler(self, "mouseenter", self.hoverStart)
    augment.add_event_handler(self, "mouseleave", self.hoverEnd)
    augment.add_event_handler(self, "click", self.onClick)
    
    self.tag.deleted = False
    self.tag.onDeleteCallback = False
    #TODO: Check parent children to remove AND
    

  def hoverStart(self, **event_args):
    hoverTracking.onHoverEnter(self)

  def hoverEnd(self, **event_args):
    hoverTracking.onHoverEnd(self)

  def onClick(self, **event_args):
    if hoverTracking.getState() and self == hoverTracking.get_primary():
      if self.tag.onDeleteCallback:
        self.tag.onDeleteCallback()
      else:
        print("No external callback found")
      
      self.clear()
      self.remove_from_parent()
      self.tag.deleted = True
      print("Run main delete")
      
