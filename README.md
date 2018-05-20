[![Build Status](https://travis-ci.org/ComputerSocietyUNB/ProjetoChatbot.svg?branch=master)](https://travis-ci.org/ComputerSocietyUNB/ProjetoChatbot)
[![codecov](https://codecov.io/gh/ComputerSocietyUNB/ProjetoChatbot/branch/master/graph/badge.svg)](https://codecov.io/gh/ComputerSocietyUNB/ProjetoChatbot)
[![Maintainability](https://api.codeclimate.com/v1/badges/ffdec12c3e0377893317/maintainability)](https://codeclimate.com/github/ComputerSocietyUNB/ProjetoChatbot/maintainability)

# ProjetoChatbot

## O que é

Chatbots são agentes de inteligência artificial, hospedados em softwares de
mensagem, ativados pela fala oral ou escrita e capazes de gerar respostas na
forma de diálogo com o usuário (Radziwill & Benton, 2017).

O objetivo é desenvolver um chatbot (isto é, um programa interativo que produz
diálogos automáticos, ex.: Joy, Cleverbot etc.), tendo em vista a garantia e
a manutenção da saúde mental da comunidade universitária, junto a uma extensa
rede de apoio.

## Como contribuir

Uma vez configurado o ambiente (detalhes mais abaixo). Deve-se criar uma
branch local e a partir dela efetuar todas as modificações a serem feitas.
Preferencialmente cada branch deve focar em uma única funcionalidade.

Exemplo:
a branch update_readme tem como função atualizar o README.md (este arquivo)
e portanto deve conter apenas modificações no arquivo README.md.

Para mais modificações, deve-se abrir outra branch e nomeá-la de acordo. Uma
vez concluídas todas as modificações, deve-se abrir uma Pull Request e esperar
(ou solicitar) uma revisão feita por outra pessoa.

O reviewer deverá verificar se os testes no Travis CI passaram, qual a
porcentagem de cobertura de testes, se a nova funcionalidade está sendo
testada e se a funcionalidade condiz com oque está sendo demandado na iteração
vigente.

## Ferramentas a instalar

* Editor de texto (Ex.: [Atom](https://atom.io/), [VSCode](https://code.visualstudio.com/));
* [Git Time Metric](https://github.com/git-time-metric/gtm);
* Git;
* [Python 3](https://www.python.org/downloads/).

## Configurando o ambiente de desenvolvimento

Deve-se primeiro criar um ambiente virtual

```
python3 -m venv venv
```

Depois deve-se instalar os pacotes contidos no `requirements.txt`. Caso você
tenha o `make` instalado, use `make install`, caso contrário:

```
pip install -r requirements.txt
```

## Como fazer o bot funcionar

Deve-se primeiramente gerar um token utilizando o @botfather. Abra o Telegram e
procure por @botfather. Inicie o diálogo, envie o comando /newbot e siga as
instruções fornecidas. Ao final do diálogo, será informado um token, este token
permitirá receber e enviar mensagens ao bot que acabou de ser criado. Também é
informado o link para a documentação que serve de referência para a construção
de bots para o Telegram: [Bot API](https://core.telegram.org/bots/api)

Uma vez tendo em mão o token do bot, deve-se criar um arquivo chamado
`config.ini` na pasta `bot`. O arquivo terá a seguinte estrutura:

```
[DEFAULT]
token={SEUTOKENGIGANTEAQUI}
```

Uma vez criado o arquivo, use `make run` para fazer o bot funcionar ou

```
python3 bot/bot.py
```

## Equipe Responsável

* Coordenador Geral
  * [Alexandre Augusto](https://github.com/alexandrebarbaruiva)
* Equipe Dev
  * [Daniella Angelos](https://github.com/daniangelos)
  * [Talitha Pumar](https://github.com/tapumar)
* Equipe Cog
