
# utils/llm.py
import openai
from utils.firestore import db
from datetime import datetime 

openai.api_key = os.getenv('OPENAI_API_KEY')


class LLM:
    @staticmethod
    def optimize_ad(ad_text, company, ads, analytics, ad_details, property_data=None):
        # Construct a prompt for ad optimization
        # prompt = f"Optimize the following ad:\n\nAd: {ad_text}\n\nCompany: {company}\n\nPrevious Ads: {ads}\n\nAnalytics: {analytics}"
        # The ad is targeting the following region:
        # {region_details}
        
        
#         Improve the following real-estate advertisement line to make it more attractive, persuasive, and likely to grab the attention of potential buyers.
# Focus on making it emotionally appealing, adding specific benefits or features, and creating a sense of urgency if needed, Don't use complex wording keep it simple and understandable,
# also make use of the details about the house such as Size: {size}, Location: {loc}, and Aminities: {aminities}, Don't make the text too long keep it between 10 to 20.
# Original ad: {original_ad}
        
        prompt =   [
                        {
                            "role": "system",
                            "content": f"""You are an expert ad optimizer for real estate, specializing in increasing clicks, engagement, and conversions through optimized ad copy.
                                            Improve the following real-estate advertisement line to make it more attractive, persuasive, and likely to grab the attention of potential buyers.
                                            Focus on making it emotionally appealing, adding specific benefits or features, and creating a sense of urgency if needed, Don't use complex wording keep it simple and understandable.
                                            Don't make the text too long keep it between 10 to 20.
                                            
                                            **Company's Details:**
                                                
                                                {company}
                                                
                                                **Previous Ads:**
                                                
                                                {ads}
                                                
                                                **Analytics of Previous Ads:**
                                                
                                                {analytics}
                                                """
                                        },
                        {
                            "role": "user",
                            "content": f"""
                                
                                **Real Estate Ad to be Optimized:**
                                
                                {ad_text}
                                
                                **Additional Property Details:**
                                
                                {ad_details}
                            """
                        }
                    ]
                    
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=100
        )
        
        # Extract the optimized ad text
        optimized_ad = response.choices[0].message['content'].strip()

        # Prepare data to store in Firestore
        ad_data = {
            'original_ad': ad_text,
            'optimized_ad': optimized_ad,
            'company_details': company,
            'timestamp': datetime.now().isoformat()
        }

        # Store the data in Firestore
        company_id = property_data['company_id']
        doc_ref = db.collection('companies').document(company_id) # Storing the property data as well
        doc_ref.set(ad_data)

        return optimized_ad

    @staticmethod
    def suggest_times(region):
        prompt = f"Suggest the best times to display ads for a property in the {region} region."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
