import os
import pdfplumber
from PIL import Image
from ultralyticsplus import YOLO
import pytesseract
import pandas as pd
import shutil

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
            table_data = []

            # Iterate over each line in table_lines starting from the second line (skipping the header line)
            for line in table_lines[1:]:
                # Split the line into individual values based on whitespace
                values = line.split()
                
                # Append the list of values to the table_data list
                table_data.append(values)

            print(headers)
            # Adjust rows to have the same number of columns as headers
            for row in table_data:
                while len(row) < len(headers):
                    row.append(" ")
                while len(row) > len(headers):
                    headers.append(" ")
            
            # Create a DataFrame from the parsed table data
            df = pd.DataFrame(table_data, columns=headers)
            
            print(f"Table Headers: {headers}")
            print(f"Table Data: \n{df}")

    return table_data 
        

# pdf_path = "dataset/244 LOWER HEIDELBERG ROAD, IVANHOE EAST STACKER - FOOTINGS.pdf"
pdf_path = "dataset/244_v1.pdf"
image_path = convert_to_images(pdf_path, resolution=300)
extracted_texts = process_image(image_path)

extract_schedule_texts(extracted_texts)

# Delete the main image file after processing
os.remove(image_path)
shutil.rmtree("runs")