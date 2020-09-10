import cv2
import numpy as np
import time

class TestVideo():
    def __init__(self):
        self.analizarVideo()
        self.dif = None

    def analizarVideo(self):

        imagenes = []
        video = cv2.VideoCapture("video.mp4")

        (grabbed, imagen) = video.read()
        fondo = imagen.copy()
        imagenes.append(fondo.copy())

        (grabbed, imagen) = video.read()
        fondo = imagen.copy()
        imagenes.append(fondo.copy())


        """i=1
        cv2.imshow("img " + str(i),fondo)
        while grabbed:
            time.sleep(1)
            i = i+1
            (grabbed, imagen) = video.read()

            iguales = self.imagenesIguales(fondo,imagen)
            if iguales is False:
                fondo = imagen.copy()
                imagenes.append(fondo.copy())
                cv2.imshow("img "+str(i),fondo)

            if i==3:
                break"""

        #print(self.imagenesIguales(imagenes[0],imagenes[1]))

        difference = cv2.subtract(imagenes[0],imagenes[1] )
        result = not np.any(difference)
        print(result)
        cv2.imshow("diff",result)
        cv2.imshow("aaa",imagenes[0])
        cv2.imshow("bbb",imagenes[1])

    def imagenesIguales(self,imagen1, imagen2):
        difference = cv2.subtract(imagen1, imagen2 )
        result = not np.any(difference)
        if result is True:
            return True
        else:
            return False

testVideo = TestVideo()
cv2.waitKey(0)
cv2.destroyAllWindows()