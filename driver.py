import cv2

TARGET_BITS = 2
CHANNELS = 3

def open_image(path):
	image = cv2.imread(path)
	cv2.imshow("image",image)
	cv2.waitKey(0)


def convert_to_bin(pixelValues):
	binValues = []
	for i in pixelValues:
		num = bin(i)[2:]
		binValues.append(num)
	return binValues


def convert_to_dec(pixelValues):
	decValues = []
	for i in pixelValues:
		num = int(i,2)
		decValues.append(num)
	return decValues

def insert_bits(pixel,bitsToHide):
	binPixels = convert_to_bin(pixel)
	newBinValues = []
	n=0
	for value in binPixels:
		if(len(value)>=TARGET_BITS):
			print(n,value)
			newBinValues.append(value[:-TARGET_BITS] + str(bitsToHide[n]))
			print(n,value)
		else:
			newBinValues.append(bitsToHide)
		n+=1
	return convert_to_dec(newBinValues)




#insert_bits([255,238,5],['10','00','11'])			





#print(convert_to_dec(convert_to_bin([255,238,5])))