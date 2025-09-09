import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import json
import io
from streamlit_copy_to_clipboard import st_copy_to_clipboard

# --- Page Configuration ---
st.set_page_config(
    page_title="PackPilot Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load Rules (The "Brain") ---
try:
    with open('rules.json', 'r') as f:
        RULES = json.load(f)
except FileNotFoundError:
    st.error("Fatal Error: `rules.json` not found. Please ensure the file exists in the repository.")
    st.stop()

# --- AI Icon Generator ---
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
    st_copy_to_clipboard(content, f"Copy {title}", key=title.replace(" ", "_").lower())

# --- Main Application UI ---
st.title("🚀 PackPilot Pro"); st.markdown("##### The One-Click Packaging Dashboard for Intune & Patch My PC"); st.divider()
with st.container():
    uploaded_file = st.file_uploader("**Step 1: Drag & Drop Your Installer File Here** (.exe or .msi)", type=['exe', 'msi'])
    if uploaded_file:
        st.success(f"✅ Uploaded `{uploaded_file.name}`"); st.divider()
        st.markdown("**Step 2: Verify Details & Select Installer Type**"); col1, col2 = st.columns(2)
        with col1:
            app_name = st.text_input("Application Name", value=uploaded_file.name.split('.')[0].replace('_', ' ').replace('-', ' ').title())
            vendor = st.text_input("Vendor", "VendorName"); version = st.text_input("Version", "1.0.0")
        with col2:
            is_interactive = st.checkbox("Installer requires user interaction (Use ServiceUI trick)")
            if is_interactive: installer_type_key = "interactive"; st.info("ServiceUI mode selected.")
            else: installer_type_key = st.selectbox("Select Installer Type", options=['exe_nsis', 'exe_inno', 'msi'], format_func=lambda x: RULES[x]['installer_type'])
        st.divider()
        if st.button("🚀 Generate Packaging Recipe", type="primary", use_container_width=True):
            with st.spinner('Cooking up your recipe...'):
                recipe = RULES[installer_type_key]
                st.header("Your Instant Recipe Card", divider='rainbow')
                info_col, icon_col = st.columns([2, 1])
                with info_col:
                    st.subheader("📋 Page 2: General Information")
                    st.text_input("App Name for PMPC:", value=app_name, disabled=True, key="d_app"); st.text_input("Vendor for PMPC:", value=vendor, disabled=True, key="d_ven"); st.text_input("Version for PMPC:", value=version, disabled=True, key="d_ver")
                with icon_col:
                    st.subheader("🎨 Generated Icon")
                    generated_icon = generate_icon(app_name)
                    st.image(generated_icon, width=128)
                    buf = io.BytesIO(); generated_icon.save(buf, format="PNG")
                    st.download_button("Download Icon (.png)", buf.getvalue(), f"{app_name.replace(' ', '_')}_icon.png", "image/png", use_container_width=True)
                st.divider()
                st.header("⚙️ Page 3 & 4: Configuration & Detection")
                install_cmd = recipe['install_command'].format(filename=uploaded_file.name)
                uninstall_cmd = recipe['uninstall_command'].format(app_name=app_name, product_code="{YOUR_PRODUCT_CODE}")
                display_recipe_card("Silent Install Command", install_cmd)
                display_recipe_card("Silent Uninstall Command", uninstall_cmd)
                st.subheader("🔍 Detection Method", divider='blue'); st.info(f"**Recommended Method:** {recipe['detection_method']}")
                if "Registry" in recipe['detection_method']:
                    display_recipe_card("Registry Path (64-bit Apps)", "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
                    display_recipe_card("Registry Path (32-bit Apps on 64-bit OS)", "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall", language='text')
                elif "MSI" in recipe['detection_method']: st.warning("For MSI detection, you will need to find the Product Code after a test installation.")
                st.divider()
                st.header("✅ Page 5: Summary & Final Steps", divider='rainbow'); st.success("**Your recipe is ready!** Use the copy buttons above to fill out Patch My PC.")
                st.markdown("- **Assignments:** Remember to assign to your primary test group: `AAD_Intune_Software_test`.")
