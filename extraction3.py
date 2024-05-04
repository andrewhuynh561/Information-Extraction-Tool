import fitz  # Import PyMuPDF
# The idea for extracting title block 
# Using text extraction to detect font style 
def extract_bold_text(pdf_path):
    doc = fitz.open(pdf_path)
    bold_texts = []  
    font_details = []  

    for page in doc:
        text_instances = page.get_text("dict")["blocks"]
        for instance in text_instances:
            for line in instance["lines"]:
                for span in line["spans"]:
                    # Collect font details for diagnostics
                    font_details.append((span['text'], span['font'], span['size']))
                    if 'bold' in span['font'].lower() and span['size'] > 21:  # Check if text is bold and larger
                        bold_texts.append(span['text'])
    doc.close()
    return bold_texts, font_details

# Path to your PDF file
file_path = 'dataset\ROSEWORTHY DRAWINGS-pages-2.pdf'
project_names, font_diagnostics = extract_bold_text(file_path)

# Print project names and font details
print("Possible Project Names:")
for name in project_names:
    print(name)

print("\nFont Details (for diagnostics):")
for text, font, size in font_diagnostics:
    print(f"Text: {text}, Font: {font}, Size: {size}")



# import fitz  # Import PyMuPDF

# def extract_project_info(pdf_path):
#     doc = fitz.open(pdf_path)
#     project_details = []  # List to hold project details based on font size

#     for page in doc:
#         text_instances = page.get_text("dict")["blocks"]
#         current_project = []
#         for instance in text_instances:
#             for line in instance["lines"]:
#                 for span in line["spans"]:
#                     # Focus on text with size around 22 or greater and capture subsequent lines of similar size
#                     if span['size'] > 20:
#                         current_project.append(span['text'])
#                     elif current_project:  # Once a smaller text is encountered, stop and join the collected text
#                         project_details.append(" ".join(current_project))
#                         current_project = []  # Reset for the next potential project title block

#         # Catch any trailing project title details not followed by smaller text
#         if current_project:
#             project_details.append(" ".join(current_project))

#     doc.close()
#     return project_details

# # Path to your PDF file
# file_path = 'ROSEWORTHY DRAWINGS-pages-2.pdf'
# project_info = extract_project_info(file_path)

# # Print extracted project info
# for info in project_info:
#     print(info)


