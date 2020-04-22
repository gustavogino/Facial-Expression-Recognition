import cv2, os, random
import numpy as np

#Funções das funções
def pegar_tamanho():
	img = cv2.imread('utils/tamanho.jpg', 0)
	return img.shape


# Funções main

def renomear():
	path = input("Digite o nome da pasta: ")
	x = int(input("Digite o número inicial do renomeio: "))


	for nome_pasta in os.listdir(path):
		path2 = path+"/"+nome_pasta+"/"
		files = os.listdir(path2)
		i = x
		for file in files:
			print("Renomeando: "+str(path2)+str(file)+"  --->   "+str(path2)+str(i))
			os.rename(str(path2)+str(file), str(path2)+str(i)+'.jpg')
			i = i+1

	x=int(i-x)*6
	print("Renomeação finalizada! Foram renomeados "+str(x)+" arquivos.")



def espelhar():
	pasta_raiz = input("Digite o nome da pasta: ")
	num_img = int(input("Digite a quantidade de imagens que deseja espelhar: "))	
	i=0
	pasta = pasta_raiz
	for nome_pasta in os.listdir(pasta):
		for i in range(num_img):
			path = pasta+"/"+nome_pasta+"/"+str(i)+".jpg"
			new_path = pasta+"/"+nome_pasta+"/"+str(i+num_img)+".jpg"
			print("Espelhando a imagem: " +path)
			img = cv2.imread(path, 0)
			img = cv2.flip(img, 1)
			cv2.imwrite(new_path, img)	



def randomizar():
	path = input("Digite o nome da pasta: ")
	qunt = int(input("Digite a quantidade total de itens: "))
	minimo =int(input("Digite o menor valor possivel a ser randomizado: "))
	maximo = int(input("Digite o maior valor possivel a ser randomizado: "))
	random = []
	i = 0
	while len(random) < qunt:
		r = randint(minimo, maximo)
		if r not in random:
			random.append(r)

	path = "../" + path;
	for nome_pasta in os.listdir(path):
		path2 = path+"/"+nome_pasta+"/"
		files = os.listdir(path2)
		for file in files:
			print("Renomeando: "+str(path2)+str(file)+"  --->   "+str(path2)+str(random[i]))
			os.rename(str(path2)+str(file), str(path2)+str(random[i])+'.jpg')
			i+=1
	print("Renomeação randomica finalizada.")	


def copiar():
	pasta_raiz = input("Digite o nome da pasta raiz: ")
	pasta_saida = input("Digite o nome da pasta de saida: ")
	i=0
	pasta = "../" + pasta_raiz
	for nome_pasta in os.listdir(pasta):
		for i in range(0,9999,10):
			path = "../"+pasta+"/"+nome_pasta+"/"+str(i)+".jpg"
			new_path = "../"+pasta_saida+"/"+nome_pasta+"/"+str(i)+".jpg"
			print("Copiando imagem -> " +path)
			img = cv2.imread(path, 0)
			cv2.imwrite(new_path, img)


def mostrar_tudo():
	gestures = os.listdir('../dados_full/')
	gestures.sort(key = int)
	begin_index = 0
	end_index = 5
	image_x, image_y = pegar_tamanho()

	if len(gestures)%5 != 0:
		rows = int(len(gestures)/5)+1
	else:
		rows = int(len(gestures)/5)

	full_img = None
	last_img_num = int(10)
	for i in range(rows):
		col_img = None
		for j in range(begin_index, end_index):
			img_path = "../dados_full/%s/%d.jpg" % (j, random.randint(1, last_img_num))
			img = cv2.imread(img_path, 0)
			if np.any(img == None):
				img = np.zeros((image_y, image_x), dtype = np.uint8)
			if np.any(col_img == None):
				col_img = img
			else:
				col_img = np.hstack((col_img, img))

		begin_index += 5
		end_index += 5
		if np.any(full_img == None):
			full_img = col_img
		else:
			full_img = np.vstack((full_img, col_img))


	cv2.imshow("../Expressoes", full_img)
	cv2.imwrite('../expressoes.jpg', full_img)
	cv2.waitKey(0)


print("	Menu de opções: ")
print(" ")
print("	1 - Renomear imagens ")
print("	2 - Espelhar imagens ")
print("	3 - Randomizar posições ")
print("	4 - Copiar imagens  ")
print("	5 - Mostrar emoções cadastradas  ")
print("	 ")

option = input("Selecione o que deseja fazer: ")

if option == "1":
	renomear()
elif option == "2":	
	espelhar()
elif option == "3":
	randomizar()
elif option == "4":
	copiar()
elif option == "5":
	mostrar_tudo()
else:
	print(" Opção informada não existe!")	