# services/company_service.py
from models.company import Company

class CompanyService:
    @staticmethod
    def get_company(company_id):
        return Company.get_company(company_id)

    @staticmethod
    def create_company(data):
        return Company.create_company(data)
    
    @staticmethod
    def create_property(company_id):
        return Company.create_property(company_id)
