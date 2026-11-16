## PROJETO - BOTGITHUB
*Bot do discord para consumir a API REST do Github e receber eventos de repositórios via webhook*

Desenvolvido por: 
 - Gabriel Ferrarezi
 - Murilo Furlanetto

---

### OBJETIVO

Integrar o Discord ao GitHub. Funcionalidades planejadas:

- Notificar commits (push), merges, pull requests, abertura e fechamento de issues;
- Consultar informações de um repositório;
- Consultar contribuições de um repositório;
- Consultar contribuições e atividades de desenvolvedores;
- Exibir estatísticas de commits dos integrantes.

---

### ESTADO ATUAL

- [x] Bot conectado ao Discord, com slash commands sincronizados no servidor
- [x] Consulta de usuário do GitHub (`/consultar_usuario`)
- [x] Vínculo repositório → canal (`/conectar_repositorio`), salvo em `conexoes.json`
- [x] Receptor de webhooks do GitHub dentro do bot (servidor `aiohttp`)
- [x] Túnel público com Cloudflare para o GitHub alcançar o bot em desenvolvimento
- [ ] Verificação da assinatura (`Secret`) dos webhooks
- [ ] Transformar os eventos recebidos em embeds e enviar no canal conectado
- [ ] Consultas de repositório, contribuições e atividades
- [ ] Estatísticas de commits dos integrantes

---

### ORGANIZAÇÃO DO PROJETO

```text
projeto/
├── cogs/
│   ├── slash.py
│   ├── conexoes.py
│   └── receptor.py
├── apigithub.py
├── armazenamento.py
├── main.py
├── requirements.txt
├── conexoes.json      (gerado automaticamente pelo bot)
├── .env               (criado por você, não vai para o Git)
└── .gitignore
```

**main.py**
- Arquivo central;
- PERMISSÕES DE ACESSO DO BOT:
  ```python
  intents = discord.Intents.default()
  intents.members = True #Acesso aos membros do servidor
  intents.guilds = True #Acesso a eventos dos servidores
  ```
- EVENTO `on_ready`: quando o bot conecta, copia os comandos para o servidor definido em `ID_SERVER` e sincroniza (`bot.tree.sync`), fazendo os `/comandos` aparecerem na hora.
- INICIALIZA O BOT E CARREGA OS COMANDOS PARA O OBJETO 'bot'
  ```python
  async def main():
    discord.utils.setup_logging() #Liga os logs do discord.py no terminal
    async with bot:
        await load_extensions() #Acessa o diretório cogs/ e carrega todos os arquivos .py dentro
        await bot.start(TOKEN) #Inicializa o bot, e o evento 'async def on_ready():'
  ```
- Qualquer arquivo `.py` novo dentro de `cogs/` é carregado automaticamente.

**cogs/slash.py**
- Classe SlashComandos
  ```python
  class SlashComandos(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
  ```
- COMANDOS:
  - @app_commands.command(name="ping", description="Responde com a latência do bot via Slash Command.")
    - /ping - retorna a latência do bot
  - @app_commands.command(name="dizer", description="Faz o bot repetir o que você digitar.")
    - /dizer (texto:str) - o bot retorna a str do parâmetro({texto})
  - @app_commands.command(name="consultar_usuario", description="Consulta a usuário cadastrado no github")
    - /consultar_usuario (usuario:str) - retorna um embed com as informações do usuário (perfil, seguidores, repositórios públicos e lista de projetos)

**cogs/conexoes.py**
- Classe Conexoes
- COMANDOS:
  - @app_commands.command(name="conectar_repositorio", description="Conecta um repositório do GitHub a este canal.")
    - /conectar_repositorio (dono:str, repositorio:str) - vincula o repositório ao **canal onde o comando foi usado**
    - O nome é padronizado em minúsculas (`dono/repositorio`), porque o GitHub não diferencia maiúsculas de minúsculas
    - O vínculo é gravado em `conexoes.json`, então continua valendo depois que o bot reinicia
  - Formato do `conexoes.json`:
    ```json
    {
      "usuario/meu-repo": 123456789012345678
    }
    ```
    A chave é `dono/repositorio` e o valor é o ID do canal.

