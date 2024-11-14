

# routes/llm_routes.py
from flask import Blueprint, jsonify, request
from services.llm_service import LLMService
from flask import request, jsonify
from werkzeug.utils import secure_filename
import pytesseract  # Optical Character Recognition library
from PIL import Image
import os


llm_bp = Blueprint('llm', __name__)

# Configuration for allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Utility function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Utility function to extract text from an image using OCR (e.g., pytesseract)
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        print("🚀 ~ extract_text_from_image ~ e:", e)
        return None

@llm_bp.route('/optimize-ad', methods=['POST'])
def optimize_ad():
    data = request.form if request.form else request.json
    print("🚀 ~ data:", data)
    company_id = data.get('company_id', None)
    ad_text = data.get('ad_text', '')
    ad_details = data.get('ad_details', {})

    # Handle errors for missing company ID
    if not company_id:
        return jsonify({"error": "Company ID is required"}), 400

    # Check if an image was uploaded
    if 'ad_image' in request.files:
        ad_image = request.files['ad_image']
        
        if ad_image and allowed_file(ad_image.filename):
            filename = secure_filename(ad_image.filename)
            image_path = os.path.join('/tmp', filename)  # Save to a temporary directory
            ad_image.save(image_path)
            print("🚀 ~ image_path:", image_path)

            # Extract text from the image
            extracted_text = extract_text_from_image(image_path)
            print("🚀 ~ extracted_text:", extracted_text)
            if not extracted_text:
                return jsonify({"error": "Unable to extract text from image"}), 400
            
            ad_text = extracted_text  # Use extracted text for optimization
        else:
            return jsonify({"error": "Invalid image format"}), 400

    # Proceed with ad optimization using the ad text
    optimized_ad = LLMService.optimize_ad(company_id, ad_text, ad_details)

    return jsonify({"optimized_ads": optimized_ad})


@llm_bp.route('/suggest-time', methods=['POST'])
def suggest_ad_time():
    data = request.json
    region = data['region']
    suggestions = LLMService.suggest_optimal_times(region)
    return jsonify({"suggestions": suggestions})


@llm_bp.route('/get-sample-ad/<company_id>', methods=['GET'])
def get_sample_ad(company_id):
    print("🚀 ~ company_id:", company_id)
    sample_ad, sample_ad_details = LLMService.get_sample_ad(company_id=company_id)
    return jsonify({"sample_ad": sample_ad, "sample_ad_details": sample_ad_details})
