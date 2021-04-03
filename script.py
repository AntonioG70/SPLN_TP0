from jjcli import *
import requests as reqs

dicionario = {}

def getIndividuoHTML(id):
    resp = reqs.get('http://pagfam.geneall.net/3418/pessoas.php?id=' + str(id)) 
    resp.raise_for_status() 
    print(resp.text)
    return resp.text

def adicionaIndiviuo(id):
    i = getIndividuoHTML(id)

    dicionario[id] = {
        nome: findall(r'<title>([\w \-]+)</title>', i),
        filhos: findall(r'>(Filhos).*<[aA]\s+[Hh][rR][Ee][Ff]=(.*?id=(\d+)"?)> (.*?)</[aA]>', i),
        casamentos: findall(r'>(Casamentos).*<nobr>(.*)<\/nobr>.*<[aA]\s+[Hh][rR][Ee][Ff]=(.*?id=(\d+)"?)> (.*?)<\/[aA]>', i)

    }

i = getIndividuoHTML(1076116)
print(i)
nome = findall(r'<title>([\w \-]+)</title>', i)
casamentos = findall(r'(Casamentos)<\/div>(<div.*?>.*<[aA]\s+[Hh][rR][Ee][Ff]=(.*?id=(\d+)"?)> (.*?)<\/[aA]>.*<\/div>)*', i)
filhos = findall(r'>(Filhos).*<[aA]\s+[Hh][rR][Ee][Ff]=(.*?id=(\d+)"?)> (.*?)</[aA]>', i)
info = findall(r'(\*.*?)<nobr>(.*?)<\/nobr>', i)
infoMais = findall(r'(\+.*?)<nobr>(.*?)<\/nobr>', i)
familiares = findall(r'<[aA]\s+[Hh][rR][Ee][Ff]=(.*?id=(\d+)"?)>(.*?)</[aA]>', i)
print(nome)
print(casamentos)
print(info)
print(infoMais)
print(filhos)
