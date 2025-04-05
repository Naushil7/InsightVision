# Dockerfile

FROM python:3.10-slim

WORKDIR /app
COPY . /app
COPY ./models /app/models


# System-level dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1-mesa-glx \
    && apt-get clean

# Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8080


# Entry point
CMD ["streamlit", "run", "app/main.py", "--server.port=8080", "--server.enableCORS=false"]
