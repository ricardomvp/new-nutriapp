from utils.scraping.e_aditivos.e_aditivos import get_e_aditivos
from utils.scraping.aditivos_alimentarios.aditivos_alimentarios import get_aditivos_alimentarios
from utils.scraping.ingredientes_de_cocina.ingredientes_de_cocina import get_ingredientes_de_cocina
from utils.scraping.hablemos_claro.hablemos_claro import get_hablemos_claro
import unicodedata
import unidecode


def find_villians(products):
    e_aditivos=get_e_aditivos() #['name','e-number','toxicity','origin','clasif','link']
    aditivos_alimentarios=get_aditivos_alimentarios()
    ingredientes_de_cocina=get_ingredientes_de_cocina()
    agentes=get_hablemos_claro()
    # print(agentes)
    villians=[]
    peligroso=[]
    sospechoso=[]
    no_nocivo=[]
    otro=[]
    desconocido=[]

    no_encontrado={
        'name':'Not finded',
        'e-number':'?',
        'toxicity':'?',
        'origin':'?',
        'clasif':'?',
        'link':'-',
    }
    #toxicity=['No nocivo','Sospechoso','¡Peligroso!']
    for product in products:
        product = unidecode.unidecode(product)
        finded=False
        if len(product)>3:

            if finded==False:
                for aditivo in e_aditivos:
                    match=0
                    #eliminar acentos
                    aditivo['name'] = unicodedata.normalize("NFKD", aditivo['name']).encode("ascii","ignore").decode("ascii")
                    match=aditivo['name'].lower().count(product)
                    if aditivo['name']==product:
                        match=1
                    if match>0:
                        finded=True
                        if aditivo['toxicity']=='¡Peligroso!':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            peligroso.append(dict)

                        if aditivo['toxicity']=='Sospechoso':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            sospechoso.append(dict)

                        if aditivo['toxicity']=='No nocivo':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            no_nocivo.append(dict)

                        break

            if finded==False:
                for aditivo in aditivos_alimentarios:
                    match=0
                    #eliminar acentos
                    aditivo['name'] = unicodedata.normalize("NFKD", aditivo['name']).encode("ascii","ignore").decode("ascii")

                    match=aditivo['name'].lower().count(product)
                    if aditivo['name']==product:
                        match=1
                    if match>0:
                        finded=True
                        if aditivo['toxicity']=='Alta':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            peligroso.append(dict)

                        if aditivo['toxicity']=='Media':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            sospechoso.append(dict)

                        if aditivo['toxicity']=='Baja':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            no_nocivo.append(dict)

                        if aditivo['toxicity']=='- - -':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            desconocido.append(dict)

                        break

            if finded==False:
                for aditivo in ingredientes_de_cocina:
                    match=0
                    #eliminar acentos
                    aditivo['name'] = unicodedata.normalize("NFKD", aditivo['name']).encode("ascii","ignore").decode("ascii")

                    match=aditivo['name'].lower().count(product)
                    if aditivo['name']==product:
                        match=1
                    if match>0:
                        finded=True
                        dict={
                            'name':product,
                            'aditivo':aditivo,
                            }
                        desconocido.append(dict)

            if finded==False:
                for aditivo in agentes:
                    match=0
                    #eliminar acentos
                    aditivo['name'] = unicodedata.normalize("NFKD", aditivo['name']).encode("ascii","ignore").decode("ascii")
                    match=aditivo['name'].lower().count(product)
                    if aditivo['name']==product:
                        match=1
                    if match>0:
                        finded=True
                        if aditivo['toxicity']=='Alta':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            peligroso.append(dict)

                        if aditivo['toxicity']=='Media':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            sospechoso.append(dict)

                        if aditivo['toxicity']=='Baja':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            no_nocivo.append(dict)

                        if aditivo['toxicity']=='---':
                            dict={
                                'name':product,
                                'aditivo':aditivo,
                            }
                            desconocido.append(dict)

                        break

            if finded==False:
                dict={
                    'name':product,
                    'aditivo':no_encontrado,
                }
                otro.append(dict)


    villians=[peligroso,sospechoso,no_nocivo,desconocido,otro]

    return villians
