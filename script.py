from jjcli import *
import requests as reqs
import json

individuos = {}
familias = {}

def get_individuo_html(id):
    resp = reqs.get('http://pagfam.geneall.net/3418/pessoas.php?id=' + str(id)) 
    resp.raise_for_status()
    return resp.text

def get_familias_html():
    resp = reqs.get('http://pagfam.geneall.net/3418/familias_search.php') 
    resp.raise_for_status()
    return resp.text

def get_familia_html(id):
    resp = reqs.get('http://pagfam.geneall.net/3418/fam_names.php?id=' + str(id)) 
    resp.raise_for_status()
    return resp.text

def parse_groups(lis):
    if len(lis) == 0:
        lis = None
    else:
        lis = lis[0]

    return lis

def tuple_to_person(lis):
    return list(map(lambda x: {'id': x[0],'nome': x[1].strip()}, lis))

def tuple_to_acontecimento(lis):
    return list(map(lambda x: {'local': x[0].strip(),'data': x[1]}, lis))


def parse_casamentos(ind):
    casamentos_total = findall(r'Casamentos<\/div>.*<\/div>', ind)

    if casamentos_total:
        casamentos = findall(r'<[aA]\s+[Hh][rR][Ee][Ff]=.*?id=(\d+)"?>(.*?)<\/[aA]>', casamentos_total[0])
    else:
        casamentos = []

    return tuple_to_person(casamentos)

def parse_info_morte(ind):
    info_total = findall(r'((.|\n)*?)(Pais|Filhos|Casamentos|Notas)', ind)            
    
    if info_total:
        morte = findall(r'(\+.*?)<nobr>(.*?)<\/nobr>', info_total[0][0]) 
    else:
        morte = [None]

    return morte    

def parse_info_nascimento(ind):
    info_total = findall(r'((.|\n)*?)(Pais|Filhos|Casamentos|Notas)', ind)            
    
    if info_total:
        nascimento = findall(r'(\*.*?)<nobr>(.*?)<\/nobr>', info_total[0][0]) 
    else:
        nascimento = [None]

    return nascimento

def parse_notas(ind):
    notas_total = findall(r'Notas((.|\n)*)', ind)

    if notas_total:
        notas = findall(r'<[Ll][Ii]>(.*)<\/[Ll][Ii]>', notas_total[0][0]) 
    else:
        notas = []

    return notas    
    
def add_indiviuo(id):
    i = get_individuo_html(id)

    nome = findall(r'<title>(.*)<\/title>', i)[0]
    print(nome)
    pai = findall(r'Pai:.*?<[Aa]\s+[Hh][rR][Ee][Ff]=.*?id=(\d+)"?>(.*?)<\/A>', i)
    mae = findall(r'Mãe:.*?<[Aa]\s+[Hh][rR][Ee][Ff]=.*?id=(\d+)"?>(.*?)<\/A>', i)  
    filhos = findall(r'<[Ll][Ii]><[aA]\s+[Hh][rR][Ee][Ff]=.*?id=(\d+)"?>(.*?)<\/[aA]>.*<\/[Ll][Ii]>', i)
    filhos = tuple_to_person(filhos)

    nascimento = parse_groups(tuple_to_acontecimento(parse_info_nascimento(i)))
    morte = parse_groups(tuple_to_acontecimento(parse_info_morte(i)))           
    notas = parse_notas(i)
    casamentos = parse_casamentos(i)

    pai = tuple_to_person(pai)
    pai = parse_groups(pai)
    mae = tuple_to_person(mae)
    mae = parse_groups(mae)

    individuos[id] = {
        "nome": nome,
        "filhos": filhos,
        "casamentos": casamentos,
        "nascimento": nascimento,
        "morte": morte,
        "notas": notas,
        "pai": pai,
        "mae": mae
    }

def get_familia(id):
    add_indiviuo(id)
    ind = individuos[id]
    
    for c in ind["casamentos"]:
        if not individuos.get(int(c['id'])):
            get_familia(int(c['id']))

    for f in ind["filhos"]:
        if not individuos.get(int(f['id'])):
            get_familia(int(f['id']))

    if ind["pai"] and not individuos.get(int(ind["pai"]['id'])):
        get_familia(int(ind["pai"]['id']))        

    if ind["mae"] and not individuos.get(int(ind["mae"]['id'])):
        get_familia(int(ind["mae"]['id']))  

def get_familias():
    fams = findall(r'<[Ll][Ii]><[aA]\s+[Hh][rR][Ee][Ff]=.*?id=(\d+)"?>(.*?)<\/[aA]>.*?<\/[Ll][Ii]>',get_familias_html())
    for f in fams:
        fam = get_familia_html(f[0])
        inds = findall(r'<[aA]\s+[Hh][rR][Ee][Ff]=pessoas.php\?id=(\d+)"?>(.*?)<\/[aA]>',fam)
        familias[f[0]] = {
            'nome': f[1],
            'pessoas': tuple_to_person(inds)
        } 

get_familia(1078242)

get_familias()



f = open("familia.json", "a")
f.write(json.dumps(individuos))
f.close()

f = open("familias.json", "a")
f.write(json.dumps(familias))
f.close()


