## PROJETO - BOTGITHUB
*Bot do discord para consumir a API REST do Github*

Desenvolvido por: 
 - ANONIMUBR
 - Canhadaz

---

### ORGANIZAÇÃO DO PROJETO

```text
projeto/
├── cogs/
│   └── slash.py
├── apigithub.py
├── main.py
└── requirements.txt
```

**main.py**
- Arquivo central;
- PERMISSÕES DE ACESSO DO BOT:
  ```python
  intents = discord.Intents.default()
  intents.members = True #Acesso aos membros do servidor
  intents.guilds = True #Acesso a eventos dos servidores
  ```
- INICIALIZA O BOT E CARREGA OS COMANDOS PARA O OBJETO 'bot'
  ```python
  async def main():
    async with bot:
        await load_extensions() #Acessa o diretório cogs/ e carrega todos os arquivos .py dentro
        await bot.start(TOKEN) #Inicializa o bot, e o evento 'async def on_ready():'
  ```

**cogs/slash.py**
- Classe SlashCommands
  ```python
  class SlashComandos(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
  ```
- COMANDOS:
  - @app_commands.command(name="ping", description="Responde com a latência do bot via Slash Command.")
    - /ping - retorna a latência do bot
  - @app_commands.command(name="dizer", description="Faz o bot repetir o que você digitar.")
    - /dizer (mensagem:str) - o bot retorna a str do parâmetro({mensagem})
  - @app_commands.command(name="consultar_usuario", description="Consulta a usuário cadastrado no github")
    - /consultar_usuario (usuario:str) - retorna um embed com as informações do usuário

**apigithub.py**
- Classe Api_github
  ```python
  class Api_github():
   def __init__(self, usuario):
      self.usuario = usuario
  ```
- FUNÇÕES
  - def requisicao_usuario(self)
    ```python
      resposta = requests.get(
         f'https://api.github.com/users/{self.usuario}'
      )
    ```
    - retorno
      ```python
      if resposta.status_code == 200:
         return resposta.json()
      else:
         return resposta.status_code
      ```
      
  - def consulta_projetos(self, pagina=None)
    ```python
    url = f'https://api.github.com/users/{self.usuario}/repos'

    params = {}
    if pagina is not None:
      params['page'] = pagina
    
    resposta = requests.get(url, params=params)
    ```
    - retorno
      ```python
      if resposta.status_code == 200:
         return resposta.json()
      else:
         return resposta.status_code
      ```

**requirements.txt**
- Bibliotecas não nativas utilizadas;

---

### BIBLIOTECAS UTILIZADAS

```text
* **`json`** — Nativa
* **`asyncio`** — Nativa
* **`os`** — Nativa
* **`requests`** — `pip install requests`
* **`discord`** — `pip install discord.py`
* **`dotenv`** — `pip install python-dotenv`
* **`apigithub`** — Módulo local (`apigithub.py`)
```

---

### CONFIGURAÇÕES
#### CONFIGURAÇÃO DE BOT
- A criação do bot e obtenção do token é uma questão tratada pelo discord developer
- [ACESSE A DOCUMENTAÇÃO AQUI](https://docs.discord.com/developers/quick-start/getting-started#what-we-ll-be-building)

#### CONFIGURAÇÃO PYTHON

**1. Ambiente Virtual Python**

Crie e ative um ambiente virtual (`.venv`) na raiz do projeto para isolar as dependências:

* **Windows:**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

* **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

**2. Instalação das bibliotecas**

```bash
pip install -r requirements.txt
```

**3. Variáveis de ambiente**

Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes chaves com as suas credenciais:

```env
DISCORD_TOKEN=TOKEN-AQUI
ID_SERVER=ID-SERVER-AQUI
```

* **`DISCORD_TOKEN`**: Token de autenticação do seu bot (obtido no Discord Developer Portal).
* **`ID_SERVER`**: ID numérico do servidor onde o bot irá operar e sincronizar os comandos.

> [!IMPORTANT]
> Nunca compartilhe seu arquivo `.env` nem faça o upload dele para repositórios públicos (certifique-se de que ele esteja listado no seu `.gitignore`).

### PARA EXECUTAR O BOT
Seguidos todos os passos até aqui, basta executar;
```bash
python main.py
```
