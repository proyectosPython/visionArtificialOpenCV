import socket
import sys
import pickle
import cv2
import numpy as np
import threading
import pytesseract


class Cliente(threading.Thread):
    def __init__(self,idCliente=0, host="localhost", port=4000):
        threading.Thread.__init__(self)
        #print("hola soy el cliente nro: ",idCliente)
        self.idCliente = idCliente
        self.mascaraRojo = self.mascaraAmarillo = self.mascaraAzul = None
        self.idCliente = idCliente
        self.imagenes = {}



        self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))

        msg_recv = threading.Thread(target=self.msg_recv)
        msg_recv.daemon = True
        msg_recv.start()


    def run(self):
        nombreVideo = "video"+str(self.idCliente)+".mp4"
        aux = "id cliente : " + str(self.sock.getsockname()[1]) + " analiza el video -> " +  str(nombreVideo)
        print(aux)
        video = cv2.VideoCapture(nombreVideo)
        while True:
            (grabbed, img) = video.read();
            if grabbed:
                imgNumero = img[0:150, 250:400]
                imgNumero = cv2.cvtColor(imgNumero,cv2.COLOR_BGR2GRAY)
                imgNumero = cv2.threshold(imgNumero, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                numeroImagen = pytesseract.image_to_string(imgNumero, config=r'--oem 3 --psm 6')
                numeroImagen = "a"+numeroImagen

                if self.imagenes.__contains__(numeroImagen) is False:
                    self.send_msg(numeroImagen)
                    self.imagenes[numeroImagen] = numeroImagen

                    aux = "id cliente: " + str(self.sock.getsockname()[1]) + " procesa imagen -> " + str(numeroImagen)
                    print(aux)
                    unidades = self.resolverProblema(img.copy())
                    cv2.imwrite(str(numeroImagen)+".png",img)
                    self.send_msg(unidades)
            else:
                self.sock.close()
                sys.exit()

    def resolverProblema(self,img):
        return self.getCuadrado(img,'azul') #azul, amarillo, rojo

    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    numeroImagen = pickle.loads(data)
                    self.imagenes[numeroImagen] = numeroImagen

                    aux = "id cliente:" + str(self.sock.getsockname()[1]) + " no procesa imagen -> " + str(numeroImagen)
                    print(aux)
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))

    """----------------------------------------------------------------------------------------"""

    def getTriangulo(self,imagen,color):
        return self.getFiguraGeometrica(imagen,color,3,0.03)

    def getCuadrado(self,imagen,color):
        return self.getFiguraGeometrica(imagen,color,4,0.03)

    def getCirculo(self,imagen,color):
        return self.getFiguraGeometrica(imagen,color,8,0.03) - self.get2Circulos(imagen,color) - self.get2cuadrados(imagen,color)

    def getEstrella(self,imagen,color):
        return self.getFiguraGeometrica(imagen,color,10,0.03)

    def get2cuadrados(self,imagen,color):
        return self.getFiguraGeometrica(imagen,color,8,0.012)

    def get2Circulos(self,imagen,color):
        return self.getFiguraGeometrica(imagen,color,11,0.014)

    def getFiguraGeometrica(self,imagen,color,tamanio,ep):
        ans = 0
        imagenPreprocesada = self.getImagenPreprocesada(imagen,color)
        contornos,hier = cv2.findContours(imagenPreprocesada,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contornos:
            approx = cv2.approxPolyDP(cnt,ep*cv2.arcLength(cnt,True),True)
            if tamanio!=11:
                if len(approx) == tamanio:
                    cv2.drawContours(imagen,[cnt],0,(0,0,0),2)
                    ans = ans + 1
            else:
                if len(approx) == tamanio or len(approx) == tamanio+1:
                    cv2.drawContours(imagen,[cnt],0,(0,0,0),2)
                    ans = ans + 1
        return ans

    def getImagenPreprocesada(self,imagen,color):
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

        if color == 'rojo':
            imagenGauss = cv2.GaussianBlur(self.mascaraRojo,(11,11),0)
            imagenEqualizada = cv2.equalizeHist(imagenGauss)
        elif color == 'amarillo':
            imagenGauss = cv2.GaussianBlur(self.mascaraAmarillo,(11,11),0)
            imagenEqualizada = cv2.equalizeHist(imagenGauss)
        else: #azul
            imagenGauss = cv2.GaussianBlur(self.mascaraAzul,(11,11),0)
            imagenEqualizada = cv2.equalizeHist(imagenGauss)

        return imagenEqualizada

    def getMascaraColorRojo(self,imagenHSV):
        rangoMinimoRojo1 = np.array([0,50,20])
        rangoMaximoRojo1 = np.array([5, 255, 255])
        rangoMinimoRojo2 = np.array([175,50,20])
        rangoMaximoRojo2 = np.array([180, 255, 255])
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



