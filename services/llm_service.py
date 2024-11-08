
# services/llm_service.py
from utils.llm import LLM
from models.company import Company
from models.ad import Ad
from models.analytics import Analytics

class LLMService:
    @staticmethod
    def optimize_ad(company_id, ad_text, ad_details):
        company = Company.get_company(company_id)
        ads = Ad.get_ads_by_company(company_id)
        analytics = [Analytics.get_analytics_by_ad(ad['ad_id']) for ad in ads]
        
        print("🚀 ~ analytics:", analytics)
        print("🚀 ~ ads:", ads)
        print("🚀 ~ company:", company)
        print("🚀 ~ ad_text:", ad_text)
        return LLM.optimize_ad(ad_text, company, ads, analytics, ad_details)
    
    @staticmethod
    def suggest_optimal_times(region):
        return LLM.suggest_times(region)
