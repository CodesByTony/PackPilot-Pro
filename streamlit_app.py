import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import json
import io
import base64
import re
import requests
import yaml

# --- Page Configuration ---
# Setting the overall page properties.
st.set_page_config(page_title="PackPilot Pro", layout="wide", initial_sidebar_state="collapsed")

# --- Custom Styling (The $100k Makeover) ---
# This is a large block of CSS to completely override Streamlit's default look and feel.
# It implements the white/orange theme, fixes all text color bugs, and creates the professional layout.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

/* --- Global Settings --- */
html, body, [class*="st-"], .st-emotion-cache-16idsys p {
    font-family: 'Inter', sans-serif;
    color: #212529; /* Default text is now black */
}
[data-testid="stSidebar"] { display: none; } /* Hide the sidebar completely */
.main .block-container { max-width: 900px; margin: 0 auto; padding-top: 5vh; }

/* --- Title & Header --- */
.title-container { text-align: center; margin-bottom: 2.5rem; }
.title-container .title { font-size: 5.5rem; font-weight: 700; color: #2c3e50; letter-spacing: -4px; margin: 0; padding: 0; }
.title-container .title sup { font-size: 2.2rem; font-weight: 600; color: #FF4500; top: -2.8rem; position: relative; left: 5px; }
.title-container .tagline { font-size: 1.5rem; color: #555; margin-top: 0.5rem; }

/* --- Card Styling with Orange Theme --- */
.card {
    background-color: #FFF5E6; /* Light, creamy orange background */
    border: 2px solid #FFA500; /* Main orange border */
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.07);
}

/* --- FIX ALL TEXT & ELEMENT COLORS --- */
.uploadedFileName, .st-emotion-cache-16idsys p { color: #212529 !important; }
[data-testid="stFileUploader"] label, [data-testid="stTextArea"] label,
[data-testid="stTextInput"] label, [data-testid="stSelectbox"] label,
[data-testid="stCheckbox"] label { color: #212529 !important; font-weight: 600; }
[data-baseweb="tab"] { font-size: 1.2rem !important; font-weight: 600 !important; color: #212529 !important; }

/* --- Dark Elements Text Fix --- */
[data-testid="stTextArea"] textarea, pre, code {
    background-color: #2B2B2B !important;
    color: #FFFFFF !important; /* White text for all dark boxes */
}

/* --- Button Styling & Differentiation --- */
/* Primary Button (Generate Recipe) */
.stButton>button[kind="primary"] {
    font-weight: 600; border-radius: 8px; padding: 0.75rem 1.5rem; border: none;
    background-image: linear-gradient(to right, #FF4500 0%, #FFA500 100%);
    color: white !important;
}
/* Secondary Buttons (Parse Data, Download) */
.stButton>button[kind="secondary"], .stDownloadButton>button {
    font-weight: 600; border-radius: 8px; padding: 0.75rem 1.5rem;
    border: 2px solid #FF4500 !important;
    background-color: #FFFFFF !important;
    color: #FF4500 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Function to apply the user's custom background image ---
@st.cache_data
def get_base64_of_image(file_path):
    try:
        with open(file_path, "rb") as f: data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError: return None

def set_background(image_file):
    base64_img = get_base64_of_image(image_file)
    if base64_img:
        st.markdown(f'<style>.stApp {{ background-image: url("data:image/png;base64,{base64_img}"); background-size: cover; }}</style>', unsafe_allow_html=True)

# --- Core Application Logic & Helper Functions ---
@st.cache_data
def load_rules():
    try:
        with open('rules.json', 'r') as f: return json.load(f)
    except FileNotFoundError: st.error("Fatal Error: `rules.json` not found."); st.stop()
RULES = load_rules()

@st.cache_data
def get_info_from_winget(app_name):
    """Searches the Microsoft Winget DB for an official, professional description."""
    try:
        search_term = app_name.split(' (')[0]
        search_url = f"https://api.github.com/search/code?q={search_term}+in:path+repo:microsoft/winget-pkgs"
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        items = response.json().get('items', [])
        if not items: return f"{app_name} is a versatile utility designed to enhance productivity."
        manifest_url = items[0]['html_url'].replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        manifest_response = requests.get(manifest_url)
        manifest_response.raise_for_status()
        manifest_data = yaml.safe_load(manifest_response.text)
        description = manifest_data.get('Description', manifest_data.get('ShortDescription', ''))
        return description.strip() if description else f"{app_name} is a widely-used application."
    except Exception: return f"{app_name} is a versatile utility designed to enhance productivity."

def parse_ps_output(output):
    data = {}
    matches = re.findall(r'^\s*([^:]+?)\s*:\s*(.*)$', output, re.MULTILINE)
    for key, value in matches: data[key.strip()] = value.strip()
    return data

@st.cache_data
def generate_professional_icon(app_name):
    """Creates a unique, professional icon for the specific app."""
    width, height = 256, 256
    top_color = (255, 120, 0); bottom_color = (255, 69, 0)
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / height)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * y / height)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    try: font = ImageFont.truetype("DejaVuSans-Bold.ttf", 100)
    except IOError: font = ImageFont.load_default()
    words = re.findall(r'[A-Z][a-z]*|\d+', app_name) or [app_name]
    initials = "".join([word[0] for word in words[:2]]).upper()
    if not initials: initials = app_name[:2].upper() if len(app_name) > 1 else app_name[0].upper()
    bbox = draw.textbbox((0,0), initials, font=font)
    text_width = bbox[2] - bbox[0]; text_height = bbox[3] - bbox[1]
    x = (width - text_width) / 2; y = (height - text_height) / 2
    draw.text((x, y), initials, font=font, fill="#FFFFFF")
    return img

# --- Main Application UI ---
set_background('Generated.png') # Make sure this file is in your GitHub repo!

st.markdown("""
<div class="title-container">
    <h1 class="title">PackPilot<sup>pro</sup></h1>
    <p class="tagline">The Intelligent Packaging Copilot for Hugo Boss</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("1. Upload All Package Files", accept_multiple_files=True, key="multi_uploader")
    
    primary_installer = None
    if uploaded_files:
        installers = [f for f in uploaded_files if f.name.endswith(('.exe', '.msi'))]
        if installers:
            primary_installer = installers[0]
            st.success(f"Primary installer identified: **{primary_installer.name}**")

    ps_output_text = st.text_area("2. Paste Output from readData.ps1", height=155, key="ps_output")
    
    parse_col, _ = st.columns([1, 2])
    with parse_col:
        if st.button("Parse Data from Script", key="parse_btn", type="secondary"): # Secondary button type
            if ps_output_text:
                st.session_state.parsed_data = parse_ps_output(ps_output_text)
                st.success("Data parsed successfully!")
            else:
                st.error("Please paste the script output into the text area.")

    if primary_installer and 'parsed_data' in st.session_state and st.session_state.parsed_data:
        st.divider()
        st.subheader("3. Verify Auto-Filled Details", anchor=False)
        
        data = st.session_state.parsed_data
        app_name = st.text_input("Application Name", value=data.get('AppName', ''), key="app_name_input")
        vendor = st.text_input("Vendor", value=data.get('Publisher', ''), key="vendor_input")
        version = st.text_input("Version", value=data.get('Version', ''), key="version_input")
        is_interactive = st.checkbox("Installer requires user interaction (Use ServiceUI trick)", key="interactive_cb")
        
        if is_interactive: installer_type_key = "interactive"
        else: installer_type_key = st.selectbox("Installer Type", options=['exe_nsis', 'exe_inno', 'msi'], format_func=lambda x: RULES[x]['installer_type'], key="type_select")
            
        if st.button("🚀 Generate Recipe", use_container_width=True, type="primary", key="generate_btn"):
            st.session_state.generate = True
            st.session_state.recipe_data = { "app_name": app_name, "vendor": vendor, "version": version, "installer_type_key": installer_type_key, "uploaded_filename": primary_installer.name, "apps_and_features_name": data.get('AppsAndFeaturesName', app_name), "architecture": data.get('Architecture', '64-bit'), "install_context": data.get('InstallContext', 'System'), }
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get('generate', False):
    data = st.session_state.recipe_data
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Deployment Recipe", anchor=False)
        recipe_rules = RULES[data['installer_type_key']]
        description = get_info_from_winget(data['app_name'])
        tab1, tab2, tab3 = st.tabs(["📋 General Information", "⚙️ Configuration", "🔍 Detection Rules"])
        with tab1:
            st.text_input("App Name", value=data['app_name'], disabled=True, key="disp_app_name")
            st.text_input("Vendor", value=data['vendor'], disabled=True, key="disp_vendor")
            st.text_area("Description (from Winget)", value=description, height=120, disabled=True, key="disp_desc")
            st.subheader("Generated App Icon", anchor=False)
            generated_icon = generate_professional_icon(data['app_name'])
            st.image(generated_icon, width=128)
            buf = io.BytesIO()
            generated_icon.save(buf, format="PNG")
            st.download_button("Download Icon (.png)", buf.getvalue(), f"{data['app_name'].replace(' ', '_')}_icon.png", type="secondary") # Secondary button type
        with tab2:
            st.text_input("Install Context", value=data['install_context'], disabled=True, key="disp_context")
            st.text_input("Architecture", value=data['architecture'], disabled=True, key="disp_arch")
            st.text_input("Apps & Features Name", value=data['apps_and_features_name'], disabled=True, key="disp_app_features")
            # This is the line with the critical KeyError fix
            install_cmd = recipe_rules['install_command'].format(filename=data['uploaded_filename'])
            st.code(install_cmd, language='powershell')
        with tab3:
            st.info(f"Recommended Method: {recipe_rules['detection_method']}")
            st.code("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
            st.code("HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
        st.markdown('</div>', unsafe_allow_html=True)
    if 'generate' in st.session_state: del st.session_state['generate']
