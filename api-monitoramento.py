#!/usr/bin/python3

from main import Monit
import getpass
import sys

#URL = sys.argv[1]
#USERNAME = sys.argv[2]
#PASSWORD = getpass.getpass("Digite a senha: ")

#api = Monit(URL,USERNAME,PASSWORD)

def menu():
  while True:
    print("---- Menu opções Hosts ----")
    print("[1] - Get hosts por grupo")
    print("[2] - Get Itens não suportados")
    print("[3] - Create users")
    print("[4] - Create users")
    print("[5] - Exit")

    opcao = input("Select an option: ")
    print()

    if opcao == '1':
     api.procura_groups()
   
    elif opcao == '2':
     api.procura_itens()
    
    elif opcao == '3':
       api.procurando_groupusers()
       api.createUserfromCSV("users.csv")
    
    elif opcao == '4':
        api.historyget()
    
    elif opcao == '5':
        break
    
    if input('Deseja continuar a consulta? (S/N): ').upper() == 'N':
       break

menu()

