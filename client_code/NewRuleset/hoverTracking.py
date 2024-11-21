hovering = []
default_color = None
enabled = False

def setEnabled(bool):
  global enabled
  enabled = bool

def getState():
  global enabled
  return enabled

def onHoverEnter(item):
  global default_color
  hovering.append(item)

  if default_color is None:
    default_color = item.outlined_card_1.background
  
  update_colors()
  print("Start hover")

def onHoverEnd(item):
  global default_color
  try:
    item.outlined_card_1.background = default_color
    hovering.remove(item)
    update_colors()
    print("Exit hover")
  except ValueError:
    print("(onHoverEnd) WARNING: item is not in list")
  
def update_colors():
  global default_color
  global enabled

  if not enabled:
    return
  
  prim = get_primary()
  for i in hovering:
    if i == prim:
      i.outlined_card_1.background = "red"
    else:
      i.outlined_card_1.background = default_color

def get_primary():
  if len(hovering) == 0:
    return None
  return hovering[-1]

def printDebug():
  print(hovering)