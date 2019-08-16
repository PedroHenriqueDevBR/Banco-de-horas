# Banco de horas

> Banco de horas

## Aplicações do projeto

O projeto está dividido em 4 aplicações, cada uma com responsabilidades bem definidas, as aplicações do projeto são:

1. core
2. usuario
3. movimentacao
4. relatorio

## Descricao das aplicações
### Core
Aplicação que serve como o núcleo do projeto, é por onde o usuário começa a utilizar a plicação, a aplicação **core** guarda a regra de negócio do projeto, toda a modelagem do projeto está centralizada nesta aplicação.

### usuario
O controle de acesso ao sistema fica na responsabilidade da aplicação **usuario**, toda a parte de cadastro de usuário, login, logout, modificação no perfil, ou ativação e inativação fica na responsabilidade da aplicação **usuario**.

### movimentacao
Aplicação responsável por gerenciar as movimentações dos usuários.

### Relatório
Aplicação que gera relatório a partir dos dados cadastrados no banco de dados do projeto.