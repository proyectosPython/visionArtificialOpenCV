import numpy as np
import cv2
import time

class DetectarMovimiento():
    def __init__(self):
        self.detectarMovimiento()

    def detectarMovimiento(self):
        # Cargamos el video
        camara = cv2.VideoCapture("video.mp4")

        # Iniciamos el primer frame vacio, Nos servira para obtener el fondo
        fondo = None

        # Recorremoss todos los frames
        while True:
            #obtenemos el frame
            (grabbed, frame) = camara.read()

            # Si se llega al final del video, salimos
            if not grabbed:
                break

            # Convertimos a escala de grises - blanco y negro, el frame
            frameGris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

            # Aplicamos el suvizado para eliminar ruido
            frameGris = cv2.GaussianBlur(frameGris,(21,21),0)

            # Obtenemos el primer frame
            if fondo is None:
                fondo = frameGris
                continue

            # Calculo de la diferencia entre el fondo y el frameGris actual
            frameResta = cv2.absdiff(fondo,frameGris)

            # Aplicamos un umbral, que supere un umbral minimo
            frameUmbral = cv2.threshold(frameResta,25,255,cv2.THRESH_BINARY)[1]

            # Dilatamos el umbral para tapar agujeros
            frameUmbral = cv2.dilate(frameUmbral, None, iterations=2)

            # Copiamos el umbral para detectar los contornos
            frameContorno = frameUmbral.copy()

            # Detectamos los contornos
            contornos, hierarchy = cv2.findContours(frameContorno, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Recorremos todos los contornos encontrados
            for c in contornos:
                # Eliminamos los contornos mas pequeños
                if cv2.contourArea(c) < 1000:
                    continue

                # Obtenemos el bound del contorno , el rectangulo mayor que engloba al contorno
                (x,y,w,h) = cv2.boundingRect(c)

                # Dibujamos el rectangulo
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            cv2.imshow("Camara",frame)
            cv2.imshow("FrameUmbral",frameUmbral)
            cv2.imshow("FrameResta",frameResta)
            cv2.imshow("FrameContorno",frameContorno)

            # Tiempo de espera para que se vea bien
            #time.sleep(0.015)

            #para salir del bucle con esc, sin esta parte del codigo no funciona
            if cv2.waitKey(33) == 27:
                break

        # Liberamos la cámara y cerramos todas las ventanas
        camara.release()
        cv2.destroyAllWindows()

detectarMovimiento = DetectarMovimiento()