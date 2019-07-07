import cv2, os

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
espelhar()