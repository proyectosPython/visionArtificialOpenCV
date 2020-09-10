import cv2
import numpy as np

#color verde
rangoMin = [20,100,20]
rangoMax = [32,255,255]



img = cv2.imread('img_b1.png',1)

#convertimos la imagen de entarda a hsv
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow("hsv",hsv)

#creamos mascaras para los rangos de colores
mascara = cv2.inRange(hsv,np.array(rangoMin),np.array(rangoMax))
cv2.imshow("mascara",mascara)

#aplicamos el suavizado Gaussiano para eliminar el ruido sobre las mascaras
gauss = cv2.GaussianBlur(mascara,(11,11),0)#11, 11, 15
cv2.imshow("gaus",gauss)

#ecualizar una imagen
#--------------------------------------------
imgE = cv2.equalizeHist(gauss)
cv2.imshow("imgE - equalizado",imgE)
#--------------------------------------------

#Calcular el detector de bordes Canny con OpenCV
canny = cv2.Canny(imgE,50,360) #50-350, 50-370, 50-355
cv2.imshow("canny",canny)

contornos,hier = cv2.findContours(canny.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print(len(contornos))

areas = [cv2.contourArea(c) for c in contornos]

i=0
for extension in areas:
    print("ex ", extension)
    if extension > 80:
        actual = contornos[i]
        approx = cv2.approxPolyDP(actual,0.05*cv2.arcLength(actual,True),True)
        #if len(approx)>=3:
        cv2.drawContours(img,[actual],0,(0,0,0),2)
        cv2.drawContours(mascara,[actual],0,(0,0,0),2)
        i+=1

cv2.imshow('ImagenOriginal',img)
cv2.waitKey(0)
cv2.destroyAllWindows()




