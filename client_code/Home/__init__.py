from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.users
import anvil.server
from ..RunRuleset.AreaSelector import AreaSelector
from .accountInfo import accountInfo
from anvil_extras import popover
from anvil_extras.storage import local_storage

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
      
    # Any code you write here will run before the form opens.
    self.serverFails = 0
    self.buttonsBlocked = False
    if local_storage.get("visited") is None and anvil.users.get_user() is None:
      anvil.users.login_with_form(allow_cancel=True, allow_remembered=True, remember_by_default=True)
      if anvil.users.get_user() is None:
        anvil.alert("Loading in anomalous mode. Your querys may not be as secure and you will not "+
                   "be able to save data between sessions. To login in the future, click the "+
                   "profile icon on the top right of the home screen.")
    local_storage["visited"] = True
    self.ruleset_repeating_panel.add_event_handler('x-delete-ruleset', self.delete_ruleset)
    self.account_button.popover(content=accountInfo(), placement="auto", trigger="click")
    anvil.users
  def loadRulesets(self, data):
    self.ruleset_repeating_panel.items = data
    if len(data) == 0:
      self.no_saved.visible = True
    else:
      self.no_saved.visible = False
  
  def new_ruleset_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.buttonsBlocked:
      self.buttonsBlocked = True
      open_form('NewRuleset', preset=False)

  def ruleset_datagrid_show(self, **event_args):
    #Make sure they are logged in
    if anvil.users.get_user() is None:
      self.not_logged_in.visible = True
      return
    else:
      self.not_logged_in.visible = False
    #Load the data
    with anvil.server.loading_indicator(self.ruleset_repeating_panel, min_height=100):
      try:
        result = anvil.server.call("getUserRulesets")
      except anvil.users.AuthenticationFailed:
        Notification("AuthenticationFailed error while getting saved rulesets", title="ERR: 401 Unauthorized", style="warning").show()
        #anvil.users.login_with_form(allow_cancel=False)
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
    self.buttonsBlocked = True
    if not self.buttonsBlocked and confirm(f'Do you really want to delete: {item["name"]}?'):
      anvil.server.call("deleteRuleset", item)
      #refresh the Data Grid
      self.ruleset_datagrid_show()
      self.buttonsBlocked = False