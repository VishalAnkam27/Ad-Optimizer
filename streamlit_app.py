import streamlit as st
import requests

# Function to fetch companies
def fetch_companies():
    # Here, you would call your API to get the list of companies
    # This is a placeholder API
    response = requests.get("http://127.0.0.1:5000/get-companies")
    if response.status_code == 200:
        return response.json()  # Return the list of companies
    else:
        # st.error("Failed to fetch companies.")
        #return []
        return [
            {"company_id": "UNR123", "company_name": "UrbanNest Realty"},
            {"company_id": "GAP456", "company_name": "Green Acres Properties"},
            {"company_id": "CDH789", "company_name": "Coastal Dream Homes"},
            {"company_id": "SHD321", "company_name": "Suburban Heights Development"},
            {"company_id": "LLE654", "company_name": "Luxe Living Estates"},
            {"company_id": "PPI987", "company_name": "Peak Property Investments"},
        ]

# Function to fetch properties based on the selected company
def fetch_properties(company_id):
    # Placeholder for fetching properties based on the company ID
    response = requests.get(f"http://127.0.0.1:5000/get-properties/{company_id}")
    if response.status_code == 200:
        return response.json()  # Return the list of properties
    else:
        # st.error("Failed to fetch properties.")
        # return []
        return [
            {"property_id": "123456", "property_name": "Properties1"},
            {"property_id": "123456", "property_name": "Properties2"},
            ]

# Function to fetch previous ads based on the company and property
def fetch_previous_ads(company_id, property_id):
    # Placeholder for fetching previous ads for the selected company and property
    response = requests.get(f"http://127.0.0.1:5000/get-previous-ads/{company_id}/{property_id}")
    if response.status_code == 200:
        return response.json()  # Return previous ads
    else:
        # st.error("Failed to fetch previous ads.")
        # return []
        return [
            {"ad_text": "Ad1", "date": "2024-01-01"},
            {"ad_text": "Ad2", "date": "2024-01-02"},
            ]

# Function to create a new property
def create_property(company_id, property_name, property_details):
    # Placeholder API for creating a property
    response = requests.post(
        f"http://127.0.0.1:5000/create-property/{company_id}",
        json={"property_name": property_name, "property_details": property_details}
    )
    if response.status_code == 201:
        st.success("Property created successfully.")
    else:
        st.error("Failed to create property.")

# Initialize session state to keep track of view, selected company, property, and ad
if "current_view" not in st.session_state:
    st.session_state.current_view = "table_view"  # Default view
if "selected_company" not in st.session_state:
    st.session_state.selected_company = None
if "selected_property" not in st.session_state:
    st.session_state.selected_property = None
if "selected_ad_text" not in st.session_state:
    st.session_state.selected_ad_text = ""


# Top navigation button to toggle between views
if st.button("Go to Optimize Ad Screen" if st.session_state.current_view == "table_view" else "Back to Table Screen"):
    st.session_state.current_view = "optimize_ad" if st.session_state.current_view == "table_view" else "table_view"

# Sidebar for company and property selection
st.sidebar.title("Select Company and Property")

# Step 1: Select Company
companies = fetch_companies()
selected_company = st.sidebar.selectbox("Select Company", [company["company_name"] for company in companies], key="company")

# Retrieve selected company ID
selected_company_id = next((company["company_id"] for company in companies if company["company_name"] == selected_company), None)
if selected_company:
    st.session_state.selected_company = selected_company_id

    # Step 2: Select Property (Optional)
    properties = fetch_properties(selected_company_id)
    selected_property = st.sidebar.selectbox("Select Property (Optional)", ["None"] + [prop["property_name"] for prop in properties], key="property")

    # Retrieve selected property ID
    selected_property_id = next((prop["property_id"] for prop in properties if prop["property_name"] == selected_property), None)
    st.session_state.selected_property = selected_property_id if selected_property != "None" else None

    # Optional: Create Property in Expander
    with st.sidebar.expander("Create New Property"):
        new_property_name = st.text_input("Property Name")
        new_property_details = st.text_area("Property Details")
        create_property_company = st.selectbox("Company for Property", [company["company_name"] for company in companies])

        # Retrieve company ID for property creation
        create_property_company_id = next((company["company_id"] for company in companies if company["company_name"] == create_property_company), None)
        
        if st.button("Create Property"):
            if new_property_name and new_property_details:
                # Function to create a new property here (not shown for brevity)
                properties = fetch_properties(selected_company_id)
            else:
                st.error("Please fill out both property name and details.")

# Render the selected view
if st.session_state.current_view == "table_view":
    st.subheader("Previous Ads")

    # Display previous ads if a property is selected
    if st.session_state.selected_company and st.session_state.selected_property:
        previous_ads = fetch_previous_ads(st.session_state.selected_company, st.session_state.selected_property)
        if previous_ads:
            # Display ads in a table with an Optimize button for each ad
            for idx, ad in enumerate(previous_ads):
                st.write(f"**Ad {idx + 1}:** {ad['ad_text']}")
                if st.button(f"Optimize Ad {idx + 1}", key=f"optimize_ad_{idx}"):
                    st.session_state.selected_ad_text = ad["ad_text"]
                    st.session_state.current_view = "optimize_ad"

elif st.session_state.current_view == "optimize_ad":
    st.subheader("Optimize Ad")

    # Allow user to create a new ad if no previous ad is selected
    ad_text = st.text_area("Enter Ad Text", value=st.session_state.selected_ad_text)
    if st.button("Optimize New Ad"):
        if ad_text:
            # Placeholder for API call to optimize the ad
            response = requests.post(
                "http://127.0.0.1:5000/optimize-ad",
                json={"ad_text": ad_text, "company_id": st.session_state.selected_company, "property": st.session_state.selected_property}
            )
            if response.status_code == 200:
                data = response.json()
                optimized_ads = data.get("optimized_ads", ["No optimized ads received."])
                st.session_state.optimized_ads = optimized_ads
                st.subheader("Optimized Ads")
                for opt_ad in optimized_ads:
                    st.markdown(f"> **{opt_ad}**")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        else:
            st.error("Please enter ad text to optimize.")
