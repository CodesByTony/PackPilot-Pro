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

# --- THE DEFINITIVE CSS FIX ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
.stApp { color: #212529; } /* Default text color is dark */
[data-testid="stSidebar"] { display: none; }
.main .block-container { max-width: 900px; margin: 0 auto; padding-top: 5vh; }

/* Title Styling */
.title-container { text-align: center; margin-bottom: 2.5rem; }
.title-container .title { font-size: 5.5rem; font-weight: 700; color: #2c3e50; letter-spacing: -4px; margin: 0; padding: 0; }
.title-container .title sup { font-size: 2.2rem; font-weight: 600; color: #FF4500; top: -2.8rem; position: relative; left: 5px; }
.title-container .tagline { font-size: 1.5rem; color: #555; margin-top: 0.5rem; }

/* Card Styling */
.card { background-color: rgba(255, 255, 255, 0.98); backdrop-filter: blur(12px); border-radius: 16px; padding: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.07); border: 1px solid #EAEAEA; }

/* FIX ALL TEXT COLORS */
[data-testid="stFileUploader"] label, 
[data-testid="stTextArea"] label, 
[data-testid="stTextInput"] label, 
[data-testid="stSelectbox"] label,
[data-testid="stCheckbox"] label,
.uploadedFileName { 
    color: #333 !important; 
    font-weight: 600;
}
.uploadedFileName {
    font-size: 0.9rem;
}

/* Primary "Generate" Button */
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
    matches = re.findall(r'^\s*([^:]+?)\s*:\s*(.*)$', output, re.MULTILINE)
    for key, value in matches:
        data[key.strip()] = value.strip()
    return data

@st.cache_data
def generate_app_icon(app_name):
    # This is the APP-SPECIFIC icon generator you wanted
    width, height = 256, 256
    img = Image.new('RGB', (width, height), (245, 245, 245))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 100)
    except IOError:
        font = ImageFont.load_default()
    
    words = app_name.split()
    initials = "".join([word[0] for word in words[:2]]).upper() if words else "X"
    
    bbox = draw.textbbox((0,0), initials, font=font)
    text_width = bbox[2] - bbox[0]; text_height = bbox[3] - bbox[1]
    x = (width - text_width) / 2; y = (height - text_height) / 2
    
    draw.text((x, y), initials, font=font, fill="#FF4500")
    return img

# --- Main Application UI ---
st.markdown("""
<div class="title-container">
    <h1 class="title">PackPilot<sup>pro</sup></h1>
    <p class="tagline">The Intelligent Packaging Copilot for Hugo Boss</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # NEW MULTI-FILE UPLOADER
    uploaded_files = st.file_uploader("1. Upload All Package Files (Installer, Docs, etc.)", 
                                      type=['exe', 'msi', 'pdf', 'txt', 'zip'], 
                                      accept_multiple_files=True, 
                                      key="multi_uploader")
    
    ps_output_text = st.text_area("2. Paste Output from readData.ps1", 
                                  height=150, 
                                  key="ps_output",
                                  help="Run the installer in a Sandbox, execute readData.ps1, and paste the output here.")

    primary_installer = None
    if uploaded_files:
        # Automatically find the primary installer
        installers = [f for f in uploaded_files if f.name.endswith(('.exe', '.msi'))]
        if installers:
            primary_installer = installers[0]
            st.success(f"Primary installer identified: **{primary_installer.name}**")
        else:
            st.warning("No .exe or .msi file found in the upload. Please include the primary installer.")

    # The Generate button now appears correctly
    if primary_installer and ps_output_text:
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
                "uploaded_filename": primary_installer.name,
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

        tab1, tab2, tab3 = st.tabs(["📋 General Information", "⚙️ Configuration", "🔍 Detection Rules"])
        with tab1:
            st.text_input("App Name", value=data['app_name'], disabled=True, key="disp_app_name")
            st.text_input("Vendor", value=data['vendor'], disabled=True, key="disp_vendor")
            st.text_area("Description (AI Generated)", value=description, height=100, disabled=True, key="disp_desc")
            
            # THE APP-SPECIFIC ICON GENERATOR, REINSTATED
            st.subheader("Generated App Icon", anchor=False)
            generated_icon = generate_app_icon(data['app_name'])
            st.image(generated_icon, width=128)
            buf = io.BytesIO()
            generated_icon.save(buf, format="PNG")
            st.download_button("Download Icon (.png)", buf.getvalue(), f"{data['app_name'].replace(' ', '_')}_icon.png", "image/png", use_container_width=True)

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
    # Important: Reset the state so the results don't persist on refresh
    if 'generate' in st.session_state:
        del st.session_state['generate']
