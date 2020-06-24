#!/usr/bin/python
# -*- coding: utf-8 -*-
# Javier Sánchez Lorente

# IMPORTACIÓN MODULOS NECESARIOS
import os
import sys
from re import sub
from Bio import SeqIO
from subprocess import call, DEVNULL, STDOUT

# DEFINICIÓN FUNCIONES

def convert(dir):
	"""
	Función para convertir uno o varios archivos genbank almacenados en un
	unico directorio en un unico archivo multifasta, en formato FASTA, es 
	decir, con cabecera con ">" y con lineas de maximo 60 caracteres. 
	"""

	if os.path.isdir(dir) == True:
		pass
	else:
		print('ERROR:No existe el directorio indicado')
		sys.exit()
	
	path="RESULTS/Multifasta"
	if os.path.isdir(path) == True:
		pass
	else:
		os.mkdir(path)

	out= path + "/multifasta.fa"
	if os.path.isfile(out) == True:
		os.remove(out)
	else:
		pass
	
	input_file=open(out, "a")
	for gbff in os.listdir(dir):
		files=dir+gbff
		if os.path.isfile(files) == True:
			input_handle=open(files,"r")
			for record in SeqIO.parse(input_handle, "genbank"):
				for feature in record.features:
					if feature.type == 'CDS':
						try:
							seqprot = feature.qualifiers['translation'][0]
						except:
							seqprot = "empty"
						if seqprot != "empty":
							seqUpper=seqprot.upper()
							seqUpper=sub('(.{60})(.)',r'\1\n\2',seqUpper)
							input_file.write(">" + feature.qualifiers
								['locus_tag'][0] +"\n"+seqUpper+"\n")								
	input_file.close()
	return out

def data_base(multifasta):
	"""
	Funcion para crear una base de datos a partir del multifasta obtenido
	previamente. Las almacena en una carpeta dentro de la carpeta de Data
	"""
	
	path="DATA/data_base"
	if os.path.isdir(path) == True:
		pass
	else:
		os.mkdir(path)

	input_file=multifasta
	output=path + "/db"
	cmd_db=['makeblastdb', '-dbtype', 'prot', '-parse_seqids', '-in', 
			input_file, '-out', output]
	
	try:
		call(cmd_db, stdout=DEVNULL, stderr=STDOUT)
	except:
		print ('ERROR:No se ha podido realizar la base de datos')
		sys.exit()
	
	return output

def dictionary(query):
	"""
	Funcion para crear un diccionario con los distintos id y secuencia de 
	uno o varios query que se encuentran en el archivo FASTA query.
	"""
	
	dict_query=dict()
	query_seq=str()
	input_file=open(query, "r")
	c=0
	
	for line in input_file:
		if line.startswith(">"):
			if c !=0:
				dict_query[query_id]=query_seq
				query_seq=str()
			query_id=line.strip()
			query_id=query_id[1:]
			c=1
		elif line.startswith("\n") == False:
			query_seq=query_seq+line.strip()
		else:
			continue
	dict_query[query_id]=query_seq
	input_file.close()

	return dict_query

def blastp(query, db):
	"""
	Función para realizar Blastp con un archivo en formato FASTA con
	una o varias secuencias query, frente a la base de datos creada
	previamente. Del Blastp se obtienen los identificadores del query
	y del subject, y los valores de cobertura. identidad y e-value
	"""
	
	out_blast="output_blast"
	cmd_blastp=['blastp', '-query', query, '-db', db, '-outfmt', 
				'6 qseqid sseqid qcovs pident evalue', '-evalue', 
				'0.00001', '-out', out_blast]
	try:
		call(cmd_blastp, stdout=DEVNULL, stderr=STDOUT)
	except:
		print('ERROR:No se ha podido realizar Blastp')
		sys.exit()

	input_file=open(out_blast, "r")
	seqid_file=open("subject_id", "w")
	for line in input_file:
		columns=line.split("\t")
		seqid_file.write(columns[1] + "\n")	
	input_file.close()
	seqid_file.close()

	cmd_blastp2 = ['blastdbcmd', '-entry_batch', 'subject_id', '-db', db,
				'-outfmt', '%s', '-out', 'subject_sequences']
	try:
		call(cmd_blastp2, stdout=DEVNULL, stderr=STDOUT)
	except:
		print('ERROR: No se ha podido realizar Blastp')
		sys.exit()

	sub_seq=open("subject_sequences", "r")
	seq=list()
	for line1 in sub_seq:
		seq.append(line1)
	sub_seq.close()

	out_final="output_blast_final"
	blast_in=open(out_blast, "r")
	blast_fi=open(out_final, "w")
	c = 0
	
	for line in blast_in:
		line=line.strip()
		blast_fi.write(line + "\t" + seq[c])
		c += 1
	blast_in.close()
	blast_fi.close()
	
	return out_final

def blastp_final(output, cov, ide, dict_query):
	"""
	Función para filtrar el archivo final del blast segun los criterios de
	cobertura e identidad indicados por el usuario y almacenarlo en un 
	archivo para cada query
	"""
	
	path="RESULTS/Blastp"
	if os.path.isdir(path) == True:
		pass
	else:
		os.mkdir(path)

	for key in dict_query:
		input_file=open(output, "r")
		file_name=path+ "/" +key+".fa"
		f=open(file_name, "w")
		f.write(">" + key + "\n" + dict_query[key] + "\n")
		for line in input_file:
			columns=line.split("\t")
			if columns[0] == key:
				if float(columns[2])>=float(cov):
					if float(columns[3])>=float(ide):
						f.write(">" + columns[1] +  "\n" + columns[5] + "\n")
		input_file.close()