# PARSEO, BLASTP, ARBOL FILOGENÉTICO Y DOMINIOS. #

Este programa de Python le permite comparar uno o varios querys de proteinas en
formato FASTA en un único archivo frente a una base de datos creada a partir de
uno o varios genbanks que se encuentran en un mismo directorio. Los resultados 
de este Blastp se filtraran segun los valores que indique el usuario, si no los
introducen se definen uno valores predeterminados para cobertura e identidad de 
un 50% y un 30% respectivamente.

Una vez se ha realizado el BLastp, se obtendra un archivo para cada query con
los ids y las secuencias de los subjects que cumplen los requisitos introducidos
por el usuario. Estos archivos se almacenaran en la carpeta "RESULTS/Blastp". 
Se trata de un archivo en formato FASTA

Además, a partir de cada archivo resultante del Blastp, se hace un alineamiento
multiple de todas las secuencias almacenadas en dicho documento, obteniendose un
nuevo archivo con todas las secuencias alineadas, en este caso, se almacenaran 
en la carpeta "RESULTS/Muscle". Además, a partir de cada alineamiento multiple, 
se realizará un arbol filogenetico siguiendo el cluster de neighbor-joining, 
almacenandose tambien en esta carpeta y con una extensión ".nw". Estos archivos 
se pueden visualizar visitando la pagina iTOL.

Por último, este programa también es capaz de buscar dominios presentes en las 
diferentes secuencias obtenidas de cada Blastp, para ello, se parsea una base 
de datos, en este caso "prosite.dat" que se almacena en la carpeta "DATA/Prosite", 
esta base de datos se puede obtener de la pagina web de Prosite. Una vez se 
obtiene dicha base se crea un diccionario para el que guarda el patron, nombre y 
descripcion de cada entrada de la base de datos. Por lo tanto, se compara cada 
secuencia con todas las entradas de dicha base y se obtiene un nuevo documento, 
esta vez en "RESULTS/Prosite" que muestra el id de cada proteina y dominio del 
patron encontrado, además de su nombre y descripcion.

Adicionalmente, el script "graficar.py" nos permite representar los resultados 
de cada Blastp de cada query mediante dos tipos de graficar. En la primera, se 
muestra para cada query los porcentajes de cobertura e identidad de cada subject.
El segundo gráfico se trata de un heatmap en el que se representa el numero de
subjects de cada query para cada intervalo de identidad y cobertura.

## Requisitos

Para ejecutrar este programa debe de tener instalado BioPython además de contar 
con una version de Python igual o superior a 3. Para la representacion hace falta
la instalacion de Matplotlib y Numpy.

Además debe de descargar los cuatro scripts de python: "Blast.py", "Muscle.py",
"Dominios.py" y "Main.py".

Por último, se recomienda crear una carpeta denominada "DATA", que a su vez 
contenga las siguientes carpetas:

- Query: Contiene el archivo multifasta con la(s) secuencia(s)
  	que se van a utilizar como query.

 - Genbank: Directorio con los archivos genbank que se van a 
  utilizar para gener el multifasta y la base de datos.
 - Prosite: Carpeta con el archivo "prosite.dat" para obtener
  la base de datos de los dominios de las proteinas

## Uso

***python3 main.py [-h] [query] [subject] [prosite] [cov] [id]***

- query: Ruta del archivo en formato FASTA que contiene una o varias 
  secuencias de proteinas en formato FASTA. Debe encontrarse en una 
  carpeta denominada "DATA/".

- subject: Ruta del directorio donde se encuentran uno o varios 
archivos genbanks. Debe de encontrarse en la carpeta "DATA/"
- prosite: Ruta del archivo "prosite.dat" con la informacion de los
dominios de las proteinas. Se obtiene de la pagina de Prosite
- cov [OPCIONAL]: Porcentaje minimo de cobertura para filtrar los
resultados de Blastp. Por lo tanto, debe ser un número entre 0 y 100.
- id [OPCIONAL]: Porcentaje de identidad minimo para filtrar tras
realizar el Blastp. Tiene que ser un numero entre 0 y 100.

### Ejemplo: ###
python3 main.py DATA/Query/PBPs_query.fa DATA/Genbanks/ DATA/Prosite/prosite.dat 50 30


