FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install -y tesseract-ocr-all && \
    rm -rf /var/lib/apt/lists/* && \ 
    pip install --no-cache-dir -r requirements.txt

# Copy the code to the container
COPY . .

# Entrypoint
CMD ["python", "receive_code.py"]
