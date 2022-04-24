
import requests

from db_models.plugins import PluginModel


def instagram_make_response( plugin: PluginModel , target):
    base_link = plugin.link
    link = '{}{}/'.format(base_link  , target)
    res = None
    try:
        res = requests.get(link , timeout=20)
    except requests.exceptions.Timeout:
        return [405,"Request Timeout"]
    if res.status_code == 403:
        return [403,"Plugin Token incorrcet"]
    if res.status_code == 200:
        return [200,link]
    elif res.status_code == 404:
        return [404 , '']
    else:
        return [res.status_code , "Unkown Error"]