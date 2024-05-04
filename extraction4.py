import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        for page in pdf.pages:
            # Extract tables using the extract_table method
            page_tables = page.extract_tables()
            for table in page_tables:
                # Convert table data into a DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)
    return all_tables

def save_tables_to_excel(tables, output_file):
    with pd.ExcelWriter(output_file) as writer:
        for idx, table in enumerate(tables):
            table.to_excel(writer, sheet_name=f'Table_{idx+1}')

# Usage
pdf_path = 'dataset\ROSEWORTHY DRAWINGS-pages-2.pdf'
output_excel = 'output.xlsx'
tables = extract_tables_from_pdf(pdf_path)
save_tables_to_excel(tables, output_excel)
