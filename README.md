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

[1] - Consultar ou extrair hosts por grupo
[2] - Consultar ou extrair itens não suportados por grupo
[3] - Criar usuários
[4] - Consultar, remover ou desabilitar hosts com errors por grupo
[5] - Consultar ou extrair últimos valores itens por grupo
[6] - Consultar, extrair ou desabilitar triggers com erros em macros
[7] - Consultar, extrair ou desabilitar triggers com erro
[8] - Consultar ou extrair triggers por grupo
[9] - Consultar ou extrair triggers gerais
[10] - Consultar ou extrair macros de templates por grupo
[11] - Consultar ou extrair macros de hosts por grupo
[12] - Criar macros a nível de hosts
[13] - Exit
```
Para cadastro de usuários é obrigatório criar o arquivo users.csv seguindo abaixo, e criação de um grupo de usuário caso não for usar os padrões:

```
*User1;Senha123*
*User2;Senha123* 
```

Para cadastro de macros é obrigatório criar o arquivo macros.csv seguindo abaixo, caso queira você extrair as usando o próprio script:

```
*{$MACROS1};1111111*
*{$MACROS2};1111111*
```

Para consultas poderá gerar arquivo .csv

## License
GPLv3