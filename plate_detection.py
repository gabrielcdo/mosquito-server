import cv2
import torch
import pytesseract
from PIL import Image

# Load OCR model
# pytesseract.pytesseract.tesseract_cmd = 'path/to/tesseract'
ocr_config = r"--oem 3 --psm 6"
# Load license plate detection model
model_plate = torch.hub.load("ultralytics/yolov5", "custom", path="models/best.pt")


def detect_license_plate(img):
    # Load image and convert to RGB

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform license plate detection
    results = model_plate(img)

    # Get bounding box coordinates of first detected plate
    plate_coords = results.xyxy[0][:4].tolist()[0]

    # Crop license plate from image
    cropped_plate = img[
        int(plate_coords[1]) : int(plate_coords[3]),
        int(plate_coords[0]) : int(plate_coords[2]),
    ]

    ocr_text = ocr_license_plate(cropped_plate)

    return ocr_text


def ocr_license_plate(cropped_plate):
    # Preprocess cropped image for OCR
    gray_plate = cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2GRAY)
    threshold_plate = cv2.threshold(
        gray_plate, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )[1]
    denoise_plate = cv2.fastNlMeansDenoising(threshold_plate, None, 20, 7, 21)

    # Convert processed image to readable format for Tesseract
    img_pil = Image.fromarray(denoise_plate)

    # Perform OCR on image
    ocr_text = pytesseract.image_to_string(img_pil, config=ocr_config)
    # remove * and . from the text
    ocr_text = ocr_text.replace("*", "").replace(".", "")
    return ocr_text
