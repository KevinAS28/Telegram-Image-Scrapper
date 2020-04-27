from PIL import Image
import pytesseract
import numpy as np
import argparse
import cv2, os
import os
import re

def image_to_text(image_full_path):

	# load the example image and convert it to grayscale
	image = cv2.imread(image_full_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	# check preprocess to apply thresholding on the image
	# if args["preprocess"] == "thresh":
	# 	gray = cv2.threshold(gray, 0, 255,
	# 		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	
	# elif args["preprocess"] == "blur":
	# 	gray = cv2.medianBlur(gray, 3)
	
	# write the grayscale image to disk as a temporary file
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	# load the image as a PIL/Pillow image
	# apply OCR
	# delete temp image
	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)

	#TO-DO : Additional processing such as spellchecking for OCR errors or NLP 
	return text
	
	# show the output images
	# cv2.imshow("Image", image)
	# cv2.imshow("Output", gray)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

image_ext = 'jpg jpeg png PNG'.split(' ')
# image_ext = ['jpg']
to_searchs = []

while True:
	keyword = input("word/sentence to search [hit enter when done]: ")
	if len(keyword)==0:
		break
	to_searchs.append(keyword)

absolute_path = os.path.dirname(os.path.realpath(__file__))

scanned = []

def main():
	bufferO = open('output.txt', 'a+')
	for ext in image_ext:
		print('Searching in {}...'.format(ext))
		full_path = os.path.join(absolute_path, 'media', ext)
		if not os.path.isdir(full_path):
			os.makedirs(full_path)
		files = os.listdir(full_path)
		for file in files:
			if file in scanned:
				continue
			file_full_path = os.path.join(full_path, file)
			text = image_to_text(file_full_path)
			# print(file, ':')
			# print(text)
			for to_search in to_searchs:
				if to_search in text.lower():
					# print('Found...')
					output = 'Found {} in {}'.format(to_search, file_full_path)
					bufferO.write(output+'\n')
					print(output, "\n")					

			# try:
			# 	text = image_to_text(file_full_path)
			# 	for to_search in to_searchs:
			# 		if to_search in text:
			# 			print('Found {} in {}'.format(to_search, file_full_path))			
			# except:
			# 	print('Error in', file_full_path)
			scanned.append(file)
	bufferO.close()

def scanImage(file_path, to_searchs=to_searchs):
	with open('result.txt', 'a+') as myfile:
		text = image_to_text(file_path)
		for to_search in to_searchs:
			if to_search in text.lower():
				myfile.write('Found {} in {}'.format(to_search, file_path))

if __name__=="__main__":
	while True:
		main()