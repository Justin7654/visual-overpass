from ._anvil_designer import operation_textTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server


class operation_text(operation_textTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
