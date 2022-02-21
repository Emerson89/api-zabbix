#!/usr/bin/python3

#from main import login
import csv
import main

api = main.login()

def menu():
    print("---- Menu ----")
    print("[1] - Get Hosts")
    print("[2] - Get Itens não suportados")
    procurando_hosts()


def procurando_hosts():
    opcao = input("Select an option: ")
    ids = []

    if opcao == '1':
     #host_ids = input("Pesquise o CD do cliente: ")
     ids = api.host.get({
        "output": ['hostid','name'],
        "selectInterfaces": ["interfaceid", "ip"],
        "selectGroups": "extend",
        #"search": {"name": '*' + host_ids + '*'},
        #"searchWildcardsEnabled": True
     })
     if ids:
        for x in ids:
         #print("***Hosts encontrados***")
         print (x)
        print()
        opcao = input("\nDeseja gerar relatorio em arquivo? [s/n]")
        if opcao == 's' or opcao == 'S':
            with open('hostsids.csv', 'w', newline='') as arquivo_csv:
               fieldnames = ['Hostid', 'Name', 'Grupo', 'Interfaces']
               escrever = csv.DictWriter(arquivo_csv, delimiter=';', fieldnames=fieldnames)
               escrever.writeheader()
            for x in ids:
               with open('hostsids.csv', 'a') as arquivo_csv:
                escrever = csv.writer(arquivo_csv, delimiter=';')
                escrever.writerow([x['hostid'],x['name'],x['groups'],x['interfaces']])
     else:
        print("***Hosts não encontrado***")
    
    elif opcao == '2':
   
     itens = api.item.get({"output": "extend", "monitored": "true", "filter": {"state": 1}})
     print("===============================================================================================")
     print("ID   ITEMID        NOME           ERRO")
     print("===============================================================================================")

     for x in itens:
            print("HOSTID: {},ITEMID: {},KEY: {},NOME: {},ERROR:{}".format(x["hostid"], x["itemid"], x["key_"], x["name"],x["error"]))
        # print(itens)
     print("============================================")
     print("Total de itens não suportados: ", len(itens))
     print("==")

print()
menu()

api.logout()

