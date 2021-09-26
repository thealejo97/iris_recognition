#Este programa lee una imagen de iris buscada y realiza sdv para compararla con un conjunto de imagenes a fin de determinar a cual iris pertenece la imagen

#IMPORTS
import os
from PIL import Image
import numpy
import sys


currentPath = os.getcwd() #Sacamos el path del proyecto
imagesFolderPath =  currentPath + "/images_svd" #Path de las imagenes de los ojos
irisImagesDirectories = os.listdir(imagesFolderPath) #Lista de las imagenes
dataMatrix = [] #
thresold = 6000 #Tolerancia
K = 240 #Ancho de las imagenes


def getEuclideanDistance(singularValuesOfImageToSearh, singularValuesOfStoredImage):
  
  if(len(singularValuesOfImageToSearh) != len(singularValuesOfStoredImage)):
    sys.exit("Los tamaños de las imagenes son distintas y no se puede calcular.")
  return numpy.linalg.norm( singularValuesOfImageToSearh - singularValuesOfStoredImage )

# Retorna un arreglo de numpy arreglos, donde cada numpy arreglo una images

def compareUserIrises(userId, irisesDirectoryPath):
    
    irisiesName = os.listdir(irisesDirectoryPath) #Saca los nombres de los archivos (izquied o derecho)

    #Calculamos sdv de la imagen a buscar K es el ancho de las imagenes
    singularValuesOfImageToSearh = loadImageToSearch(currentPath+"/search.bmp", K) 

    #Ahora buscamos por cada imagen de cada ojo
    for iris in irisiesName:
        fileName, filExtension = os.path.splitext(iris)#Sacamos la extension
        if filExtension == '.bmp':#Miramos si la extension existe
          # Con l convierte la imagen a imagen gris
          grayScalePillImage = Image.open(irisesDirectoryPath + iris).convert('L')
          # Convertimos la imagen a imagen comprimida
          compressed = compressMatrix( numpy.array(grayScalePillImage), K )
          
          #Calculamos la distancia euclidiana
          e_distance = getEuclideanDistance(singularValuesOfImageToSearh, compressed)
          if(e_distance <= thresold):#Si la distancia es menor al umbral de tolerancia se considera que se encontro
            print("El iris buscado pertenece al usuario con ID " , userId ," . E_DISTANCE: ", e_distance)
            #print(e_distance)
            return True

    print(".")
    
    return False


def compressMatrix(matrix, k):
  
  #U vectores singulares izquierdos - Imagen comprimida
  #VT (vtranspuesta) valores singulares derechos - determina  la mezcla de todas las fotos mezclada
  #D (Sigma) valores singulares - Matriz diagonal que determina la importancia de cada parte de la imagen
  U, D, VT = numpy.linalg.svd(matrix)  #Le calculamos el sdv a la imagen en escala de grises
  
  # construir la nueva matriz D con los elementos de la diagonal superior 
  # toma los elementos que estan por debajo de la diagonal de U
  U_p = U[:,:k]
	# toma los elementos que estan por arriba de la diagonal de VT
  VT_p = VT[:k,:]
  
  #Crea una matriz de 0 de tamaño ancho,ancho
  D_p = numpy.zeros((k, k), int)
  for i in range(k):
   D_p[i][i] = D[i]#Crea una matriz diagonal con los valores de D

  #Devuelve producto punto de U_p , D_p producto VT_p para formar la imagen
  return numpy.dot(numpy.dot(U_p, D_p), VT_p) #Devuelve una matriz con la imagen comprimida y ajustada con sdv

#Carga la imagen a buscar
def loadImageToSearch(imagePathToSearch, k):
  
  grayScalePillImage = Image.open(imagePathToSearch).convert('L') #Convertimos la imagen a escala de grises
  #Ejecuta el compressImage le pasamos la imen a escala convertida a arreglo
  compressedImage = compressMatrix(numpy.array(grayScalePillImage), K)#Tenemos la imagen comprimida con el sdv
  return compressedImage

#########MAIN#########
irisMatrix = [] #Matriz
for irisDirectory in irisImagesDirectories: #Por cada persona


  rightIrisesDirectoryPath = imagesFolderPath + "/" + irisDirectory + "/right/" #Ojo derecho de cada persona
  lefttIrisesDirectoryPath = imagesFolderPath + "/" + irisDirectory + "/left/" #Ojo izquierdo de cada persona



  #Comparamos izquierdo y derecho
  if(compareUserIrises(irisDirectory, rightIrisesDirectoryPath) or compareUserIrises(irisDirectory, lefttIrisesDirectoryPath)):
    break
  


