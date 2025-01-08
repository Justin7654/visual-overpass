import anvil.server

@anvil.server.callable
def getKeyList():
  import taginfo
  page1 = taginfo.query.get_page_of_all_keys_with_wiki_page(1)
  page2 = taginfo.query.get_page_of_all_keys_with_wiki_page(2)
  keys = page1+page2
  keys = [item['key'] for item in keys if 'key' in item]
  return keys

@anvil.server.callable
def getValueListForKey(key):
  import taginfo
  MIN_COUNT = 1000
  MAX_AMOUNT = 50
  
  page1 = taginfo.query.get_page_of_key_values(key, 1)
  values = [item['value'] for item in page1[:MAX_AMOUNT] if 'value' in item and item['count'] > MIN_COUNT]  
  return values
  