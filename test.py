import os
import pdfplumber
from PIL import Image

def convert_to_images(pdf_path, resolution=300):
    # Get the directory of the PDF file
    # output_dir = os.path.dirname(pdf_path)
    
    image_paths = []

    with pdfplumber.open(pdf_path) as pdf:
        # Iterate over each page in the PDF
        for page_num, page in enumerate(pdf.pages):
            image = page.to_image(resolution=resolution).original
            
            # # Define the path to save the image
            image_path = os.path.join( f"page_{page_num + 1}.png")
            # Save the image
            image.save(image_path)

            # # Add the image path to the list
            image_paths.append(image_path)

            # # Print a confirmation message
            # print(f"Saved page {page_num + 1} as image {image_path}")

    return image_paths
# Example usage
pdf_path = "dataset/578-580 RIVERSDALE ROAD, CAMBERWELL - FOOTINGS.pdf"
image_paths = convert_to_images(pdf_path, resolution=300)

# Now you can use image_paths for the next step
print(image_paths)
