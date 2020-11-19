import logging
import csv
import os

def get_hablemos_claro():
    lista_dict=[]
    lista=_read_data()
    for row in lista:
        diccionario={
        lista[0][0] : row[0].replace('/',','), #name
        lista[0][1] : row[1],                  #e-number
        lista[0][2] : row[2],                  #toxicity
        lista[0][3] : row[3],                  #origin
        lista[0][4] : row[4],                  #clasification
        lista[0][5] : row[5],                  #link
        }
        lista_dict.append(diccionario)
    return lista_dict

def _read_data():
    lista=[]
    cwd = os.getcwd()
    with open(cwd + '/utils/scraping/hablemos_claro/hablemos_claro.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
                lista.append(row)
    return lista
