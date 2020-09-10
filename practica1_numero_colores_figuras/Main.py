import cv2
import numpy as np

listaRango = [[[50,50,50],[80,255,255]], #49,50,50 - 80,255,255 verde
              [[100,65,75],[130,255,255]], #100,65,75 - 130,255,255 azul
              [[160,100,100],[179,255,255]], #rojo
              [[20,100,20],[32,255,255]] #amarillo
              ]
listaColores = ['verde','azul','rojo','amarillo']

img = cv2.imread('entrada.png',1)

#convertimos la imagen de entarda a hsv
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#creamos mascaras para los rangos de colores
listaMascara = [];
for i in range(len(listaRango)):
    mascara = cv2.inRange(hsv,np.array(listaRango[i][0]),np.array(listaRango[i][1]))
    #cv2.imshow("mascara",mascara)
    listaMascara.append(mascara)

#aplicamos el suavizado Gaussiano para eliminar el ruido sobre las mascaras
listaGauss = []
for i in range(len(listaMascara)):
    gauss = cv2.GaussianBlur(listaMascara[i],(9,9),0)
    #cv2.imshow("suavisado",gauss)
    listaGauss.append(gauss)

#Calcular el detector de bordes Canny con OpenCV
listaCanny = []
for i in range(len(listaGauss)):
    canny = cv2.Canny(listaGauss[i],50,100)
    #cv2.imshow("Bordes",canny)
    listaCanny.append(canny)

for i in range(len(listaCanny)):
    (contornos,_) = cv2.findContours(listaCanny[i].copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    print(listaColores[i]," : ", len(contornos))

cv2.imshow('ImagenOriginal',img)
cv2.waitKey(0)
cv2.destroyAllWindows()