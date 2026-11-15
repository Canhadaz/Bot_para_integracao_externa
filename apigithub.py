import requests
import json

class Api_github():
   def __init__(self, usuario):
      self.usuario = usuario

   # get no /users/{usuario}
   def requisicao_usuario(self):
      resposta = requests.get(
         f'https://api.github.com/users/{self.usuario}'
      )
      if resposta.status_code == 200:
         return resposta.json()
      else:
         return resposta.status_code

   # get no /users/{usuario}/repos
   def consulta_projetos(self, pagina=None):
      url = f'https://api.github.com/users/{self.usuario}/repos'
      
      params = {}
      if pagina is not None:
         params['page'] = pagina
         
      resposta = requests.get(url, params=params)
      
      if resposta.status_code == 200:
         return resposta.json()
      else:
         return resposta.status_code