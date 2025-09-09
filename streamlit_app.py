import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import json
import io
import base64
import re
import requests

# --- Page Configuration ---
st.set_page_config(page_title="PackPilot Pro", layout="wide", initial_sidebar_state="collapsed")

# --- Function to load and encode YOUR background image from the repository ---
@st.cache_data
def get_base64_of_image(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def set_background(image_file):
    base64_img = get_base64_of_image(image_file)
    if base64_img:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{base64_img}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# --- Custom CSS for the Professional White & Orange Theme ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
.stApp { color: #0d1117; }
[data-testid="stSidebar"] { display: none; }
.main .block-container { max-width: 900px; margin: 0 auto; padding-top: 5vh; }

.title-container { text-align: center; margin-bottom: 2.5rem; }
.title-container .title { font-size: 5.5rem; font-weight: 700; color: #2c3e50; letter-spacing: -4px; margin: 0; padding: 0; }
.title-container .title sup { font-size: 2.2rem; font-weight: 600; color: #FF4500; top: -2.8rem; position: relative; left: 5px; }
.title-container .tagline { font-size: 1.5rem; color: #555; margin-top: 0.5rem; }

.card { background-color: rgba(255, 255, 255, 0.98); backdrop-filter: blur(12px); border-radius: 16px; padding: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.07); border: 1px solid #EAEAEA; }
[data-testid="stFileUploader"] label { font-size: 1.1rem !important; font-weight: 600 !important; color: #333 !important; }
[data-testid="stFileUploader"] button { border-color: #FF4500; background-color: white; color: #FF4500; }
[data-testid="stFileUploader"] button:hover { border-color: #FF4500; background-color: #FFF9F0; color: #FF4500; }

.stButton>button { font-weight: 600; border-radius: 8px; padding: 0.75rem 1.5rem; border: none; background-image: linear-gradient(to right, #FF4500 0%, #FFA500 100%); color: white; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(255, 69, 0, 0.2); }
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 69, 0, 0.3); }
</style>
""", unsafe_allow_html=True)

# --- Load Your Background Image ---
set_background('Generated.png')

# --- Load Rules & Helper Functions ---
@st.cache_data
def load_rules():
    try:
        with open('rules.json', 'r') as f: return json.load(f)
    except FileNotFoundError: st.error("Fatal Error: `rules.json` not found."); st.stop()
RULES = load_rules()

@st.cache_data
def generate_description(app_name, vendor):
    """Uses a free LLM API to generate a professional description."""
    try:
        prompt = f"Write a concise, professional, 2-sentence description for the software '{app_name}' from vendor '{vendor}'. The description is for an enterprise software catalog. Focus on its primary function."
        response = requests.post("https://api.deepinfra.com/v1/openai/chat/completions", json={
            "model": "meta-llama/Llama-2-7b-chat-hf",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 80
        })
        response.raise_for_status()
        description = response.json()['choices'][0]['message']['content']
        # Clean up the response
        description = description.replace("\"", "").strip()
        return description
    except Exception as e:
        return f"A versatile application, '{app_name}' from {vendor} helps users accomplish key tasks with efficiency."

def parse_ps_output(output):
    """Parses the key-value output from the readData.ps1 script."""
    data = {}
    lines = output.strip().split('\n')
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            data[key] = value
    return data

# --- Main Application UI ---
st.markdown("""
<div class="title-container">
    <h1 class="title">PackPilot<sup>pro</sup></h1>
    <p class="tagline">Software Packaging & Deployment for Hugo Boss</p>
</div>
""", unsafe_allow_html=True)

# --- Uploader & Inputs Section ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("1. Upload Primary Installer", type=['exe', 'msi'])
    with col2:
        ps_output_text = st.text_area("2. Paste Output from readData.ps1", height=150, placeholder="AppName             : 7-Zip 24.05 (x64)\nPublisher           : Igor Pavlov\nArchitecture        : 64-bit\n...")

    # Initialize session state for holding parsed data
    if 'parsed_data' not in st.session_state:
        st.session_state.parsed_data = {}

    if ps_output_text:
        st.session_state.parsed_data = parse_ps_output(ps_output_text)
    
    if uploaded_file:
        st.divider()
        st.subheader("3. Verify Details & Generate Recipe", anchor=False)
        
        # Use parsed data if available, otherwise use defaults
        app_name_default = st.session_state.parsed_data.get('AppName', uploaded_file.name.split('.')[0].replace('_', ' ').replace('-', ' ').title())
        vendor_default = st.session_state.parsed_data.get('Publisher', "VendorName")
        version_default = st.session_state.parsed_data.get('Version', "1.0.0")
        arch_default_index = 0 if st.session_state.parsed_data.get('Architecture', '64-bit') == '64-bit' else 1
        
        c1, c2, c3 = st.columns(3)
        with c1:
            app_name = st.text_input("Application Name", value=app_name_default)
        with c2:
            vendor = st.text_input("Vendor", value=vendor_default)
        with c3:
            version = st.text_input("Version", value=version_default)
        
        is_interactive = st.checkbox("Installer requires user interaction (Use ServiceUI trick)")
        if is_interactive:
            installer_type_key = "interactive"
        else:
            installer_type_key = st.selectbox("Installer Type (for silent command suggestion)", options=['exe_nsis', 'exe_inno', 'msi'], format_func=lambda x: RULES[x]['installer_type'])
            
        if st.button("🚀 Generate Recipe", use_container_width=True, type="primary"):
            st.session_state.generate = True
            st.session_state.recipe_data = {
                "app_name": app_name,
                "vendor": vendor,
                "version": version,
                "installer_type_key": installer_type_key,
                "uploaded_filename": uploaded_file.name,
                "apps_and_features_name": st.session_state.parsed_data.get('AppsAndFeaturesName', app_name),
                "architecture": st.session_state.parsed_data.get('Architecture', '64-bit'),
                "install_context": st.session_state.parsed_data.get('InstallContext', 'System'),
                "conflicting_processes": st.session_state.parsed_data.get('PotentialConflictingProcesses', 'N/A')
            }

    st.markdown('</div>', unsafe_allow_html=True)

# --- Results Section ---
if st.session_state.get('generate', False):
    data = st.session_state.recipe_data
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Deployment Recipe", anchor=False)
        
        recipe_rules = RULES[data['installer_type_key']]
        description = generate_description(data['app_name'], data['vendor'])

        tab1, tab2, tab3 = st.tabs(["📋 General Information", "⚙️ Configuration", "🔍 Detection Rules"])
        with tab1:
            st.text_input("App Name", value=data['app_name'], disabled=True)
            st.text_input("Vendor", value=data['vendor'], disabled=True)
            st.text_area("Description (AI Generated)", value=description, height=100)
            # Icon generation is removed for brevity, assuming you will generate one separately
        with tab2:
            install_cmd = recipe_rules['install_command'].format(filename=data['uploaded_filename'])
            uninstall_cmd = recipe_rules['uninstall_command'].format(app_name=data['app_name'], product_code="{YOUR_PRODUCT_CODE}")
            
            st.text_input("Install Context", value=data['install_context'], disabled=True)
            st.text_input("Architecture", value=data['architecture'], disabled=True)
            st.text_input("Apps & Features Name", value=data['apps_and_features_name'], disabled=True)
            st.code(install_cmd, language='powershell')
        with tab3:
            st.info(f"**Recommended Method:** {recipe_rules['detection_method']}")
            st.code("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
            st.code("HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')

        st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.generate = False
