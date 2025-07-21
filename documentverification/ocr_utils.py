import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import docx2txt
import os
import re
from django.conf import settings


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_field(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(2).strip() if match else None

def extract_text_fields(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    full_text = ""

    if ext == ".pdf":
        images = convert_from_path(file_path, poppler_path=settings.POPPLER_PATH)
        for img in images:
            full_text += pytesseract.image_to_string(img) + "\n"
    elif ext in [".jpg", ".jpeg", ".png"]:
        image = Image.open(file_path)
        full_text += pytesseract.image_to_string(image)
    elif ext == ".docx":
        full_text += docx2txt.process(file_path)
    else:
        full_text = "Unsupported file format"

    return {
        "raw_text": full_text,
        "name": extract_field(full_text, r"(Name|Full Name)\s*[:\-]?\s*([\w\s]+)"),
        "name": extract_field(full_text, r"(Name|Full Name|Surname)\s*[:\-]?\s*([A-Z\s]+)"),
        "dob": extract_field(full_text, r"(Date of Birth|DOB|Birth Date|Nationality & Date of Birth)\s*[:\-]?\s*([0-9]{1,2}\s*[A-Za-z]{3,9}\s*[0-9]{2,4}|[0-9]{2}/[0-9]{2}/[0-9]{4})"),
        "doc_number": extract_field(full_text, r"(Passport Number|Document Number|Doc Number|Passport No\.?)\s*[:\-]?\s*([A-Z0-9]+)"),
        "expiry_date": extract_field(full_text, r"(Expiry Date|Date of Expiry|Expires|Valid Until)\s*[:\-]?\s*([0-9]{1,2}\s*[A-Za-z]{3,9}\s*[0-9]{2,4}|[0-9]{2}/[0-9]{2}/[0-9]{4})")
    }

