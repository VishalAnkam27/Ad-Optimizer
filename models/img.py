from flask import Blueprint, request, jsonify
import pytesseract as pt
from PIL import Image
import io
import base64
from utils.firestore import db

model_bp = Blueprint("model", __name__)

pt.pytesseract.tesseract_cmd = r'C:\Users\Tanishq\AppData\Local\Programs\Tesseract-OCR\tesseract'

class Img:
    @staticmethod
    def img_txt(data):
        if 'file' not in data or not data['file']:
            return {"error": "No file part"}, 400
        
        file_data = base64.b64decode(data['file'])
        img = Image.open(io.BytesIO(file_data))
        img_to_txt = pt.image_to_string(img)
        
        # Store the extracted text in Firestore
        ad_id = data.get('ad_id', db.collection('ads').document().id)
        ad_data = {
            'ad_id': ad_id,
            'company_id': data.get('company_id'),
            'ad_text': img_to_txt,
            'region': data.get('region'),
            'property_id': data.get('property_id')
        }
        db.collection('ads').document(ad_id).set(ad_data)
        
        return {"ad_id": ad_id, "extracted_text": img_to_txt}
