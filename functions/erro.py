from keras.models import load_model
import numpy as np
import pickle
from keras.utils import np_utils

resp = None
with open("../treino/imagem_teste", "rb") as f:
	imagem_treino = np.array(pickle.load(f))
with open("../treino/rotulo_teste", "rb") as f:
	rotulo_treino = np.array(pickle.load(f), dtype=np.uint8)

imagem_treino = np.reshape(imagem_treino, (imagem_treino.shape[0], 250, 250, 1))
rotulo_treino = np_utils.to_categorical(rotulo_treino)

def erro():
	print("---------- CALCULAR ERRO DA REDE -----------")
	model_name = input('Digite o nome do modelo: ')
	modelo = load_model("../old/"+model_name+".h5")
	erro = modelo.evaluate(imagem_treino, rotulo_treino, verbose=1)
	print("ERRO DA REDE: %.4f%%" % (100-erro[1]*100))
	print("ACERTO DA REDE: %.4f%%" % (erro[1]*100))

while resp != "X":
	erro()
	resp = input("Digite X se deseja finalizar, qualquer outra tecla para continuar: ")	