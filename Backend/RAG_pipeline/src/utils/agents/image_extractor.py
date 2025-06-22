"""
Image extraction from PDF files using different tools.
This module provides a class to extract images from PDF files using various tools such as pdf2image, PyMuPDF, and pdfplumber.
"""

import os
class ImageDataExtract:
    def __init__(self, pdf_path, tool_name):
        self.pdf_path = pdf_path
        self.tool_name = tool_name
        self.images = []
        self.image_dir = os.path.join(os.path.dirname(pdf_path), "images")
        os.makedirs(self.image_dir, exist_ok=True)

    