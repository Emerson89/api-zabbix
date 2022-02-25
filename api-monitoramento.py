#!/usr/bin/python3

from main import Monit
import getpass
import sys

api = Monit("http://192.168.33.10","Admin","zabbix")

def menu():
    print("---- Menu opções Hosts ----")
    print("[1] - Get hosts por grupo")
    print("[2] - Get Itens não suportados")
    print("[3] - Create users")
    geral()

def geral():
    opcao = input("Select an option: ")
    print()

    if opcao == '1':
     api.procura_groups()
   
    elif opcao == '2':
     api.procura_itens()

    elif opcao == '3':
       api.procurando_groupusers()
       api.createUserfromCSV("users.csv")


menu()

