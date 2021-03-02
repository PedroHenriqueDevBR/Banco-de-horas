# Banco de horas

> Banco de horas

## Aplicações do projeto

O projeto está dividido em 4 aplicações, cada uma com responsabilidades bem definidas, as aplicações do projeto são:

1. core
2. usuaário
3. movimentação
4. relatório

## Descricao das aplicações

### Core
Aplicação que serve como o núcleo do projeto, é por onde o usuário começa a utilizar a plicação, a aplicação **core** guarda a regra de negócio do projeto, toda a modelagem do projeto está centralizada nesta aplicação.

### usuario
O controle de acesso ao sistema fica na responsabilidade da aplicação **usuario**, todas as funcionalidades que são cadastro de usuário, login, logout, modificação no perfil, ou ativação e inativação fica na responsabilidade da aplicação **usuario**.

### movimentacao
Aplicação responsável por gerenciar as movimentações dos usuários se referindo principalmente à modificação da quantidade de horas de um determinado usuário.

### Relatório
Aplicação responsável por gerar relatórios de acordo com a solicitação do usuário.

### Modelagem

A modelagem consiste no gerenciemento de 7 (sete) entidades, são elas:
 - Setor
 - Perfil
 - Status
 - Forma de pagamento
 - Movimentação
 - Log da movimentação
 - Hash

A seguir a modelagem em uma linguagemn visual.

![BancoDeHoras](https://user-images.githubusercontent.com/36716898/72946725-91c44280-3d5e-11ea-9d1b-b32ecdc18e05.png)