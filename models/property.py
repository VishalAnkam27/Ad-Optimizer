from utils.firestore import db
import uuid

class Property:
    def __init__(self, company_id, property_name, address, property_type, property_details):
        self.property_id = str(uuid.uuid4())
        self.company_id = company_id
        self.property_name = property_name
        self.address = address
        self.property_type = property_type
        self.property_details = property_details

    def to_dict(self):
        return {
            "property_id": self.property_id,
            "company_id": self.company_id,
            "property_name": self.property_name,
            "address": self.address,
            "property_type": self.property_type,
            "property_details": self.property_details
        }

    @staticmethod
    def get_property(company_id, property_id):
        doc_ref = db.collection("companies").document(company_id).collection("properties").document(property_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    @staticmethod
    def get_all_properties(company_id):
        docs = db.collection("properties").where("company_id", "==", company_id).stream()
        return [doc.to_dict() for doc in docs]

    @staticmethod
    def create_property(company_id, data):
        print("🚀 ~ data:", data)
        print("🚀 ~ company_id:", company_id)
        # Generate a new property ID if not provided
        if "property_id" not in data:
            data["property_id"] = str(uuid.uuid4())
        doc_ref = db.collection("properties").document(data["property_id"])
        doc_ref.set(data)
        return data

    def save(self):
        # Save the current instance to Firestore
        data = self.to_dict()
        doc_ref = db.collection("properties").document(self.property_id)
        doc_ref.set(data)
        return data
