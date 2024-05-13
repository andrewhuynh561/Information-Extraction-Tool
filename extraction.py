import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import cv2
import pytesseract
import numpy as np
import pdfplumber
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_table(pdf_path, target_header):
    table_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"Extracting tables from page {page_num + 1} with header containing '{target_header}'")
            tables = page.extract_tables()
            for table in tables:
                # get header of table
                headers = table[0]  
                # Removing none in title line
                remove_headers = []
                for header in headers:
                    if header is not None:
                        Header = str(header).strip()
                        remove_headers.append(Header)
               
                # Check if target header is in the headers list
                if target_header in remove_headers:
                    # get data after the header
                    data = table[1:] 
                    print(f"Table Headers: {remove_headers}")
                    print(f"Table Data: {data}")
                    df = pd.DataFrame(table[1:], columns=table[0])
                    table_data.append(df)
               
    return table_data

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        table_data = extract_table(file_path,target_header)
        print("\nTable Data:")
        for table in table_data:
            print(table)


# Key word for title table
target_header = 'FOOTING SCHEDULE'

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Table Extractor")

    # Create a button for uploading a file
    upload_button = tk.Button(root, text="Upload PDF File", command=upload_file)
    upload_button.pack(pady=20)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()