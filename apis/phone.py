
import requests
import phonenumbers
from phonenumbers import geocoder , carrier , timezone
from telethon import TelegramClient
from telethon import functions
from telethon import errors
from telethon.tl.types import InputPhoneContact
from db_models.plugins import PluginModel
import asyncio

async def checker(loop, client, target):
    await client.connect()
    username = None
    contact = await InputPhoneContact(client_id = 0, phone = target, first_name="a", last_name="b")
    contacts = await client(functions.contacts.ImportContactsRequest([contact]))
    username = await contacts.to_dict()['users'][0]['username']
    await print("\n\n----username : " , username)
    del_usr = client(functions.contacts.DeleteContactsRequest(id=[username]))
    return await username

def phone_make_response( plugin: PluginModel , target):
    res = None
    teleg_res = ''
    # id = "15592805"
    # hash = "4626884d21fbc6db521cf2730a909ebb"
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # base_link = plugin.link
    # res = None
    # try:
    #     id = int(id)
    #     client =  TelegramClient('Checker', id, hash, loop=loop)
    #     try:
    #         res = loop.run_until_complete(checker(loop, client, target))
    #         if not res:
    #             teleg_res = ''      
    #         else:
    #             teleg_res = '{}{}/'.format(base_link  , res)
    #     except errors.FloodWaitError as fW:
    #         return [403,"Plugin Token incorrcet"]
    #     except errors.UsernameInvalidError as uI:
    #         return [404 , ''] 
    # except requests.exceptions.Timeout:
    #     return [500,"Unkown Error"]
    try:
        phone_number =  phonenumbers.parse(str(target)) 
        geocode =  geocoder.description_for_number(phone_number, 'en')
        carry =  carrier.name_for_number(phone_number,'en')
        tzone =  timezone.time_zones_for_number(phone_number)
        valid =  phonenumbers.is_valid_number(phone_number)
        res =  {'geocode':geocode, 'carry':carry , 'tzones': tzone , 'valid':valid , 'telegram':teleg_res}    
        # loop.close()
        return  [200,res]
   
    except Exception as e:
        return [str(e) , "Unkown Error"]