import tkinter as tk
from tkinter import filedialog, messagebox
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
                # checking the header with remove none in the target hearders
                valid_header = False
                for header in target_headers:
                    if header in remove_headers:
                        valid_header = True
                        break
                # true
                if valid_header:
                    # get data after the header
                    data = table[1:]  
                    print(f"Table Headers: {remove_headers}")
                    print(f"Table Data: {data}")
                    df = pd.DataFrame(table[1:], columns=table[0])
                    table_data.append(df)
    return table_data

# export to excel funtion
def export_to_excel (table_data, excel_path):
     with pd.ExcelWriter(excel_path) as writer:
        for i, table_df in enumerate(table_data):
            table_df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)

def upload_file():
   
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])

    if file_paths:
        combined_table = []  # List to store all tables extracted from the PDFs

        # Loop through each selected file
        for file_path in file_paths:
            # Extract tables from the current PDF file
            table_data = extract_table(file_path, target_headers)
            combined_table.extend(table_data)  # Add the extracted tables 
        
        # Check if any tables were found
        if combined_table:
            # Open a file d select the save excel file path
            excel_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if excel_path:
                export_to_excel(combined_table, excel_path)
                # Show a success message
                messagebox.showinfo("Success", "Tables extracted and exported to Excel successfully!")
        else:
            # Show a message if no matching tables were found
            messagebox.showinfo("No Tables Found", "No tables found in PDF files.")
    
   
# Key word for title table
target_headers = ['FOOTING SCHEDULE', 'FOUNDATION SCHEDULE']

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Table Extractor")

    # Create a button for uploading a file
    upload_button = tk.Button(root, text="Upload PDF File", command=upload_file)
    upload_button.pack(pady=20)

    width = 300
    height = 200

    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # find the center point
    center_x = int(screen_width/2 - width / 2)
    center_y = int(screen_height/2 - height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f'{width}x{height}+{center_x}+{center_y}')


    root.mainloop()

if __name__ == "__main__":
    main()