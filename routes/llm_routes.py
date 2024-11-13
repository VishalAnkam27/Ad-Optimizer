

# routes/llm_routes.py
from flask import Blueprint, jsonify, request
from services.llm_service import LLMService

llm_bp = Blueprint('llm', __name__)

@llm_bp.route('/optimize-ad', methods=['POST'])
def optimize_ad():
    data = request.json
    company_id = data.get('company_id', None)
    ad_text = data.get('ad_text', '')
    ad_details = data.get('ad_details', {})
    if not company_id:
        return jsonify({"error": "Company ID is required"}), 400
    # return jsonify({"optimized_ads": ["ad1", "ad2", "ad3"]})  #remove after testing

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
