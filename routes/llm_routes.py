

# routes/llm_routes.py
from flask import Blueprint, jsonify, request
from services.llm_service import LLMService
from services.img_service import ImgService

llm_bp = Blueprint('llm', __name__)


@llm_bp.route('/optimize-ad', methods=['POST'])
def optimize_ad():
    data = request.json
    company_id = data.get('company_id', None)
    property_id = data.get('property_id')# Taking in the property_id as well
    ad_text = data.get('ad_text', '')
    ad_details = data.get('ad_details', {})
    file_data = data.get('file', None)

    if not company_id:
        return jsonify({"error": "Company ID is required"}), 400
    
    #Extract text from the image
    extracted_text_response = ImgService.create_text(data)
    if 'error' in extracted_text_response:
        return jsonify(extracted_text_response), 400
    
    extracted_text = extracted_text_response.get('extracted_text', '')

    #Optimizing the text using extracted text
    optimized_ad = LLMService.optimize_ad(company_id, property_id, ad_text, ad_details, extracted_text)
    return jsonify({"optimized_ad": optimized_ad})


@llm_bp.route('/suggest-time', methods=['POST'])
def suggest_ad_time():
    data = request.json
    region = data['region']
    suggestions = LLMService.suggest_optimal_times(region)
    return jsonify({"suggestions": suggestions})
