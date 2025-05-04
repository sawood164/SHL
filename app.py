import streamlit as st
import pandas as pd
from google.generativeai import configure, GenerativeModel
import base64
import io
import html

# Load SHL catalog
df_catalog = pd.read_csv("shl_assessment_catalog.csv")

# Gemini API Configuration - Directly using the provided API key
GEMINI_API_KEY = "AIzaSyC7OUgPJXHPljqSVnK0TSqXKGZkzobDG8Q"

configure(
    api_key=GEMINI_API_KEY,
    transport="rest"
)

# Gemini Model
model = GenerativeModel(
    model_name="models/gemini-1.5-pro-latest",
    generation_config={"temperature": 0.7}
)

# Generate recommendation prompt
def get_recommendations(query, df, top_k=3):
    context = "\n".join([
        f"{row['Assessment Name']} - {row['Test Type']} - {row['Duration']} - Remote: {row['Remote Testing Support']} - Adaptive: {row['Adaptive/IRT Support']}"
        for _, row in df.iterrows()
    ])
    prompt = f"""
    Based on the following assessment catalog:
    {context}
    Recommend the top {top_k} most relevant SHL assessments for the following query:
    "{query}"
    Return a table with these columns:
    Assessment Name, Assessment URL, Remote Testing Support, Adaptive/IRT Support, Duration, Test Type
    """
    response = model.generate_content(prompt)
    return response.text

# --- UI/UX ENHANCEMENTS ---
# Set page config
st.set_page_config(page_title="SHL Assessment Recommender", layout="wide", page_icon="🧠")

# Google Fonts (Inter)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"]  {
        font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SHL LOGO CENTERED ---
# (Logo removed as per user request)

# --- TITLE & SUBTITLE ---
title_color = "#fff"
subtitle_color = "#fda085"

st.markdown(f'''
<h1 style="text-align:center;font-weight:800;letter-spacing:1px;margin-bottom:0.2rem;
    color:{title_color}; 
    text-shadow: 2px 2px 8px rgba(253,160,133,0.18);">
    SHL Assessment Recommendation Engine
</h1>''', unsafe_allow_html=True)
st.markdown(f'''
<div style="text-align:center;font-size:24px;color:{subtitle_color};font-weight:700;margin-bottom:1.5rem;">
    AI-powered, beautiful, and professional assessment suggestions for your hiring needs
</div>''', unsafe_allow_html=True)

# --- NIGHT MODE STYLING ONLY ---
st.markdown("""
<style>
    body, .main {
        background: linear-gradient(120deg, #232526 0%, #414345 100%);
        color: #f1f1f1;
    }
    .main, .stTextArea textarea, .stButton>button, .box, .card {
        background: #232526 !important;
        color: #f1f1f1 !important;
    }
    .box {
        background: rgba(40, 44, 52, 0.95) !important;
        box-shadow: 0px 8px 32px rgba(0,0,0,0.25);
    }
    .card {
        background: #232526 !important;
        border: 1.5px solid #fda085;
    }
    .stButton>button {
        background: linear-gradient(90deg, #232526 0%, #fda085 100%) !important;
        color: #fff !important;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #fda085 0%, #232526 100%) !important;
        color: #fff !important;
    }
    .footer {
        color: #f1f1f1 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ABOUT SECTION ---
about_text_color = "#fff"
about_heading_color = "#fda085"
creator_color = "#00e676"
with st.sidebar:
    st.markdown(f"""
    <h2 style='color:{about_heading_color};'>About</h2>
    <p style='font-size:16px;color:{about_text_color};'>
    <b>SHL Assessment Recommendation Engine</b> is an AI-powered tool that recommends the best SHL assessments for your job descriptions or hiring queries.<br><br>
    <b style='color:#ff7e5f;'>Features:</b><br>
    - Natural language input<br>
    - Gemini AI-powered recommendations<br>
    - Beautiful, modern UI<br>
    - Night mode only<br><br>
    <b style='color:{creator_color};'>Created by Md Sawood Alam</b>
    </p>
    <hr>
    <p style='font-size:14px;color:{about_text_color};'>For queries, contact: <a href='mailto:md.sawood.alam@gmail.com' style='color:{about_heading_color};'>md.sawood.alam@gmail.com</a></p>
    """, unsafe_allow_html=True)

# --- MAIN INPUT & RESULTS ---
st.markdown('<div class="box">', unsafe_allow_html=True)
# Enhanced input label for visibility
st.markdown('<label style="font-size:18px;font-weight:600;color:#ff7e5f;">💼 Enter job description or hiring query:</label>', unsafe_allow_html=True)

# Add selectbox for number of results
num_results = st.selectbox(
    "How many recommendations do you want?",
    options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    index=2,
    help="Select how many top recommendations to display (default is 3)"
)

query = st.text_area(" ", height=120, placeholder="e.g., Hiring Java developers with strong communication skills...", key="query_input")

recommendations_df = None
recommendations_raw = None

if st.button("✨ Get Smart Recommendations"):
    if query.strip():
        with st.spinner("⏳ Generating your custom SHL assessment plan..."):
            result = get_recommendations(query, df_catalog, top_k=num_results)
            recommendations_raw = result
            try:
                rows = [r for r in result.split('\n') if r.strip() and (',' in r or '|' in r)]
                if len(rows) > 1:
                    if '|' in rows[0]:
                        # Markdown table: show only top_k rows (header + top_k)
                        header = rows[0]
                        divider = rows[1] if rows[1].startswith('|') else ''
                        topk = rows[:num_results+2] if divider else [header] + rows[1:num_results+1]
                        st.markdown('\n'.join(topk), unsafe_allow_html=True)
                    else:
                        # CSV table: show only top_k rows
                        df = pd.read_csv(io.StringIO('\n'.join(rows)))
                        df = df.head(num_results)
                        for i, row in df.iterrows():
                            st.markdown(f'<div class="card"><b>Assessment Name:</b> {html.escape(str(row["Assessment Name"]))}<br>'
                                        f'<b>Test Type:</b> {html.escape(str(row["Test Type"]))}<br>'
                                        f'<b>Duration:</b> {html.escape(str(row["Duration"]))}<br>'
                                        f'<b>Remote Testing Support:</b> {html.escape(str(row["Remote Testing Support"]))}<br>'
                                        f'<b>Adaptive/IRT Support:</b> {html.escape(str(row["Adaptive/IRT Support"]))}<br>'
                                        f'<b>Assessment URL:</b> <a href="{html.escape(str(row["Assessment URL"]))}" target="_blank">Link</a></div>', unsafe_allow_html=True)
                else:
                    st.markdown(result, unsafe_allow_html=True)
            except Exception:
                st.markdown(result, unsafe_allow_html=True)
    else:
        st.warning("Please enter a query to proceed.")

# --- FOOTER ---
st.markdown('''
<style>
.footer-bottom {
    width: 100vw;
    background: transparent;
    text-align: center;
    font-size: 16px;
    color: #fda085;
    margin-top: 60px;
    font-weight: 600;
    letter-spacing: 1px;
    padding-bottom: 10px;
}
</style>
<div class="footer-bottom">⚡ SHL Assessment Recommendation Engine © 2025 | Created by Md Sawood Alam</div>
''', unsafe_allow_html=True)
