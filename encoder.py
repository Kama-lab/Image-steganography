import cv2
import binascii
import numpy as np

TARGET_BITS = 1


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

def one_bit_slicing(bits):
	return [bits[0],bits[1],bits[2]]

def two_bit_slicing(bits):
	return [bits[0]+bits[1],bits[2]+bits[3],bits[4]+bits[5]]

def encode(image,text):
	steps_per_pixel = TARGET_BITS*3
	function = None
	if TARGET_BITS==1:
		function = one_bit_slicing
	elif TARGET_BITS==2:
		function = two_bit_slicing
	else:
		pass
	image = cv2.imread(image)
	storage_size = calc_image_storage(image.shape[:2],image.shape[2])
	written_size = 0
	file = open(text,"r")
	nBits = []
	nthBit = 0
	nthChar = 0

	char = file.read(nthChar+1)[nthChar:]
	binChar = bin(int.from_bytes(char.encode(),"big"))[2:]

	for row in range(image.shape[0]):
		for col in range(image.shape[1]):
			for i in range(steps_per_pixel):
				try:
					nBits.append(binChar[nthBit])
					nthBit+=1
				except IndexError:
					nthChar+=1
					nthBit = 0
					char = file.read(nthChar+1)[nthChar:]
					binChar = bin(int.from_bytes(char.encode(),"big"))[2:]
					nBits.append(binChar[nthBit])
			try:
				image[row][col] = insert_bits(image[row][col],function(nBits))
			except TypeError:
				print("Invalid target bits")
				return 0

			written_size += steps_per_pixel
			print(f"{storage_size}/{written_size}")
			nBits = []
	cv2.imwrite("one_bit_steg.png",image)
	cv2.imshow("img",image)
	cv2.waitKey(0)
			

encode("res/test_image2.png","res/test.txt")
