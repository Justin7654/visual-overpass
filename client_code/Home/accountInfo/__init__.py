from ._anvil_designer import accountInfoTemplate
from anvil import *
import m3.components as m3
import anvil.server
import anvil.users
from anvil import users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js as js

class accountInfo(accountInfoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.update_details()

  def update_details(self):
    user = users.get_user()
    if user is None:
      self.user_email.visible = False
      self.change_password.visible = False
      self.log_out.visible = False
      self.log_in.visible = True
    else:
      #Email
      email = user["email"]
      self.user_email.text = email
      # Hide "Change Password" if they dont use a password to login
      if user["password_hash"] is None:
        self.change_password.visible = False
      #Visible
      self.log_out.visible = True
      self.log_in.visible = False

  def refresh_page(self):
    anvil.server.reset_session()
    js.window.location.reload()
  
  def log_out_click(self, **event_args):
    users.logout()
    self.refresh_page()

  def change_password_click(self, **event_args):
    users.change_password_with_form(require_old_password=True)

  def log_in_click(self, **event_args):
    users.login_with_form(allow_cancel=True)
    if users.get_user() is not None:
      self.refresh_page()
    

