import cv2
import numpy as np

rangoMin1 = [0,65,75]
rangoMax1 = [12, 255, 255]
rangoMin2 = [240,65,75]
rangoMax2 = [256, 255, 255]



img = cv2.imread('img_c.png',1)

#convertimos la imagen de entarda a hsv
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow("hsv",hsv)

#creamos mascaras para los rangos de colores
mascaraRojo1 = cv2.inRange(hsv,np.array(rangoMin1),np.array(rangoMax1))
mascaraRojo2 = cv2.inRange(hsv,np.array(rangoMin2),np.array(rangoMax2))
mascara = cv2.add(mascaraRojo1,mascaraRojo2)
cv2.imshow("mascara",mascara)

#aplicamos el suavizado Gaussiano para eliminar el ruido sobre las mascaras
gauss = cv2.GaussianBlur(mascara,(11,11),0)#11, 11, 15
cv2.imshow("gaus",gauss)

#ecualizar una imagen
#--------------------------------------------
imgE = cv2.equalizeHist(gauss)
cv2.imshow("imgE - equalizado",imgE)
#--------------------------------------------

"""#Calcular el detector de bordes Canny con OpenCV
canny = cv2.Canny(imgE,50,360) #50-350, 50-370, 50-355
cv2.imshow("canny",canny)"""



contornos,hier = cv2.findContours(imgE,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print(len(contornos))

"""areas = [cv2.contourArea(c) for c in contornos]
i=0
for extension in areas:
    if extension > 5:
        actual = contornos[i]
        approx = cv2.approxPolyDP(actual,0.03*cv2.arcLength(actual,True),True)
        print("apr: ",len(approx))
        if len(approx)==3:
            cv2.drawContours(img,[actual],0,(0,0,0),2)
            #cv2.drawContours(mascara,[actual],0,(0,0,0),2)
        i+=1"""

for cnt in contornos:
    approx = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)
    print(len(approx))
    #print(approx)
    #print("----------")

    if len(approx) == 8:
        cv2.drawContours(img,[cnt],0,(0,0,0),2)

cv2.imshow('ImagenOriginal',img)
cv2.waitKey(0)
cv2.destroyAllWindows()




