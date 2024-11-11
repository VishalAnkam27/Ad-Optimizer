# models/company.py
from utils.firestore import db

class Company:
    def __init__(self, company_id, name, target_audience, brand_tone, specialty):
        self.company_id = company_id
        self.name = name
        self.target_audience = target_audience
        self.brand_tone = brand_tone
        self.specialty = specialty

    def get_company(company_id):
        if not company_id:
            raise ValueError("Company ID must be provided")

        doc_ref = db.collection("companies").document(company_id)
        return doc_ref.get().to_dict()

    
    def get_property(company_id, property_id):
        if not company_id:
            raise ValueError("Company ID must be provided")
        
            # Reference to the specific property document
        doc_ref = db.collection('companies').document(company_id).collection('properties').document(property_id)
        property_data = doc_ref.get().to_dict()
        return property_data        
    
    
    @staticmethod
    def create_company(data):
        if 'company_id' in data and data['company_id']:
            # Use the provided company_id if it exists
            doc_ref = db.collection('companies').document(data['company_id'])
        else:
            # Auto-generate an ID if company_id is not provided
            doc_ref = db.collection('companies').document()
            data['company_id'] = doc_ref.id  # Set the generated ID in the data dictionary
        
        doc_ref.set(data)
        return data  # Returning data with the generated company_id for reference
    
    
    @staticmethod
    def create_property(company_id, data=None, property_id=None):
        if not company_id:
            raise ValueError("Company ID must be provided")
    
        data['company_id'] = company_id
        
        if property_id:
            doc_ref = db.collection('companies').document(company_id).collection('properties').document(property_id)
        else:
            doc_ref = db.collection('companies').document(company_id).collection('properties').document()
            data['property_id'] = doc_ref.id  # Set the generated ID in the data dictionary
        
        print("Creating Property with ID: ", data['property_id'])
        
        # Set data and confirm completion
        doc_ref.set(data)
        print("Property created successfully with data: ", data)
        
        return data