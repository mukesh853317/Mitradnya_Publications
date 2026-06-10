import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
import random
import streamlit.components.v1 as components
import re

# फाईल पाथ सुरक्षित करणे (ही महत्वाची ओळ आहे)
base_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_path, 'All in one.csv')

# डेटा लोड करण्यासाठी फंक्शन
@st.cache_data
def load_data():
    if not os.path.exists(csv_path):
        st.error(f"फाईल सापडली नाही: {csv_path}")
        return None
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        df.columns = df.columns.str.strip()
        df.fillna("None", inplace=True)
        return df
    except Exception as e:
        st.error(f"डेटा लोड करताना एरर: {e}")
        return None

df = load_data()

# पोर्टल स्ट्रक्चर (इथे तुमचे आधीचे लॉजिक व्यवस्थित लावले आहे)
if df is not None:
    # तुमची पूर्ण लॉजिक इथे सुरू करा
    st.title("📚 Mitradnya Publication's Online Portal 📚")
    # ... तुमचा बाकीचा कोड जो तुम्ही दिला होता ...
else:
    st.warning("डेटा फाईल लोड होऊ शकली नाही. कृपया फाईलचे नाव आणि लोकेशन तपासा.")
