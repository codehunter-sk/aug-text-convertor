from PIL import Image
from pytesseract import pytesseract

# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = r"C:\Pytemp1\Myvenv1\mini-project-1\picsave_02-02-2022_22-09-51.jpg"
# image_path = r"C:\Pytemp1\Myvenv1\mini-project-1\sampletext.png"


# Opening the image & storing it in an image object
img = Image.open(image_path)

# Providing the tesseract executable
# location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract

# Passing the image object to image_to_string() function
# This function will extract the text from the image
text = pytesseract.image_to_string(img)

with open('picsave_02-02-2022_22-09-51.txt','w') as f:
	f.write(text)

# Displaying the extracted text
print(text[:-1])

# print(pytesseract.image_to_osd(img))

boxes = pytesseract.image_to_boxes(img)
print(boxes)