import cv2

class Main():
    def __init__(self):
        self.run()

    def run(self):
        #Cargamos el archivo cascade

        faceDetector = cv2.CascadeClassifier('C:/Program Files/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
        imagen = cv2.imread('vengadores.jpg',1)

        #análisis de la imagen y devolver los rostros encontrados en una matriz.
        rostros = faceDetector.detectMultiScale(imagen,1.1,5)

        # recorremos la matriz resultante con la información de los rostros encontrados en la imagen
        # y dibujamos rectangulos de colores correspondientes a la matriz
        for (x,y,w,h) in rostros:
            cv2.rectangle(imagen,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow('Rostros encontrados',imagen)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

main = Main()
