#!/usr/bin/python
# -*- coding: utf-8 -*-
# Javier Sánchez Lorente

# IMPORTACIÓN MODULOS NECESARIOS
import os
import sys
from subprocess import call, DEVNULL, STDOUT

# DEFINICION FUNCIONES

def muscle():
	"""
	Función para hacer un alineamiento multiple y un arbol filogenetico a
	partir de un archivo FASTA con un query (id y secuencia) y con los 
	subjects (id y secuencia) obtenidos tras el blast y su filtración
	"""

	path="RESULTS/Muscle"
	if os.path.isdir(path) == True:
		pass
	else:
		os.mkdir(path)
	
	dir="RESULTS/Blastp/"
	for input_file in os.listdir(dir):
		input=dir + input_file
		output=path + "/" + input_file[:-3] + "_alineamiento" 
		comando_alineamiento=['muscle', '-in', input,  '-out', output]

		try:
			call(comando_alineamiento, stdout=DEVNULL, stderr=STDOUT)
		except:
			print('ERROR:No se ha podido realizar el alineamiento')
			sys.exit()

		output_arbol= path + "/" + input_file[:-3] + "_arbol.nw"
		comando_arbol=['muscle', '-maketree', '-in', output, '-out', 
						output_arbol, '-cluster', 'neighborjoining']
		
		try:
			call(comando_arbol, stdout=DEVNULL, stderr=STDOUT)
		except:
			print('ERROR:No se ha podido realizar el arbol filogenetico')
			sys.exit()