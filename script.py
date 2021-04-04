from jjcli import *
import requests as reqs

dicionario = {}

"""
def getverifica():
    resp = reqs.get('http://pagfam.geneall.net/3418/pessoas_search.php?start=90&orderby=&sort=&idx=0&search=')
    resp.raise_for_status()
    return resp.text
"""

def getIndividuoHTML(id):
    resp = reqs.get('http://pagfam.geneall.net/3418/pessoas.php?id=' + str(id)) 
    resp.raise_for_status()
    return resp.text

def parseGroups(lis):
    if len(lis) == 0:
        lis = None
    else:
        lis = lis[0]

    return lis    

def parseCasamentos(ind):
    casamentosTotal = findall(r'Casamentos<\/div>.*<\/div>', ind)

    if casamentosTotal:
        casamentos = findall(r'<[aA]\s+[Hh][rR][Ee][Ff]=.*?id=(\d+)"?>(.*?)<\/[aA]>', casamentosTotal[0])
    else:
        casamentos = []

    return casamentos

def parseInfoMorte(ind):
    infoTotal = findall(r'((.|\n)*?)(Pais|Filhos|Casamentos|Notas)', ind)            
    
    if infoTotal:
        morte = findall(r'(\+.*?)<nobr>(.*?)<\/nobr>', infoTotal[0][0]) 
    else:
        morte = [None]

    return morte    

def parseInfoNascimento(ind):
    infoTotal = findall(r'((.|\n)*?)(Pais|Filhos|Casamentos|Notas)', ind)            
    
    if infoTotal:
        nascimento = findall(r'(\*.*?)<nobr>(.*?)<\/nobr>', infoTotal[0][0]) 
    else:
        nascimento = [None]

    return nascimento

def parseNotas(ind):
    notasTotal = findall(r'Notas((.|\n)*)', ind)

    if notasTotal:
        notas = findall(r'<[Ll][Ii]>(.*)<\/[Ll][Ii]>', notasTotal[0][0]) 
    else:
        notas = []

    return notas    
    
def addIndiviuo(id):
    i = getIndividuoHTML(id)

    nome = findall(r'<title>(.*)<\/title>', i)
    print(nome)
    pai = findall(r'Pai:.*?<[Aa]\s+[Hh][rR][Ee][Ff]=.*?id=(\d+)"?>.*?<\/A>', i)
    mae = findall(r'Mãe:.*?<[Aa]\s+[Hh][rR][Ee][Ff]=.*?id=(\d+)"?>.*?<\/A>', i)  
    filhos = findall(r'<[Ll][Ii]><[aA]\s+[Hh][rR][Ee][Ff]=.*?id=(\d+)"?> (.*?).*<\/[Ll][Ii]>', i)

    nascimento = parseGroups(parseInfoNascimento(i))
    morte = parseGroups(parseInfoMorte(i))           
    notas = parseNotas(i)
    casamentos = parseCasamentos(i)

    pai = parseGroups(pai)
    mae = parseGroups(mae)

    dicionario[id] = {
        "nome": nome[0],
        "filhos": filhos,
        "casamentos": casamentos,
        "nascimento": nascimento,
        "morte": morte,
        "notas": notas,
        "pai": pai,
        "mae": mae
    }

def getFamilia(id):
    addIndiviuo(id)
    ind = dicionario[id]
    
    for c in ind["casamentos"]:
        if not dicionario.get(int(c[0])):
            getFamilia(int(c[0]))

    for f in ind["filhos"]:
        if not dicionario.get(int(f[0])):
            getFamilia(int(f[0]))

    if ind["pai"] and not dicionario.get(int(ind["pai"])):
        getFamilia(int(ind["pai"]))        

    if ind["mae"] and not dicionario.get(int(ind["mae"])):
        getFamilia(int(ind["mae"]))  

getFamilia(1078242)
print(len(dicionario))


