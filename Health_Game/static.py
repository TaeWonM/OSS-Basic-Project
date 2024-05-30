import json
import datetime as dt


# This method makes json file for recode
# It contains times and exercise recodes
def get_statious():
    # variable that contains time data
    now = dt.datetime.now()
    # variable that contains recodes which is in json file
    health_data = []
    # variable to check current date
    flag = False
    # Add try statement for exception
    try:
        # statement to open staticsitc.json file
        with open("src\\staticsitc.json", "r", encoding="utf-8-sig") as json_file:
            # statement to get recodes in staticsitc.json file and find current date
            health_data = json.load(json_file)
            for i in range(0, len(health_data)):
                if (
                    health_data[i]["year"] == now.year
                    and health_data[i]["month"] == now.month
                    and health_data[i]["day"] == now.day
                ):
                    flag = True
        # statement to make current recode if it doesn't have current recode
        if not flag:
            with open("src\\staticsitc.json", "w", encoding="utf-8-sig") as json_file:
                temp_health_data = {
                    "year": now.year,
                    "month": now.month,
                    "day": now.day,
                    "Upper_body": 0,
                    "Lower_body": 0,
                }
                health_data.append(temp_health_data)
                json.dump(health_data, json_file, indent=4)
        return health_data
    # exception will be occured by having no data in staticsitc.json file
    except:
        # Add new recode for frist starters
        with open("src\\staticsitc.json", "w", encoding="utf-8-sig") as json_file:
            temp_health_data = {
                "year": now.year,
                "month": now.month,
                "day": now.day,
                "Upper_body": 0,
                "Lower_body": 0,
            }
            health_data.append(temp_health_data)
            json.dump(health_data, json_file, indent=4)
            return health_data


# This method write json file for recode
# It contains times and exercise recodes
def set_statious(data):
    # variable that contains recodes which is in json file
    health_data = []
    with open("src\\staticsitc.json", "r", encoding="utf-8-sig") as json_file:
        # if statement for checking same data and write json file into recode
        health_data = json.load(json_file)
        for i in range(0, len(health_data)):
            if (
                health_data[i]["year"] == data["year"]
                and health_data[i]["month"] == data["month"]
                and health_data[i]["day"] == data["day"]
            ):
                health_data[i] = data
    with open("src\\staticsitc.json", "w", encoding="utf-8-sig") as json_file:
        json.dump(health_data, json_file, indent=4)


# This method write json file for recode about empty data
# It contains times and exercise recodes
def nomalization_statious():
    # variable that contains recodes which is in json file
    health_data = []
    # statement to get recodes in staticsitc.json file
    with open("src\\staticsitc.json", "r", encoding="utf-8-sig") as json_file:
        health_data = json.load(json_file)
        first = dt.datetime(
            year=health_data[0]["year"],
            month=health_data[0]["month"],
            day=health_data[0]["day"],
        )
        # variable to add one day frist recode
        first = first + dt.timedelta(days=1)
        # variable to check health_data's lengh
        i = 1
        # statement write json file for recode about empty data
        while i < len(health_data):
            if (
                health_data[i]["year"] != first.year
                or health_data[i]["month"] != first.month
                or health_data[i]["day"] != first.day
            ):
                temp = {
                    "year": first.year,
                    "month": first.month,
                    "day": first.day,
                    "Upper_body": 0,
                    "Lower_body": 0,
                }
                health_data.insert(i, temp)
                first += dt.timedelta(days=1)
            else:
                first += dt.timedelta(days=1)
            i += 1
    with open("src\\staticsitc.json", "w", encoding="utf-8-sig") as json_file:
        json.dump(health_data, json_file, indent=4)
