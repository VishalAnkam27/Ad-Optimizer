import streamlit as st
from table_view import render_table_view
from optimize_ad import render_optimize_ad
from utils import fetch_companies, fetch_properties, create_property

# Set page title and main title
st.set_page_config(page_title="Real Estate Ad Optimizer")
st.title("Real Estate Ad Optimizer")

# Initialize session state
if "current_view" not in st.session_state:
    st.session_state.current_view = "table_view"
if "selected_company" not in st.session_state:
    st.session_state.selected_company = None
if "selected_property" not in st.session_state:
    st.session_state.selected_property = None

# Sidebar for company and property selection
st.sidebar.title("Select Company and Property")

# Step 1: Select Company
companies = fetch_companies()
selected_company = st.sidebar.selectbox(
    "Select Company", 
    [company["company_name"] for company in companies], 
    key="company"
)

# Retrieve selected company ID and set in session state
selected_company_id = next((company["company_id"] for company in companies if company["company_name"] == selected_company), None)
st.session_state.selected_company = selected_company_id

# Step 2: Select Property (Optional)
if selected_company:
    properties = fetch_properties(selected_company_id)
    selected_property = st.sidebar.selectbox(
        "Select Property (Optional)", 
        ["None"] + [prop["property_name"] for prop in properties], 
        key="property"
    )
    
    # Retrieve selected property ID
    st.session_state.selected_property = next((prop["property_id"] for prop in properties if prop["property_name"] == selected_property), None) if selected_property != "None" else None

# Optional: Create Property in Expander
with st.sidebar.expander("Create New Property"):
    new_property_name = st.text_input("Property Name")
    new_property_details = st.text_area("Property Details")
    create_property_company = st.selectbox("Company for Property", [company["company_name"] for company in companies])
    create_property_company_id = next((company["company_id"] for company in companies if company["company_name"] == create_property_company), None)
    
    if st.button("Create Property"):
        if new_property_name and new_property_details:
            create_property(create_property_company_id, new_property_name, new_property_details)
        else:
            st.error("Please fill out both property name and details.")

# Top navigation button to toggle between views
if st.button("Go to Optimize Ad Screen" if st.session_state.current_view == "table_view" else "Back to Table Screen"):
    st.session_state.current_view = "optimize_ad" if st.session_state.current_view == "table_view" else "table_view"

# Render the selected view
if st.session_state.current_view == "table_view":
    render_table_view()
elif st.session_state.current_view == "optimize_ad":
    render_optimize_ad()
