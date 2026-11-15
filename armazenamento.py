import os
import json

#provisorio, vou ver de adicionar uma conexão com o Postgres depois
ARQUIVO = 'conect.json'

#le o arquivo e retorna um dicionario
#o tratamento é: se ele n existe, devolve vazio
def carregar():
    if not os.path.exists(ARQUIVO):
        return {} # retorna vazio
    with open(ARQUIVO, 'w', encoding = 'utf-8') as arq:
        return json.load(arq)

# grava o dicionario retornado, dentro do arquivo
def salvar(data):
    with open(ARQUIVO, 'w', encoding = 'utf-8') as arq:
        json.dump(data, arq, indent = 2)# o indent deixa o arquivo JSON mais legivel

