import os
import numpy as np
import pickle
import cv2
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from keras.layers.normalization import BatchNormalization
from keras import backend as K
from keras.callbacks import TensorBoard
from keras.models import load_model
from time import time
import tensorflow as tf
K.image_data_format()
#K.set_image_dim_ordering('tf')
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def pega_tam_img():
	img = cv2.imread('utils/tamanho.jpg', 0)
	return img.shape

def pega_num_tipos():
	return len(os.listdir('dados/'))

image_x, image_y = pega_tam_img()

def cnn_modelo():
	num_tipos = pega_num_tipos()
	modelo = Sequential()
	modelo.add(Conv2D(32, (5,5), input_shape=(image_x, image_y, 1), activation='relu'))
	modelo.add(BatchNormalization())
	modelo.add(MaxPooling2D(pool_size=(10, 10), strides=(10, 10), padding='same'))
	modelo.add(Flatten())
	modelo.add(Dense(1024, activation='relu'))
	modelo.add(BatchNormalization())
	modelo.add(Dropout(0.6))
	modelo.add(Dense(num_tipos, activation='softmax'))
	sgd = optimizers.SGD(lr=1e-3)
	modelo.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
	filepath="modelo/expressao.h5"
	checkpoint1 = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
	callbacks_list = [checkpoint1]
	from keras.utils import plot_model
	plot_model(modelo, to_file='modelo/treino/modelo.png', show_shapes=True)
	return modelo, callbacks_list

def treinar():
	epoca = 300
	tamanho = 100

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

	imagem_treino = np.reshape(imagem_treino, (imagem_treino.shape[0], image_x, image_y, 1))
	imagem_teste = np.reshape(imagem_teste, (imagem_teste.shape[0], image_x, image_y, 1))
	valor_imagem = np.reshape(valor_imagem, (valor_imagem.shape[0], image_x, image_y, 1))

	rotulo_treino = np_utils.to_categorical(rotulo_treino)
	rotulo_teste = np_utils.to_categorical(rotulo_teste)
	valor_rotulo = np_utils.to_categorical(valor_rotulo)

	modelo, callbacks_list = cnn_modelo()
	tensorboard = TensorBoard(log_dir="logs\\{}".format(time()))
	callbacks_list.append(tensorboard)
	modelo.fit(imagem_treino, rotulo_treino, validation_data=(imagem_teste, rotulo_teste), epochs=epoca, batch_size=tamanho, callbacks=callbacks_list)
	modelo = load_model('modelo/expressao.h5')
	scores = modelo.evaluate(valor_imagem, valor_rotulo, verbose=1)
	print("Erro de treinamento (CNN ERROR): %.2f%%" % (100-scores[1]*100))

treinar()	