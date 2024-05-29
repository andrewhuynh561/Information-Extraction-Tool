from ultralyticsplus import YOLO, render_result

# load model
model = YOLO('foduucom/table-detection-and-extraction')

# set model parameters
model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # maximum number of detections per image

# set image
image = 'images/page_1.png'

# perform inference
results = model.predict(image,save_crop=True)

# #print coordinates
# print("Detected boxes coordinates:")
# for box in results[0].boxes:
#     x1, y1, x2, y2 = box.xyxy[0]  # Extract coordinates
#     print(f"Box: ({x1}, {y1}), ({x2}, {y2})")

# # observe results
# print(results[0].boxes)
render = render_result(model=model, image=image, result=results[0])
render.show()
