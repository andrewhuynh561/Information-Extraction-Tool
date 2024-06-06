# Information-Extraction-Tool

Welcome to the Information-Extraction-Tool! This AI-powered tool can automatically recognize and extract elements of each drawing and their associated textual annotations in PDF documents. Perfect for streamlining your workflow and enhancing productivity.

## Key Features of the Project

1. **Automated Table Detection**

   - **Fully Bordered Tables:** Utilizes pdfplumber to accurately detect and extract tables with complete borders directly from PDF files.
   - **Partly Borderless Tables:** Converts PDF pages to images and employs the YOLOv8 model to detect tables, even with partial borders, and crops the table images for further processing.

2. **OCR-Based Text Extraction**

   - **Table Extraction with Title Header Keywords:** Uses pytesseract to perform OCR on cropped table images, extracting text based on specific title header keywords such as "FOOTING SCHEDULE," "FOUNDATION SCHEDULE," etc.
   - **Additional Text Extraction:** Extracts other relevant text data from the PDF files to ensure comprehensive data capture for construction estimation.

3. **Multi-Page and Multi-File Processing**

   - **Folder Selection:** Allows users to select a folder containing multiple PDF files. The system can detect and process tables across multiple pages in each PDF and across multiple PDF files.

4. **Structured Data Output**

   - **Export to Excel:** Organizes the extracted tables and text data into a structured Excel file, with each sheet named after the corresponding PDF file. This facilitates easy integration with other tools and aids in construction estimation.

## Initial Project Setup

Follow the steps below to set up and run the project. The sample PDF file is from:
[Cornell-Engineers-Sample-Drawings.pdf (cornellengineers.com.au)](https://www.cornellengineers.com.au/wp-content/uploads/2014/03/Cornell-Engineers-Sample-Drawings.pdf?_gl=1*1nmpisi*_ga*MTUxNjA0NjA3OC4xNzE3NjY3ODcw*_ga_6LNZSCKJL8*MTcxNzY2Nzg2OS4xLjEuMTcxNzY2ODAwMi4wLjAuMA..)

### Environment Setup

1. Open your terminal.
2. Navigate to your project directory:

   ```bash
   cd <your-project-directory>
   ```

3. Install the necessary dependencies:

   ```bash
   pip install opencv-python
   pip install pytesseract
   pip install pdfplumber
   pip install ultralyticsplus==0.0.28 ultralytics==8.0.43
   ```

### YOLOv8 Integration

We leverage YOLOv8 for object detection and extraction, specifically tailored for table detection and extraction. For more details, visit the [Hugging Face repository](https://huggingface.co/foduucom/table-detection-and-extraction).

### Citation

If you use this software, please cite it using the following metadata:

```plaintext
cff-version: 1.2.0
title: Ultralytics YOLO
message: >-
If you use this software, please cite it using the
metadata from this file.
type: software
authors:
- given-names: Glenn
  family-names: Jocher
  affiliation: Ultralytics
  orcid: 'https://orcid.org/0000-0001-5950-6979'
- given-names: Ayush
  family-names: Chaurasia
  affiliation: Ultralytics
  orcid: 'https://orcid.org/0000-0002-7603-6750'
- family-names: Qiu
  given-names: Jing
  affiliation: Ultralytics
  orcid: 'https://orcid.org/0000-0003-3783-7069'
repository-code: 'https://github.com/ultralytics/ultralytics'
url: 'https://ultralytics.com'
license: AGPL-3.0
version: 8.0.0
date-released: '2023-01-10'
```
