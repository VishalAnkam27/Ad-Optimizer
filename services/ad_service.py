from models.ad import Ad
from models.ad_optimization import AdOptimization
class AdService:
    @staticmethod
    def create_ad(data):
        return Ad.create_ad(data)

    @staticmethod
    def get_ads_by_company(company_id):
        return Ad.get_ads_by_company(company_id)
    
    @staticmethod
    def get_optimized_ads_by_company(company_id):
        return AdOptimization.get_all_ad_optimizations(company_id)
    
    @staticmethod
    def update_selected_ad(optimization_id, selected_ad):
        return AdOptimization.update_selected_ad(optimization_id, selected_ad)

