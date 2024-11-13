from utils.firestore import db
from datetime import datetime
import uuid

class AdOptimization:
    def __init__(self, company_id, property_id, optimized_ads, original_ad, company_details, property_details):
        self.optimization_id = str(uuid.uuid4())
        self.company_id = company_id
        self.property_id = property_id
        self.optimized_ads = optimized_ads  # Example: {'1': "Optimized ad content here"}
        self.selected_ad = optimized_ads[0] if optimized_ads else ""
        self.company_details = company_details
        self.property_details = property_details
        self.original_ad = original_ad
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "optimization_id": self.optimization_id,
            "company_id": self.company_id,
            "company_details": self.company_details,
            "property_id": self.property_id,
            "property_details": self.property_details,
            "optimized_ads": self.optimized_ads,
            "selected_ad": self.selected_ad,
            "original_ad": self.original_ad,
            "timestamp": self.timestamp
        }

    @staticmethod
    def create_ad_optimization(optimized_ads, original_ad, company_details, property_id=None, property_details=None):
        ad_optimization = AdOptimization(company_details.get('company_id', ""), property_id, optimized_ads, original_ad, company_details, property_details)
        data = ad_optimization.to_dict()
        doc_ref = db.collection("ad_optimizations").document(ad_optimization.optimization_id)
        doc_ref.set(data)
        return data
    
    @staticmethod
    def update_selected_ad(optimization_id, selected_ad):
        doc_ref = db.collection("ad_optimizations").document(optimization_id)
        doc_ref.update({"selected_ad": selected_ad})
        return True

    @staticmethod
    def get_ad_optimization(optimization_id):
        doc_ref = db.collection("ad_optimizations").document(optimization_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    @staticmethod
    def get_all_ad_optimizations(company_id, property_id=None):
        query = db.collection("ad_optimizations").where("company_id", "==", company_id)
        if property_id:
            query = query.where("property_id", "==", property_id)
        docs = query.stream()
        return [doc.to_dict() for doc in docs]
