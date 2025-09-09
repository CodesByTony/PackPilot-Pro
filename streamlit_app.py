import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import json
import io

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="PackPilot Pro",
    page_icon="🚀", # We'll set the custom icon in the header
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for the $100k Professional Look ---
st.markdown("""
<style>
/* --- General Theme: White & Orange --- */
body {
    background-color: #F0F2F6; /* Light grey background */
    color: #333333; /* Dark grey text */
}

/* --- Main App Container & Font --- */
.main .block-container {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    padding: 2rem 3rem;
}

/* --- Header Styling --- */
.header {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
}
.header h1 {
    font-size: 3rem;
    font-weight: 700;
    margin-left: 1rem;
    color: #2c3e50;
    letter-spacing: -2px;
}

/* --- Card Styling for Inputs and Outputs --- */
.card {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    border: 1px solid #EAEAEA;
    margin-bottom: 2rem;
}

/* --- Uploader Styling --- */
[data-testid="stFileUploader"] {
    border: 2px dashed #FFA500;
    background-color: #FFF9F0;
    border-radius: 8px;
    padding: 1.5rem;
}
[data-testid="stFileUploader"] label {
    font-weight: 600;
    color: #FF4500;
}

/* --- Input Widget Styling --- */
.stTextInput > div > div > input, .stSelectbox > div > div {
    background-color: #F0F2F6;
    border: 1px solid #DDDDDD;
}

/* --- Primary Button: The "Generate" Button --- */
.stButton>button {
    font-weight: 600;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    border: 2px solid #FF4500;
    background-image: linear-gradient(to right, #FF4500 0%, #FFA500 100%);
    color: white;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255, 69, 0, 0.2);
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 69, 0, 0.3);
}

/* --- Disabled Buttons for "Future Capabilities" --- */
.stButton>button:disabled {
    background-image: none;
    background-color: #E0E0E0;
    border: 2px solid #BDBDBD;
    color: #9E9E9E;
    cursor: not-allowed;
}

/* --- Tabs Styling --- */
[data-baseweb="tab-list"] {
    justify-content: center;
}
[data-baseweb="tab"] {
    background-color: transparent;
    font-weight: 600;
}
[aria-selected="true"] {
    background-color: #FFF9F0;
    border-bottom: 3px solid #FF4500 !important;
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

# --- NEW Unique Icon Generator ---
@st.cache_data
def generate_packpilot_icon():
    width, height = 256, 256
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Load a bold, clean font
    try:
        font_main = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
        font_pro = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    except IOError:
        font_main = ImageFont.load_default(); font_pro = ImageFont.load_default()

    main_text = "packpilot"
    pro_text = "pro"
    
    # Calculate positions
    main_bbox = draw.textbbox((0,0), main_text, font=font_main)
    main_width = main_bbox[2] - main_bbox[0]
    main_height = main_bbox[3] - main_bbox[1]
    main_x = (width - main_width) / 2
    main_y = (height - main_height) / 2 + 10 # Shift down slightly
    
    pro_bbox = draw.textbbox((0,0), pro_text, font=font_pro)
    pro_x = main_x + main_width + 5 # To the right of the main text
    pro_y = main_y - (pro_bbox[3] - pro_bbox[1]) + 5 # Positioned like a superscript

    # Draw the text with outline
    draw.text((main_x, main_y), main_text, font=font_main, fill="#FF4500", stroke_width=3, stroke_fill="black")
    draw.text((pro_x, pro_y), pro_text, font=font_pro, fill="#FF4500", stroke_width=2, stroke_fill="black")
    
    return img

# --- UI Helper Functions ---
def display_recipe_card(title, content, language='powershell'):
    st.subheader(title, divider='orange')
    st.code(content, language=language)

# --- Header Section ---
icon_image = generate_packpilot_icon()
st.markdown('<div class="header">', unsafe_allow_html=True)
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image(icon_image, width=100)
with col2:
    st.title("PackPilot Pro")
st.markdown('</div>', unsafe_allow_html=True)


# --- Input Section: "The Pilot's Cockpit" ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("The Pilot's Cockpit", anchor=False)
    st.markdown("Upload your installer and provide the basic details to begin analysis.")
    
    uploaded_file = st.file_uploader("", type=['exe', 'msi'])
    
    if uploaded_file:
        col1, col2, col3 = st.columns(3)
        with col1:
            app_name = st.text_input("Application Name", value=uploaded_file.name.split('.')[0].replace('_', ' ').replace('-', ' ').title())
        with col2:
            vendor = st.text_input("Vendor", "VendorName")
        with col3:
            version = st.text_input("Version", "1.0.0")

        is_interactive = st.checkbox("Installer requires user interaction (Use ServiceUI trick)")
        if is_interactive:
            installer_type_key = "interactive"
        else:
            installer_type_key = st.selectbox("Installer Type", options=['exe_nsis', 'exe_inno', 'msi'], format_func=lambda x: RULES[x]['installer_type'])
            
        generate_button = st.button("🚀 Generate Recipe", use_container_width=True)
    else:
        st.info("Awaiting installer upload to proceed...")
        generate_button = False
        
    st.markdown('</div>', unsafe_allow_html=True)


# --- Output Section: "The Flight Plan" ---
if generate_button:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("The Flight Plan: Your Deployment Recipe", anchor=False)
        
        with st.spinner('Analyzing installer and generating recipe...'):
            recipe = RULES[installer_type_key]
            
            tab1, tab2, tab3 = st.tabs(["📋 General Info & Icon", "⚙️ Commands", "🔍 Detection Rules"])

            with tab1:
                info_col, icon_col = st.columns([2, 1])
                with info_col:
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

            with tab2:
                install_cmd = recipe['install_command'].format(filename=uploaded_file.name)
                uninstall_cmd = recipe['uninstall_command'].format(app_name=app_name, product_code="{YOUR_PRODUCT_CODE}")
                display_recipe_card("Silent Install Command", install_cmd)
                display_recipe_card("Silent Uninstall Command", uninstall_cmd)

            with tab3:
                st.info(f"**Recommended Method:** {recipe['detection_method']}")
                if "Registry" in recipe['detection_method']:
                    display_recipe_card("Registry Path (64-bit Apps)", "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
                    display_recipe_card("Registry Path (32-bit Apps on 64-bit OS)", "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
                elif "MSI" in recipe['detection_method']:
                    st.warning("For MSI detection, you will need to find the Product Code after a test installation.")
        st.markdown('</div>', unsafe_allow_html=True)


# --- Future Capabilities Section ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("Future Capabilities", anchor=False, help="These features are on our roadmap to make PackPilot Pro even more powerful.")
cols = st.columns(4)
with cols[0]:
    st.button("📄 Analyze Release Notes", disabled=True, use_container_width=True)
with cols[1]:
    st.button("🛡️ Check for CVEs", disabled=True, use_container_width=True)
with cols[2]:
    st.button("➡️ Publish to Intune (API)", disabled=True, use_container_width=True)
with cols[3]:
    st.button("📊 Monitor Deployment", disabled=True, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
