# -*- coding: utf-8 -*-

import requests
import json
from config import ctoken
from whitelist import WhiteLister

class Curlinger:

    def __init__(self, ctoken):
        self.headers = {'Accept': 'application/json',
                   'Authorization': 'Token ' + ctoken
                        }
        self.error_text = 'Что-то пошло не так'
        self.item_types = ['burster', 'ultrastrike', 'ada', 'jarvis', 'resonator', 'powercube', 'capsule', 'heatsink', 'multihack', 'shield', 'linkamp', 'forceamp', 'turret', 'transmutter']
        whitelist = WhiteLister()
        self.account_id = whitelist.get_account_id(ctoken)

    def check_item_type(self, item_type):
        if item_type in self.item_types:
            return True
        else:
            return False
    
    def get_bursters(self):
        try: 
            r = requests.get('https://curlingaround.com/api/inventory/', headers=self.headers)

            if r.status_code == 200:
                values= json.loads(r.text)
                #print (json.dumps(values, indent=4, sort_keys=True))

                imax = values['count']
                i = 0
                result = ''
                while i < imax:
                    result = result + str(values['results'][i]['name']) + ": " + str(values['results'][i]['items']['burster']) + "\n"
                    i += 1

                return result
            else:
                return self.error_text
        except requests.exceptions.RequestException as e:
            return self.error_text

    def get_type(self, item_type):
        try: 
            r = requests.get('https://curlingaround.com/api/inventory/', headers=self.headers)

            if r.status_code == 200:
                values= json.loads(r.text)
                #print (json.dumps(values, indent=4, sort_keys=True))

                imax = values['count']
                i = 0
                result = "<b>" + item_type + '</b>\n'
                count = None
                while i < imax:
                    if i == 0:
                        count = values['results'][i]['items'][item_type]
                    else:
                        if item_type in ['ada', 'jarvis', 'forceamp', 'turret', 'fracker']:
                            count += values['results'][i]['items'][item_type]
                        else:
                            for j, item in enumerate(values['results'][i]['items'][item_type]):
                                count[j] += item

                    if item_type in ['ada', 'jarvis', 'forceamp', 'turret', 'fracker']:
                        result = result + "    " + str(values['results'][i]['name']) + ": " + str(values['results'][i]['items'][item_type]) + "\n"
                    else:
                        result = result + "    " + str(values['results'][i]['name']) + ": " + ', '.join(map(str, values['results'][i]['items'][item_type])) + "\n"
                    i += 1

                print (count)
                if item_type in ['ada', 'jarvis', 'forceamp', 'turret', 'fracker']:
                    result += u'    <b>Итого: ' + str(count) + "</b>\n"
                else:
                    result += u'    <b>Итого: ' + ', '.join(map(str, count)) + "</b>\n"

                return result
            else:
                print (r)
                return self.error_text
        except requests.exceptions.RequestException as e:
            print (e)
            return self.error_text

    def search_my_keys(self, keyname):
        try: 
            if self.account_id != None:
                params = {'name' : keyname, 'agent' : self.account_id}
            else:
                params = {'name' : keyname}
            r = requests.get('https://curlingaround.com/api/portals/', headers=self.headers, params=params)
            #print (r.url)

            if r.status_code == 200:
                values= json.loads(r.text)
                #print (json.dumps(values, indent=4, sort_keys=True))

                imax = values['count']
                if imax >= 5:
                    result = "<b>" + str(imax) + "</b> возможных портала(ов). Что-то больно дохера. "
                    return result

                if imax == 0:
                    result = "Нет такого ключика."
                    return result
                
                i = 0
                result = ''
                while i < imax:
                    ar = values['results'][i]['my_keys']
                    if ar:
                        result = result + "<b>" + unicode(values['results'][i]['portal']['name']) + "</b>\n"

                        for j in values['results'][i]['my_keys']:
                            result = result + "        " + unicode(j['name']) + " " + unicode(j['count']) + " " + unicode(j['capsule']) + "\n"

                    i += 1

                return result
            else:
                return self.error_text
        except requests.exceptions.RequestException as e:
            return self.error_text
        
    def get_known_types(self):
        return self.item_types

    def get_empty_space(self):
        try: 
            r = requests.get('https://curlingaround.com/api/holders/', headers=self.headers)
            if r.status_code == 200:
                values_keys = json.loads(r.text)
            else:
                return self.error_text

            r = requests.get('https://curlingaround.com/api/inventory/', headers=self.headers)
            if r.status_code == 200:
                values_inv = json.loads(r.text)
            else:
                return self.error_text

            imax = values_keys['count']
            imax2 = values_inv['count']
            
            if imax != imax2:
                return self.error_text

            i = 0
            result = ''
            item_count = 0

            while i < imax:
                item_count = 0
                base_count = 2000
                result += "<b>" + str(values_keys['results'][i]['name']) + "</b>\n"
                for item_type in values_inv['results'][i]['items']:
                    if item_type == 'capsule':
                        base_count += 100 * values_inv['results'][i]['items'][item_type][2]
                    
                    if item_type in ['ada', 'jarvis', 'forceamp', 'turret', 'fracker']:
                        item_count += values_inv['results'][i]['items'][item_type]
                    else:
                        item_count += sum(values_inv['results'][i]['items'][item_type])

                result += "        free space: <b>" + str(base_count - values_keys['results'][i]['keys']-item_count) + "</b>\n"

                result += "        keys: " + str(values_keys['results'][i]['keys'])
                result += " items: " + str(item_count)+ "\n"

                i += 1

            return result

        except requests.exceptions.RequestException as e:
            return self.error_text

    def search_city_keys(self, keyname):
        try: 
            params = {'name' : keyname, 'city' : '17336'}
            r = requests.get('https://curlingaround.com/api/portals/', headers=self.headers, params=params)
            #print (r.url)

            if r.status_code == 200:
                values= json.loads(r.text)
                #print (json.dumps(values, indent=4, sort_keys=True))

                imax = values['count']
                if imax >= 5:
                    result = "<b>" + str(imax) + "</b> возможных портала(ов). Что-то больно дохера. "
                    return result

                if imax == 0:
                    result = "Нет такого ключика."
                    return result
                
                i = 0
                result = ''
                while i < imax:
                    ar = values['results'][i]['holders']
                    for idx1, country in enumerate(ar):
                        c = ar[idx1]['children']
                        for idx2, city in enumerate(c):
                            if c[idx2]['name'] == 'Novosibirsk':
                                result += "<b>" + unicode(values['results'][i]['portal']['name']) + "</b>\n"
                                for j in c[idx2]['children']:
                                    result += "        " + unicode(j['name']) + ": " + unicode(j['count']) + "\n"

                    i += 1

                    if result == '':
                        result = self.error_text
                return result
            else:
                return self.error_text
        except requests.exceptions.RequestException as e:
            return self.error_text
        

#cur = Curlinger(ctoken)
#print (cur.check_item_type('123'))
#print (cur.check_item_type('ada'))
