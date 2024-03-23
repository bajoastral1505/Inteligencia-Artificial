#MySigueme_V2.0
#10 octubre 2018 00:58 am
#Incorporo el control de colores a detectar

import cv2
import numpy as np
import serial  
import time

# Iniciamos la camara
#captura = cv2.VideoCapture(0)
captura = cv2.VideoCapture(1)
#captura = cv2.VideoCapture('http://192.168.1.137:8080/video')

#ser = serial.Serial('/dev/ttyUSB0', 115200)
ser = serial.Serial('COM3', 115200)

def nothing(x):
   pass
 
#Creamos una ventana llamada 'control' en la que habra todos los sliders
cv2.namedWindow('control')
cv2.createTrackbar('Hue Minimo','control',0,255,nothing)
cv2.createTrackbar('Hue Maximo','control',0,255,nothing)
cv2.createTrackbar('Saturation Minimo','control',0,255,nothing)
cv2.createTrackbar('Saturation Maximo','control',0,255,nothing)
cv2.createTrackbar('Value Minimo','control',0,255,nothing)
cv2.createTrackbar('Value Maximo','control',0,255,nothing)

while(1):

	# Capturamos una imagen y la convertimos de RGB -> HSV
	_, imagen = captura.read()
	hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

	#Los valores maximo y minimo de H,S y V se guardan en funcion de la posicion de los sliders
	hMin = cv2.getTrackbarPos('Hue Minimo','control')
	hMax = cv2.getTrackbarPos('Hue Maximo','control')
	sMin = cv2.getTrackbarPos('Saturation Minimo','control')
	sMax = cv2.getTrackbarPos('Saturation Maximo','control')
	vMin = cv2.getTrackbarPos('Value Minimo','control')
	vMax = cv2.getTrackbarPos('Value Maximo','control')
 
	#Se crea un array con las posiciones minimas y maximas
	lower=np.array([hMin,sMin,vMin])
	upper=np.array([hMax,sMax,vMax])
 
	#Deteccion de colores
	mask = cv2.inRange(hsv, lower, upper)

	#Filtrar el ruido con un CLOSE seguido de un OPEN
	kernel = np.ones((6,6),np.uint8)
	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

	# Encontrar el area de los objetos que detecta la camara
	moments = cv2.moments(mask)
	area = moments['m00']

	# Descomentar para ver el area por pantalla
	print (area)

 #aqui pongo el codigo del servomotor, repetido 2 veces...

	if moments['m00'] > 0:

		# Buscamos el centro x, y del objeto
		x = int(moments['m10'] / moments['m00'])
		y = int(moments['m01'] / moments['m00'])

		# Mostramos sus coordenadas por pantalla
		# time.sleep(1)

		print("x = ", x)

		if area < 3000000:
			ser.write(b'f')
			time.sleep(0.01)
			ser.write(b'p')

		elif x < 200:
			ser.write(b'i')
			time.sleep(0.01)
			ser.write(b'p')

		elif x > 350:
			ser.write(b'd')
			time.sleep(0.01)
			ser.write(b'p')

		elif x > 200 and x < 350:
			ser.write(b'p')
		else:
			ser.write(b'p')

		print("y = ", y)

		# Dibujamos una marca en el centro del objeto
		cv2.rectangle(imagen, (x, y), (x + 2, y + 2), (0, 0, 255), 2)

	# Mostramos la imagen original con la marca del centro y
	# la mascara
	cv2.imshow('mask', mask)
	cv2.imshow('Camara', imagen)
	tecla = cv2.waitKey(5) & 0xFF
	if tecla == 27:  # ESC
		break

cv2.destroyAllWindows()
