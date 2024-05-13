import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import cv2
import pytesseract
import numpy as np
import pdfplumber
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_file_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_file_path)
    
    # Initialise text and table data
    text_data = []
    table_data = []

    # Iterate over each page in the PDF document
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        # Extract text from the page
        text = page.get_text()
        text_data.append(text)
        
        # Extract tables from the page using pdfplumber
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    table_data.append(df)
    
    # Close the PDF file
    pdf_document.close()

    return text_data, table_data

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        text_data, table_data = extract_text_from_pdf(file_path)
        # Process and display text and table data as needed
        print("Text Data:")
        for text in text_data:
            print(text)
        print("\nTable Data:")
        for table in table_data:
            print(table)
        
# Create the main window
root = tk.Tk()
root.title("PDF Text and Table Extractor")

# Create a button for uploading a file
upload_button = tk.Button(root, text="Upload PDF File", command=upload_file)
upload_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
