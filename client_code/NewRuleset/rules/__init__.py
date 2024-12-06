import anvil.server
from .rule_match_tag import rule_match_tag
from .rule_has_tag import rule_has_tag
from .rule_intersects import rule_intersects
from .rule_or_group import rule_or_group
from .rule_newer_than import rule_newer_than

def get_all_rule_data():
  def genRuleData(form, name):
    return {
      "form": form,
      "name": name
    }
  #Find the rules    
  #copy = rule_has_tag()
  
  #print(copy.layout.slots['content'].get_components())
  
  return [
    genRuleData(rule_match_tag, "Match Tag"),
    genRuleData(rule_has_tag, "Has Tag"),
    genRuleData(rule_intersects, "Intersects"),
    genRuleData(rule_or_group, "OR"),
    genRuleData(rule_newer_than, "Newer Than")
  ]
