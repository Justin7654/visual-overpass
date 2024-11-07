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
    anvil.users.login_with_form(allow_cancel=False, allow_remembered=True, remember_by_default=True)
      

  def loadHistory(self):
    pass  

  def addNewHistoryItem(self):
    pass

  def loadRulesets(self, data):
    print(data)
  
  def new_ruleset_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('NewRuleset')

  def ruleset_datagrid_show(self, **event_args):
    with anvil.server.loading_indicator(self.ruleset_datagrid):
      #self.loadRulesets()
      try:
        result = anvil.server.call("getUserRulesets")
      except anvil.users.AuthenticationFailed:
        Notification("Must be logged in to show this information", title="ERR: 401 Unauthorized", style="warning").show()
        anvil.users.login_with_form(allow_cancel=False)
        return self.ruleset_datagrid_show()
      self.loadRulesets(result)
    
