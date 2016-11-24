
# -*- coding: utf-8 -*-


#!export LC_ALL=en_US.UTF-8
#!export LANG=en_US.UTF-8
print('CARGANDO LIBRERIAS')
import numpy as np
import pandas as pd
import os


"""
Programa
Objetivo: Resolve el problema del agente viajero con reducciones.
Para cada nodo 

"""

#python utils.py
#os.system("utils.py")
nObs=100
nEdos=10
nNodos=9	

execfile('utils.py')

print('CARGANDO PROBLEMAS - SIISTEMAS A RESOLVER')
sistema=getSistema() #utils.py
sistema=pd.DataFrame(sistema)
sisCode=getCode(sistema)

#resolviendo el sistema
#def resoler(sisCode, sistema ):

#all(sisCode==sisCode2)
#Funcion de igualdad

sistema1=getSistema()
sistema1=pd.DataFrame(sistema1)
sisCode1=getCode(sistema1)

sistema2=getSistema()
sistema2=pd.DataFrame(sistema2)
sisCode2=getCode(sistema2)

sistema3=getSistema()
sistema3=pd.DataFrame(sistema3)
sisCode3=getCode(sistema3)

sistema4=getSistema()
sistema4=pd.DataFrame(sistema4)
sisCode4=getCode(sistema4)

sistemaMenor=getSistema(nNodos=5)
sistemaMenor=pd.DataFrame(sistemaMenor)
sisCodeMenor=getCode(sistemaMenor)

sistema4=getSistema()
sistema4=pd.DataFrame(sistema4)
sisCode4=getCode(sistema4)


#soluciones={1:(sisCode1, sisCode1.sum()), 2:(sisCode2, sisCode2.sum()), 3:(sisCode3, 4:sisCode4}
#sisCode.sum()#EN lugar de comparar todos los valores es mas 
#facil fijarnos primero en un numero y ver si la suma hace match


print('GENERANDO RSPUESTAS ')

soluciones={}
soluciones=agregarSolucion(soluciones, sisCode)
soluciones=agregarSolucion(soluciones, sisCode2)
soluciones=agregarSolucion(soluciones, sisCode3)
soluciones=agregarSolucion(soluciones, sisCodeMenor)


#En el siguiente proceso resoleremos el problema del agente
#con programacion dinamica

def resolverProblema(sistema, sisCode):

#primero buscamos la solucion en el mapa de soluciones
busqueda=buscarSolucion(soluciones, sisCode)
if busqueda['respuesta']==TRUE:
	print('El sistama ya ha sido resulto\n \tEl peso del problema es {} \n  \tLa solucion es : {} '.format(busqueda['sistema']['peso'], busqueda['sistema']['solucion']) )
else:
	print('Solucion no guardada')
	#Debemos iterar  para la primera columna(A) y resolver los subsistemas
	for Ax in sistema['A']:
		elegimos B 
		elegimos C
		elegimos D...
		
