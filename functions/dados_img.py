import cv2, os
import numpy as np
import random
from sklearn.utils import shuffle
import pickle

def rotular_imagem(dados):
	rotulo_imagem = []
	imagens = []
	rotulos = []
	for rotulo in os.listdir(dados):
		pacote_dados = dados+rotulo+'/'
		for imagem in os.listdir(pacote_dados):
			pacote_dados = dados+rotulo+'/'+imagem
			img = cv2.imread(pacote_dados, 0)
			if np.any(img == None):
				continue
			rotulo_imagem.append((np.array(img, dtype=np.float32), int(rotulo)))
	return rotulo_imagem

def dividir_rotulo(rotulo_imagem):
	imagens = []
	rotulos = []
	for (imagem, rotulo) in rotulo_imagem:
		imagens.append(imagem)
		rotulos.append(rotulo)
	return imagens, rotulos

def dados_img():
	dados = input("Digite o nome da pasta de dados: ")
	treino_percent = float(input("Digite a % para treinamento: (0.1 ~ 1.0): "))

	rotulo_imagem = rotular_imagem(dados+"/")
	rotulo_imagem = shuffle(shuffle(shuffle(rotulo_imagem)))
	imagens, rotulos = dividir_rotulo(rotulo_imagem)
	print("Itens totais de dados:", len(rotulo_imagem))

	imagem_treino = imagens[:int(treino_percent*len(imagens))]
	print("Itens em imagem_treino", len(imagem_treino))
	with open("../modelo/treino/imagem_treino", "wb") as f:
		pickle.dump(imagem_treino, f)
	del imagem_treino

	rotulo_treino = rotulos[:int(treino_percent*len(rotulos))]
	print("Itens em rotulo_treino", len(rotulo_treino))
	with open("../modelo/treino/rotulo_treino", "wb") as f:
		pickle.dump(rotulo_treino, f)
	del rotulo_treino

	imagem_teste = imagens[int(treino_percent*len(imagens)):]
	valor_imagem = imagem_teste[:int(len(imagem_teste) / 2)]
	imagem_teste = imagem_teste[int(len(imagem_teste) / 2):]
	print("Itens em imagem_teste", len(imagem_teste))
	with open("../modelo/treino/imagem_teste", "wb") as f:
		pickle.dump(imagem_teste, f)
	del imagem_teste

	rotulo_teste = rotulos[int(treino_percent*len(rotulos)):]
	valor_rotulo = rotulo_teste[:int(len(rotulo_teste) / 2)]
	rotulo_teste = rotulo_teste[int(len(rotulo_teste) / 2):]
	print("Itens em rotulo_teste", len(rotulo_teste))
	with open("../modelo/treino/rotulo_teste", "wb") as f:
		pickle.dump(rotulo_teste, f)
	del rotulo_teste

	print("Itens em valor_imagem", len(valor_imagem))
	with open("../modelo/treino/valor_imagem", "wb") as f:
		pickle.dump(valor_imagem, f)

	print("Itens em valor_rotulo", len(valor_rotulo))
	with open("../modelo/treino/valor_rotulo", "wb") as f:
		pickle.dump(valor_rotulo, f)

dados_img()		