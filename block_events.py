import requests
import secrets
import datetime
from notion_headers import headers
from pprint import pprint


req = requests.get(
    f'https://api.notion.com/v1/blocks/{secrets.EVENTS_BLOCK_ID}', headers=headers)

pprint(req.json())
print("=============================================================")

req2 = requests.patch(
    f'https://api.notion.com/v1/blocks/{secrets.EVENTS_BLOCK_ID}',
    headers=headers,
    json={'archived': False,
          'created_time': '2022-01-24T23:15:00.000Z',
          'has_children': False,
          'heading_3': {'text': [{'annotations': {'bold': False,
                                                  'code': False,
                                                  'color': 'default',
                                                  'italic': False,
                                                  'strikethrough': False,
                                                  'underline': False},
                                  'href': None,
                                  'plain_text': 'yolo',
                                  'text': {'content': 'yolo', 'link': None},
                                  'type': 'text'}]},
          'id': '1e710c29-40b8-4ae6-b34a-38b6d9a42051',
          'last_edited_time': '2022-01-24T23:32:00.000Z',
          'object': 'block',
          'type': 'heading_3'})

pprint(req2.json())
