# Created this as I needed OOP slides, and sir was abit busy :)
# Author: Hamza Imran | FAST ISB 

from PIL import Image
from os import listdir
from os.path import isfile, join
from os import getcwd
import re
from typing import List

# The images to be cropped must have numbered names i.e 1.png, 2.png and so on
# the reason being as this helps in sorting and making sure each page of the 
# PDF is in it's right order and no page get's misplaced
folderContainingImagesToCrop = r"images/"
folderContainingCroppedImages = r"cropped/"


def getFilesList() -> List[str]:

	# The folder name in which all the screenshots are kept in

	# Gets all the file names from the above folder specfified
	# Please make sure they are numbered i.e 1.png, 2.png
	# as it helps in sorting
	onlyfiles = [f for f in listdir(folderContainingImagesToCrop) if isfile(join(folderContainingImagesToCrop, f))]

	# This will sort the files in ascending order
	onlyfiles.sort(key=lambda f: int(re.sub('\D', '', f)))

	return onlyfiles


def cropImages():
	print("---Croping Images---")

	for file in getFilesList():
		
		# Opens the image to crop it
		imageToCrop = Image.open(folderContainingImagesToCrop+file)

		# These are dimensions which will crop the image
		# you can find them through trial and error method
		left = 445
		top = 205
		right = 1480
		bottom = 980

		# This will crop the current image being looped over
		myImage = imageToCrop.crop((left, top, right, bottom))
		
		myImage = myImage.save(folderContainingCroppedImages+file)

	print("---Images Cropped---")

def mergeFilesIntoPDF():

	print("---Merging Images Into PDF---")

	im_list = []


	for file in getFilesList():
		
		# Opens file to work on it
		im = Image.open(folderContainingCroppedImages+file)
		
		# The following lines 3 lines help in converting the image to RGB
		im.load() # required for png.split()
		newImage = Image.new("RGB", im.size, (255, 255, 255))
		newImage.paste(im, mask=im.split()[3]) # 3 is the alpha channel

		# Appends the image to a list after converting into RGB format
		im_list.append(newImage);	

	
	
	pdfFileName = "overloading.pdf"
	# This saves the PDF in the current working directory
	im_list[0].save(getcwd()+"/"+pdfFileName, "PDF" ,resolution=100.0, save_all=True, append_images=im_list[1:]) # Creates a pdf file

	print("---Images Merged Into PDF---")
  
if __name__ == "__main__":
	cropImages()
	mergeFilesIntoPDF()
