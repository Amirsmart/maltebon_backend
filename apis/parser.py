from apis.github import github_make_response
from apis.instagram import instagram_make_response
from apis.linkedin import linkedin_make_response
from apis.phone import phone_make_response
from apis.telegram import telegram_make_response
from apis.whois import whois_make_response
from db_models.plugins import PluginCrudModel, PluginModel
from db_models.users import UserModel


def parse_plugin_request(user: UserModel , plugin: PluginModel , crud: PluginCrudModel , param1 , param2 , param3 ):
    name = plugin.p_name
    if name == 'whois':
        return whois_make_response(crud.param1 , plugin  , param1 , param2)
    elif name == 'github':
        return github_make_response(plugin , param1)
    elif name == 'instagram':
        return instagram_make_response(plugin , param1)
    elif name == 'telegram':
        return telegram_make_response(plugin , param1)
    elif name == 'phone':
        return phone_make_response(plugin , param1)
    elif name == 'linkedin':
        return linkedin_make_response(plugin  , param1)