import requests
import secrets
import datetime
from notion_headers import headers

def get_db_query_url(database_id):
    return f"https://api.notion.com/v1/databases/{database_id}/query"

def get_page_update_url(page_id):
    return f"https://api.notion.com/v1/pages/{page_id}"


def get_schedules():
    return requests.post(get_db_query_url(secrets.NOTION_SCHEDULE_ID), headers=headers)


def get_schedule(schedules, day_of_week, branch_id):
    for s in schedules:
        number = s['properties']['Jour']['number']
        relation = ''.join([title["id"]
                            for title in s['properties']['Branche']['relation']])

        if number == day_of_week and relation == branch_id:
            return s
    return None


def get_homeworks():
    # Get the homework database
    response = requests.post(get_db_query_url(secrets.NOTION_HOMEWORK_ID), headers=headers, json={
        "filter": {
                "and": [
                    {
                        "property": "U",
                        "checkbox": {
                            "equals": False
                        }
                    }
                ]
            }
    })
    homeworks_data = response.json()

    # dict to return
    homeworks = {}

    schedules = get_schedules().json()['results']

    # For each homework
    for h in homeworks_data['results']:
        # Get the homework title
        h_props = h['properties']

        id = h['id']
        branch_id = [relation["id"]
                     for relation in h_props['Branche']['relation']][0]
        title = ''.join([title["plain_text"]
                        for title in h_props['Nom']['title']])
        date = datetime.datetime.fromisoformat(
            h_props['Date']['date']['start'])
        gcal_id = ''.join([title["plain_text"]
                           for title in h_props['Gcal ID']['rich_text']])
        try:
            state = h_props['État']['status']['name']
        except TypeError:
            state = 'a faire'
        evaluated = h_props['E']['checkbox']

        # Get the day of the week of the homework
        day_of_week = date.weekday()

        # Get the schedule from the branch id and the day of the homework
        schedule = get_schedule(schedules, day_of_week, branch_id)
        try:
            schedule_properties = schedule['properties']

            time_start = ''.join([title["plain_text"]
                                for title in schedule_properties['Heure debut']['rich_text']])
            time_end = ''.join([title["plain_text"]
                                for title in schedule_properties['Heure fin']['rich_text']])
        except TypeError:
            # There is no lesson of this branch this day
            # Set the homeworks to be at the beginning of the day
            time_start = '7:30'
            time_end = '8:15'

        homework = {
            'title': title,
            'state': state,
            'evaluated': evaluated,
            'date': date.strftime('%Y-%m-%d'),
            'hour_start': time_start,
            'hour_end': time_end,
            'gcal_id': gcal_id
        }

        homeworks[id] = homework

    return homeworks

def update_gcal_id(notion_hw_id, gcal_hw_id):
    response = requests.patch(get_page_update_url(notion_hw_id), headers=headers, json={
        "properties": {
                "Gcal ID": {
                    'type' : 'rich_text',
                    'rich_text': [{
                        'type': 'text',
                        'text': {
                            'content': gcal_hw_id,
                            'link': None
                        },
                        'plain_text': gcal_hw_id,
                        'annotations': {
                            'bold': False,
                            'italic': False,
                            'strikethrough': False,
                            'underline': False,
                            'code': False,
                            'color': 'default'
                        }
                    }]
                }
            }
    })