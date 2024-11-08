from flask import Blueprint, request, jsonify
from services.ad_service import AdService

ad_bp = Blueprint('ad', __name__)

@ad_bp.route('/ad', methods=['POST'])
def create_ad():
    data = request.json
    response = AdService.create_ad(data)
    return jsonify({"message": "Ad created successfully", "data": response}), 201

@ad_bp.route('/ads/<company_id>', methods=['GET'])
def get_ads_by_company(company_id):
    ads = AdService.get_ads_by_company(company_id)
    return jsonify(ads)
