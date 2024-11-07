from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
      
    # Any code you write here will run before the form opens.
    #anvil.users.login_with_form(allow_cancel=False, allow_remembered=True, remember_by_default=True)
    #with anvil.server.loading_indicator(self.saved_datagrid):
      #self.loadHistory()
    
    with anvil.server.loading_indicator(self.saved_datagrid):
      #self.loadRulesets()
      result = anvil.server.call("getUserRulesets")
      self.loadRulesets(result)
      

  def loadHistory(self):
    pass  

  def addNewHistoryItem(self):
    pass

  def loadRulesets(self):
    
  
  def new_ruleset_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('NewRuleset')
    
