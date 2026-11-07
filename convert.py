import json


# convert json string to a Python list of dates and requirements from RFP from ask.py
def convert_json_to_list(json_string):
    try:
        # parse the JSON string into a Python list
        data = json.loads(json_string)
        
        # check if the parsed data is a list
        if isinstance(data, list):
            return data
        else:
            print("The provided JSON string does not represent a list.")
            return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []


json_data = """ [
  {"event": "RFP issued", "date": "Monday, June 8, 2026"},
  {"event": "Questions from candidates to AIC deadline (email to procurement@aicanada.ca)", "date": "Monday, July 13, 2026 at 5:00 PM"},
  {"event": "Closing date", "date": "Thursday, July 23, 2026 at 5:00 PM ET"}
] """

dates_list = convert_json_to_list(json_data)

# go through the list one deadline at a time
for item in dates_list:
    print(f"Event: {item['event']}, Date: {item['date']}")