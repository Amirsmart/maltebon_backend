from re import search
import resources
from resources.account import *
from resources.plugins import PluginCrud, PluginUse
from resources.session import *
from resources.payment import *
from db_models.plugins import init_plugins
from tools.string_tools import gettext


def init_endpoints(api, engine, mail, mail_username,config):
    init_plugins(engine)

    api.add_resource(login, gettext("url_login"), endpoint="login", resource_class_kwargs={'engine': engine})
    api.add_resource(refresh_login, gettext("url_refresh_login"), endpoint="refresh_login", resource_class_kwargs={'engine': engine})
    api.add_resource(register, gettext("url_register"), endpoint="register", resource_class_kwargs={'engine': engine, 'mail': mail, 'mail_username': mail_username})
    api.add_resource(logout, gettext("url_logout"), endpoint="logout", resource_class_kwargs={'engine': engine})

    api.add_resource(myprofile, gettext("url_myprofile"), endpoint="myprofile", resource_class_kwargs={'engine': engine, 'mail': mail, 'mail_username': mail_username})
    api.add_resource(fname, gettext("url_fname"), endpoint="fname" , resource_class_kwargs={'engine': engine})
    api.add_resource(password, gettext("url_change_pass"), endpoint="changepassword", resource_class_kwargs={'engine': engine})
    api.add_resource(bio, gettext("url_change_bio"), endpoint="changebio", resource_class_kwargs={'engine': engine})
    api.add_resource(dob, gettext("url_change_dob"), endpoint="changedob", resource_class_kwargs={'engine': engine})
    api.add_resource(profile_picture, gettext("url_upload_pp"), endpoint="uploadpp", resource_class_kwargs={'engine': engine})
    api.add_resource(Notifications, gettext("url_notifications") , endpoint="notifications", resource_class_kwargs={'engine': engine})


    api.add_resource(credit, gettext("url_credit_change"), endpoint="credit", resource_class_kwargs={'engine': engine})

    api.add_resource(PluginCrud, gettext("url_plugins"), endpoint="plugins", resource_class_kwargs={'engine': engine})
    api.add_resource(PluginUse, gettext("url_plugins_use"), endpoint="plugins_use", resource_class_kwargs={'engine': engine})





