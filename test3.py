import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob

names = ['happy', 'sad', 'surprised' , 'disgust' , 'fear' , 'angry' , 'neutral']


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
js=0;
for name in names:
	js+=1;
	final_res = np.zeros(65536);
	s=0;
	for image in glob.glob("/home/yashjain/IIVProject/jaffe2/" + name +  "/*.tiff"):
		img = cv2.imread(image, 0)
		s=s+1;
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
				hist=(hist/float(16*16))
				result = np.append(result,hist)
		print(str(js) +"\t" + str(s))	
		final_res +=result
		
	final_res= final_res/s;
	np.save("/home/yashjain/IIVProject/jaffe2/" + name + "/hist1.txt",final_res);
	

