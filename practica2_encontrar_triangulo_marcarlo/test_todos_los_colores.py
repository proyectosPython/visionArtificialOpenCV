import cv2
import numpy as np

#color verde
rangoRojoMin1 = [0,65,75]
rangoRojoMax1 = [12, 255, 255]
rangoRojoMin2 = [240,65,75]
rangoRojoMax2 = [256, 255, 255]

rangoAmarilloMin = [20,100,20]
rangoAmarilloMax = [32,255,255]

rangoAzulMin = [100,65,75]
rangoAzulMax = [130,255,255]

img = cv2.imread('img_c1.png',1)

#convertimos la imagen de entarda a hsv
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow("hsv1",hsv)

#creamos mascaras para los rangos de colores
mascaraRojo1 = cv2.inRange(hsv,np.array(rangoRojoMin1),np.array(rangoRojoMax1))
mascaraRojo2 = cv2.inRange(hsv,np.array(rangoRojoMin2),np.array(rangoRojoMax2))
mascaraAmarillo = cv2.inRange(hsv,np.array(rangoAmarilloMin),np.array(rangoAmarilloMax))
mascaraAzul = cv2.inRange(hsv,np.array(rangoAzulMin),np.array(rangoAzulMax))


mascara = cv2.add(mascaraRojo1,mascaraRojo2)
mascara = cv2.add(mascara,mascaraAmarillo)
mascara = cv2.add(mascara,mascaraAzul)

#mascara = cv2.inRange(hsv,np.array(rangoMin),np.array(rangoMax))
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

contornos,hier = cv2.findContours(imgE,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print(len(contornos))

areas = [cv2.contourArea(c) for c in contornos]

i=0
for extension in areas:
    #print("ex: ",extension)
    if extension >5:
        actual = contornos[i]
        approx = cv2.approxPolyDP(actual,0.03*cv2.arcLength(actual,True),True)
        print(len(approx))
        if len(approx)==10:
            cv2.drawContours(img,[actual],0,(0,0,0),2)
            cv2.drawContours(mascara,[actual],0,(0,0,0),2)
        i+=1

cv2.imshow('ImagenOriginalaaa',img)
cv2.waitKey(0)
cv2.destroyAllWindows()




