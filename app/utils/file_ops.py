import os
import shutil
from werkzeug.utils import secure_filename
from app.config import settings

def save_uploaded_file(uploaded_file) -> str:
    filename = secure_filename(uploaded_file.name)
    save_path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

def get_file_type(path: str) -> str:
    if path.lower().endswith(".pdf"):
        return "pdf"
    elif path.lower().endswith((".png", ".jpg", ".jpeg")):
        return "image"
    return "unknown"

def cleanup_temp_dir():
    temp_dir = settings.UPLOAD_DIR
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
