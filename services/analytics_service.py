from models.analytics import Analytics

class AnalyticsService:
    @staticmethod
    def get_analytics_by_ad(ad_id):
        return Analytics.get_analytics_by_ad(ad_id)

    @staticmethod
    def create_analytics(data):
        Analytics.create_analytics(data)
