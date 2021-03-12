import cv2
import numpy as np
import dlib
import pickle
import os
from imutils import face_utils
from imutils.face_utils import FaceAligner
from random import shuffle, randint

def cria_mascara(shape, img):
	altura, largura = img.shape
	mascara = np.zeros((altura, largura), dtype=np.uint8)

	mascara = cv2.line(mascara,(shape[67,0],shape[67,1]),(shape[60,0],shape[60,1]),255,1)
	mascara = cv2.line(mascara,(shape[60,0],shape[60,1]),(shape[48,0],shape[48,1]),255,1)
	mascara = cv2.line(mascara,(shape[41,0],shape[41,1]),(shape[36,0],shape[36,1]),255,1)
	mascara = cv2.line(mascara,(shape[47,0],shape[47,1]),(shape[42,0],shape[42,1]),255,1)
	mascara = cv2.line(mascara,(shape[30,0],shape[30,1]),(shape[35,0],shape[35,1]),255,1)
	mascara = cv2.line(mascara,(shape[31,0],shape[31,1]),(shape[30,0],shape[30,1]),255,1)

	for i in range(0,67): 
		if i in [16,21,26,30,35,41,47]:
			continue
		mascara = cv2.line(mascara,(shape[i,0],shape[i,1]),(shape[i+1,0],shape[i+1,1]),255,1)

	return mascara	

def criar_web():
	shape_predictor_68 = dlib.shape_predictor("../utils/shape_predictor_68_face_landmarks.dat")
	detector = dlib.get_frontal_face_detector()

	cam = cv2.VideoCapture(0) #Camera default
	if cam is None:
		cam = cv2.VideoCapture(1) #Segunda camera
		if cam is None:
			cam = cv2.VideoCapture(2) #terceira
			if cam is None:
				cam = cv2.VideoCapture(3) #quarta

	fa = FaceAligner(shape_predictor_68, desiredFaceWidth=1000)


	base_dados = '../dados/'
	id_img = int(input('Digite o ID: '))
	num_img = int(input('Digite a quantidade de imagens que deseja: '))
	num_inicial = int(input('Digite o número de inicio: '))
	contador_img = num_inicial
	capturando = False
	if not os.path.exists(base_dados+str(id_img)):
		os.mkdir(base_dados+str(id_img))
	while True:
		img = cam.read()[1]
		img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = detector(img_cinza)
		if len(faces) > 0:

			rosto = faces[0]
			shape_68 = shape_predictor_68(img, rosto)
			shape = face_utils.shape_to_np(shape_68)
			mascara = cria_mascara(shape, img_cinza)
			mascara_alinhada = fa.align(mascara, img_cinza, rosto)
			mascara_alinhada = cv2.resize(mascara_alinhada, (250, 250))
			(x, y, w, h) = face_utils.rect_to_bb(rosto)
			cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
			if contador_img-num_inicial < int(num_img):
				if capturando:
					cv2.putText(img, "Imagens tiradas: "+str(contador_img-num_inicial)+" / "+str(num_img), (55, 55), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255),3)
					cv2.imwrite(base_dados+str(id_img)+'/'+str(contador_img)+'.jpg', mascara_alinhada)
					contador_img += 1
			else:
				break
			cv2.imshow('Mascara ', mascara_alinhada)
		cv2.imshow('Imagem da Camera', img)
		keypress = cv2.waitKey(1)
		if keypress == ord('q'):
			break
		elif keypress == ord('c'):
			if capturando:
				capturando = False
			else:
				capturando = True

criar_web()				