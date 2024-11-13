import requests
import streamlit as st

# Function to fetch companies
def fetch_companies():
    response = requests.get("http://127.0.0.1:5000/get-companies")
    if response.status_code == 200:
        return response.json()
    else:
        return [
            {"company_id": "UNR123", "company_name": "UrbanNest Realty"},
            {"company_id": "GAP456", "company_name": "Green Acres Properties"},
            # Add other companies as needed
        ]

# Function to fetch properties based on the selected company
def fetch_properties(company_id):
    response = requests.get(f"http://127.0.0.1:5000/get-properties/{company_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return [
            {"property_id": "123456", "property_name": "Property1"},
            {"property_id": "654321", "property_name": "Property2"},
        ]

# Function to fetch previous ads based on the company and property
def fetch_previous_ads(company_id, property_id):
    response = requests.get(f"http://127.0.0.1:5000/get-previous-ads/{company_id}/{property_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return [
            {"ad_text": "Ad1", "date": "2024-01-01"},
            {"ad_text": "Ad2", "date": "2024-01-02"},
        ]

# Function to create a new property
def create_property(company_id, property_name, property_details):
    response = requests.post(
        f"http://127.0.0.1:5000/create-property/{company_id}",
        json={"property_name": property_name, "property_details": property_details}
    )
    return response.status_code == 201
