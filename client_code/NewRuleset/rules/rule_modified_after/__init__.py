from ._anvil_designer import rule_modified_afterTemplate
from anvil import *
import datetime

#Example quarry:
#https://overpass-turbo.eu/?q=LyoKVGhpcyBoYcSGYmVlbiBnxI1lcmF0ZWQgYnkgdGhlIG92xJJwxIlzLXR1cmJvIHdpemFyZC7EgsSdxJ9yaWdpbmFsIHNlxLBjaMSsxIk6CsOiwoDCnMSEZ2h3YXk9KsWIwp0KKi8KW291dDpqc29uXVt0aW1lxZrFnDI1XTsKLy_Ej8SUxJ1yIHJlc3VsdHMKKAogIMWvIHF1xJLEmsSjcnQgZm9yOiDFiMWKxLjFjcWPxZHFk8W_IG5vZGVbIsWLxpR5Il0obmV3xJI6IjIwMTctxq3GsDFUMDA6xrXGtzBaIikoe3tixKp4fX0pxa3GgMWOecaexqDHicajxqXGp8apxqvGrcavxrHGrca0xrbGuMa1xrvGvca_x4Fvx4PHhceHxbVlbMSUacWgx4vGk8eNxqTGpsaoxo7HksauxrLGsseXxrnGucebxr7HgMeCx4THhgrHvMaCcMS3bsaKxbbFuMW6xbzFqMSYxpt5xa0-xa3IiHNrx6TGg3Q7&c=CITEGLvHTP

#nwr["name"="River Oaks Drive"](changed:"2000-01-01T00:00:00Z","2008-12-09T00:00:00Z");

class rule_modified_after(rule_modified_afterTemplate):
  def __init__(self, lastTag=False, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.tag = {
      "type": "Newer Than",
      "not": False,
      "year": 0,
      "month": 0,
      "day": 0
    }
    
    if lastTag:
      self.date_picker.date = datetime.date(lastTag["year"], lastTag["month"], lastTag["day"])
      self.notSwitch.checked = lastTag["not"]
      self.notSwitch_change()

  def date_picker_start_change(self, **event_args):
    """This method is called when the selected date changes"""
    date = self.date_picker.date
    self.tag["year"] = date.year
    self.tag["month"] = date.month
    self.tag["day"] = date.day
    print(type(self.date_picker.date))