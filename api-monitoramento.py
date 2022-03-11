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
    print("---- Menu opções monitoramento ----")
    print("[1] - Get hosts por grupo")
    print("[2] - Get Itens não suportados por grupo")
    print("[3] - Criar users")
    print("[4] - Remove ou desabilita hosts com errors por grupo")
    print("[5] - Get Itens últimos valores")
    print("[6] - Exit")

    opcao = input("Selecione uma das opções: ")
    print()

    if opcao == '1':
     api.get_hosts()
   
    elif opcao == '2':
     api.procura_itens()
    
    elif opcao == '3':
       api.procurando_groupusers()
       api.createUserfromCSV("users.csv")
    
    elif opcao == '4':
        api.get_hosts_errors()
    
    elif opcao == '5':
       api.procura_itens_values()
    
    elif opcao == '6':
        break
    print()
    if input('Deseja continuar a consulta? (S/N): ').upper() == 'N':
       break

menu()

