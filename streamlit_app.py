import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import json
import io
import base64

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="PackPilot Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Function to load and encode YOUR background image from the repository ---
@st.cache_data
def get_base64_of_image(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"Background image '{file_path}' not found. Please ensure it's uploaded to the GitHub repository.")
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
/* --- Font & General --- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    color: #0d1117; /* Dark text for readability */
}

/* --- HIDE THE UNWANTED SIDEBAR --- */
[data-testid="stSidebar"] {
    display: none;
}

/* --- Top-Right Navigation Header --- */
.header {
    position: fixed;
    top: 0;
    right: 0;
    padding: 1rem 2rem;
    z-index: 999;
}
.header .stButton>button {
    background-color: transparent;
    border: 1px solid #d0d0d0;
    color: #505050;
    font-weight: 600;
    border-radius: 8px;
}
.header .stButton>button:hover {
    background-color: #f0f0f0;
    border-color: #a0a0a0;
}
.header .stButton>button:disabled {
    color: #aaa;
}

/* --- Main Content Centering --- */
.main .block-container {
    max-width: 900px;
    margin: 0 auto;
    padding-top: 10vh; /* Push content down from the top */
}

/* --- BIGGER Title & Tagline --- */
.title-container {
    text-align: center;
    margin-bottom: 2.5rem;
}
.title-container .title {
    font-size: 5.5rem; /* Increased size */
    font-weight: 700;
    color: #2c3e50;
    letter-spacing: -4px;
    margin: 0;
}
.title-container .title sup {
    font-size: 2rem; /* Increased size */
    font-weight: 600;
    color: #FF4500;
    top: -2.5rem; /* Adjust position */
}
.title-container .tagline {
    font-size: 1.5rem; /* Increased size */
    color: #555;
    margin-top: 0.5rem;
}

/* --- Card Styling --- */
.card {
    background-color: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.07);
    border: 1px solid #EAEAEA;
}

/* --- FIX UPLOADER BUTTON TEXT COLOR --- */
[data-testid="stFileUploader"] label {
    font-weight: 600;
    color: #333 !important; /* Make label text dark */
}
[data-testid="stFileUploader"] button {
    border-color: #FF4500;
    background-color: white;
    color: #FF4500; /* Make button text orange */
}
[data-testid="stFileUploader"] button:hover {
    border-color: #FF4500;
    background-color: #FFF9F0;
    color: #FF4500;
}

/* --- Primary "Generate" Button --- */
.stButton>button.primary-button {
    font-weight: 600;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    border: none;
    background-image: linear-gradient(to right, #FF4500 0%, #FFA500 100%);
    color: white;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255, 69, 0, 0.2);
}
.stButton>button.primary-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 69, 0, 0.3);
}

</style>
""", unsafe_allow_html=True)

# --- Load Your Background Image ---
set_background('Generated.png') # This must match the filename on GitHub EXACTLY

# --- Load Rules (The "Brain") ---
@st.cache_data
def load_rules():
    try:
        with open('rules.json', 'r') as f: return json.load(f)
    except FileNotFoundError:
        st.error("Fatal Error: `rules.json` not found."); st.stop()
RULES = load_rules()

# --- UI Helper Functions ---
def display_recipe_card(title, content, language='powershell'):
    st.subheader(title, divider='orange')
    st.code(content, language=language)

# --- Header Section (Top Right Buttons) ---
with st.container():
    st.markdown('<div class="header">', unsafe_allow_html=True)
    cols = st.columns([1, 1])
    with cols[0]:
        st.button("📄 View Recipes", disabled=True, use_container_width=True, key="nav1")
    with cols[1]:
        st.button("📊 View Dashboard", disabled=True, use_container_width=True, key="nav2")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main Title & Tagline ---
st.markdown("""
<div class="title-container">
    <h1 class="title">PackPilot<sup>pro</sup></h1>
    <p class="tagline">Software Packaging & Deployment for Hugo Boss</p>
</div>
""", unsafe_allow_html=True)

# Uploader & Inputs
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=['exe', 'msi'], label_visibility="collapsed")
    
    if uploaded_file:
        if 'app_name' not in st.session_state or st.session_state.get('uploaded_filename') != uploaded_file.name:
            st.session_state.app_name = uploaded_file.name.split('.')[0].replace('_', ' ').replace('-', ' ').title()
            st.session_state.vendor = "VendorName"
            st.session_state.version = "1.0.0"
            st.session_state.uploaded_filename = uploaded_file.name
        
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.app_name = st.text_input("Application Name", value=st.session_state.app_name)
        with col2:
            st.session_state.vendor = st.text_input("Vendor", value=st.session_state.vendor)
        with col3:
            st.session_state.version = st.text_input("Version", value=st.session_state.version)

        is_interactive = st.checkbox("Installer requires user interaction (Use ServiceUI trick)")
        if is_interactive:
            st.session_state.installer_type_key = "interactive"
        else:
            st.session_state.installer_type_key = st.selectbox("Installer Type", options=['exe_nsis', 'exe_inno', 'msi'], format_func=lambda x: RULES[x]['installer_type'])
            
        if st.button("🚀 Generate Recipe", use_container_width=True, type="primary"):
            st.session_state.generate = True
        
    else:
        st.session_state.generate = False
            
    st.markdown('</div>', unsafe_allow_html=True)

# Results Section
if st.session_state.get('generate', False):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Deployment Recipe", anchor=False)
        recipe = RULES[st.session_state.installer_type_key]
        
        tab1, tab2, tab3 = st.tabs(["📋 General Info", "⚙️ Commands", "🔍 Detection"])
        with tab1:
            st.text_input("App Name:", value=st.session_state.app_name, disabled=True, key="d_app")
            st.text_input("Vendor:", value=st.session_state.vendor, disabled=True, key="d_ven")
            st.text_input("Version:", value=st.session_state.version, disabled=True, key="d_ver")
        with tab2:
            install_cmd = recipe['install_command'].format(filename=uploaded_file.name)
            uninstall_cmd = recipe['uninstall_command'].format(app_name=st.session_state.app_name, product_code="{YOUR_PRODUCT_CODE}")
            display_recipe_card("Silent Install Command", install_cmd)
            display_recipe_card("Silent Uninstall Command", uninstall_cmd)
        with tab3:
            st.info(f"**Recommended Method:** {recipe['detection_method']}")
            display_recipe_card("Registry Path (64-bit Apps)", "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
            display_recipe_card("Registry Path (32-bit Apps on 64-bit OS)", "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')

        st.markdown('</div>', unsafe_allow_html=True)
