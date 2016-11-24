def agregarSolucion(soluciones, sisCodeData):
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
		soluciones[len(sisCodeData)]={ 1:{ 'sisCode':sisCodeData , 'suma':sisCode.sum() } }
		#print(soluciones)
		print('Insertando solcion para sistema de {} NODOS  '.format(len(sisCodeData)))
	else :
		try: #EXISTE un diccionario en solcuiones para datos de x nodos?
			if not bool(soluciones[len(sisCodeData)]) : #Esta vacio el nievel de solucion []
				#print('Existe pero esta vacio')
				soluciones[len( sisCodeData )]\
				={ 1:{ 'sisCode':sisCodeData , 'suma':sisCode.sum() } }

			else: #Agregar una solucion
				#print( len( soluciones[len( sisCodeData )].keys() ) )
				soluciones[len( sisCodeData )][len( soluciones[len( sisCodeData )].keys() ) +1 ]\
				     ={'sisCode':sisCodeData, 'suma': sisCode.sum()}  

		except: #Entonces creamos un diccionario para sistemas de x nodos
			soluciones[len( sisCodeData )]\
				={ 1:{ 'sisCode':sisCodeData , 'suma':sisCode.sum() } }


	return(soluciones)

soluciones={}
soluciones=agregarSolucion(soluciones, sisCode1)
#print(soluciones)