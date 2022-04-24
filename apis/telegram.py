
from pydoc import cli
import requests
from telethon import TelegramClient
from telethon import functions
from telethon import errors
from db_models.plugins import PluginModel
import asyncio

async def getter(loop, client, target):
    await client.connect()
    return await client(functions.account.CheckUsernameRequest(username=target))

def telegram_make_response( plugin: PluginModel , target):
    id = "15592805"
    hash = "4626884d21fbc6db521cf2730a909ebb"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    base_link = plugin.link
    link = '{}{}/'.format(base_link  , target)
    res = None
    try:
        id = int(id)
        client = TelegramClient('Checker', id, hash, loop=loop)
        try:
            res = getter(loop, client, target)
            if res == True:
                return [404 , '']        
            else:
                return [200,link]
        except errors.FloodWaitError as fW:
            return [403,"Plugin Token incorrcet"]
        except errors.UsernameInvalidError as uI:
            return [404 , ''] 
    except requests.exceptions.Timeout:
        return [500,"Unkown Error"]