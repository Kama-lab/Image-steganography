import cv2
import binascii

TARGET_BITS = 2

def open_image(path):
	image = cv2.imread(path)
	#cv2.imshow("image",image)
	#cv2.waitKey(0)
	return image


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
			newBinValues.append(value[:-TARGET_BITS] + str(bitsToHide[n]))
		else:
			newBinValues.append(bitsToHide)
		n+=1
	return convert_to_dec(newBinValues)

def calc_image_storage(imageSize,channels):
	width, height = imageSize
	storage = width*height*channels*TARGET_BITS
	#print(f"Available:{storage}bits or {storage/8}bytes")
	return storage



def hide_text(image,text):
	image = cv2.imread(image)
	file = open(text,"r")
	print(image)
	nBits = []
	nthBit = 0
	nthChar = 0
	char = file.read(nthChar+1)[nthChar:]
	#binChar = bin(int(binascii.hexlify(char), 16))[2:]
	binChar = bin(int.from_bytes(char.encode(),"big"))
	print(binChar)
	for row in image:
		for col in row:
			for i in range(3):
				try:
					nBits.append(binChar[nthBit]+binChar[nthBit+1])
					nthBit+=2
				except IndexError:
					nthChar+=1
					nthBit = 0
					char = file.read(nthChar+1)[nthChar:]
					nBits.append(binChar[nthBit]+binChar[nthBit+1])
			print(nBits)
			#print(map("".join(),[nBits[:2],nBits[2:4],nBits[4:]]))
			image[row,col] = insert_bits(col,[nBits[:2],nBits[2:4],nBits[4:5]])
			nBits = []

	print(image)
	cv2.imshow("img",image)
	cv2.waitKey(0)
			

#hide_text(,"res/test.txt")
hide_text("res/test_image2.png","res/test.txt")





#insert_bits([255,238,5],['10','00','11'])			





#print(convert_to_dec(convert_to_bin([255,238,5])))
