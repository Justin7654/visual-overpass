from ._anvil_designer import deletable_cardTemplate
from anvil_extras import augment


class deletable_card(deletable_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
  
    # Any code you write here will run before the form opens.
    augment.add_event_handler(self, "hover", self.hover)

  def hover(self, **event_args):
    print("Hover")
    print(event_args)
