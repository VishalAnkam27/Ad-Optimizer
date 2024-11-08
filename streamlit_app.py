import requests
import streamlit as st

st.title("Real Estate Ad Optimizer")

# Sample data of companies and their IDs
companies = {
    "UrbanNest Realty": "UNR123",
    "Green Acres Properties": "GAP456",
    "Coastal Dream Homes": "CDH789",
    "Suburban Heights Development": "SHD321",
    "Luxe Living Estates": "LLE654",
    "Peak Property Investments": "PPI987",
}

# Input fields
ad_text = st.text_area("Enter Ad:", "")
company_name = st.selectbox("Select Company:", list(companies.keys()))
ad_details = st.text_area("Enter Additional Ad Details (Optional):", "")

# Get the selected company's ID
company_id = companies.get(company_name)

# Display the inputs for debugging (optional)
print("🚀 ~ ad_text:", ad_text)
print("🚀 ~ company_id:", company_id)
print("🚀 ~ ad_details:", ad_details)

# Button to optimize ad
if st.button("Optimize Ad"):
    # Make sure required fields are provided
    if not ad_text or not company_id:
        st.error("Please provide both the Ad Text and Company ID.")
    else:
        try:
            # Make the request to the API
            response = requests.post(
                "http://127.0.0.1:5000/optimize-ad",
                json={"ad_text": ad_text, "company_id": company_id, "ad_details": ad_details}
            )
            
            # Check if the response is successful
            if response.status_code == 200:
                data = response.json()
                optimized_ad = data.get("optimized_ad", "No optimized ad received.")
                
                # Display the optimized ad in a nicely formatted way
                st.subheader("Optimized Ad Copy:")
                st.markdown(f"> **{optimized_ad}**")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
