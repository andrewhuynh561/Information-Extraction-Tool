import pdfplumber
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Load the PDF file
pdf_path = "244 LOWER HEIDELBERG ROAD, IVANHOE EAST STACKER - FOOTINGS.pdf"

with pdfplumber.open(pdf_path) as pdf:
    
    first_page = pdf.pages[0]

    page_image = first_page.to_image()

    image_path = "page_image.png"
    page_image.save(image_path)


