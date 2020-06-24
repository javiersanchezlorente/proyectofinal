#!/usr/bin/python
# -*- coding:utf-8 -*-
# Javier Sánchez Lorente

# IMPORTACIÓN MODULOS NECESARIOS
import os
import sys
import numpy as np
from shutil import rmtree
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# DEFINICION DE FUNCIONES

def result_blast(output, cov, ide, dict_query):
	"""
	Función para obtener los porcentajes de coverage e identidad y el evalue
	de cada subject para cada arhcivo query obtenido del blastp. Despues, se
	representa para cada query, los porcentajes de coverage e identidad de 
	cada subject
	"""

	path="RESULTS/Blast_Graficar"
	if os.path.isdir(path) == True:
		pass
	else:
		os.mkdir(path)

	for key in dict_query:
		input_file=open(output, "r")
		file_name=path + "/" + key 
		f=open(file_name, "w")  
		f.write("SEQ_ID\tCOVERAGE\tIDENTITY\n")
		for line in input_file:
			columns=line.split("\t")
			if columns[0] == key:
				if float(columns[2])>=float(cov):
					if float(columns[3])>=float(ide):
						f.write(columns[1]+"\t"+columns[2] +"\t" + 
								columns[3] + "\n")
		f.close()
		input_file.close()

def graph_blast():
	"""
	Funcion para representar los porcentajes de coverage e identidad de
	cada subject para un mismo query
	"""

	path="RESULTS/Blast_Graficar"
	path2="RESULTS/Graficos"
	if os.path.isdir(path2) == True:
		pass
	else:
		os.mkdir(path2)
	
	for file1 in os.listdir(path):
		out= path2 + "/" + file1 + "grafica.jpg"
		input_file1=open(path + "/" + file1, "r")
		name=list()
		cov=list()
		ide=list()
		for line1 in input_file1:
			if line1.startswith("SEQ_ID"):
				pass
			else:
				columns=line1.split("\t")
				name.append(columns[0])
				cov.append(float(columns[1]))
				ide.append(float(columns[2]))
		plt.plot(name, cov, '+', label="cobertura", color="red")
		plt.plot(name, ide, 'x', label="identidad", color="blue")
		plt.legend()
		plt.xlabel("Nombre de las secuencias")
		plt.xticks(rotation=270)
		plt.ylabel("Porcentaje")
		plt.ylim(30,100)
		title='Porcentaje de cobertura e identidad de cada subject del query '
		plt.title(title + file1)
		plt.savefig(out)
		input_file1.close()
		
def archivos_heatmap():
	"""
	Funcion para obtener los archivos a partir de los cuales se generará
	un heatmap para cada query. Para ello, se dividen los porcentajes de
	cobertura e identidad en intervalos de 10 y se calcula el numero de 
	subjects de cada query que estan presentes en cada intervalo.
	"""
	path="RESULTS/Blast_Graficar"
	path2="RESULTS/Graficar_HeatMap"
	if os.path.isdir(path2) == True:
		pass
	else:
		os.mkdir(path2)

	for file1 in os.listdir(path):
		cov=list()
		ide=list()
		out=path2 + "/" + file1 + "datos.txt"
		
		input_file1=open(path + "/" + file1, "r")
		for line1 in input_file1:
			if line1.startswith("SEQ_ID"):
				pass
			else:
				columns=line1.split("\t")
				cov.append(float(columns[1]))
				ide.append(float(columns[2]))

		output_file=open(out, "w")
		for a in range(0,110,10):
			for b in range(0,110,10):
				count=0
				for c in range(0,len(cov)):
					for d in range(0, len(ide)):
						if float(a)<=float(cov[c]):
							if float(cov[c])<float(a+10):
								if float(b)<=float(ide[d]):
									if float(ide[d])<float(b+10):
										count += 1
				output_file.write(str(a) + "\t" + str(b) + "\t" + 
								str(count) +"\n")
		output_file.close()
		input_file1.close()

def graph_heatmap():
	"""
	Funcion par representar los archivos heatmap creados anteriormente. Nos
	permite obtener una vision de la distribucion de los distintos subjects
	segun sus porcentajes de cobertura e identidad
	"""

	path="RESULTS/Graficar_HeatMap"
	path2="RESULTS/Graficos"
	if os.path.isdir(path2) == True:
		pass
	else:
		os.mkdir(path2)

	for file1 in os.listdir(path):
		out=path2+ "/" + file1[:-9] + "_heatmap.jpg"
		input_file1=open(path + "/" + file1, "r")
		z=list()
		for line1 in input_file1:
			columns=line1.split("\t")
			z.append(float(columns[2]))
		
		coverage=np.linspace(0,100,11)
		identity=np.linspace(0,100,11)
		cantidad=np.array(z).reshape(11,11)
		z_min, z_max = np.abs(z).min(), np.abs(z).max()

		fig, ax = plt.subplots()
		levels=MaxNLocator(nbins=10).tick_values(z_min, z_max)
		c=ax.contourf(coverage, identity, cantidad, levels=levels, 
		cmap='GnBu', vmin=z_min, vmax=z_max)
		title='Nº de subjects para cada intervalo de \ncobertura e identidad'
		ax.set_title(title + " del query " + file1[:-9])
		ax.axis([coverage.min(),coverage.max(), 
				identity.min(), identity.max()])
		fig.colorbar(c, ax=ax)
		plt.ylabel('Porcentaje de cobertura')
		plt.xlabel('Porcentaje de identidad')
		plt.savefig(out)