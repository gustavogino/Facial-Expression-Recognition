import cv2, os, random
import numpy as np

def pegar_tamanho():
	img = cv2.imread('utils/tamanho.jpg', 0)
	return img.shape

def mostrar_tudo():
	gestures = os.listdir('dados_full/')
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
			img_path = "dados_full/%s/%d.jpg" % (j, random.randint(1, last_img_num))
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


	cv2.imshow("Expressoes", full_img)
	cv2.imwrite('expressoes.jpg', full_img)
	cv2.waitKey(0)

mostrar_tudo()