# Information-Extraction-Tool

Welcome to the Information-Extraction-Tool! This AI-powered tool can automatically recognize and extract elements of each drawing and their associated textual annotations in PDF documents. Perfect for streamlining your workflow and enhancing productivity.

## Initial Project Setup

Follow the steps below to set up and run the project.The sample pdf file from:
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

Thank you for using Information-Extraction-Tool! If you encounter any issues or have any questions, feel free to reach out.
