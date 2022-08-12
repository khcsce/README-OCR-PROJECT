import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def OCR(image):
    # Take the saved image and send to ocr pytesseract function to process
    img = cv2.imread("image")

    # save the processed text in 'text' to send with mqtt
    text = pytesseract.image_to_string(img)
    print(text)

    # Return converted text
    return text
