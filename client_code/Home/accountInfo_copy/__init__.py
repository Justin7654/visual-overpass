from ._anvil_designer import accountInfo_copyTemplate
from anvil import *
import m3.components as m3
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
from anvil import users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class accountInfo_copy(accountInfo_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    # Add the users email text
    user = users.get_user()
    email = user["email"]
    self.user_email.text = email
    # Hide "Change Password" if they dont use a password to login
    if user["password_hash"] is None:
      self.change_password.visible = False

  def log_out_click(self, **event_args):
    """This method is called when the component is clicked."""
    users.logout
    anvil.server.reset_session()
    anvil.server.call("renew_session")  # Get the popup to appear

  def change_password_click(self, **event_args):
    """This method is called when the component is clicked."""
    users.change_password_with_form(require_old_password=True)
