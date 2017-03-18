import numpy as np
import cv2
from matplotlib import pyplot as plt
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

def thresholded(center, pixels):
    out = []
    for a in pixels:
        if a >= center:
            out.append(1)
        else:
            out.append(0)
    return out

def get_pixel_else_0(l, idx, idy, default=0):
    try:
        return l[idx,idy]
    except IndexError:
        return default

correct_count =0
total_count =0
print("Actual\tExpected") 

for named in names:
	for image in glob.glob("/home/yashjain/IIVProject/jaffe4/testing/" + named +  "/*.tiff"):
		total_count += 1
		img = cv2.imread(image, 0)
		img = gamma_correction(img, 0.2)
		img = dog(img)
		transformed_img = cv2.imread(image, 0)

		for x in range(0, len(img)):
		    for y in range(0, len(img[0])):
			center        = img[x,y]
			top_left      = get_pixel_else_0(img, x-1, y-1)
			top_up        = get_pixel_else_0(img, x, y-1)
			top_right     = get_pixel_else_0(img, x+1, y-1)
			right         = get_pixel_else_0(img, x+1, y )
			left          = get_pixel_else_0(img, x-1, y )
			bottom_left   = get_pixel_else_0(img, x-1, y+1)
			bottom_right  = get_pixel_else_0(img, x+1, y+1)
			bottom_down   = get_pixel_else_0(img, x,   y+1 )

			values = thresholded(center, [top_left, top_up, top_right, right, bottom_right,
				                      bottom_down, bottom_left, left])

			weights = [1, 2, 4, 8, 16, 32, 64, 128]
			res = 0
			for a in range(0, len(values)):
			    res += weights[a] * values[a]

			transformed_img.itemset((x,y), res)

		result = np.array([])
		for i in range(0,16):
			for j in range(0,16):
				hist=np.zeros(256)
				for k in range(0,16):
					for l in range(0,16):
						hist[transformed_img[i*16+k][j*16+l]]+=1
				hist= (hist/float(16*16))
				result = np.append(result,hist)
		min = 10000
		s = "neutral"
		for name in names:
			x=np.load("/home/yashjain/IIVProject/jaffe2/" + name + "/hist1.txt.npy")
			p = np.asarray(x, dtype=np.float)
			q = np.asarray(result, dtype=np.float)
			np.seterr(divide='ignore', invalid='ignore')
			ans = np.sum(np.where(np.logical_and(q != 0,p!=0), q* np.log(q / p), 0))
			if ans <= min :
				min = ans
				s = name
		
		print(s + "\t" + named)
		if s == named :
			correct_count += 1
print("Final Accuracy on Testing data set :")
print(correct_count*100/total_count)
