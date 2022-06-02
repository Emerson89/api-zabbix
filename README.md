# api-zabbix

## Automação utilizando api zabbix

## Dependências

- Python3.8
- zabbix-api==0.5.4
- Testado até a versão 5.0 do Zabbix

## Como Usar

```
./api-monitoramento.py http://IP-ZABBIX User
```
Será solicitado a senha
Podemos realizar a seguintes opções:
```
---- Menu opções monitoramento ----

[1] - Consultar hosts por grupo
[2] - Consultar itens não suportados por grupo
[3] - Criar usuários
[4] - Consultar, remover ou desabilitar hosts com errors por grupo
[5] - Consultar últimos valores itens por grupo
[6] - Consultar triggers não suportados por grupo
[7] - Consultar triggers por grupo
[8] - Consultar macros templates por grupo
[9] - Consultar macros hosts por grupo
[10] - Exit
```
Para cadastro de usuários é obrigatório criar o arquivo users.csv seguindo abaixo, e criação de um grupo de usuário caso não for usar os padrões:

*User1;Senha123* 

Para consultas poderá gerar arquivo .csv

## License
GPLv3