**cogs/receptor.py**
- Classe Receptor
- Sobe um **servidor web dentro do próprio bot** (biblioteca `aiohttp`), que recebe os avisos (webhooks) enviados pelo GitHub:
  ```python
  async def cog_load(self):  #Roda automaticamente quando o cog é carregado
      app = web.Application()
      app.router.add_post('/github', self.receber)  #Rota que recebe os POST do GitHub
      ...
      site = web.TCPSite(self.runner, '127.0.0.1', 8080)  #Escuta na porta 8080
  ```
- `cog_unload` desliga o servidor quando o cog é descarregado, liberando a porta.
- Método `receber`:
  - lê o cabeçalho `X-GitHub-Event`, que informa o **tipo** do evento (`push`, `issues`, `pull_request`...);
  - lê o corpo da requisição (`payload`), um JSON com os detalhes do evento;
  - por enquanto, apenas imprime no terminal o tipo do evento e o repositório (`repository.full_name`);
  - responde `ok` (status 200), que é a resposta de sucesso que o GitHub espera.
- O servidor escuta apenas em `127.0.0.1`, ou seja, só aceita conexões da própria máquina. O acesso externo é feito pelo túnel (veja a seção do Cloudflare).

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

**armazenamento.py**
- Funções simples para ler e gravar o `conexoes.json`:
  - `carregar()` - lê o arquivo e devolve um dicionário (se o arquivo ainda não existe, devolve um dicionário vazio);
  - `salvar(dados)` - grava o dicionário no arquivo.
- Pode ser substituído por um banco de dados no futuro, sem mudar o restante do código.

**requirements.txt**
- Bibliotecas não nativas utilizadas;

---

### FLUXO GERAL

**Consulta sob demanda (o usuário digita um comando):**

```text
Discord → main.py → cogs/slash.py → apigithub.py → API do GitHub
                          ↓
                 embed enviado no Discord
```

**Notificação automática (o GitHub avisa o bot):**

```text
GitHub → URL pública (Cloudflare) → túnel → 127.0.0.1:8080/github → cogs/receptor.py
                                                                          ↓
                                              (próximo passo) embed no canal conectado
```

---

### BIBLIOTECAS UTILIZADAS

* **`json`** — Nativa
* **`asyncio`** — Nativa
* **`os`** — Nativa
* **`requests`** — `pip install requests`
* **`discord`** — `pip install discord.py`
* **`dotenv`** — `pip install python-dotenv`
* **`aiohttp`** — Instalada automaticamente junto com o `discord.py`
* **`apigithub`** — Módulo local (`apigithub.py`)
* **`armazenamento`** — Módulo local (`armazenamento.py`)

Ferramenta externa (não é biblioteca Python):

* **`cloudflared`** — Cliente do Cloudflare Tunnel, usado para expor o receptor na internet durante o desenvolvimento

---

