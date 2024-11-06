import anvil.facebook.auth
def match_tag(tags):
    quary = ""
    for tag in tags:
        key = tag.get("key")
        value = tag.get("value")
        is_not = tag.get("not", False)
        
        if is_not:
          quary += f'[!"{key}"="{value}"]'
        else:
          quary += f'["{key}"="{value}"]'
    
    # Join all parts with an empty string (no space) to form the Overpass API query
    return quary+";

def has_tag(list):
  pass

def intersects(list):
  pass

def OR(list):
  pass