

from db_models.plugins import PluginModel
from linkedin_api import Linkedin , client

def linkedin_make_response( plugin: PluginModel , target):
    base_link = plugin.link
    api = None
    try:
        api = Linkedin('gaxafa1258@krunsea.com', '85859090')
    except client.ChallengeException :
        return [405,"Api Challenge Excepted"]
    except Exception as e:
        return [500 , 'Unknown Error']
        
    res = None
    try:
        #res = api.get_profile(target)
        res = api.search_people(target )
        if str(res) == '{}':
            return [404 , '']
        return [200 , res]
    except Exception as e:
        print(e)
        return [405,"Api Error"]
    # if res.status_code == 403:
    #     return [403,"Plugin Token incorrcet"]
    # if res.status_code == 200:
    #     res = res.json()
    #     if "message" in res:
    #         if res["message"] == "Not Found":   # Just to be double sure
    #             return [404 , ['']]
    #     return [200,link]
    # elif res.status_code == 404:
    #     return [404 , '']
    # else:
    #     return [res.status_code , "Unkown Error"]