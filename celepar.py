import json
import requests
import datetime
from bs4 import BeautifulSoup

URL = "http://celepar7.pr.gov.br/sima/cotdiap1.asp"
TIME = str(datetime.datetime.now())[:-7].replace(':', '-').replace('/', '-')
print(TIME)
def get_dom(URL,produto):
    res = requests.post(URL, data = {'produto':produto,'submit1':'Pesquisar'})
    dom = BeautifulSoup(res.text, 'lxml')
    return dom

def get_data(URL):
    count = 1
    data = {}
    while count <= 16:
        dom = get_dom(URL, count)
        nome = dom.select_one('[color=RoyalBlue] > b')
        nome = nome.text[:-16].strip()
        grao = {}
        if 'Pesquisa descontinuada' in nome:
            count += 1
            continue
        else:
            tables = dom.select('[border=1]')
            # print(data)
            for table in tables:
                
                rows = table.select('tr')
                for row in rows[1:]:
                    cidade = {}
                    line = list(row.stripped_strings)
                    if '\\' in line[1] or 'AUS' in line[1] or 'SINF' in line[1]:
                        continue
                    else:
                        cidade['min']=float(line[1])
                        cidade['m_c']=float(line[2])
                        cidade['max']=float(line[3])
                    grao[line[0]] = cidade
            print(nome)
        count += 1
        data[nome] = grao
    return data

data = get_data(URL)
print(data)
arquivo = open('historico/' + TIME + '.json', 'w')
arquivo.write(json.dumps(data, indent=2))
arquivo.close()