### CONFIGURAÇÕES
#### CONFIGURAÇÃO DE BOT
- A criação do bot e obtenção do token é uma questão tratada pelo discord developer
- [ACESSE A DOCUMENTAÇÃO AQUI](https://docs.discord.com/developers/quick-start/getting-started#what-we-ll-be-building)
- No **Developer Portal**, na aba **Bot**, ative o **Server Members Intent** (o `main.py` usa `intents.members = True`; sem isso o bot não conecta).
- **Convite do bot ao servidor:** em **OAuth2 → URL Generator**, marque os escopos `bot` e `applications.commands` e as permissões **Send Messages** e **Embed Links**. Abra o link gerado e autorize no servidor. Sem o convite, a sincronização dos comandos falha com o erro `403 Missing Access`.

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
* **`ID_SERVER`**: ID numérico do servidor onde o bot irá operar e sincronizar os comandos (no Discord, ative o *Modo desenvolvedor* em Configurações → Avançado, clique com o botão direito no ícone do servidor e use *Copiar ID do servidor*).

> [!IMPORTANT]
> Nunca compartilhe seu arquivo `.env` nem faça o upload dele para repositórios públicos (certifique-se de que ele esteja listado no seu `.gitignore`).

**4. Arquivo `.gitignore`**

```text
.env
.venv/
__pycache__/
```

---

### INTEGRAÇÃO COM O CLOUDFLARE (TÚNEL PARA OS WEBHOOKS)

#### Por que é necessário

O receptor (`cogs/receptor.py`) roda no computador de quem está desenvolvendo, no endereço `127.0.0.1:8080`, que só existe na própria máquina. O GitHub, que envia os webhooks a partir dos servidores dele, não consegue chegar até lá.

O **Cloudflare Tunnel** resolve isso: o programa `cloudflared` abre uma conexão **de dentro para fora** e recebe uma **URL pública**. Tudo que chega nessa URL é repassado pelo túnel até a porta local do bot. Não é preciso abrir portas nem mexer no roteador.

Usamos o modo **Quick Tunnel**, que não exige conta nem configuração de DNS.

> [!NOTE]
> A integração com o Cloudflare **não está no código Python**. O `cloudflared` é um programa separado, que roda em outro terminal e aponta para a porta do receptor.

#### 1. Instalar o cloudflared (Linux/Fedora)

**Opção A: pelo repositório da Cloudflare**
```bash
curl -fsSl https://pkg.cloudflare.com/cloudflared.repo | sudo tee /etc/yum.repos.d/cloudflared.repo
sudo dnf install cloudflared -y
```

**Opção B: baixando o binário direto**
```bash
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/
```

Conferir a instalação:
```bash
cloudflared --version
```

#### 2. Abrir o túnel

Com o bot rodando (para a porta 8080 estar aberta), em **outro terminal**:

```bash
cloudflared tunnel --url http://127.0.0.1:8080
```

Ele imprime um endereço no formato:

```text
https://palavras-aleatorias.trycloudflare.com
```

Esse é o endereço público do receptor. Mantenha esse terminal aberto: se fechar, o túnel cai.

> [!WARNING]
> No Quick Tunnel a URL **muda toda vez** que o comando é reiniciado. Sempre que isso acontecer, é preciso atualizar a **Payload URL** do webhook no GitHub.

#### 3. Testar o caminho completo (simulando o GitHub)

```bash
curl -X POST https://palavras-aleatorias.trycloudflare.com/github \
  -H "X-GitHub-Event: ping" \
  -H "Content-Type: application/json" \
  -d '{"repository": {"full_name": "teste/repo"}}'
```

Resultado esperado: o `curl` retorna `ok` e o terminal do bot imprime o evento e o repositório.

#### 4. Cadastrar o webhook no GitHub

No repositório: **Settings → Webhooks → Add webhook**

| Campo | Valor |
|---|---|
| **Payload URL** | `https://palavras-aleatorias.trycloudflare.com/github` (URL do túnel **com `/github` no final**) |
| **Content type** | `application/json` (obrigatório: o receptor lê o corpo com `request.json()`) |
| **Secret** | vazio por enquanto (será usado na verificação de assinatura) |
| **Eventos** | *Let me select individual events*: Pushes, Pull requests e Issues |
| **Active** | marcado |

Ao salvar, o GitHub envia um evento de teste `ping`. Em seguida, um `git push` no repositório gera um evento `push` real, que aparece no terminal do bot.

Para depurar, use a aba **Recent Deliveries** do webhook (mostra cada entrega, a resposta do bot e permite **Redeliver**). Problemas comuns:

- **404:** faltou o `/github` no final da URL;
- **502 / erro da Cloudflare:** o túnel caiu ou a URL mudou;
- **500:** normalmente o *Content type* não está como `application/json`;
- **Nenhuma entrega:** confira se o bot e o túnel estão rodando ao mesmo tempo.

#### Segurança

Como a URL é pública, qualquer pessoa que a descubra pode enviar avisos falsos. Por isso, **antes de usar em produção**, será implementada a verificação da assinatura do GitHub (`Secret` do webhook). Quick Tunnels são indicados apenas para desenvolvimento.

---

### PARA EXECUTAR O BOT
Seguidos todos os passos até aqui, são necessários **dois terminais** abertos ao mesmo tempo (com o `.venv` ativo no primeiro):

**Terminal 1: o bot**
```bash
python main.py
```
Saída esperada:
```text
[Módulo Carregado] cogs/slash.py
[Módulo Carregado] cogs/conexoes.py
[Módulo Carregado] cogs/receptor.py
[Receptor] ouvindo em http://127.0.0.1:8080/github
Comandos sincronizados instantaneamente no servidor: 4
```

**Terminal 2: o túnel (apenas para receber webhooks)**
```bash
cloudflared tunnel --url http://127.0.0.1:8080
```

> [!TIP]
> Se o `ID_SERVER` não for encontrado, aparece o erro `TypeError: int() argument must be ... not 'NoneType'`: confira se o `.env` está na mesma pasta do `main.py` e se o nome da variável está idêntico.