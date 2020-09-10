import cv2
import  numpy as np
import threading

class Cliente():
    def __init__(self):
        imagen = cv2.imread('img_c1.png',1)
        self.mascaraRojo = self.mascaraAmarillo = self.mascaraAzul = None

        """img1 = self.getTriangulo(imagen.copy(),'rojo')
        cv2.imshow('img tria',img1)"""

    def getColor(self,color):
        return self.colores[color]

    def getTriangulo(self,imagen,color=None):
        return self.getFiguraGeometrica(imagen,color,3)

    def getCuadrado(self,imagen,color=None):
        return self.getFiguraGeometrica(imagen,color,4)

    def getCirculo(self,imagen,color=None):
        return self.getFiguraGeometrica(imagen,color,8)

    def getEstrella(self,imagen,color=None):
        return self.getFiguraGeometrica(imagen,color,10)

    def getFiguraGeometrica(self,imagen,color,tamanio):
        contornos = hier = None
        if color != None:
            imagenPreprocesada = self.getImagenPreprocesada(imagen,color)
            contornos,hier = cv2.findContours(imagenPreprocesada,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        else:
            imagenPreprocesada = self.getImagenPreprocesada(imagen)
            imagenCanny = cv2.Canny(imagenPreprocesada,50,350)
            contornos,hier = cv2.findContours(imagenCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contornos:
            approx = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)
            print(" -> ", len(approx))
            if len(approx) == tamanio:
                cv2.drawContours(imagen,[cnt],0,(0,0,0),2)
        return imagen

    def getImagenPreprocesada(self,imagen,color=None):
        imagenHSV = cv2.cvtColor(imagen,cv2.COLOR_BGR2HSV)
        imagenGauss = None
        imagenEqualizada = None

        h_rojo = threading.Thread(name='mascaraRojo',target=self.getMascaraColorRojo(imagenHSV))
        h_amarillo = threading.Thread(name='mascaraAmarillo',target=self.getMascaraColorAmarillo(imagenHSV))
        h_azul = threading.Thread(name='mascaraAzul',target=self.getMascaraColorAzul(imagenHSV))

        h_rojo.daemon = True
        h_amarillo.daemon = True
        h_azul.daemon = True

        h_rojo.start()
        h_amarillo.start()
        h_azul.start()

        h_rojo.join()
        h_amarillo.join()
        h_azul.join()

        if color != None:
            if color == 'rojo':
                imagenGauss = cv2.GaussianBlur(self.mascaraRojo,(11,11),0)
                imagenEqualizada = cv2.equalizeHist(imagenGauss)
            elif color == 'amarillo':
                imagenGauss = cv2.GaussianBlur(self.mascaraAmarillo,(11,11),0)
                imagenEqualizada = cv2.equalizeHist(imagenGauss)
            else: #azul
                imagenGauss = cv2.GaussianBlur(self.mascaraAzul,(11,11),0)
                imagenEqualizada = cv2.equalizeHist(imagenGauss)
        else: #todos los colores
            mascara = cv2.add(self.mascaraRojo,self.mascaraAmarillo)
            mascara = cv2.add(mascara,self.mascaraAzul)
            imagenGauss = cv2.GaussianBlur(mascara,(11,11),0)
            imagenEqualizada = cv2.equalizeHist(imagenGauss)

        return imagenEqualizada

    def getMascaraColorRojo(self,imagenHSV):
        rangoMinimoRojo1 = np.array([0,65,75])
        rangoMaximoRojo1 = np.array([12, 255, 255])
        rangoMinimoRojo2 = np.array([240,65,75])
        rangoMaximoRojo2 = np.array([256, 255, 255])
        mascaraRojo1 = cv2.inRange(imagenHSV,rangoMinimoRojo1,rangoMaximoRojo1)
        mascaraRojo2 = cv2.inRange(imagenHSV,rangoMinimoRojo2,rangoMaximoRojo2)
        self.mascaraRojo = cv2.add(mascaraRojo1,mascaraRojo2)

    def getMascaraColorAmarillo(self,imagenHSV):
        rangoMinimoAmarillo = np.array([20,100,20])
        rangoMaximoAmarillo = np.array([32,255,255])
        mascaraAmarillo = cv2.inRange(imagenHSV,rangoMinimoAmarillo,rangoMaximoAmarillo)
        self.mascaraAmarillo = mascaraAmarillo

    def getMascaraColorAzul(self,imagenHSV):
        rangoMinimoAzul = np.array([100,65,75])
        rangoMaximoAzul = np.array([130,255,255])
        mascaraAzul = cv2.inRange(imagenHSV,rangoMinimoAzul,rangoMaximoAzul)
        self.mascaraAzul = mascaraAzul

cliente = Cliente()
cv2.waitKey(0)
cv2.destroyAllWindows()

