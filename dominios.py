#!/usr/bin/python
# -*- coding_ utf-8 -*-
# Javier Sánchez Lorente

# IMPORTACIÓN MODULOS NECESARIOS
import re
import os
import sys
from Bio.ExPASy import Prosite

# DEFINICION FUNCIONES

def parseo_dat(input_file):
    """
    Función para pasear un archivo .dat con la informacion de todos los
    dominios de la base de datos de prosite, además de su nombre, aceso
    y descripcion, se guardar en una archivo en la carpta de "DATA/"
    """

    if os.path.isfile(input_file) == True:
        pass
    else:
        print('ERROR:No existe el archivo indicado')
        sys.exit()

    path="DATA/data_base_prosite/"
    if os.path.isdir(path) == True:
        pass
    else:
        os.mkdir(path)
    
    handle = open(input_file,"r")
    out=path + "/db"
    output=open(out, "w")
    records = Prosite.parse(handle)
    for record in records:
        output.write(record.name + "\t")
        output.write(record.accession + "\t")
        output.write(record.description + "\t")
        output.write(record.pattern + "\n")
    handle.close()
    output.close()

    return out
    
def dictionary_patterns(db):
    """
    Función para, a partir de la base de datos, crear un diccionario en el
    que cada acceso tenga asociado un patrón, nombre y descripción, pero 
    solo para aquellos que tengan un patrón.
    """

    dict_pattern=dict()
    input_f=open(db, "r")
    
    for line in input_f:
        columns=line.split("\t")
        name=columns[0]
        accession=columns[1]
        description=columns[2]
        pattern=columns[3].strip()
        pattern=pattern.replace("-", "" )
        pattern=pattern.replace("x", ".")
        pattern=pattern.replace("(", "{")
        pattern=pattern.replace(")", "}")
        pattern=pattern.strip()
        if pattern == "":
            pass
        else:
            dict_pattern[accession]=[pattern, name, description]
    
    input_f.close()
    return dict_pattern

def search_pattern(dict_pattern):
    """
    Función para buscar dominios de la base de datos creada, almacenada en el
    diccionario tambien creado, en los archivos con las secuencias obtenidas 
    del Blastp. El resultado final se trata de un archivo para cada query en 
    el que se muestra el nombre de cada subject y todos los dominios presentes
    en su secuencia, además del nombre y la descripción.
    """
    
    path="RESULTS/Prosite"
    if os.path.isdir(path) == True:
        pass
    else:
        os.mkdir(path)

    dir="RESULTS/Blastp/"
    for input_file in os.listdir(dir):
        f=open(dir + input_file, "r")

        output=path + "/" + input_file[:-3] + "_dominios.txt" 
        g=open(output, "w")
        for line in f:
            if line.startswith(">"):
                id=line
                id=id[1:]
                g.write("PROTEINA: " + id + "\n")
            elif line.startswith("\n") == False:
                seq = line.strip()
                count=0
                for key in dict_pattern:
                    rgx=re.compile(dict_pattern[key][0])
                    result=rgx.search(seq)
                    if result == None:
                        pass
                    else:
                        count += 1
                        result_final=result.group()
                        g.write(str(count) + "º Dominio: \n\n" + 
                        "Nombre del dominio: " + dict_pattern[key][1] + "\n" 
                        + "Acceso del dominio: " + key + "\n" + "Patron: " +
                        str(result_final)  + "\n" + "Descripcion: " + 
                        dict_pattern[key][2] + "\n\n")
            else:
                pass
        g.close()
        f.close()