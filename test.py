import os
import pdfplumber
from PIL import Image

def convert_to_images(pdf_path, output_path, resolution=300):
    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    with pdfplumber.open(pdf_path) as pdf:
        # Iterate over each page in the PDF
        for page_num, page in enumerate(pdf.pages):
            image = page.to_image(resolution=resolution).original
            
            # Define the path to save the image
            image_path = os.path.join(output_path, f"page_{page_num + 1}.png")
            # Save the image
            image.save(image_path)

            # Print a confirmation message
            print(f"Saved  {page_num + 1} as image {image_path}")

# Example usage
pdf_path = "dataset/244_v1.pdf"
output_path = "images"
convert_to_images(pdf_path, output_path, resolution=300)

# table_headers = ['MARK', 'WIDTH x DEPTH', 'REINFORCEMENT', 'LIGATURES']
# table_data = [
#     ['RAFT & STRIP FOOTING', None, None, None],
#     ['E,M', '300 x 850', '6-N16 (3T,3B)', 'W8 @ 800 C/C'],
#     ['M1', '400 x 750', '8-N20 (4T,4B)', 'W8 @ 800 C/C'],
#     ['et', 'MIN 250 x 350', '1-N16 TOP', 'N/A'],
#     ['PAD FOOTING', None, None, None],
#     ['PF1', '1900 SQ x 1100', 'N16 @ 200 C/C EACH WAY TOP & BOTTOM', None],
#     ['PF2', '1500 SQ x 1100', 'N16 @ 200 C/C EACH WAY TOP & BOTTOM', None],
#     ['PF3', '1200 SQ x 800', 'N16 @ 200 C/C EACH WAY TOP & BOTTOM', None]
# ]
# def search_table_data(column_name, search_term):
#     # Initialize an empty list to hold the filtered data
#     filtered_data = []
    
#     # Check if the column name exists in the table headers
#     if column_name not in table_headers:
#         print(f"Column '{column_name}' not found.")
#         return filtered_data
    
#     # Get the index of the column
#     column_index = table_headers.index(column_name) 
#     # Iterate over each row 
#     for row in table_data:
#         # Check if the cell in the specified column is not None and contains the search term
#         cell = row[column_index]
#         if cell is not None and search_term in cell:
#             # If the condition is met, add the row to the filtered data
#             filtered_data.append(row)
    
#     return filtered_data

# # Search for all footings with a reinforcement of 'N16'
# search_results = search_table_data('REINFORCEMENT', 'N16')
# for result in search_results:
#     print(result)



