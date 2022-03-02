from os import getgroups
from zabbix_api import ZabbixAPI,Already_Exists
import csv

class Monit(ZabbixAPI):
  def __init__(self, URL, USERNAME, PASSWORD):
   self.zapi = self.conect_api(URL, USERNAME, PASSWORD)

  def conect_api(self, URL, USERNAME, PASSWORD): 
   try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
   except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')
  
   return zapi

  def procura_groups(self):
     geral = self.zapi.hostgroup.get({
        "output": ['name'],
        "monitored_hosts": "extend",
     })
     print("***Grupos encontrados***")
     print()
     for x in geral:
        print(x['name'])
     print()   
     getgrupos = input("Digite o nome do grupo que deseja pesquisar: ")
     grupos = self.zapi.hostgroup.get({
        "output": 'extend',
        "filter": { "name": [getgrupos]},
        "selectHosts": ["name","host"],
        "monitored_hosts": "extend",
     })
     for x in grupos:
      group_ids = x['groupid']
       
     ids = self.zapi.host.get({
        "output": ['hostid','name'],
        "selectInterfaces": ["interfaceid", "ip"],
        "selectGroups": "extend",
        "selectParentTemplates": ["templateid", "name"],
        "groupids": [group_ids],
     })
     print()
     print(f'***Hosts encontrados do Grupo {getgrupos}***')
     print()
     print(ids)   
     print()
     opcao = input("\nDeseja gerar relatorio em arquivo? [S/N]").upper()
     if opcao == 'S':
            namefile = input("Digite o nome do arquivo em .csv: ")
            with open(namefile, 'w', newline='') as arquivo_csv:
               fieldnames = ['Hostid', 'Name', 'Grupo', 'Interfaces', 'Macros', 'Template']
               escrever = csv.DictWriter(arquivo_csv, delimiter=';', fieldnames=fieldnames)
               escrever.writeheader()    
            for x in ids:
               for grupos in x['groups']:
                  for interface in x['interfaces']:
                     for template in x['parentTemplates']:
                         with open(namefile, 'a') as arquivo_csv:
                          escrever = csv.writer(arquivo_csv, delimiter=';')
                          escrever.writerow([x['hostid'],x['name'],grupos['name'],interface['ip'],template['name']])
     else:
        print("***Hosts não encontrado***")
     self.zapi.logout()
  
  def procura_itens(self):
     itens = self.zapi.item.get({"output": "extend", "monitored": "true", "filter": {"state": 1}})
     
     for x in itens:
            print("HOSTID: {},ITEMID: {},KEY: {},NOME: {},ERROR:{}".format(x["hostid"], x["itemid"], x["key_"], x["name"],x["error"]))
     print()
     print("Total de itens não suportados: ", len(itens))
     opcao = input("\nDeseja gerar relatorio em arquivo? [S/N]").upper()
     if opcao == 'S':
            itemfile = input("Digite o nome do arquivo em .csv: ")
            with open(itemfile, 'w', newline='') as arquivo_csv:
               fieldnames = ['Hostid', 'ItemID', 'Key', 'Nome', 'Error']
               escrever = csv.DictWriter(arquivo_csv, delimiter=';', fieldnames=fieldnames)
               escrever.writeheader()
            for x in itens:
               with open(itemfile, 'a') as arquivo_csv:
                escrever = csv.writer(arquivo_csv, delimiter=';')
                escrever.writerow([x['hostid'],x['itemid'],x['key_'],x['name'],x['error']])
     self.zapi.logout()

  def procurando_groupusers(self):
    group_ids = input("Pesquise o nome do grupo de usuario: ")
    ids = self.zapi.usergroup.get({
        "output": ['name','usrgrpid'],
        "sortfield": "name",
        "search": {"name": '*' + group_ids + '*'},
        "searchWildcardsEnabled": True
    })
    if ids:
        print("***GroupsUsers encontrados***")
        print()
        for x in ids:
            print (x['name'],"-", x['usrgrpid'])            
    else:
        print("***GroupsUsers não encontrados***")
  print()

  def create_user(self, user, password):
    GROUPID = input("Insira o groupid...: ")
    try:
       create_user = self.zapi.user.create({
           "alias": user,
           "passwd": password,
           "usrgrps": [{"usrgrpid":GROUPID}],
       })
       self.zapi.logout()

       print(f'User cadastrado {user}')
    except Already_Exists:
       print(f'User(s) já cadastrado {user}')
    except Exception as err:
       print(f'Falha ao cadastrar user {err}')

  def createUserfromCSV(self, fileName):
      with open(fileName) as file:
         file_csv = csv.reader(file, delimiter=';')
         for [nome,senha] in file_csv:
            self.create_user(user=nome,password=senha)
