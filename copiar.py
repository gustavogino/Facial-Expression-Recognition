import cv2, os

def copiar():
	pasta_raiz = input("Digite o nome da pasta raiz: ")
	pasta_saida = input("Digite o nome da pasta de saida: ")
	i=0
	pasta = pasta_raiz
	for nome_pasta in os.listdir(pasta):
		for i in range(0,9999,10):
			path = pasta+"/"+nome_pasta+"/"+str(i)+".jpg"
			new_path = pasta_saida+"/"+nome_pasta+"/"+str(i)+".jpg"
			print("Copiando imagem -> " +path)
			img = cv2.imread(path, 0)
			cv2.imwrite(new_path, img)
			
copiar()