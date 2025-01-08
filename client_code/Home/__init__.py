from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.users
import anvil.server

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
      
    # Any code you write here will run before the form opens.
    self.serverFails = 0
    if anvil.users.get_user() is None:
      alert("This is used to keep track of your saved sets, and to track who to send the output data to when running a ruleset. The login "+
            "process is handled securely by Anvil",title="Login Required", large=True)
      anvil.users.login_with_form(allow_cancel=False, allow_remembered=True, remember_by_default=True)
      
      #anvil.users.logout()
    self.ruleset_repeating_panel.add_event_handler('x-delete-ruleset', self.delete_ruleset)

  def loadRulesets(self, data):
    self.ruleset_repeating_panel.items = data
    if len(data) == 0:
      self.no_saved.visible = True
    else:
      self.no_saved.visible = False
  
  def new_ruleset_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('NewRuleset', preset=False)

  def ruleset_datagrid_show(self, **event_args):
    with anvil.server.loading_indicator(self.ruleset_repeating_panel, min_height=100):
      #self.loadRulesets()
      try:
        result = anvil.server.call("getUserRulesets")
      except anvil.users.AuthenticationFailed:
        Notification("Must be logged in to show this information", title="ERR: 401 Unauthorized", style="warning").show()
        anvil.users.login_with_form(allow_cancel=False)
        return self.ruleset_datagrid_show()
      except (anvil.server.RuntimeUnavailableError, anvil.server.AppOfflineError) as err:
        self.serverFails += 1
        if self.serverFails <= 2:
          print("Retrying... attempt ",self.serverFails)
          return self.ruleset_datagrid_show()
        else:
          notifStr = "An error occured while loading your data. Please refresh the page or try again later.\
          \n\nRuntimeUnavailableError: "+str(err)
          Notification(notifStr, title="Unexpected Server Error", style="warning", timeout=15).show()
          self.serverFails = 0
          return #self.ruleset_datagrid_show()
          #return anvil.server.reset_session()
      self.loadRulesets(result)

  def delete_ruleset(self, sender, event_name, item):
    if confirm(f'Do you really want to delete: {item["name"]}?'):
      anvil.server.call("deleteRuleset", item)
      #refresh the Data Grid
      self.ruleset_datagrid_show()