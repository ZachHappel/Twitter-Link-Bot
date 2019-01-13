import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageFile
import numpy as np
import cv2
import requests
from io import StringIO

def performOCR(img):

    def method_a(img):
        pic = cv2.imread(img)
        lower = np.array([219, 219, 219])  #Lower limit of RGB Values ==> Gray Color
        upper = np.array([255, 255, 255])  #Upper limit of RGB Values ==> White Color
        shapeMask = cv2.inRange(pic, lower, upper)
        print("a")
        _, contours, _ = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imwrite("masked.png", shapeMask, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  # Save Edited Picture as Masked.PNG
        cv2.imwrite
        text = pytesseract.image_to_string(Image.open("masked.png"))  # raw text from image
        print('b')

        return text.split('\n')



    def method_b(img):
        image = Image.open(img)
        image.filter(ImageFilter.SHARPEN)
        results = pytesseract.image_to_string(image)
        return results.split('\n')



    resultOfA = method_a(img)
    print("Results: \n"+str(resultOfA))
    return(resultOfA)





