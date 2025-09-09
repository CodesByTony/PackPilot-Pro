import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import json
import io

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="PackPilot Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded" # Keep the sidebar open by default
)

# --- Custom CSS for the $100k Look ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# You could also put this in a separate css file
st.markdown("""
<style>
/* General Body and Font */
body {
    color: #EAEAEA;
    background-color: #0E1117;
}
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF;
}

/* Main App container */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 5rem;
    padding-right: 5rem;
}

/* Sidebar Styling */
.st-emotion-cache-16txtl3 {
    background-color: #1A1F2B;
    border-right: 1px solid #2D3748;
}

/* Input Widgets in Sidebar */
.st-emotion-cache-16txtl3 .stTextInput > div > div > input,
.st-emotion-cache-16txtl3 .stSelectbox > div > div > div {
    background-color: #2D3748;
    color: #EAEAEA;
    border: 1px solid #4A5568;
}

/* Button Styling */
.stButton>button {
    border-radius: 8px;
    border: 1px solid #4A90E2;
    color: #4A90E2;
    background-color: transparent;
    transition: all 0.2s ease-in-out;
}
.stButton>button:hover {
    border-color: #FFFFFF;
    color: #FFFFFF;
    background-color: #4A90E2;
    box-shadow: 0 0 15px rgba(74, 144, 226, 0.5);
}
.stButton>button:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px #2D3748, 0 0 0 4px #4A90E2 !important;
}

/* Recipe Card Styling */
.recipe-card {
    background-color: #1A1F2B;
    border-radius: 12px;
    padding: 25px;
    border: 1px solid #2D3748;
    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
}

/* Code block styling */
div[data-baseweb="block"] {
    background-color: #0E1117 !important;
    border: 1px solid #2D3748 !important;
}

</style>
""", unsafe_allow_html=True)

# --- Load Rules (The "Brain") ---
@st.cache_data
def load_rules():
    try:
        with open('rules.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Fatal Error: `rules.json` not found. Please ensure the file exists in the repository.")
        st.stop()
RULES = load_rules()

# --- AI Icon Generator ---
@st.cache_data
def generate_icon(app_name):
    width, height = 256, 256
    color1 = (25, 32, 43); color2 = (44, 56, 75)
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    words = app_name.split(); initials = ""
    if len(words) >= 2: initials = words[0][0] + words[1][0]
    elif len(words) == 1 and len(words[0]) > 0: initials = words[0][:2] if len(words[0]) > 1 else words[0][0]
    else: initials = "App"
    initials = initials.upper()
    try: font = ImageFont.truetype("DejaVuSans-Bold.ttf", 120)
    except IOError: font = ImageFont.load_default()
    try:
        text_bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = text_bbox[2] - text_bbox[0]; text_height = text_bbox[3] - text_bbox[1]
        x = (width - text_width) / 2; y = (height - text_height) / 2
        draw.text((x, y), initials, font=font, fill=(255, 255, 255))
    except Exception: draw.text((60, 60), initials, font=font, fill=(255, 255, 255))
    return img

# --- UI Helper Functions ---
def display_recipe_card(title, content, language='powershell'):
    st.subheader(title, divider='blue')
    st.code(content, language=language)

# --- Sidebar (Inputs) ---
with st.sidebar:
    st.title("⚙️ Configuration")
    st.markdown("Provide the installer details to generate a deployment recipe.")
    
    uploaded_file = st.file_uploader("Upload Installer", type=['exe', 'msi'])
    
    if uploaded_file:
        app_name = st.text_input("Application Name", value=uploaded_file.name.split('.')[0].replace('_', ' ').replace('-', ' ').title())
        vendor = st.text_input("Vendor", "VendorName")
        version = st.text_input("Version", "1.0.0")
        is_interactive = st.checkbox("Installer requires user interaction (Use ServiceUI trick)")
        
        if is_interactive:
            installer_type_key = "interactive"
        else:
            installer_type_key = st.selectbox("Installer Type", options=['exe_nsis', 'exe_inno', 'msi'], format_func=lambda x: RULES[x]['installer_type'])
        
        generate_button = st.button("🚀 Generate Packaging Recipe", type="primary", use_container_width=True)
    else:
        generate_button = False

# --- Main Page (Outputs) ---
st.title("🚀 PackPilot Pro")
st.markdown("##### The One-Click Packaging Dashboard for Intune & Patch My PC")
st.divider()

if not uploaded_file:
    st.info("Please upload an installer file in the sidebar to begin.")
    st.image("https://images.unsplash.com/photo-1593431188949-74a1d48c7921?w=800", caption="Ready to streamline your packaging workflow?")

if generate_button:
    with st.spinner('Cooking up your recipe...'):
        recipe = RULES[installer_type_key]
        
        st.header("Your Instant Recipe Card", divider='rainbow')
        
        # Create tabs for organized output
        tab1, tab2, tab3 = st.tabs(["📋 General Info & Icon", "⚙️ Commands", "🔍 Detection Rules"])

        with tab1:
            with st.container():
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                info_col, icon_col = st.columns([2, 1])
                with info_col:
                    st.subheader("General Information")
                    st.text_input("App Name for PMPC:", value=app_name, disabled=True, key="d_app")
                    st.text_input("Vendor for PMPC:", value=vendor, disabled=True, key="d_ven")
                    st.text_input("Version for PMPC:", value=version, disabled=True, key="d_ver")
                with icon_col:
                    st.subheader("Generated Icon")
                    generated_icon = generate_icon(app_name)
                    st.image(generated_icon, width=128)
                    buf = io.BytesIO()
                    generated_icon.save(buf, format="PNG")
                    st.download_button("Download Icon (.png)", buf.getvalue(), f"{app_name.replace(' ', '_')}_icon.png", "image/png", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            with st.container():
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                install_cmd = recipe['install_command'].format(filename=uploaded_file.name)
                uninstall_cmd = recipe['uninstall_command'].format(app_name=app_name, product_code="{YOUR_PRODUCT_CODE}")
                display_recipe_card("Silent Install Command", install_cmd)
                display_recipe_card("Silent Uninstall Command", uninstall_cmd)
                st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            with st.container():
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                st.info(f"**Recommended Method:** {recipe['detection_method']}")
                if "Registry" in recipe['detection_method']:
                    display_recipe_card("Registry Path (64-bit Apps)", "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
                    display_recipe_card("Registry Path (32-bit Apps on 64-bit OS)", "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
                elif "MSI" in recipe['detection_method']:
                    st.warning("For MSI detection, you will need to find the Product Code after a test installation.")
                st.markdown('</div>', unsafe_allow_html=True)

        st.success("Recipe generated successfully! Use the built-in copy icons in the code boxes above.")
