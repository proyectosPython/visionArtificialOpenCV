import cv2

class Camara:
    def __init__(self):
        self.manejoCamara()

    def manejoCamara(self):
        print('inicia uso de la camara')
        cap = cv2.VideoCapture(0) #accedemos a la camara por defecto, si hay mas camaras podemos probar, 1,2,3, etc
        leido, foto = cap.read()
        if leido == True:
            cv2.imwrite('foto1.png',foto)
            print('foto tomada correctamente')
        else:
            print('error al acceder a la camara')

        cap.release()

camara = Camara()
