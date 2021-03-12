import cv2
import numpy as np
import dlib, os
from imutils import face_utils
from imutils.face_utils import FaceAligner
from keras.models import load_model
import time

def transparencia(face_img, sobreposicao):
    #Pega a imagem em RGB
    sobreposicao_img = sobreposicao[:,:,:3]
    sobreposicao_mascara = sobreposicao[:,:,3:]

    #Calcula a máscara inversa
    fundo_mascara = 255 - sobreposicao_mascara

    #Converte pra três vetores (R, G, B) para utilizar como pesos
    sobreposicao_mascara = cv2.cvtColor(sobreposicao_mascara, cv2.COLOR_GRAY2BGR)
    fundo_mascara = cv2.cvtColor(fundo_mascara, cv2.COLOR_GRAY2BGR)

    #Converte imagem para pesos de 0.00 a 1.00
    face_parcial = (face_img * (1 / 255.0)) * (fundo_mascara * (1 / 255.0))
    sobreposicao_parcial = (sobreposicao_img * (1 / 255.0)) * (sobreposicao_mascara * (1 / 255.0))

    #Junta tudo em uma imagem de 8 bits  
    imagem = np.uint8(cv2.addWeighted(face_parcial, 255.0, sobreposicao_parcial, 255.0, 0.0))
    return imagem

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

def transforma_vetor(img):	
	img = cv2.resize(img, (250, 250))
	img = np.array(img, dtype=np.float16)
	img = np.reshape(img, (1, 250, 250, 1))
	return img

def keras_predicao(modelo, image):
	processamento = transforma_vetor(image)
	predicao = modelo.predict(processamento)
	predicao_probabilidade = predicao
	probabilidade_max = predicao[0] 
	predicao_id = list(probabilidade_max).index(max(probabilidade_max))
	return predicao_probabilidade, max(probabilidade_max), predicao_id

clear = lambda: os.system('cls')
cnn_modelo = load_model("modelo/expressao.h5")
shape_predictor_68 = dlib.shape_predictor("utils/shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()


disp_probab, disp_class = 0, 0
expressao = ['Neutro','Feliz','Triste','Surpreso','Bravo','Medo','Nojo']

fa = FaceAligner(shape_predictor_68, desiredFaceWidth=1000)
clear()

_path = input("Digite o nome da pasta que contem as imagens para realizar a predição: ")
path = _path + "/"
imagespath = os.listdir(path)
t_start = time.time()
i = 0 
for image in imagespath:	
	img = cv2.imread(path + image)		
	if img is not None: 
		i+=1		
		img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = detector(img_cinza)		
		if len(faces) > 0:
			shape_68 = shape_predictor_68(img, faces[0])
			shape = face_utils.shape_to_np(shape_68)
			mascara = cria_mascara(shape, img_cinza)
			mascara_alinhada = fa.align(mascara, img_cinza, faces[0])
			mascara_resize = cv2.resize(mascara_alinhada, (250, 250))
			predicao_probabilidade, probabilidade_max, predicao_id = keras_predicao(cnn_modelo, mascara_resize)	
t_end = time.time()	
t_dif = t_end - t_start
print ("Tempo para detectar um total de " + str(i) + " imagens:" + str(t_dif))
print ("Em frames por segundo (FPS): " + str(i / t_dif))

