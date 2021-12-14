#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import sys


def status(info):
    info = str(info)
    if 'verde' in info:
        return 0
    elif 'amarelo' in info:
        return 1
    elif 'vermelho' in info:
        return 2
    else:
        return 0


def consultaStatus(UF, servico):
    url = "http://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    g_data = soup.find_all("table", {"class": "tabelaListagemDados"})
    for item in g_data:
            estado = dict()
            for tr in item.find_all("tr"):
                line = tr.contents
                estado[line[1].text] = {'Autorizacao': status(line[2].img), 
                                        'Retorno autorizacao': status(line[3].img),
                                        'Inutilizacao': status(line[4].img),
                                        'Consulta protocolo': status(line[5].img),
                                        'Status servico': status(line[6].img),
                                        'Consulta cadastro': status(line[8].img),
                                        'Recepcao evento': status(line[9].img)}

    return estado[UF][servico]

print(consultaStatus(sys.argv[1], sys.argv[2]))
