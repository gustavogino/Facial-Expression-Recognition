import os
from random import *

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

	for nome_pasta in os.listdir(path):
		path2 = path+"/"+nome_pasta+"/"
		files = os.listdir(path2)
		for file in files:
			print("Renomeando: "+str(path2)+str(file)+"  --->   "+str(path2)+str(random[i]))
			os.rename(str(path2)+str(file), str(path2)+str(random[i])+'.jpg')
			i+=1
	print("Renomeação randomica finalizada.")
randomizar()