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
        with open(file_path, "rb") as f: data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError: return None

def set_background(image_file):
    base64_img = get_base64_of_image(image_file)
    if base64_img:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{base64_img}");
                background-size: cover; background-repeat: no-repeat; background-attachment: fixed;
            }}
            </style>""", unsafe_allow_html=True)

# --- Custom CSS for the Professional White & Orange Theme ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
.stApp { color: #212529; }
[data-testid="stSidebar"] { display: none; }
.main .block-container { max-width: 900px; margin: 0 auto; padding-top: 5vh; }
.title-container { text-align: center; margin-bottom: 2.5rem; }
.title-container .title { font-size: 5.5rem; font-weight: 700; color: #2c3e50; letter-spacing: -4px; margin: 0; padding: 0; }
.title-container .title sup { font-size: 2.2rem; font-weight: 600; color: #FF4500; top: -2.8rem; position: relative; left: 5px; }
.title-container .tagline { font-size: 1.5rem; color: #555; margin-top: 0.5rem; }
.card { background-color: rgba(255, 255, 255, 0.98); backdrop-filter: blur(12px); border-radius: 16px; padding: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.07); border: 1px solid #EAEAEA; }
[data-testid="stFileUploader"] label { font-size: 1.1rem !important; font-weight: 600 !important; color: #333 !important; }
[data-testid="stFileUploader"] button { border-color: #FF4500; background-color: white; color: #FF4500; }
[data-testid="stTextArea"] label, [data-testid="stTextInput"] label, [data-testid="stSelectbox"] label { color: #333 !important; font-weight: 600;}
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
def generate_description_from_api(app_name, vendor):
    try:
        prompt = f"Write a concise, professional, 2-sentence description for the software '{app_name}' from vendor '{vendor}'. The description is for an enterprise software catalog. Focus on its primary function."
        # Using a free, public API for the LLM
        response = requests.post("https://api.deepinfra.com/v1/openai/chat/completions", json={
            "model": "meta-llama/Llama-2-7b-chat-hf",
            "messages": [{"role": "user", "content": prompt}], "max_tokens": 80
        })
        response.raise_for_status()
        description = response.json()['choices'][0]['message']['content'].replace("\"", "").strip()
        return description
    except Exception:
        return f"{app_name} is a utility from {vendor} designed to enhance productivity and streamline workflows."

def parse_ps_output(output):
    data = {}
    # Regex to find key-value pairs separated by a colon
    matches = re.findall(r'^\s*([^:]+?)\s*:\s*(.*)$', output, re.MULTILINE)
    for key, value in matches:
        data[key.strip()] = value.strip()
    return data

@st.cache_data
def generate_packpilot_icon(text):
    width, height = 256, 256
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    try:
        font_main = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
        font_pro = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    except IOError:
        font_main = ImageFont.load_default(); font_pro = ImageFont.load_default()
    main_text = "packpilot"; pro_text = "pro"
    main_bbox = draw.textbbox((0,0), main_text, font=font_main)
    main_width = main_bbox[2] - main_bbox[0]; main_height = main_bbox[3] - main_bbox[1]
    main_x = (width - main_width) / 2; main_y = (height - main_height) / 2 + 10
    pro_bbox = draw.textbbox((0,0), pro_text, font=font_pro)
    pro_x = main_x + main_width + 5; pro_y = main_y - (pro_bbox[3] - pro_bbox[1]) + 5
    draw.text((main_x, main_y), main_text, font=font_main, fill="#FF4500", stroke_width=3, stroke_fill="black")
    draw.text((pro_x, pro_y), pro_text, font=font_pro, fill="#FF4500", stroke_width=2, stroke_fill="black")
    return img

# --- Main Application UI ---
st.markdown("""
<div class="title-container">
    <h1 class="title">PackPilot<sup>pro</sup></h1>
    <p class="tagline">Software Packaging & Deployment for Hugo Boss</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        uploaded_file = st.file_uploader("1. Upload Primary Installer", type=['exe', 'msi'], key="uploader")
    with c2:
        ps_output_text = st.text_area("2. Paste Output from readData.ps1", height=155, key="ps_output")

    if uploaded_file and ps_output_text:
        st.divider()
        st.subheader("3. Verify Auto-Filled Details", anchor=False)
        
        parsed_data = parse_ps_output(ps_output_text)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            app_name = st.text_input("Application Name", value=parsed_data.get('AppName', ''), key="app_name_input")
        with col2:
            vendor = st.text_input("Vendor", value=parsed_data.get('Publisher', ''), key="vendor_input")
        with col3:
            version = st.text_input("Version", value=parsed_data.get('Version', ''), key="version_input")
        
        is_interactive = st.checkbox("Installer requires user interaction (Use ServiceUI trick)", key="interactive_cb")
        if is_interactive:
            installer_type_key = "interactive"
        else:
            installer_type_key = st.selectbox("Installer Type", options=['exe_nsis', 'exe_inno', 'msi'], format_func=lambda x: RULES[x]['installer_type'], key="type_select")
            
        if st.button("🚀 Generate Recipe", use_container_width=True, type="primary", key="generate_btn"):
            st.session_state.generate = True
            st.session_state.recipe_data = {
                "app_name": app_name, "vendor": vendor, "version": version,
                "installer_type_key": installer_type_key,
                "uploaded_filename": uploaded_file.name,
                "apps_and_features_name": parsed_data.get('AppsAndFeaturesName', app_name),
                "architecture": parsed_data.get('Architecture', '64-bit'),
                "install_context": parsed_data.get('InstallContext', 'System'),
            }

    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get('generate', False):
    data = st.session_state.recipe_data
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Deployment Recipe", anchor=False)
        
        recipe_rules = RULES[data['installer_type_key']]
        description = generate_description_from_api(data['app_name'], data['vendor'])

        tab1, tab2, tab3 = st.tabs(["📋 General Info", "⚙️ Configuration", "🔍 Detection Rules"])
        with tab1:
            st.text_input("App Name", value=data['app_name'], disabled=True, key="disp_app_name")
            st.text_input("Vendor", value=data['vendor'], disabled=True, key="disp_vendor")
            st.text_area("Description (AI Generated)", value=description, height=100, disabled=True, key="disp_desc")
            st.image(generate_packpilot_icon(data['app_name']), caption="Custom App Icon", width=128)
        with tab2:
            install_cmd = recipe_rules['install_command'].format(filename=data['uploaded_filename'])
            uninstall_cmd = recipe_rules['uninstall_command'].format(app_name=data['app_name'], product_code="{YOUR_PRODUCT_CODE}")
            st.text_input("Install Context", value=data['install_context'], disabled=True, key="disp_context")
            st.text_input("Architecture", value=data['architecture'], disabled=True, key="disp_arch")
            st.text_input("Apps & Features Name", value=data['apps_and_features_name'], disabled=True, key="disp_app_features")
            st.code(install_cmd, language='powershell')
        with tab3:
            st.info(f"**Recommended Method:** {recipe_rules['detection_method']}")
            st.code("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
            st.code("HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')

        st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.generate = False
