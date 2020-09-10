import cv2
import numpy as np


#color verde
rangoMin = [0,0,0]
rangoMax = [100,45,54] #81 - 44 - 29



img = cv2.imread('img_c.png',1)

#convertimos la imagen de entarda a hsv
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
cv2.imshow("gray",gray)


grayF = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow("grayF",grayF)


#aplicamos el suavizado Gaussiano para eliminar el ruido sobre las mascaras
gauss = cv2.GaussianBlur(grayF,(11,11),0)#11, 11, 15
cv2.imshow("gaus",gauss)

#Calcular el detector de bordes Canny con OpenCV
canny = cv2.Canny(gauss,50,370) #50-350, 50-370, 50-355
cv2.imshow("canny",canny)

contornos,hier = cv2.findContours(canny.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print(len(contornos))

areas = [cv2.contourArea(c) for c in contornos]

i=0
for extension in areas:
    print("ext ", extension)
    if extension >= 0:
        actual = contornos[i]
        approx = cv2.approxPolyDP(actual,0.05*cv2.arcLength(actual,True),True)
        print("-> ",len(approx))
        #if len(approx)>=3:
        cv2.drawContours(img,[actual],0,(0,45,20),2)
        i+=1

cv2.imshow('ImagenOriginal',img)
cv2.waitKey(0)
cv2.destroyAllWindows()




