#!/usr/bin/python3

#from main import login
import csv
import main

api = main.login()

def menu():
    print("---- Menu ----")
    print("[1] - Get Host")
    print("[2] - Get GroupHost")
    procurando_hosts()

#ids = []

def procurando_hosts():
    opcao = input("Select an option: ")
    
    if opcao == '1':
     host_ids = input("Pesquise o CD do cliente: ")
     ids = api.host.get({
        "output": ['host','hostid', 'description'],
        "sortfield": "name",
        "search": {"name": '*' + host_ids + '*'},
        "searchWildcardsEnabled": True
     })
     if ids:
        print("***Hosts encontrados***")
        print()
        for x in ids:
            with open('hostsids.csv', 'a') as arquivo_csv:
               escrever = csv.writer(arquivo_csv, delimiter=';')
               escrever.writerow([x['host'],x['hostid'],x['description']])
            print (x['host'],"-", x['description'])            
     else:
        print("***Hosts não encontrado***")
    
    elif opcao == '2':
     group_ids = input("Pesquise o CD do cliente: ")
     grp_ids = api.hostgroup.get({
        "output": ['name','groupid'],
        "sortfield": "name",
        "search": {"name": '*' + group_ids + '*'},
        "searchWildcardsEnabled": True
     })
     if grp_ids:
         for x in grp_ids:
          print("***Groups encontrados***")
          print (x['name'],"-", x['groupid'])            
          print()
         opcao = input("\nDeseja gerar relatorio em arquivo? [s/n]") 
         if opcao == 's' or opcao == 'S':
          for x in grp_ids:
            with open('groupids.csv', 'w') as arquivo_csv:
               arquivo_csv.write("Name;Groupid\r\n")
               escrever = csv.writer(arquivo_csv, delimiter=';')
               escrever.writerow([x['name'],x['groupid']])
            print (x['name'],"-", x['groupid'])            
     else:
        print("***Groups não encontrados***")

print()
menu()

api.logout()

