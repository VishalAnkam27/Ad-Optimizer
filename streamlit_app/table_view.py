import streamlit as st
from utils import fetch_companies, fetch_properties, fetch_previous_ads, create_property

def render_table_view():
   
    st.subheader("Previous Ads")

    # Display previous ads if a property is selected
    if st.session_state.selected_company and st.session_state.selected_property:
        previous_ads = fetch_previous_ads(st.session_state.selected_company, st.session_state.selected_property)
        if previous_ads:
            for idx, ad in enumerate(previous_ads):
                st.write(f"**Ad {idx + 1}:** {ad['ad_text']}")
                if st.button(f"Optimize Ad {idx + 1}", key=f"optimize_ad_{idx}"):
                    st.session_state.selected_ad_text = ad["ad_text"]
                    st.session_state.current_view = "optimize_ad"
