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


def inserir_emoticon(imagem, emoticon):    
    x,y=[20,20]
    x1,y1=[120,120]
    emoticon = cv2.resize(emoticon, (x1-x, y1-y))
    try:
        imagem[x:x1, y:y1] = transparencia(imagem[x:x1, y:y1], emoticon)
    except:
        pass
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

def pega_emoticon():
	emoticon = []
	for emoti in range(len(os.listdir("utils/emoticon/"))):
		print("Carregando emoticon com ID "+str(emoti))
		emoticon.append(cv2.imread("utils/emoticon/"+str(emoti)+".png", -1))
	return emoticon

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


cnn_modelo = load_model("modelo/expressao.h5")
shape_predictor_68 = dlib.shape_predictor("utils/shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

cam = cv2.VideoCapture(0) #Camera default
if cam is None:
	cam = cv2.VideoCapture(1) #Segunda camera
	if cam is None:
		cam = cv2.VideoCapture(2) #terceira
		if cam is None:
			cam = cv2.VideoCapture(3) #quarta

emoticon = pega_emoticon()
disp_probab, disp_class = 0, 0
expressao = ['Neutro','Feliz','Triste','Surpreso','Bravo','Medo','Nojo']

fa = FaceAligner(shape_predictor_68, desiredFaceWidth=1000)

_, anterior = cam.read()
_, img = cam.read()

while True:
	start = time.time()
	_, img = cam.read()
	img = cv2.flip(img, 1)
	img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = detector(img_cinza)

	if len(faces) > 0:
		#for i, rosto in enumerate(faces): #trocar faces[0] -> rosto
		shape_68 = shape_predictor_68(img, faces[0])
		shape = face_utils.shape_to_np(shape_68)
		mascara = cria_mascara(shape, img_cinza)
		mascara_alinhada = fa.align(mascara, img_cinza, faces[0])
		mascara_alinhada = cv2.resize(mascara_alinhada, (250, 250))
		(x, y, w, h) = face_utils.rect_to_bb(faces[0])
		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
		predicao_probabilidade, probabilidade_max, predicao_id = keras_predicao(cnn_modelo, mascara_alinhada)
		
		probabilidade_max = float(probabilidade_max*100)
		cv2.putText(img, "Precisao: %.2f" % probabilidade_max+"%", (300, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0),2)	

		if (probabilidade_max > 95):
			img = inserir_emoticon(img, emoticon[predicao_id])
			cv2.putText(img, str(expressao[predicao_id]), (20, 150), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0),3)
			anterior = predicao_id
		else:
			img = inserir_emoticon(img, emoticon[int(anterior)])
			cv2.putText(img, str(expressao[int(anterior)]), (20, 150), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0),3)

		for z in range(6):
			predicao_probabilidade[0][z] = float(predicao_probabilidade[0][z]*100)
			cv2.putText(img, str(expressao[z])+": %.2f" % predicao_probabilidade[0][z]+"%", (10, 300+(30*int(z))), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 75, 255),2)
		cv2.imshow('Mascara', mascara_alinhada)

	end = time.time()
	seconds = end - start
	fps  = int(1 / seconds)

	cv2.putText(img, "FPS: "+str(fps), (500, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 100, 255),2)
	cv2.imshow('Imagem da Camera', img)	
	if cv2.waitKey(1) == ord('q'):
		break
	
	
