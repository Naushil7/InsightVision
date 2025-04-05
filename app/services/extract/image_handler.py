import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
from typing import Union
import os


def extract_text_from_image(image_path: Union[str, os.PathLike], min_confidence: int = 70) -> str:
    """
    Extracts text from a given image using Tesseract OCR.
    Supports JPG, PNG, etc.
    """
    # try:
    #     image = Image.open(image_path)
    #     text = pytesseract.image_to_string(image)
    #     return text
    # except Exception as e:
    #     print(f"[ERROR] Failed to extract text from image: {e}")
    #     return ""

    try:
        image = Image.open(image_path)
        ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

        lines = []
        current_line = []

        for i in range(len(ocr_data["text"])):
            text = ocr_data["text"][i]
            conf = int(ocr_data["conf"][i])
            if conf > min_confidence and text.strip():
                current_line.append(text)
            elif current_line:
                # end of a line
                lines.append(" ".join(current_line))
                current_line = []

        if current_line:
            lines.append(" ".join(current_line))

        cleaned_text = "\n".join(lines)
        return cleaned_text.strip()

    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")
        return ""