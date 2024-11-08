from utils.firestore import db

# models/analytics.py
class Analytics:
    def __init__(self, ad_id, clicks, conversions, engagement):
        self.ad_id = ad_id
        self.clicks = clicks
        self.conversions = conversions
        self.engagement = engagement

    @staticmethod
    def get_analytics_by_ad(ad_id):
        doc_ref = db.collection('analytics').document(ad_id)
        return doc_ref.get().to_dict()
