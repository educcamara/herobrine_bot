# Herobrine Discord Bot

Repositório do meu *Bot* do Discord que guarda certos tipos de dados para meu servidor de Minecraft. Feito em Python 3.11.

## Sumário

- [Visão Geral](#visão-geral)
- [Como Usar](#como-usar)
- [Recursos para o Bot](#recursos-para-o-bot)
- [Comandos](#comandos)

## Visão Geral

Este bot Discord foi desenvolvido especificamente para o nosso servidor de Minecraft. O principal propósito do bot é armazenar informações cruciais sobre várias localizações no servidor, incluindo coordenadas de construções, biomas, e outros pontos de interesse.

Antes da criação do bot, nós usávamos um canal de texto para manter essas informações, mas à medida que o número de dados cresceu, tornou-se impraticável. O Herobrine Bot foi concebido para resolver esse problema, armazenando essas informações num banco de dados SQL (SQLite no momento) e simplificando o processo de adição de novas informações.

## Como Usar

1. **Instalação de Dependências:** Execute o comando `pip install discord python-dotenv` para instalar as dependências necessárias.

2. **Configuração do Token:** Crie um arquivo `.env` no diretório do projeto e insira o token do seu bot do Discord:

```dotenv
DISCORD_TOKEN=seu_token_aqui
```

3. **Execução do Bot:** Inicie o bot executando o comando `python3 main.py`

## Recursos para o Bot

### Inicialização do Bot

```python
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
```
- As bibliotecas `os` e `dotenv` são usadas para carregar o token do bot do arquivo `.env`
- A biblioteca `discord` é usada para criar o bot e interagir com o Discord
- A biblioteca `discord.ext` é usada para criar comandos personalizados

```python
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)
```

- A classe `discord.Intents` é usada para definir as permissões do bot
- A classe `commands.Bot` é usada para criar o bot e definir o prefixo dos comandos

```python
@bot.event
async def on_ready():
    print(f"{bot.user} logged in as {bot.user.name}")
```

- O evento `on_ready` é usado para imprimir uma mensagem no console quando o bot estiver pronto
- O método `bot.user` é usado para obter o usuário do bot, e o método `name` é usado para obter o nome do usuário, que neste caso é o bot

### Armazenamento de Dados

O arquivo `dbmanager.py` contém as classes e métodos usados para armazenar e recuperar dados do banco de dados.
É nele que as operações de banco de dados são definidas, utilizando a biblioteca `sqlite3`.

```python
import sqlite3
```

`LocationsManager` é a classe que interage com o arquivo `locations.db` para armazenar e recuperar dados sobre localizações.

```python
class LocationsManager:
    def __init__(self):
        self.conn = sqlite3.connect('locations.db')
        self.cur = self.conn.cursor()
        self._initialize_locations()
```

Seu `__init__` inicializa a conexão com o banco de dados e chama o método `_initialize_locations` para inicializar as tabelas em `locations.db` caso ainda não existam.

Há cinco tabelas, sendo elas as categorias de localizações:

- Estruturas (`Structures`):
  - `id`: Chave primária inteira
  - `name`: Nome da estrutura (limite de 127 caracteres)
  - `x, y, z`: Três elementos que juntos compõem as coordenadas da estrutura
  - `explored`: Status de exploração da estrutura (não explorada, parcialmente explorada, já explorada)
- Biomas (`Biomes`):
  - `id`: Chave primária inteira
  - `name`: Nome do bioma
  - `x, y, z`: Coordenadas
  - `desc`: Descrição do bioma (limite de 255 caracteres)
- Cavernas (`Caves`):
  - `id`: Chave primária inteira
  - `name`: Nome da caverna
  - `x, y, z`: Coordenadas
  - `size`: Tamanho da caverna (limite de 31 caracteres)
  - `desc`: Descrição da caverna
- Paisagens (`Landscapes`):
  - `id`: Chave primária inteira
  - `name`: Nome da paisagem
  - `x, y, z`: Coordenadas
  - `beauty`: Beleza da paisagem (convenção de 0-10)
  - `desc`: Descrição da paisagem
- Outros (`Others`):
  - `id`: Chave primária inteira
  - `name`: Nome da localização
  - `x, y, z`: Coordenadas
  - `desc`: Descrição da localização

## Comandos

- [Ajuda](#ajuda)
- [Mostrar Localizações](#mostrar-localizações)
- [Adicionar Localização](#adicionar-localização)
- [Editar Localização](#editar-localização)
- [Remover Localização](#remover-localização)

### Ajuda

`>help <*args>`

> **WIP**

Mostra todos os comandos disponíveis. Se um comando for especificado, mostra informações sobre ele.

### Mostrar Localizações

`>locate <categoria>`

Mostra todas as localizações no formato `embed` de uma categoria específica.

### Adicionar Localização

`>add <categoria>`

Adiciona uma nova localização à categoria especificada.

### Editar Localização

`>edit <categoria>`

Edita uma localização existente na categoria especificada.

### Remover Localização

`>delete <categoria>`

Remove uma localização da categoria especificada.
