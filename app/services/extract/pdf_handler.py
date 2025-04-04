import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from typing import Tuple


def extract_text_from_pdf(path: str) -> Tuple[str, bool]:
    """
    Extracts text from a text-based PDF using PyMuPDF.
    Returns the text and a flag indicating if it's text-based.
    """
    doc = fitz.open(path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    doc.close()
    is_text_based = len(full_text.strip()) > 100
    return full_text, is_text_based


def extract_text_from_image_pdf(path: str, dpi=300) -> str:
    """
    Converts image-based PDFs to images and runs OCR using Tesseract.
    """
    images = convert_from_path(path, dpi=dpi)
    ocr_text = ""

    for image in images:
        text = pytesseract.image_to_string(image)
        ocr_text += text + "\n"

    return ocr_text


def extract_text_smart(path: str) -> str:
    """
    Unified method: detects whether PDF is text-based or image-based
    and chooses the right method to extract text.
    """
    extracted_text, is_text_based = extract_text_from_pdf(path)
    if is_text_based:
        return extracted_text
    print(f"[INFO] PDF '{path}' appears image-based — using OCR...")
    return extract_text_from_image_pdf(path)
