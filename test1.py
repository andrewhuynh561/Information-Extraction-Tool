from ultralyticsplus import YOLO, render_result
import os
import cv2
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# load model
model = YOLO('foduucom/table-detection-and-extraction')

# set model parameters
model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # maximum number of detections per image

# set image
image = 'images/page_1.png'

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
load_image=Image.open(cropped_image_path)

#using pytesseract to extract text from image
extracted_text= pytesseract.image_to_string(load_image)

print(extracted_text)