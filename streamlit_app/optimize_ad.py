import streamlit as st
import requests
from PIL import Image

# Set page configuration at the very top
st.set_page_config(page_title="Real Estate Ad Optimizer", layout="wide")

# Initialize session state for tracking the active step
if 'active_step' not in st.session_state:
    st.session_state.active_step = 0

# Function to render the ad optimization interface
def render_optimize_ad():
    st.title("Optimize Ad")
    
    # Company and property selection
    st.sidebar.selectbox("Select Company", ["Company A", "Company B"], key="selected_company")
    st.sidebar.selectbox("Select Property", ["Property 1", "Property 2"], key="selected_property")
    
    # Stepper UI
    steps = ["Enter Text", "Upload Image"]
    st.subheader(f"Step {st.session_state.active_step + 1}: {steps[st.session_state.active_step]}")
    
    # Step content
    if st.session_state.active_step == 0:
        # Step 1: Text input for ad optimization
        ad_text = st.text_area("Enter Ad Text", key="ad_text")
        
        optimize_text_clicked = st.button("Optimize Ad Text")
        if optimize_text_clicked and ad_text:
            response = requests.post(
                "http://127.0.0.1:5000/optimize-ad-text",
                json={
                    "ad_text": ad_text,
                    "company_id": st.session_state.selected_company,
                    "property": st.session_state.selected_property
                }
            )
            if response.status_code == 200:
                data = response.json()
                optimized_ads = data.get("optimized_ads", ["No optimized ads received."])
                st.session_state.optimized_ads = optimized_ads
                display_optimized_ads(optimized_ads)
            else:
                st.error(f"Error {response.status_code}: {response.text}")

    elif st.session_state.active_step == 1:
        # Step 2: Image input for ad optimization
        uploaded_image = st.file_uploader("Upload Ad Image", type=["jpg", "jpeg", "png"], key="ad_image")
        
        optimize_image_clicked = st.button("Optimize Ad Image")
        if optimize_image_clicked and uploaded_image:
            files = {"file": uploaded_image.getvalue()}
            response = requests.post(
                "http://127.0.0.1:5000/optimize-ad-image",
                files=files,
                data={
                    "company_id": st.session_state.selected_company,
                    "property": st.session_state.selected_property
                }
            )
            if response.status_code == 200:
                data = response.json()
                optimized_ads = data.get("optimized_ads", ["No optimized ads received."])
                st.session_state.optimized_ads = optimized_ads
                display_optimized_ads(optimized_ads)
            else:
                st.error(f"Error {response.status_code}: {response.text}")

    # Stepper navigation
    prev_clicked = st.button("Previous", disabled=st.session_state.active_step == 0)
    next_clicked = st.button("Next", disabled=st.session_state.active_step == len(steps) - 1)
    if prev_clicked and st.session_state.active_step > 0:
        st.session_state.active_step -= 1
    if next_clicked and st.session_state.active_step < len(steps) - 1:
        st.session_state.active_step += 1

# Function to display optimized ads
def display_optimized_ads(optimized_ads):
    st.subheader("Optimized Ads")
    for idx, opt_ad in enumerate(optimized_ads):
        st.markdown(f"> **Option {idx + 1}:** {opt_ad}")

# Render the Optimize Ad section
render_optimize_ad()
