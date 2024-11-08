from utils.firestore import db

# models/ad.py
class Ad:
    def __init__(self, ad_id, company_id, ad_text, region):
        self.ad_id = ad_id
        self.company_id = company_id
        self.ad_text = ad_text
        self.region = region

    @staticmethod
    def get_ads_by_company(company_id):
        docs = db.collection('ads').where('company_id', '==', company_id).stream()
        return [doc.to_dict() for doc in docs]

    @staticmethod
    def create_ad(data):
        ad_id = data.get('ad_id', db.collection('ads').document().id)
        data['ad_id'] = ad_id
        db.collection('ads').document(ad_id).set(data)
        return data 