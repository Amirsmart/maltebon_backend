
import requests
import phonenumbers
from phonenumbers import geocoder , carrier , timezone

from db_models.plugins import PluginModel


def phone_make_response( plugin: PluginModel , target):
    resp = {}
    res = None
    try:
        phone_number = phonenumbers.parse(str(target)) 
        geocode = geocoder.description_for_number(phone_number, 'en')
        carry = carrier.name_for_number(phone_number,'en')
        tzone = timezone.time_zones_for_number(phone_number)
        valid = phonenumbers.is_valid_number(phone_number)
        res = {'geocode':geocode, 'carry':carry , 'tzones': tzone , 'valid':valid}    
        return [200,res]
   
    except Exception as e:
        return [str(e) , "Unkown Error"]