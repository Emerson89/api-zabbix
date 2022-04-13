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
     print("***Grupo(s) de Host(s) encontrado(s)***")
     print()
     for x in geral:
        print(x['name'])
     print()
     try:   
      getgrupos = input("Digite o nome do grupo: ")
      grupos = self.zapi.hostgroup.get({
        "output": "extend",
        "filter": { "name": [getgrupos]},
        "selectHosts": ["name","host"],
        "monitored_hosts": "extend",
      })[0]['groupid']
     except IndexError:
        print()
        print("***Nenhum grupo encontrado o nome deve ser exato ex: Zabbix servers***")
        print()
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
     if len(ids) > 0:
      print("***Hosts encontrados***")
     for x in ids:
         print("HOSTID: {},NAME: {}".format(x["hostid"],x["name"]))
     print()
     if len(ids) > 0:
      opcao = input("Deseja gerar relatorio em arquivo? [S/N]").upper()
      if opcao == 'S':
            namefile = input("Digite o nome do arquivo: ") + ".csv"
            with open(namefile, 'w', newline='') as arquivo_csv:
               fieldnames = ['Hostid', 'Name', 'Grupo', 'Interfaces', 'Template']
               escrever = csv.DictWriter(arquivo_csv, delimiter=';', fieldnames=fieldnames)
               escrever.writeheader()    
            for x in ids:
               for grupos in x['groups']:
                  for interface in x['interfaces']:
                     for template in x['parentTemplates']:
                         with open(namefile, 'a') as arquivo_csv:
                          escrever = csv.writer(arquivo_csv, delimiter=';')
                          escrever.writerow([x['hostid'],x['name'],grupos['name'],interface['ip'],template['name']])
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
     elif len(itens) > 0:
        print("***Não há itens não suportados para este grupo de hosts***")
     #self.zapi.logout()
  
  def procura_itens_values(self):
     key = input("Digite a chave key do item para consulta - Ex: agent.version: ")
     itens = self.zapi.item.get({
            "output": "extend",
            "search": {"key_":key},
            "monitored": "true",
            "selectHosts": "extend",
            "selectInterfaces": "extend",
            "groupids": [self.procura_groups(grupos='')],
            "filter": {"state": 0}
            })
     
     for x in itens:
        for names in x['hosts']:
           for interface in x['interfaces']:
            print("HOST: {}, INTERFACE: {}, ITEMID: {}, KEY: {}, NOME: {}, LASTVALUE: {}".format(names['host'],interface['ip'],x["itemid"], x["key_"], x["name"], x["lastvalue"]))
     if len(itens) > 0:
      print()
      print("Total de itens: ", len(itens))       
      opcao = input("Deseja gerar relatorio em arquivo? [S/N]").upper()
      if opcao == 'S':
               itemfile = input("Digite o nome do arquivo: ") + ".csv"
               with open(itemfile, 'w', newline='') as arquivo_csv:
                  fieldnames = ['Host', 'Interface', 'ItemID', 'Key', 'Nome', 'LastValue']
                  escrever = csv.DictWriter(arquivo_csv, delimiter=';', fieldnames=fieldnames)
                  escrever.writeheader()
               for x in itens:
                  for names in x['hosts']:
                    for interface in x['interfaces']:
                     with open(itemfile, 'a') as arquivo_csv:
                      escrever = csv.writer(arquivo_csv, delimiter=';')
                      escrever.writerow([names['host'],interface['ip'],x['itemid'],x['key_'],x['name'],x['lastvalue']])
     elif len(itens) > 0:
        print()
        print(f"Não há itens chave key {key} para este grupo de hosts")
     #self.zapi.logout()
  
  def procura_triggers(self):
     triggers = self.zapi.trigger.get({
            "output": "extend", 
            "monitored": "true",
            "groupids": [self.procura_groups(grupos='')],
            "filter": {"state": 1}
            })
     
     for x in triggers:
            print("TRIGGERID: {},DESCRIPTION: {}, ERROR: {}".format(x["triggerid"], x["description"], x["error"]))
     if len(triggers) > 0:
      print()
      print("Total de triggers não suportadas: ", len(triggers))
      opcao = input("Deseja gerar relatorio de macros em arquivo? [S/N]").upper()
      if opcao == 'S':
            itemfile = input("Digite o nome do arquivo: ") + ".csv"
            for x in triggers:
             with open(itemfile, 'a') as arquivo_csv:
                errors = x['expression']
                erro = errors.split('>')
                macros = erro[1]
                escrever = csv.writer(arquivo_csv)
                new = macros.replace('"','')
                escrever.writerow([new])
      opcao = input("Deseja gerar relatorio em arquivo geral? [S/N]").upper()
      if opcao == 'S':
            itemfile = input("Digite o nome do arquivo: ") + ".csv"
            with open(itemfile, 'w', newline='') as arquivo_csv:
               fieldnames = ['Triggerid', 'Description', 'Error']
               escrever = csv.DictWriter(arquivo_csv, delimiter=';', fieldnames=fieldnames)
               escrever.writeheader()
            for x in triggers:
               with open(itemfile, 'a') as arquivo_csv:
                escrever = csv.writer(arquivo_csv, delimiter=';')
                escrever.writerow([x['triggerid'],x['description'],x['error']])
      opcao = input("Deseja desabilitar as triggers? (S/N): ").upper()
      if opcao == 'S':
            for x in triggers:
               self.zapi.trigger.update({
                  "triggerid": x['triggerid'],
                  "status": 1
               })
     elif len(triggers) > 0:
        print()
        print("***Não há triggers não suportados para este grupo de hosts***")
     #self.zapi.logout()

  def get_triggers(self):
     triggers = self.zapi.trigger.get({
            "output": ['triggerid','expression','description','priority'], 
            "monitored": "true",
            "groupids": [self.procura_groups(grupos='')],
            "filter": {"state": 0}
            })
     severidades = [
         'Não classificada',
         'Informação',
         'Atenção',
         'Média',
         'Alta',
         'Desastre'
     ]
     for x in triggers:
           severidade = severidades[(int(x['priority']))]
           print(x["triggerid"],'-',x['expression'],'-', x["description"],' - ' + severidade)
     if len(triggers) > 0:
      print()
      print("Total de triggers: ", len(triggers))
      opcao = input("Deseja gerar relatorio em arquivo? [S/N]").upper()
      if opcao == 'S':
            itemfile = input("Digite o nome do arquivo: ") + ".csv"
            with open(itemfile, 'w', newline='') as arquivo_csv:
               fieldnames = ['Triggerid', 'Expression', 'Description', 'Severidades']
               escrever = csv.DictWriter(arquivo_csv, delimiter=';', fieldnames=fieldnames)
               escrever.writeheader()
            for x in triggers:
               with open(itemfile, 'a') as arquivo_csv:
                escrever = csv.writer(arquivo_csv, delimiter=';')
                escrever.writerow([x['triggerid'],x['expression'],x['description'], severidade])
     elif len(triggers) > 0:
      print()
      print("***Não há triggers para este grupo de hosts***")
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
        print()
        print("***GroupsUsers encontrados***")
        print()
        for x in ids:
            print ("NAME: {}, ID: {}".format(x['name'], x['usrgrpid']))
        print()            
    else:
        print("***Grupo(s) de Usuário(s) não encontrado(s)***")
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
        "filter": { "available": [2]},
        "groupids": [self.procura_groups(grupos='')],
     })
     if len(geral) > 0:  
      print("***Host(s) encontrado(s) com error(s)***")
      for x in geral:
        print("HOSTID: {}, NOME: {}, ERROR: {}".format(x['hostid'],x['name'],x['error']))
     
      print()
      print("Escolha uma das opções:\n1 - Desabilitar host(s)?\n2 - Remover host(s)\n3 - Nenhuma(enter)?")
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