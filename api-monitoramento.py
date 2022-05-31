#!/usr/bin/python3

from main import Monit
import getpass
import sys

URL = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = getpass.getpass("Digite a senha: ")

api = Monit(URL,USERNAME,PASSWORD)
print()

def menu():
  while True:
    print("---- Menu opções monitoramento ----")
    print()
    print("[1] - Consultar hosts por grupo")
    print("[2] - Consultar itens não suportados por grupo")
    print("[3] - Criar users")
    print("[4] - Remover ou desabilitar hosts com errors por grupo")
    print("[5] - Consultar últimos valores itens por grupo")
    print("[6] - Consultar triggers não suportados por grupo")
    print("[7] - Consultar triggers por grupo")
    print("[8] - Consultar macros templates por grupo")
    print("[9] - Consultar macros hosts por grupo")
    print("[10] - Criar macros em nivel hosts in DEV")
    print("[11] - Exit")
    print()

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
       api.procura_triggers()
    
    elif opcao == '7':
       api.get_triggers()
   
    elif opcao == '8':
       api.procura_macros_templates()
    
    elif opcao == '9':
       api.procura_macros_hosts()
    
    elif opcao == '10':
       api.create_macros()
       api.createmacrosfromCSV()
          
    elif opcao == '11':
        break
    if input('Deseja realizar uma nova consulta? (S/N): ').upper() == 'N':
       break

menu()

