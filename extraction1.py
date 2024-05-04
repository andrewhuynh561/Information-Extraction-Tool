import fitz  # Import PyMuPDF
# The idea is determine the specific of text coordinate 
def extract_text_with_coordinates(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]  

    text_instances = page.get_text("dict")["blocks"]  
    text_data = []

    for block in text_instances:
        if block['type'] == 0:  
            text = block['lines']
            bbox = block['bbox']  
            block_text = ""
            for line in text:
                for span in line['spans']:  
                    block_text += span['text'] + " "
            text_data.append((block_text.strip(), bbox))
    
    doc.close()
    return text_data

# Usage
pdf_path = 'dataset\ROSEWORTHY DRAWINGS-pages-2.pdf'
text_blocks = extract_text_with_coordinates(pdf_path)
for text, bbox in text_blocks:
    print(text, bbox)
