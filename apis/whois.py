from itsdangerous import json
from db_models.plugins import PluginModel
from db_models.users import UserModel
import requests



def whois_make_response(token , plugin: PluginModel  , typ , target):
    base_link = plugin.link
    if typ == 'emailverification':
        link = 'https://emailverification.{}/api/v2?outputFormat=JSON&apiKey={}&emailAddress={}'.format(base_link , token , target)
        res = None
        try:
            res = requests.get(link , timeout=20)
        except requests.exceptions.Timeout:
            return [405,"Request Timeout"]
        if res.status_code == 403:
            return [403,'Plugin Token incorrcet']
        if res.status_code == 200:
            res = res.json()
            out ={
                'username':res['username'] , 'domain': res['domain'] , 'emailAddress':res['emailAddress'] ,'mxRecords':res['mxRecords']
            }
            return [200,out]
        else:
            return [res.status_code , "Unkown Error"]
    
    elif typ == 'dns-history':
        link = 'https://dns-history.{}/api/v1?outputFormat=JSON&apiKey={}&ip={}'.format(base_link , token , target)
        res = None
        try:
            res = requests.get(link , timeout=20)
        except requests.exceptions.Timeout:
            return [405,"Request Timeout"]
        if res.status_code == 403:
            return [403,'Plugin Token incorrcet']
        if res.status_code == 200:
            try:
                res = res.json()
            except json.decoder.JSONDecodeError:
                return [500 , "Json Decode Error"]
            out ={
                'size':res['size'] , 'result': [row['name'] for row in res['result']] 
            }
            return [200,out]
        else:
            return [res.status_code , "Unkown Error {}".format(res.json())]
    
    elif typ == 'website-categorization':
        link = 'https://website-categorization.{}/api/v2?outputFormat=JSON&apiKey={}&domainName={}'.format(base_link , token , target)
        res = None
        try:
            res = requests.get(link , timeout=20)
        except requests.exceptions.Timeout:
            return [405,"Request Timeout"]
        if res.status_code == 403:
            return [403,'Plugin Token incorrcet']
        if res.status_code == 200:
            out = {}
            print(link)
            try:
                res = res.json()
            except json.decoder.JSONDecodeError:
                return [500 , "Json Decode Error"]
            print("\n\nres:" ,res , '\n--\n')
            categories = []
            for row in res['categories']:
                for key in row:
                    categories.append(row[key]['name'])
                # insert the list to the set
            list_set = set(categories)
            # convert the set to the list
            categories = list(list_set)
            out = {
                'websiteResponded':res['websiteResponded'] , 'domainName':res['domainName'] , 'categories':categories
            }
            return [200,out]
        else:
            return [res.status_code , "Unkown Error {}".format(res.json())]

    elif typ == 'whois-history':
        link = 'https://whois-history.{}/api/v1?mode=purchase&outputFormat=JSON&apiKey={}&domainName={}'.format(base_link , token , target)
        res = None
        out = {}
        try:
            res = requests.get(link , timeout=20)
        except requests.exceptions.Timeout:
            return [405,"Request Timeout"]
        if res.status_code == 403:
            return [403,'Plugin Token incorrcet']
        if res.status_code == 200:
            try:
                res = res.json()
            except json.decoder.JSONDecodeError:
                return [500 , "Json Decode Error"]
            results = []
            names = []
            emails = []
            telephones = []

            for row in res['records']:
                if row['registrantContact']['name'] != None and row['registrantContact']['name'] != '':
                    names.append(row['registrantContact']['name'])
                if row['administrativeContact']['name'] != None and row['registrantContact']['name'] != '':
                    names.append(row['administrativeContact']['name'])

                if row['registrantContact']['email'] != None and row['registrantContact']['email'] != '':
                    emails.append(row['registrantContact']['email'])
                if row['administrativeContact']['email'] != None and row['registrantContact']['email'] != '':
                    emails.append(row['administrativeContact']['email'])

                if row['registrantContact']['telephone'] != None and row['registrantContact']['telephone'] != '':
                    telephones.append(row['registrantContact']['telephone'].replace(' ' , ''))
                if row['administrativeContact']['telephone'] != None and row['registrantContact']['telephone'] != '':
                    telephones.append(row['administrativeContact']['telephone'].replace(' ' , ''))
                
            telephones = list(set(telephones))
            names = list(set(names))
            emails = list(set(emails))

            results= {
                'telephones': telephones, 'names':names , 'emails':emails
            }

            out ={
                'size':res['recordsCount'] , 'result': results
            }
            return [200,out]
        else:
            return [res.status_code , "Unkown Error {}".format(res.json())]
    elif typ == 'website-contacts':
        link = 'https://website-contacts.{}/api/v1?outputFormat=JSON&apiKey={}&domainName={}'.format(base_link , token , target)
        res = None
        try:
            res = requests.get(link , timeout=20)
        except requests.exceptions.Timeout:
            return [405,"Request Timeout"]
        if res.status_code == 403:
            return [403,'Plugin Token incorrcet']
        if res.status_code == 200:
            try:
                res = res.json()
            except json.decoder.JSONDecodeError:
                return [500 , "Json Decode Error"]
            out = res
            
            return [200,out]
        else:
            return [res.status_code , "Unkown Error {}".format(res.json())]
    elif typ == 'ip-geolocation':
        link = 'https://ip-geolocation.{}/api/v1?outputFormat=JSON&apiKey={}&ipAddress={}'.format(base_link , token , target)
        res = None
        try:
            res = requests.get(link , timeout=20)
        except requests.exceptions.Timeout:
            return [405,"Request Timeout"]
        if res.status_code == 403:
            return [403,'Plugin Token incorrcet']
        if res.status_code == 200:
            try:
                res = res.json()
            except json.decoder.JSONDecodeError:
                return [500 , "Json Decode Error"]
            out = res
            
            return [200,out]
        else:
            return [res.status_code , "Unkown Error {}".format(res.json())]
    elif typ == 'subdomains':
        link = 'https://subdomains.{}/api/v1?outputFormat=JSON&apiKey={}&domainName={}'.format(base_link , token , target)
        res = None
        try:
            res = requests.get(link , timeout=20)
        except requests.exceptions.Timeout:
            return [405,"Request Timeout"]
        if res.status_code == 403:
            return [403,'Plugin Token incorrcet']
        if res.status_code == 200:
            try:
                res = res.json()
                res = res['result']
                out = {
                    'count': res['count'],
                    'records':[row['domain'] for row in res['records']]
                }
            except json.decoder.JSONDecodeError:
                return [500 , "Json Decode Error"]
            
            return [200,out]
        else:
            return [res.status_code , "Unkown Error {}".format(res.json())]
    else:
        return [404,"Request Type not found !"]