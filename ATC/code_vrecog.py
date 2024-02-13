from PIL import Image
from pytesseract import pytesseract
def recog(img_path=0):
    if not img_path:
        img_path=input('Enter img_path for testing')
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img = Image.open(img_path)
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(img)
    text=text.lower()
    print("Text:")
    print(text)
    return text
if __name__ == '__main__':
    recog()