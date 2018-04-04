import requests

def getIndexForActivity (system_indices, activity):
    for index in system_indices.get("cost_indices")[:]:
        if index["activity"] == activity:
            return index["cost_index"]

def getNameForSystemId (system_id):
    system_url = 'https://esi.tech.ccp.is/latest/universe/systems/' + repr(system_id) + '/?datasource=tranquility&language=en-us'
    system_response = requests.get(system_url);
    system_json = system_response.json();
    return system_json["name"]

def getActivityIndexForAlliance (alliance_id, activity, topX):
    sovereignty_url = 'https://esi.tech.ccp.is/latest/sovereignty/map/?datasource=tranquility'
    indices_url = 'https://esi.tech.ccp.is/latest/industry/systems/?datasource=tranquility'
    sovereignty_response = requests.get(sovereignty_url)
    sovereignty_json = sovereignty_response.json()

    alliance_systems = [x["system_id"] for x in sovereignty_json if x.get("alliance_id", 0) == alliance_id]

    indices_response = requests.get(indices_url)
    indices_json = indices_response.json()

    alliance_indices = [x for x in indices_json if x["solar_system_id"] in alliance_systems]
    alliance_indices.sort(key=lambda x: getIndexForActivity(x, activity), reverse=True)

    for index in alliance_indices[:topX]:
        print('System:' + getNameForSystemId(index["solar_system_id"]) + ' Manufacturing Index:' + repr(getIndexForActivity(index, activity)))


alliance_id = 99003214
activity = "manufacturing"

getActivityIndexForAlliance(alliance_id, activity, 5)
