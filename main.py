#!/usr/bin/python
# -*- coding:utf-8 -*-
# Javier Sánchez Lorente

# IMPORTACIÓN MODULOS NECESARIOS
import sys
import os
import blast as bl
import muscle as mu
import dominios as do
import graficar as gr
from shutil import rmtree

# DEFINICIÓN FUNCIONES

## Función ayuda

def help():
	message = (
	"""
	#Script para parsear, hacer blastp, arbol filogenetico y buscar dominios#
	Este script de phyton le permite comparar uno o varios querys de protei$
	frente a una base de datos creada a partir de uno o varios genbanks.
	Además, calcula el arbol filogenetico para cada query y busca dominios
	repetidos en los diferentes resultados obtenidos

	Uso: python3 main.py [-h] query subject prosite cov id
		- query: Ruta del archivo en formato FASTA que contiene una o varias 
		secuencias de proteinas en formato FASTA. Debe encontrarse en una 
		carpeta denominada "DATA/".
		- subject: Ruta del directorio donde se encuentran uno o varios 
		archivos genbanks a partir de los cuales se va a crear una base de 
		datos en formato FASTA para llevar a cabo blastp. Debe encontrarse
		eun la carpeta "DATA/"
		- prosite: Ruta donde se encuentra el archivo "prosite.dat" con la
		informacion de todos los dominios. 
		- cov [OPCIONAL]: Porcentaje minimo de cobertura para filtrar los
		resultados de Blastp. Por lo tanto, debe ser un número entre 0 y 100.
		- id [OPCIONAL]: Porcentaje de identidad minimo para filtrar tras
		realizar el Blastp. Tiene que ser un numero entre 0 y 100.
	"""
	)
	print(message)
	sys.exit()


# ARGUMENTOS

## Control de argumentos

def ctrl_cov_ide(cov,ide):
	"""
	Función para controlar que los argumentos de coverage e identidad sean
	números y enn caso afirmatico, que esten entre 0 y 100.
	"""
	
	try:
		cov=float(cov)
	except:
		print('ERROR:El argumento de covergae debe de ser un numero')
		print('\nPara obtener más ayuda: python3 main.py -h')
		sys.exit()

	try:
		ide=float(ide)
	except:
		print('ERROR:El argumento de identidad debe de ser un número')
		print('\nPara obtener más ayuda: python3 main.py -h')
		sys.exit()

	if cov>100 or cov<0:
		print('ERROR:El valor de coverage debe estar entre 0 y 100')
		print('\nPara obtener más ayuda: python3 main.py -h')
		sys.exit()

	if ide>100 or ide<0:
		print('ERROR:El valor de identidad debe de estar entre 0 y 100')
		print('\nPara obtener más ayuda: python3 main.py -h')
		sys.exit()

def ctrl_arguments():
	"""
	Controlar el numero de argumentos y las variables que definen
	"""

	arguments = sys.argv

	for argument in arguments:
		if argument == "-h":
			help()
			sys.exit()
	
	query = sys.argv[1]
	subject = sys.argv[2]
	prosite = sys.argv[3]

	if len(arguments) == 4:
		cov = 50
		ide = 30
	elif len(arguments) == 6:
		cov = sys.argv[4]
		ide = sys.argv[5]
		ctrl_cov_ide(cov, ide)
	else:
		print('ERROR:Número de argumentos introducidos incorrecto')
		print('\nPara obtener más ayuda: python3 main.py -h')
		sys.exit()

	return (query, subject, prosite, cov, ide)

def es_fasta(query):
	"""
	Función para comprobar si el query introducido tiene o no formato FASTA
	"""
	
	input_file=open(query, "r")
	result = False
	for line in input_file:
		if line.startswith(">"):
			result = True
			break
	
	if result == False:
		print('ERROR:Query introducido no tiene formato FASTA')
		print('\nPara obtener más ayuda: python3 main.py -h')
		sys.exit() 

def results():
	"""
	Función para comprobar si existe la carpeta donde se almacenarán los
	resultados, en caso negativo, la creará.
	"""

	path="RESULTS/"
	if os.path.isdir(path) == True:
		pass
	else:
		os.mkdir(path)

def clear():
	"""
	Función para eliminar los archivos obtenidos a lo largo de la ejecucción
	de las diferentes funciones de este script y que no forman parte de los
	resultados finales
	"""
	
	os.remove("output_blast")
	os.remove("subject_id")
	os.remove("subject_sequences")
	os.remove("output_blast_final")
	rmtree("RESULTS/Blast_Graficar")
	rmtree("RESULTS/Graficar_HeatMap")

def main():
	"""
	Función que ejecuta todas las demas funciones
	"""
	
	# Control de argumentos

	try:
		query, subject, prosite, cov, ide=ctrl_arguments()
		es_fasta(query)
		results()
	except:
		sys.exit()

	# Blastp

	try:
		print("EJECUTANDO MODULO BLASTP...")
		multifasta=bl.convert(subject)
		db=bl.data_base(multifasta)
		dict_query=bl.dictionary(query)
		output=bl.blastp(query, db)
		bl.blastp_final(output, cov, ide, dict_query)
		print("\n~ Se ha realizado Blastp\n")
	except:
		print("\n~ No se ha realizado Blastp\n")
		sys.exit()

	# Muscle

	try:
		print("EJECUTANDO MODULO MUSCLE...")
		mu.muscle()
		print("\n~ Se ha realizado Muscle\n")
	except:
		print("\n~ No se ha realizado Muscle\n")
		sys.exit()

	# Dominios

	try:
		print("EJECUTANDO MODULO DOMINIOS...")
		db=do.parseo_dat(prosite)
		dict_pattern=do.dictionary_patterns(db)
		do.search_pattern(dict_pattern)
		print("\n~ Se ha realizado la busqueda de dominios\n")
	except:
		print("\n~ No se ha realizado la busqueda de dominios\n")
		sys.exit()

	# Graficos de Blastp

	try:
		print("EJECUTANDO MODULO GRAFICACIÓN...")
		gr.result_blast(output, cov, ide, dict_query)
		gr.graph_blast()
		gr.archivos_heatmap()
		gr.graph_heatmap()
		print("\n~ Se ha realizado la grafiaccion de los resultados"
			" del Blastp")
	except:
		print("\n~ No se ha realizado la graficacion de los resultados" 
			" del Blastp")
		sys.exit()

	# Eliminar residuos

	clear()

	# Concluir

	message = (
	""" 
-------------------------------------------------------------\n
	    SE HA EJECUTADO EL PROGRAMA CON EXITO\n
-------------------------------------------------------------
	"""
	)
	print(message)

# EJECUCION
main()
