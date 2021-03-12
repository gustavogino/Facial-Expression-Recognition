import cv2
import numpy as np
import random
import os

def rotate(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

print("Iniciando data augmentation...")
destino_path = 'C://Users/gusta/Desktop/Facial Expression Recognition/new/'
data = ("images/")
folders = os.listdir(data)
for folder in folders:
	folder = folder + '/'	
	for image in os.listdir(data+folder):
		path = data + folder + image
		img = cv2.imread(path)
		if img is not None: 
			rand0 = random.randint(10,30)
			rand1 = random.randint(330,350)
			img0 = cv2.flip(img, 1)
			img1 = rotate(img, rand0)
			img2 = rotate(img, rand1)			
			img3 = cv2.flip(img1, 1)
			img4 = cv2.flip(img2, 1)
			cv2.imwrite(destino_path+folder+'img_'+image, img)
			cv2.imwrite(destino_path+folder+'img0_'+image, img0)
			cv2.imwrite(destino_path+folder+'img1_'+image, img1)
			cv2.imwrite(destino_path+folder+'img2_'+image, img2)
			cv2.imwrite(destino_path+folder+'img3_'+image, img3)
			cv2.imwrite(destino_path+folder+'img4_'+image, img4)