from zabbix_api import ZabbixAPI
import sys
import getpass

def login():
 URL = 'http://192.168.33.10'
 USERNAME = 'Admin'
 PASSWORD = 'zabbix'

 try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
 except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')
 
 return zapi