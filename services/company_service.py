# services/company_service.py
from models.company import Company
from models.property import Property

class CompanyService:
    @staticmethod
    def get_company(company_id):
        return Company.get_company(company_id)  

    @staticmethod
    def get_all_companies():
        return Company.get_all_companies()

    @staticmethod
    def create_company(data):
        return Company.create_company(data)
    
    @staticmethod
    def create_property(company_id, data):
        return Property.create_property(company_id, data)
    
    @staticmethod
    def get_all_properties(company_id):
        return Property.get_all_properties(company_id)
