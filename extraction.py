import tkinter as tk
from tkinter import Label, filedialog, messagebox
import cv2
import os
import pytesseract
import numpy as np
import pdfplumber
import pandas as pd
from PIL import Image
from ultralyticsplus import YOLO
import shutil

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

def convert_to_images(pdf_path, resolution=300):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            image = page.to_image(resolution=resolution).original
            image_path = os.path.join("converted.png")
            image.save(image_path)
    return image_path

def process_image(image_path):
    # load model
    model = YOLO('foduucom/table-detection-and-extraction')

    # set model parameters
    model.overrides['conf'] = 0.25  # NMS confidence threshold
    model.overrides['iou'] = 0.45  # NMS IoU threshold
    model.overrides['agnostic_nms'] = False  # NMS class-agnostic
    model.overrides['max_det'] = 1000  # maximum number of detections per image

    # perform inference and save cropped images
    results = model.predict(image_path, save_crop=True)

    # Directory where cropped images are saved
    crops_dir = "runs/detect/predict/crops/"

    # List all cropped images
    cropped_image_paths = []
    for root, dirs, files in os.walk(crops_dir):
        for file in files:
            if file.endswith((".png", ".jpg", ".jpeg")):
                cropped_image_paths.append(os.path.join(root, file))

    extracted_texts = []

    for cropped_image_path in cropped_image_paths:
        load_image = Image.open(cropped_image_path)

        # Using pytesseract to extract text from image
        extracted_text = pytesseract.image_to_string(load_image)

        extracted_texts.append(extracted_text)
        
        # Optionally delete the cropped image after processing
        # os.remove(cropped_image_path)
    
    return extracted_texts

def extract_schedule_texts(extracted_texts):
    table_data = []
    for extracted_text in extracted_texts:
        # Split the text into lines
        lines = extracted_text.split('\n')

        # Find the index of the line that contains the keyword "FOOTING SCHEDULE"
        start_index = None
        for i, line in enumerate(lines):
            if 'FOOTING SCHEDULE' in line:
                start_index = i
                break
            elif 'FOUNDATION SCHEDULE' in line:
                start_index = i
                break
            elif 'GROUND FOOTING SCHEDULE' in line:
                start_index = i
                break
            elif 'WALL SCHEDULE' in line:
                start_index = i
                break
            elif 'RAFT FOOTING SCHEDULE' in line:
                start_index = i
                break
            elif 'SLAB BEAM SCHEDULE' in line:
                start_index = i
                break
            elif 'PAD FOOTING SCHEDULE' in line:
                start_index = i
                break
            elif 'STRIP FOOTING SCHEDULE (BEAM BASED)' in line:
                start_index = i
                break
            elif'STRUCTURAL FOUNDATION SCHEDULE - PAD FOOTINGS' in lines:
                start_index =i
                break

        if start_index is not None:
            # Extract the lines following the target header
            table_lines = lines[start_index :]
            
            # Remove any empty lines
            table_lines = [line for line in table_lines if line.strip()]
        
            # Determine headers and parse the table data
            headers = table_lines[0].split()
            # table_data = [line.split() for line in table_lines[1:]]
            # Initialize an empty list to store the table data
            data = []

            # Iterate over each line in table_lines starting from the second line (skipping the header line)
            for line in table_lines[1:]:
                # Split the line into individual values based on whitespace
                values = line.split()
                
                # Append the list of values to the data list
                data.append(values)

            print(headers)
            # Adjust rows to have the same number of columns as headers
            for row in data:
                while len(row) < len(headers):
                    row.append(" ")
                while len(row) > len(headers):
                    headers.append(" ")
            
            # Create a DataFrame from the parsed table data
            # df = pd.DataFrame(data, columns=headers)
            df = pd.DataFrame(data[1:], columns=headers)
            
            print(f"Table Headers: {headers}")
            print(f"Table Data: \n{df}")
            table_data.append(df)
    return table_data
        


# export to excel funtion
# def export_to_excel (table_data, excel_path):
#      writer="extracted_table.xlsx"
#      with pd.ExcelWriter(excel_path) as writer:
#         for i, table_df in enumerate(table_data):
#             table_df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
def upload_file():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    combined_table = {}
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)
            table_data = extract_table(file_path, target_headers)
            if not table_data:
                image_path = convert_to_images(file_path, resolution=300)
                extracted_texts = process_image(image_path)
                table_data=extract_schedule_texts(extracted_texts)
                # Delete the main image file after processing 
                os.remove(image_path)
                shutil.rmtree("runs")
                    
            combined_table[file_name] = pd.concat(table_data)
   

    if combined_table:
        excel_path = os.path.join(folder_path, "extracted_data.xlsx")
        with pd.ExcelWriter(excel_path) as writer:
            for sheet_name, table_df in combined_table.items():
                table_df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Excel sheet name limit is 31 characters
        messagebox.showinfo("Success", "Tables extracted and exported to Excel successfully!")
    else:
        messagebox.showinfo("No Tables Found", "No tables found in the selected folder.")
# def upload_file():
   
#     file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])

#     if file_paths:
#         combined_table = []  # List to store all tables extracted from the PDFs

#         # Loop through each selected file
#         for file_path in file_paths:
#             # Extract tables from the current PDF file
#             table_data = extract_table(file_path, target_headers)
#             if not table_data:
#                 image_path = convert_to_images(file_path, resolution=300)
#                 extracted_texts = process_image(image_path)
#                 table_data=extract_schedule_texts(extracted_texts)
#             combined_table.extend(table_data)  # Add the extracted tables 
#             print(table_data)
#         # Delete the main image file after processing
#         os.remove(image_path)
#         shutil.rmtree("runs")
#         # Check if any tables were found
#         if combined_table:
#             # Open a file d select the save excel file path
#             excel_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
#             if excel_path:
#                 export_to_excel(combined_table, excel_path)
#                 # Show a success message
#                 messagebox.showinfo("Success", "Tables extracted and exported to Excel successfully!")
#         else:
#             # Show a message if no matching tables were found
#             messagebox.showinfo("No Tables Found", "No tables found in PDF files.")
    
   
# Key word for title table
target_headers = ['FOOTING SCHEDULE', 'FOUNDATION SCHEDULE', 'GROUND FOOTING SCHEDULE', 'WALL SCHEDULE','PAD FOOTING SCHEDULE','STRIP FOOTING SCHEDULE (BEAM BASED)','STRIP FOOTING SCHEDULE (BEAM BASED)']

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Table Extractor")
    lbl = Label(root, text="Hello")
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