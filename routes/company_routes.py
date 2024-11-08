# routes/company_routes.py
from flask import Blueprint, request, jsonify
from services.company_service import CompanyService

company_bp = Blueprint('company', __name__)

@company_bp.route('/company', methods=['POST'])
def create_company():
    data = request.json
    response = CompanyService.create_company(data)
    return jsonify({"message": "Company created successfully", "data": response}), 201

@company_bp.route('/company/<company_id>', methods=['GET'])
def get_company(company_id):
    company = CompanyService.get_company(company_id)
    return jsonify(company)



#Create a API to store the property details of a company in the database
@company_bp.route('/company/<company_id>/property', methods=['POST'])
def create_property(company_id):
    data = request.json
    response = CompanyService.create_property(company_id, data)
    return jsonify({"message": "Property created successfully", "data": response}), 201