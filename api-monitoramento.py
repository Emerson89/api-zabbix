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
    print("[1] - Consultar ou extrair hosts por grupo")
    print("[2] - Consultar ou extrair itens não suportados por grupo")
    print("[3] - Criar usuários")
    print("[4] - Consultar, remover ou desabilitar hosts com errors por grupo")
    print("[5] - Consultar ou extrair últimos valores itens por grupo")
    print("[6] - Consultar, extrair ou desabilitar triggers com erros em macros")
    print("[7] - Consultar, extrair ou desabilitar triggers com erro")
    print("[8] - Consultar ou extrair triggers por grupo")
    print("[9] - Consultar ou extrair triggers gerais")
    print("[10] - Consultar ou extrair macros de templates por grupo")
    print("[11] - Consultar ou extrair macros de hosts por grupo")
    print("[12] - Criar macros a nível de hosts")
    print("[13] - Exit")
    print()

    opcao = input("Selecione uma das opções: ")
    print()

    if opcao == '1':
     api.get_hosts()
   
    elif opcao == '2':
     api.procura_itens_error()
    
    elif opcao == '3':
       api.procurando_groupusers()
       api.id()
       api.createUserfromCSV("users.csv")
    
    elif opcao == '4':
        api.get_hosts_errors()
    
    elif opcao == '5':
       api.procura_itens_values()
    
    elif opcao == '6':
       api.procura_triggers_error()
    
    elif opcao == '7':
      api.procura_triggers_error_2()
    
    elif opcao == '8':
       api.procura_triggers()
    
    elif opcao == '9':
       api.procura_triggers_all()

    elif opcao == '10':
       api.procura_macros_templates()
    
    elif opcao == '11':
       api.procura_macros_hosts()
    
    elif opcao == '12':
       api.procura_host()
       api.procura_id()
       api.createUserfromCSV("macros.csv")
          
    elif opcao == '13':
        break
    if input('Deseja realizar uma nova consulta? (S/N): ').upper() == 'N':
       break

menu()

