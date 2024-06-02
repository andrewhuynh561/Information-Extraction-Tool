from ultralyticsplus import YOLO, render_result
import os
import cv2
import pytesseract
import pdfplumber
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"




def convert_to_images(pdf_path, resolution=300):
    # Get the directory of the PDF file
    # output_dir = os.path.dirname(pdf_path)
    

    with pdfplumber.open(pdf_path) as pdf:
        # Iterate over each page in the PDF
        for page_num, page in enumerate(pdf.pages):
            image = page.to_image(resolution=resolution).original
            
            # # Define the path to save the image
            image_path = os.path.join( f"page_{page_num + 1}.png")
            # Save the image
            image.save(image_path)

            # # Add the image path to the list
            # image_paths.append(image_path)

            # # Print a confirmation message
            # print(f"Saved page {page_num + 1} as image {image_path}")

    return image_path

pdf_path = "dataset/2-6 GWYNNE STREET, CREMORNE - FOOTINGS.pdf"
image_path = convert_to_images(pdf_path, resolution=300)

# load model
model = YOLO('foduucom/table-detection-and-extraction')

# set model parameters
model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # maximum number of detections per image

# set image
image = image_path
# image = 'images/page_1.png'

# perform inference and save croped images
# results = model.predict(image)
results = model.predict(image,save_crop=True)
# image = cv2.imread(image)
#print coordinates
# print("Detected boxes coordinates:")
# for i,box in enumerate(results[0].boxes):
#     x1, y1, x2, y2 = map(int,box.xyxy[0])  # Extract coordinates
#     print(f"Box: ({x1}, {y1}), ({x2}, {y2})")
#     #getting cropped image by using x,y coordinate
#     cropped_image=image[y1:y2,x1:x2]

#     image_path=os.path.join('images',f"cropped_image_{i+1}.png")
#     cv2.imwrite(image_path,cropped_image)
    


# # observe results
# print(results[0].boxes)
# render = render_result(model=model, image=image, result=results[0])
# render.show()

cropped_image_path="runs/detect/predict/crops/bordered/page_12.jpg"
# cropped_image_path="cropped_table_4.png"

load_image=Image.open(cropped_image_path)

#using pytesseract to extract text from image
extracted_text= pytesseract.image_to_string(load_image)

print(extracted_text)

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
    

# Extract the lines following the "FOOTING SCHEDULE" keyword
table_lines = lines[start_index:]

# Remove any empty lines
# Create a new list to store non-empty lines
filtered = []
for line in table_lines:
    if line.strip():  # Check if the line is not empty after removing  whitespace
        filtered.append(line)

table_lines = filtered

# Combine the relevant lines to form the table data
table_data = "\n".join(table_lines)
target_headers = ['FOOTING SCHEDULE', 'FOUNDATION SCHEDULE', 'GROUND FOOTING SCHEDULE', 'WALL SCHEDULE']

# Display the extracted table data
print(table_lines)


# Delete the image file after processing
os.remove(image_path)
