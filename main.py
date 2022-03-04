from os import getgroups
from tokenize import group
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

  def procura_groups(self, grupos):
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
     })[0]['groupid']
     
     print()
     #print(f'***Hosts encontrados do Grupo {getgrupos}***')
     #print()
     return grupos

  def get_hosts(self):       
     ids = self.zapi.host.get({
        "output": ['hostid','name'],
        "selectInterfaces": ["interfaceid", "ip"],
        "selectGroups": "extend",
        "selectParentTemplates": ["templateid", "name"],
        "groupids": [self.procura_groups(grupos='')],
        "filter": { "status": [0]}
     })
     print()
     print(ids)   
     print()
     opcao = input("Deseja gerar relatorio em arquivo teste? [S/N]").upper()
     if opcao == 'S':
            namefile = input("Digite o nome do arquivo: ") + ".csv"
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
     #else:
     #   print("***Hosts não encontrado***")
     #self.zapi.logout()

  def procura_itens(self):
     itens = self.zapi.item.get({
            "output": "extend", 
            "monitored": "true",
            "groupids": [self.procura_groups(grupos='')],
            "filter": {"state": 1}
            })
     
     for x in itens:
            print("HOSTID: {},ITEMID: {},KEY: {},NOME: {},ERROR:{}".format(x["hostid"],x["itemid"], x["key_"], x["name"],x["error"]))
     if len(itens) > 0:
      print()
      print("Total de itens não suportados: ", len(itens))
      opcao = input("Deseja gerar relatorio em arquivo? [S/N]").upper()
      if opcao == 'S':
            itemfile = input("Digite o nome do arquivo: ") + ".csv"
            with open(itemfile, 'w', newline='') as arquivo_csv:
               fieldnames = ['Hostid', 'ItemID', 'Key', 'Nome', 'Error']
               escrever = csv.DictWriter(arquivo_csv, delimiter=';', fieldnames=fieldnames)
               escrever.writeheader()
            for x in itens:
               with open(itemfile, 'a') as arquivo_csv:
                escrever = csv.writer(arquivo_csv, delimiter=';')
                escrever.writerow([x['hostid'],x['itemid'],x['key_'],x['name'],x['error']])
      opcao = input("Deseja desabilitar os itens? (S/N): ").upper()
      if opcao == 'S':
            for x in itens:
               self.zapi.item.update({
                  "itemid": x['itemid'],
                  "status": 1
               })
     else:
        print("Não há itens não suportados para este grupo de hosts")
     #self.zapi.logout()

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
        print()            
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
     try:
      with open(fileName) as file:
         file_csv = csv.reader(file, delimiter=';')
         for [nome,senha] in file_csv:
            self.create_user(user=nome,password=senha)       
     except Exception as err:
        print("***ATENCAO***Para cadastro do Hosts obrigatório criar o arquivo users.csv")
  
  def get_hosts_errors(self):
     
     geral = self.zapi.host.get({
        "output": ['hostid','name', 'error'],
        "selectGroups": "extend",
        "filter": { "available": [2]} 
     })
     if len(geral) > 0:  
      print("***Host(s) encontrado(s) com error(s)***")
      for x in geral:
        print("HOSTID: {}, NOME: {}, ERROR: {}".format(x['hostid'],x['name'],x['error']))
     
      print()
      print("Escolha uma opção:\n1 - Desabilitar host(s)?\n2 - Remover host(s)?")
      opcao = input()
      if opcao == '1':
         for x in geral:
            self.zapi.host.update({
                  "hostid": x['hostid'],
                  "status": 1
            })
         print('Host(s) desabilitado(s)')
      elif opcao == '2':
         for x in geral:
          r = x['hostid']
          self.zapi.host.delete([r])
         
         print('Host(s) removido(s)')
     else:
        print("***Nenhum host(s) encontrado(s) com errors***")
