from ._anvil_designer import rule_newer_thanTemplate
from anvil import *

#Example quarry:
#https://overpass-turbo.eu/?q=LyoKVGhpcyBoYcSGYmVlbiBnxI1lcmF0ZWQgYnkgdGhlIG92xJJwxIlzLXR1cmJvIHdpemFyZC7EgsSdxJ9yaWdpbmFsIHNlxLBjaMSsxIk6CsOiwoDCnMSEZ2h3YXk9KsWIwp0KKi8KW291dDpqc29uXVt0aW1lxZrFnDI1XTsKLy_Ej8SUxJ1yIHJlc3VsdHMKKAogIMWvIHF1xJLEmsSjcnQgZm9yOiDFiMWKxLjFjcWPxZHFk8W_IG5vZGVbIsWLxpR5Il0obmV3xJI6IjIwMTctxq3GsDFUMDA6xrXGtzBaIikoe3tixKp4fX0pxa3GgMWOecaexqDHicajxqXGp8apxqvGrcavxrHGrca0xrbGuMa1xrvGvca_x4Fvx4PHhceHxbVlbMSUacWgx4vGk8eNxqTGpsaoxo7HksauxrLGsseXxrnGucebxr7HgMeCx4THhgrHvMaCcMS3bsaKxbbFuMW6xbzFqMSYxpt5xa0-xa3IiHNrx6TGg3Q7&c=CITEGLvHTP

class rule_newer_than(rule_newer_thanTemplate):
  def __init__(self, lastTag=False, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.tag = {
      "type": "Newer Than",
      "date": self.date_picker.date,
    }
    
    if lastTag:
      self.date_picker.date = lastTag["date"]
      self.notSwitch_change()

  def date_picker_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.tag["date"] = self.date_picker.date
    print(type(self.date_picker.date))
