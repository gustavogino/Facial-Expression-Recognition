import os

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
renomear()