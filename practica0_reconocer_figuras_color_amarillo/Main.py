import cv2
import numpy as np

#detecta color amarillo

img = cv2.imread('entrada.png',1)
cv2.imshow('Imagen original',img)

#convertimos la imagen de entrada a hsv
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow('Imagen hsv',hsv)

#creamos una mascara para que acepte solo el rango de color amarillo
maskMat = cv2.inRange(hsv,np.array([20,100,20]),np.array([32,255,255])) #min - max rango de colores
cv2.imshow('Mascara verde',maskMat)

#Aplicamos el suavisado gaussiano
gaussMat = cv2.GaussianBlur(maskMat,(5,5),0)
cv2.imshow('Imagen con suavisado gaussiano',gaussMat)

#Detectamos los bordes con canny
cannyMat = cv2.Canny(gaussMat,50,150)
cv2.imshow('bordes con canny', cannyMat)

#contamos los bordes detectados, es una matriz
(contornos,_) = cv2.findContours(cannyMat.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )

print("->",len(contornos))

k = cv2.waitKey(0)
cv2.destroyAllWindows()






