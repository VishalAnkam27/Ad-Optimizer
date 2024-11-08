from flask import Blueprint, request, jsonify
from services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/<ad_id>', methods=['GET'])
def get_analytics_by_ad(ad_id):
    analytics = AnalyticsService.get_analytics_by_ad(ad_id)
    if analytics:
        return jsonify(analytics)
    return jsonify({"error": "Analytics not found"}), 404

@analytics_bp.route('/analytics', methods=['POST'])
def create_analytics():
    data = request.json
    AnalyticsService.create_analytics(data)
    return jsonify({"message": "Analytics data saved successfully"}), 201
