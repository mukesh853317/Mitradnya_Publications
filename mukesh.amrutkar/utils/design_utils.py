import streamlit as st

def apply_premium_design():
    """
    ही फंक्शन सर्व पेजेसवर प्रीमियम आणि प्रोफेशनल थीम (CSS) लागू करण्यासाठी आहे.
    Mitradnya Publications च्या सर्व पोर्टल फाइल्समध्ये (student, admin, parent) 
    याचा वापर करता येईल.
    """
    st.markdown("""
    <style>
    /* डॅशबोर्डचे मुख्य हेडर */
    .main-title {
        color: #1e3a8a;
        font-size: 36px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #4b5563;
        font-size: 18px;
        text-align: center;
        margin-bottom: 25px;
        font-weight: 500;
    }
    /* ट्रायल बॅलन्स टेबलसाठी मॉडर्न लूक */
    .acc-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-radius: 8px;
        overflow: hidden;
    }
    .acc-table th {
        background-color: #2563eb; /* सुंदर निळा रंग */
        color: white;
        font-weight: bold;
        padding: 12px 15px;
        text-align: center;
        border: 1px solid #1d4ed8;
    }
    .acc-table td {
        padding: 10px 15px;
        border: 1px solid #e5e7eb;
        color: #1f2937;
    }
    /* टेबलच्या ओळींना आकर्षक बनवण्यासाठी Zebra Striping */
    .acc-table tr:nth-child(even) {
        background-color: #f8fafc;
    }
    .acc-table tr:hover {
        background-color: #e2e8f0; /* माउस नेल्यावर रंग बदलेल */
    }
    /* एक्सपँडरच्या मजकुरासाठी */
    .question-text {
        font-size: 16px;
        line-height: 1.6;
        color: #374151;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
