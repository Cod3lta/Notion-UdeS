import notion
import gcal
import json

def main():

    gcal.init_gcal()

    """*******************************************\
    |*      1. Get the homeworks from notion     *|
    \*******************************************"""
    print("Getting Notion datas...")

    hw_notion = notion.get_homeworks()
    hw_data = {}
    hw_to_add = []
    hw_to_remove = []
    hw_to_edit = []


    """*******************************************\
    |*      2. Get the JSON data file            *|
    \*******************************************"""
    print("Getting the JSON file datas...")

    try:
        with open('data.json', 'r') as fp:
            hw_data = json.load(fp)
    except FileNotFoundError:
        # No data file found
        print("No JSON data file found - writing a new one")
        with open('data.json', 'w') as fp:
            pass #json.dump(hw_notion, fp)
    except json.JSONDecodeError:
        # Error while reading the JSON data file
        print("Error while reading the JSON data file")
    

    """*******************************************\
    |*      3. process every homework and        *|
    |*         build the resulting dicts         *|
    \*******************************************"""
    print("Processing the datas...")

    # Homeworks to add
    for key, value in hw_notion.items():
        # If the homework exists in notion but not in the JSON file
        if key not in hw_data:
            # This is a new homework
            value['notion_id'] = key
            hw_to_add.append(value)
    
    # Homeworks to remove
    for key, value in hw_data.items():
        # If the homework exists in notion but not in the JSON file
        if key not in hw_notion:
            # This is a homework to remove
            value['notion_id'] = key
            hw_to_remove.append(value)
    
    # Homeworks to edit
    for key, value in hw_notion.items():
        if key in hw_data:
            # This homeworks already existed
            if value != hw_data[key]:
                hw_to_edit.append(value)
    
        

    # 4. Parse the dict and send to Google Calendar

    """*******************************************\
    |*      4. Send the modifications to GCal    *|
    |*         and update the Notion Database    *|
    \*******************************************"""
    print("Adding the events to Gcal and Updating Notion...")

    # Events to add
    for h in hw_to_add:
        gcal_event_id = gcal.add_hw(h)
        notion.update_gcal_id(h['notion_id'], gcal_event_id)
        hw_notion[h['notion_id']]['gcal_id'] = gcal_event_id
    
    # Events to remove
    for h in hw_to_remove:
        gcal.remove_hw(h['gcal_id'])
        notion.update_gcal_id(h['notion_id'], "")

    # Events to edit
    for h in hw_to_edit:
        gcal.edit_hw(h)


    print("Homeworks to add --------------------------------\n" + str(hw_to_add))
    print("Homeworks to edit -------------------------------\n" + str(hw_to_edit))
    print("Homeworks to remove -----------------------------\n" + str(hw_to_remove))


    """*******************************************\
    |*      5. Save the Notion homeworks         *|
    |*         in the JSON file                  *|
    \*******************************************"""
    with open('data.json', 'w') as fp:
        json.dump(hw_notion, fp)


if __name__ == '__main__':
    main()