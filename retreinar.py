from keras.models import load_model
from keras.utils import np_utils
from keras import optimizers
from keras.callbacks import ModelCheckpoint
import numpy as np
import pickle
from time import time

def train(pre_modelo, novo_modelo, taxa_aprendizado, epocas, tam_lote_dados):
	with open("modelo/treino/imagem_treino", "rb") as f:
		imagem_treino = np.array(pickle.load(f))
	with open("modelo/treino/rotulo_treino", "rb") as f:
		rotulo_treino = np.array(pickle.load(f), dtype=np.uint8)

	with open("modelo/treino/imagem_teste", "rb") as f:
		imagem_teste = np.array(pickle.load(f))
	with open("modelo/treino/rotulo_teste", "rb") as f:
		rotulo_teste = np.array(pickle.load(f), dtype=np.uint8)

	with open("modelo/treino/valor_imagem", "rb") as f:
		valor_imagem = np.array(pickle.load(f))
	with open("modelo/treino/valor_rotulo", "rb") as f:
		valor_rotulo = np.array(pickle.load(f), dtype=np.uint8)

	imagem_treino = np.reshape(imagem_treino, (imagem_treino.shape[0], 250, 250, 1))
	imagem_teste = np.reshape(imagem_teste, (imagem_teste.shape[0], 250, 250, 1))
	valor_imagem = np.reshape(valor_imagem, (valor_imagem.shape[0], 250, 250, 1))

	rotulo_treino = np_utils.to_categorical(rotulo_treino)
	rotulo_teste = np_utils.to_categorical(rotulo_teste)
	valor_rotulo = np_utils.to_categorical(valor_rotulo)

	checkpoint = ModelCheckpoint(novo_modelo, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
	callbacks_list = [checkpoint]
	modelo = load_model(pre_modelo)
	sgd = optimizers.SGD(lr=taxa_aprendizado)
	modelo.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
	modelo.fit(imagem_treino, rotulo_treino, validation_data=(imagem_teste, rotulo_teste), epochs=epocas, batch_size=tam_lote_dados, callbacks=callbacks_list)
	modelo = load_model(novo_modelo)
	erro = modelo.evaluate(valor_imagem, valor_rotulo, verbose=1)
	print("Erro de treinamento (CNN ERROR): %.2f%%" % (100-erro[1]*100))

def retreinar():
	while True:
		pre_modelo = input('Digite o nome do modelo pré-treinado: ')
		if pre_modelo != '':
			break

	novo_modelo = input('Digite o nome do modelo de saída: ')
	if novo_modelo == '':
		novo_modelo = pre_modelo

	while True:
		taxa_aprendizado = input('Digite a taxa de aprendizagem (padrão 0.01): ')
		if taxa_aprendizado == '':
			taxa_aprendizado = 0.01
			break
		try:
			taxa_aprendizado = float(taxa_aprendizado)
			break
		except:
			continue

	while True:
		epocas = input('Digite número de epocas (padrão 10): ')
		if epocas == '':
			epocas = 10
			break
		try:
			epocas = int(epocas)
			break
		except:
			continue

	while True:
		tam_lote_dados = input('Digite o tamanho da amostra (padrão 100): ')
		if tam_lote_dados == '':
			tam_lote_dados = 100
			break
		try:
			tam_lote_dados = int(tam_lote_dados)
			break
		except:
			continue

	train("modelo/"+pre_modelo+".h5", "modelo/"+novo_modelo+".h5", taxa_aprendizado, epocas, tam_lote_dados)

retreinar()	