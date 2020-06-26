import cv2
import numpy as np
import binascii

TARGET_BITS = 2
BIN_BASE_DECODING = 7

def convert_to_ascii(bits):
	char = int("".join(bits),2)
	return char.to_bytes((char.bit_length()+7)//8,'big').decode()

def calc_image_storage(imageSize):
	width, height, channels = imageSize
	storage = width*height*channels*TARGET_BITS
	return storage

def decoder(image):
	image = cv2.imread(image)
	chars = []
	binBits = []
	print(bin(image[0][1][0]))
	print(bin(image[0][1][1]))
	print(bin(image[0][1][2]))
	print(bin(image[0][2][0]))
	storage_size = calc_image_storage(image.shape)
	for row in range(image.shape[0]):
		for col in range(image.shape[1]):
			for byte in image[row][col]:
				binNum = bin(byte)[-TARGET_BITS:]
				for i in range(TARGET_BITS):
					if len(binBits)==BIN_BASE_DECODING:
						chars.append(convert_to_ascii(binBits))
						#print(chars,convert_to_ascii(binBits))
						binBits = []
					else:
						binBits.append(binNum[i])
	newfile = open("decoded_text.txt","w")
	newfile.write("".join(chars))
	newfile.close()

decoder("two_bit_steg.png")