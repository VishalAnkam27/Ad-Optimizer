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


@ad_bp.route('/get-optimized-ads/<company_id>', methods=['GET'])
def get_optimized_ads_by_company(company_id):
    ads = AdService.get_optimized_ads_by_company(company_id)
    return jsonify(ads)

@ad_bp.route('/update-selected-ad/<optimization_id>', methods=['PUT'])
def update_selected_ad(optimization_id):
    data = request.json
    selected_ad = data.get('selected_ad',"")
    response = AdService.update_selected_ad(optimization_id, selected_ad)
    return jsonify({"message": "Selected ad updated successfully", "data": response}), 200
