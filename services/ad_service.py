from models.ad import Ad

class AdService:
    @staticmethod
    def create_ad(data):
        return Ad.create_ad(data)

    @staticmethod
    def get_ads_by_company(company_id):
        return Ad.get_ads_by_company(company_id)
