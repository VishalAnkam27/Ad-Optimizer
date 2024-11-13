
# utils/llm.py
import openai
from utils.firestore import db
from datetime import datetime 
import os   
import re
from models.ad_optimization import AdOptimization

openai.api_key = os.getenv('OPENAI_API_KEY')
class LLM:
    @staticmethod
    def optimize_ad(ad_text, company, ads, analytics, ad_details):
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
                                            Don't make the text too long. Provide 5 different versions of the optimized ad.
                                            
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
        optimized_ads = re.findall(r'\d+\.\s*"(.*?)"(?:$|\n)', optimized_ad)
        # Prepare data to store in Firestore
        # add property id to the data

        created_ad_optimization = AdOptimization.create_ad_optimization(optimized_ads, ad_text, company, property_details=ad_details)

        print("🚀 ~ optimized_ad:", optimized_ad)
        print("🚀 ~ optimized_ads:", optimized_ads)
        return created_ad_optimization

    @staticmethod
    def suggest_times(region):
        prompt = f"Suggest the best times to display ads for a property in the {region} region."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=50
        )
        return response.choices[0].message['content'].strip()


    #TODO: these following methods can be combined to get the sample ad and sample ad details
    @staticmethod
    def get_sample_ad(company):
        prompt = [{"role": "system", "content": f"Suggest some sample ad which can be used by user for optimization. Based on the company details {company}, it should be short and simple. also include the informative message for the user"}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=50
        )
        print("🚀 ~ response.choices[0].message['content'].strip():", response.choices[0].message['content'].strip())
        return response.choices[0].message['content'].strip()

    @staticmethod
    def get_sample_ad_details(company):
        prompt = [{"role": "system", "content": f"Suggest some sample property details like aminity, location, size, etc which user can you along with the ad for optimization Based on the company details {company}, it should be short and simple. also include the informative message for the user"}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=50
        )
        print("🚀 ~ response.choices[0].message['content'].strip():", response.choices[0].message['content'].strip())
        return response.choices[0].message['content'].strip()
