# utils/firestore.py
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("/Users/vishalankam/Desktop/Velotio/Ad-Optimiser/firestore_service_account.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
