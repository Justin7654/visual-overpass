import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import OSMPythonTools

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable(require_user=True)
def getUserRulesets():
  currentUser = anvil.users.get_user()
  if currentUser is None:
    return
  return app_tables.user_rulesets.search(
    tables.order_by("date", ascending=False),
    user = currentUser
  )
  

@anvil.server.callable(require_user=True)
def saveRuleset(name, structure, topLayerIncludes):
  if name == "":
    name = "Unnamed Ruleset"
  user = anvil.users.get_user()
  date = datetime.now()
  app_tables.user_rulesets.add_row(
    user=user,
    date=date,
    name=name,
    savedStructure=structure,
    topLayerIncludeTypes=topLayerIncludes
  )

@anvil.server.callable(require_user=True)
def deleteRuleset(record):
  pass

@anvil.server.background_task()
def runQuaryTask(quaryText):
  pass