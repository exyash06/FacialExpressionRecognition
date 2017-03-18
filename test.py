import cv2
import numpy as np
import glob

names = ['happy', 'sad', 'surprised' , 'disgust' , 'fear' , 'angry' , 'neutral']

def gamma_correction(img, correction):
    img = img/255.0
    img = cv2.pow(img, correction)
    return np.uint8(img*255)

def dog(img):
	g1= img;
	g2 = img;
	g1 = cv2.GaussianBlur(img,  (5,5), 2);
	g2 = cv2.GaussianBlur(img,  (11,11), 2);
	result = g2 - g1;
	return result


for name in names:
	i=0
	for img in glob.glob("/home/yashjain/IIVProject/jaffe4/" + name +  "/*.tiff"):
    		print(i)
    		i += 1
    		n= cv2.imread(img,0)
    		dst = gamma_correction(n, 0.2)
    		dst = dog(dst)
    		cv2.imwrite('/home/yashjain/IIVProject/jaffe2/' + name  + "/" +  str(i) + '.tiff',dst)



