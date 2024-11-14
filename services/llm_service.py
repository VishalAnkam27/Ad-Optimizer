
# services/llm_service.py
from utils.llm import LLM
from models.company import Company
from models.ad import Ad
from models.analytics import Analytics

class LLMService:
    @staticmethod
    def optimize_ad(company_id, property_id, ad_text, ad_details, extracted_text):
        company = Company.get_company(company_id)
        
        if property_id:
            property_data = Company.get_property(company_id, property_id)
        else:
            # If property_id is not provided, create a new property with initial data
            new_property_data = {"ad_details": ad_details}  # Add relevant initial data here
            property_data = Company.create_property(company_id, new_property_data)
            property_id = property_data['property_id']  # Use the generated property ID
        
        ads = Ad.get_ads_by_company(company_id)
        analytics = [Analytics.get_analytics_by_ad(ad['ad_id']) for ad in ads]

        # Combine the extracted text with the provided ad text
        combined_ad_text = f"{ad_text} {extracted_text}"
        
        # Optionally, retrieve property-specific data if property_id is provided
        #property_data = None
        #if property_id:
         #   property_data = Company.create_property(company_id, property_id)
        
        print("🚀 ~ analytics:", analytics)
        print("🚀 ~ ads:", ads)
        print("🚀 ~ company:", company)
        print("🚀 ~ property_data:", property_data)        
        print("🚀 ~ ad_text:", ad_text)
        return LLM.optimize_ad(combined_ad_text, company, ads, analytics, ad_details, property_data)
    
    @staticmethod
    def suggest_optimal_times(region):
        return LLM.suggest_times(region)
