import cv2
import pytesseract
import numpy as np
from PIL import Image
import io
import os
from google.cloud import vision
from ai_classifier import extract_amount, classify_expense

# ✅ Direct Credentials Set Kar
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Tanu/OneDrive/Desktop/finance_manager/vision_ai_key.json"

# Google Vision AI Client Initialize
client = vision.ImageAnnotatorClient()


def extract_text_and_classify(uploaded_file):
    """Google Vision AI OCR + Keyword Classification + Amount Extraction"""
    if uploaded_file is None:
        return "No file uploaded", "No category detected", "Amount not found", []

    client = vision.ImageAnnotatorClient()

    # Convert uploaded file to bytes for Vision AI
    image_bytes = uploaded_file.read()
    image = vision.Image(content=image_bytes)

    # Vision AI OCR
    response = client.document_text_detection(image=image)

    if response.text_annotations:
        extracted_text = response.text_annotations[0].description
    else:
        extracted_text = "No text found"

    # Extract Amount
    detected_amount = extract_amount(extracted_text)

    # Keyword Classification
    predicted_category, matched_keywords = classify_expense(extracted_text)

    return extracted_text, predicted_category, detected_amount, matched_keywords