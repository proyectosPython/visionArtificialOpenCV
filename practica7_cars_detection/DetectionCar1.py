import cv2

class DetectionCar1():
    def __init__(self):
        self.detectionCar()

    def detectionCar(self):
        cap = cv2.VideoCapture('video1.avi')
        carCascade = cv2.CascadeClassifier('cars.xml')

        while True:
            ret, foto = cap.read()
            if type(foto) != type(None):
                imgGray = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)
                cars = carCascade.detectMultiScale(imgGray,1.1,2)
                for (x,y,w,h) in cars:
                    cv2.rectangle(foto,(x,y),(x+w,y+h),(0,255,255),2)
                cv2.imshow('video',foto)
            else:
                break

            #para salir del bucle con esc, sin esta parte del codigo no funciona
            if cv2.waitKey(33) == 27:
                break

        # Liberamos la cámara y cerramos todas las ventanas
        cap.release()
        cv2.destroyAllWindows()

detectionCar = DetectionCar1()

