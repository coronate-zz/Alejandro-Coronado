
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os
nObs=100
nEdos=10
nNodos=9	

def getSistema( nObs=nObs, nEdos=nEdos, nNodos=nNodos):

	"""
	getsistema:  FUNCION  DE CREACION DE PESOS(nEdos) ALEATORIOS 
	PARA # NODOS ( nNodos ).

	Genera un diccionario con #keys==#numeroNodos
	cada key tiene su propio diccionario en donde el valor de 

	diccionario['A']['B']==diccionario['B']['A']
	diccionario['A']['A']==-00
	diccionario['A']['X']==numero:{ nEdos }  para toda X!=A


	"""	
	nodosLetras=map(chr, range(65, 65+nNodos))
	dicNodos={nodo:-100 for nodo in nodosLetras}
	#print(dicNodos)

	#nodos={'A':0 , 'B':0 ...}

	for nodoI in dict.keys( dicNodos ):
		#Empieza en dicNodos['A']
		print('       NODO CABEZA : {}'.format(nodoI ) )
		if dicNodos[nodoI]==-100: # elemento Vacio A:-100
			
			dicNodos[nodoI]={nodo:-100 for nodo in nodosLetras} 

			# [  A[A:-100 , B:-100, ...], B[A:-100, b: -100, ...H:-100]  ]
			for nodoJ in dict.keys( dicNodos[nodoI] ): 
				print(' Nodo CONEXION: {}'.format(nodoJ ) )
				#nodos[i]=np.random.randint(nEdos, size=(nObs))
				#print(dicNodos[nodoJ])
				if nodoJ==nodoI:
					dicNodos[nodoI][nodoJ]=-np.inf
					print('nodos iguales, asignado -00')
				elif dicNodos[nodoJ]== - 100: # El diccionario no se ha credao en ambos puntos
					#CREAR CONEXION
				
					dicNodos[nodoI][nodoJ]=np.random.randint(nEdos)
					print('CREAR {}'.format(dicNodos[nodoI][nodoJ]))
				else:
				
					#COPIAR CONEXION
					if dicNodos[nodoJ][nodoI] != - 100: 
						#El diccionario existe en J y tambien el balor nodo_ji
						dicNodos[nodoI][nodoJ]= dicNodos[nodoJ][nodoI]
				   		print('COPIAR  {}'.format(dicNodos[nodoI][nodoJ]))
					else:
						print('xxxxx')

		else:
			print('dic no creado ')

	print(dicNodos)
	return (dicNodos)			







def getCode( sistema ):
	"""
	decode: REGRESAR UN CODIGO QUE REPRESENTE EL TIPO DE PROBLEMA A RESOLVER

	Cada sistema tendra una matriz = nNodos * nNodos donde 
	matriz[X][Y]=distancia nodoX a nodoY
	==>

	[A]        [][][][][]
	[B][A]       [][][][]
	[C][A][C]        [][]
	[D][B][B][A]       []
	[A][D][D][D][B][C]

	donde A,B,C,D pertenecen a nEstados 
	El codigo estara Reprsentado por el triangulo inferior dado que el triangulo superior sera una repeticion del inferior.

	entonces tendremos un total de:
	[ nNodos + [nNodos-1] + [nNodos-2]  ... +[1] ]** nEdos

	"""
	#i=0
	#j=1
	j=0
	for i in range(len(sistema.iloc[1])):
		j=j+1
		#print(sistema.iloc[i][j:]) #triangulo inferior
		if i==0:
			codigo= sistema.iloc[i][j:]
			letras=pd.Series([codigo.name for i in range(len(codigo)) ] , index=codigo.index)
			codigo=pd.concat([codigo, letras], axis=1)
		else:	

			codigo2= sistema.iloc[i][j:]
			letras=pd.Series([codigo2.name for i in range(len(codigo2)) ] , index=codigo2.index)
			codigo2.name='A'
			codigo2=pd.concat([codigo2, letras], axis=1)
			codigo= pd.concat( [codigo, codigo2])

	codigo=codigo.set_index([0,codigo.index])
	codigo.index.names=['nodoI'],['nodoJ']
	return(codigo)



def agregarSolucion(soluciones, sisCodeData,  solucion=1000, peso=555):
	"""
	DICCIONARIO CON CON SOLUCIONES PARA CADA TIPO DE SISTEMA CON N ESTAOS

	NIVEL 1 <- NUMERO DE NODOS
		NIVEL 2 <- SOLUCIONES RESUELTAS PARA SISTEMAS DE X NODOS
			NIVEL 3 <- INFORMACION DEL SISTEMA RESUELTO
				-Decodificacion del problema
				-Suma del vector de Decodificacion
				-##solucion del sistema
				-##peso aportado al problema

	soluciones[numeroNodos][numeroSolucion][ Decodificacion, suma ... etc ]
	
	"""
	if not bool(soluciones): #Las soluciones estan vacias para cualquier nivel
		soluciones[len(sisCodeData)]={ 1:{ 'sisCode':sisCodeData , 'suma':sisCodeData.sum(), 'solucion':solucion, 'peso':peso  } }
		#print(soluciones)
		print('Insertando solcion para sistema de {} NODOS  '.format(len(sisCodeData)))
	else :
		try: #EXISTE un diccionario en solcuiones para datos de x nodos?
			if not bool(soluciones[len(sisCodeData)]) : #Esta vacio el nivel de solucion []
				print('Existe pero esta vacio')
				soluciones[len( sisCodeData )]\
				={ 1:{ 'sisCode':sisCodeData , 'suma':sisCodeData.sum(), 'solucion':solucion, 'peso':peso } }

			else: #Agregar una solucion
				#print( len( soluciones[len( sisCodeData )].keys() ) )
				soluciones[len( sisCodeData )][len( soluciones[len( sisCodeData )].keys() ) +1 ]\
				     ={'sisCode':sisCodeData, 'suma': sisCodeData.sum(), 'solucion':solucion, 'peso':peso }  

		except: #Entonces creamos un diccionario para sistemas de x nodos
			soluciones[len( sisCodeData )]\
				={ 1:{ 'sisCode':sisCodeData , 'suma':sisCodeData.sum(), 'solucion':solucion, 'peso':peso  } }


	return(soluciones)

def buscarSolucion(soluciones, sisCode):
	"""
	BUSCA UN CODIGO IGUAL A sisCode EN EL DICCIONARIO DE SOLUCIONES
	
	A: Primero debemos estar seguros de que el diccionario de soluciones
	tenga valores para sistemas de nNodos = numero de nod de sisCode 
	B: Para no tener que buscar en todas las combinaciones primero 
	hacemos una prueba utilizando la suma de codigos
	Si el Valor no se encuentra regresamos FALSE***
	"""

	try:
		
		solucionesLV2=soluciones[len(sisCode)] #A
		
		#print(solucionesLV2 )
		for key in  solucionesLV2.keys():
			if np.all(solucionesLV2[key]['suma'].values==sisCode.sum() ): #B
				if np.all( solucionesLV2[key]['sisCode'] ==sisCode): #No funciona comparacion
					print('solucion ENCONTRADA')
					return ({'respuesta':True, 'sistema':solucionesLV2[key] })#Haciendo clic en el atributo de resultado y peso tendremos los datos que necesitamos 
		print('Valor NO ENCONTRADO no hay valores en soluciones[{}][respuestas]'.format(len(sisCode)) )
		return({'respuesta':False, 'sistema':False})

	except:
		print('Valor NO ENCONTRADO no hay valores en soluciones[{}]'.format(len(sisCode)) )

		return({'sistema':False,'respuesta':False})

