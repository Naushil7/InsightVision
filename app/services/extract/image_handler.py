import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
from typing import Union
import os


def extract_text_from_image(image_path: Union[str, os.PathLike]) -> str:
    """
    Extracts text from a given image using Tesseract OCR.
    Supports JPG, PNG, etc.
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"[ERROR] Failed to extract text from image: {e}")
        return ""
