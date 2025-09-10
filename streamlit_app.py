"""
PackPilot Pro - Enterprise Software Packaging Automation Platform
Version 3.0 - Enhanced with Copy Functions & Better Icons
Author: Production Ready Version
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import io
import base64
import re
import requests
import yaml
import os
import time
from datetime import datetime
import hashlib
from typing import Dict, Optional, List, Tuple
import random

# ============================================================================
# PAGE CONFIGURATION & INITIALIZATION
# ============================================================================
st.set_page_config(
    page_title="PackPilot Pro - Intelligent Packaging Platform",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ENHANCED CSS WITH ALL FIXES
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* =========================== GLOBAL RESET =========================== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* =========================== BASE TYPOGRAPHY =========================== */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Force ALL text to be black except where specifically overridden */
    p, span, div, label, h1, h2, h3, h4, h5, h6, li {
        color: #1a1a1a !important;
    }
    
    /* =========================== MAIN CONTAINER =========================== */
    .stApp {
        background-color: #FAFAFA;
    }
    
    .main .block-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 3rem;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-top: 1rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
    }
    
    /* =========================== HERO HEADER =========================== */
    .hero-header {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.95) !important;
        font-weight: 400;
    }
    
    /* =========================== COPY BUTTON STYLES =========================== */
    .copy-button {
        position: absolute;
        top: 5px;
        right: 5px;
        background: linear-gradient(135deg, #FF6B35, #F7931E);
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 12px;
        z-index: 100;
        transition: all 0.3s ease;
    }
    
    .copy-button:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .copy-container {
        position: relative;
        margin: 10px 0;
    }
    
    /* =========================== CARD STYLING =========================== */
    .custom-card {
        background: linear-gradient(145deg, #FFFFFF, #FFF8F5);
        border: 2px solid #FF6B35;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 20px rgba(255, 107, 53, 0.1);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(255, 107, 53, 0.15);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(255, 107, 53, 0.15);
    }
    
    .card-icon {
        font-size: 1.8rem;
        margin-right: 1rem;
    }
    
    .card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a1a !important;
    }
    
    /* =========================== FILE UPLOADER FIX =========================== */
    [data-testid="stFileUploadDropzone"] {
        background-color: #FFF8F5 !important;
        border: 2px dashed #FF6B35 !important;
    }
    
    [data-testid="stFileUploadDropzone"] div {
        color: #FF6B35 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stFileUploadDropzone"] small {
        color: #FF6B35 !important;
    }
    
    /* =========================== INPUT FIELDS =========================== */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: #1a1a1a !important;
        border: 2px solid #FFE4DC !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
        outline: none !important;
    }
    
    /* =========================== BUTTONS =========================== */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.2) !important;
        transition: all 0.3s ease !important;
        min-height: 2.5rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.3) !important;
    }
    
    /* =========================== CODE BLOCKS =========================== */
    .stCodeBlock, pre, code {
        background-color: #2B2B2B !important;
        color: #F0F0F0 !important;
        border: 2px solid #FF6B35 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        font-family: 'Consolas', 'Monaco', monospace !important;
        line-height: 1.5 !important;
    }
    
    /* =========================== RESPONSIVE ADJUSTMENTS =========================== */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .custom-card {
            padding: 1.5rem;
        }
        .main .block-container {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
def init_session_state():
    """Initialize all session state variables with proper defaults"""
    defaults = {
        'parsed_data': {},
        'recipe_generated': False,
        'recipe_data': None,
        'step_number': 1,
        'validation_passed': False,
        'deployment_history': [],
        'current_mode': 'standard',
        'api_cache': {},
        'last_api_call': 0,
        'primary_installer': None,
        'uploaded_files': [],
        'copy_status': {}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# ENHANCED ICON GENERATION
# ============================================================================
def generate_high_quality_icon(app_name: str, style: str = 'modern') -> Image.Image:
    """Generate high-quality application icon with modern design"""
    size = 512  # Higher resolution for better quality
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Get initials
    words = app_name.split()
    initials = "".join([w[0].upper() for w in words[:2]]) if words else "AP"
    
    # Create gradient background with better quality
    if style == 'modern':
        # Create circular gradient background
        center_x, center_y = size // 2, size // 2
        max_radius = size // 2
        
        for radius in range(max_radius, 0, -2):
            # Calculate color based on radius
            progress = 1 - (radius / max_radius)
            
            # Gradient from orange to deep orange
            r = int(255 - progress * 30)
            g = int(107 - progress * 20)
            b = int(53 - progress * 10)
            alpha = 255
            
            # Draw circle
            left = center_x - radius
            top = center_y - radius
            right = center_x + radius
            bottom = center_y + radius
            
            draw.ellipse([left, top, right, bottom], fill=(r, g, b, alpha))
    
    elif style == 'flat':
        # Flat design with rounded corners
        corner_radius = size // 8
        
        # Draw rounded rectangle background
        draw.rounded_rectangle(
            [20, 20, size-20, size-20],
            radius=corner_radius,
            fill=(255, 107, 53, 255)
        )
        
        # Add subtle inner shadow
        shadow_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_img)
        shadow_draw.rounded_rectangle(
            [25, 25, size-25, size-25],
            radius=corner_radius-5,
            fill=(0, 0, 0, 30)
        )
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=5))
        img = Image.alpha_composite(img, shadow_img)
        draw = ImageDraw.Draw(img)
    
    else:  # gradient style
        # Linear gradient
        for y in range(size):
            progress = y / size
            r = int(255 - progress * 50)
            g = int(107 - progress * 40)
            b = int(53 - progress * 20)
            draw.rectangle([(0, y), (size, y+1)], fill=(r, g, b, 255))
    
    # Add text with better font handling
    try:
        # Try to load a better font
        font_size = size // 3
        try:
            # Try system fonts
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("helvetica.ttf", font_size)
            except:
                # Fallback to default
                font = ImageFont.load_default()
                # Scale up text for default font
                temp_img = Image.new('RGBA', (200, 100), (0, 0, 0, 0))
                temp_draw = ImageDraw.Draw(temp_img)
                temp_draw.text((10, 10), initials, font=font, fill=(255, 255, 255, 255))
                temp_img = temp_img.resize((size//2, size//4), Image.Resampling.LANCZOS)
                img.paste(temp_img, (size//4, size//2 - size//8), temp_img)
                
                # Skip the normal text drawing if using default font
                font = None
    except:
        font = None
    
    if font:
        # Draw text with shadow for depth
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        # Draw shadow
        shadow_offset = size // 50
        draw.text((x + shadow_offset, y + shadow_offset), initials, 
                 font=font, fill=(0, 0, 0, 100))
        
        # Draw main text
        draw.text((x, y), initials, font=font, fill=(255, 255, 255, 255))
    
    # Add subtle overlay for depth
    overlay = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Top highlight
    for y in range(size // 3):
        alpha = int(30 * (1 - y / (size // 3)))
        overlay_draw.rectangle([(0, y), (size, y+1)], fill=(255, 255, 255, alpha))
    
    img = Image.alpha_composite(img, overlay)
    
    # Resize to standard icon size with high quality
    img = img.resize((256, 256), Image.Resampling.LANCZOS)
    
    return img

# ============================================================================
# COPY TO CLIPBOARD FUNCTION
# ============================================================================
def create_copy_button(text: str, button_key: str):
    """Create a copy to clipboard button with feedback"""
    if st.button(f"📋 Copy", key=button_key, help="Copy to clipboard"):
        st.session_state.copy_status[button_key] = True
        # JavaScript to copy to clipboard
        st.markdown(f"""
        <script>
        navigator.clipboard.writeText(`{text}`);
        </script>
        """, unsafe_allow_html=True)
        st.success("✅ Copied to clipboard!")
        time.sleep(1)
        st.rerun()
    
    # Reset copy status
    if button_key in st.session_state.copy_status:
        del st.session_state.copy_status[button_key]

def display_code_with_copy(code: str, language: str, unique_key: str):
    """Display code block with copy button"""
    col1, col2 = st.columns([10, 1])
    
    with col1:
        st.code(code, language=language)
    
    with col2:
        if st.button("📋", key=f"copy_{unique_key}", help="Copy to clipboard"):
            # Use session state to track copy action
            st.session_state[f'copied_{unique_key}'] = True
            # JavaScript injection for clipboard
            escaped_code = code.replace('`', '\\`')  # Move this outside the f-string
            js = f"""
            <script>
            function copyToClipboard_{unique_key}() {{
                const text = `{escaped_code}`;
                navigator.clipboard.writeText(text).then(function() {{
                    console.log('Copied to clipboard');
                }}, function(err) {{
                    console.error('Could not copy text: ', err);
                }});
            }}
            copyToClipboard_{unique_key}();
            </script>
            """
            st.markdown(js, unsafe_allow_html=True)
    
    # Show success message if copied
    if st.session_state.get(f'copied_{unique_key}', False):
        st.success("✅ Copied!")
        st.session_state[f'copied_{unique_key}'] = False

# ============================================================================
# CONFIGURATION LOADER
# ============================================================================
@st.cache_data(ttl=3600)
def load_configuration_files():
    """Load and validate all configuration files"""
    configs = {}
    
    # Default rules
    default_rules = {
        "exe_nsis": {
            "installer_type": "NSIS Installer (.exe)",
            "install_command": "\"{filename}\" /S",
            "uninstall_command": "\"{uninstall_string}\" /S",
            "detection_method": "Registry Key Detection",
            "requires_restart": False
        },
        "exe_inno": {
            "installer_type": "Inno Setup Installer (.exe)",
            "install_command": "\"{filename}\" /VERYSILENT /NORESTART",
            "uninstall_command": "\"{uninstall_string}\" /VERYSILENT",
            "detection_method": "Registry Key Detection",
            "requires_restart": False
        },
        "msi": {
            "installer_type": "MSI Package",
            "install_command": "msiexec /i \"{filename}\" /qn /norestart",
            "uninstall_command": "msiexec /x \"{product_code}\" /qn",
            "detection_method": "MSI Product Code",
            "requires_restart": False
        },
        "interactive": {
            "installer_type": "Interactive Installer (ServiceUI)",
            "install_command": "ServiceUI.exe -process:explorer.exe \"{filename}\"",
            "uninstall_command": "ServiceUI.exe -process:explorer.exe \"{uninstall_string}\"",
            "detection_method": "Registry Key Detection",
            "requires_restart": False
        }
    }
    
    try:
        if os.path.exists('rules.json'):
            with open('rules.json', 'r', encoding='utf-8') as f:
                configs['rules'] = json.load(f)
        else:
            configs['rules'] = default_rules
            # Save default rules
            with open('rules.json', 'w', encoding='utf-8') as f:
                json.dump(default_rules, f, indent=2)
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        configs['rules'] = default_rules
    
    return configs

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def set_background_image():
    """Set custom background image if available"""
    try:
        if os.path.exists('Generated.png'):
            with open('Generated.png', 'rb') as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background-image: url("data:image/png;base64,{b64}");
                        background-size: cover;
                        background-position: center;
                        background-repeat: no-repeat;
                        background-attachment: fixed;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
    except Exception:
        pass

def parse_powershell_output(output: str) -> Dict[str, str]:
    """Parse PowerShell output into dictionary"""
    if not output or not output.strip():
        return {}
    
    data = {}
    lines = output.strip().split('\n')
    
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                if key and value:
                    data[key] = value
        elif '=' in line:
            parts = line.split('=', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                if key and value:
                    data[key] = value
    
    return data

@st.cache_data(ttl=7200)
def fetch_app_description(app_name: str) -> str:
    """Fetch app description with fallback"""
    try:
        time.sleep(0.5)
        search_term = re.sub(r'[^\w\s]', '', app_name).strip()
        
        url = f"https://api.github.com/search/code?q={search_term}+in:path+repo:microsoft/winget-pkgs&per_page=1"
        headers = {'Accept': 'application/vnd.github.v3+json'}
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            items = response.json().get('items', [])
            if items:
                return f"{app_name} is a professional software application designed for enterprise deployment."
    except:
        pass
    
    return f"{app_name} is a specialized application that enhances productivity and workflow efficiency in enterprise environments."

def create_deployment_json(data: Dict) -> str:
    """Create deployment package JSON"""
    package = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'version': '1.0.0',
            'packager': 'PackPilot Pro'
        },
        'application': {
            'name': data.get('app_name', ''),
            'vendor': data.get('vendor', ''),
            'version': data.get('version', ''),
            'architecture': data.get('architecture', '64-bit'),
            'context': data.get('install_context', 'System')
        },
        'deployment': {
            'installer_type': data.get('installer_type_key', ''),
            'filename': data.get('uploaded_filename', ''),
            'timeout': data.get('timeout', 30),
            'priority': data.get('priority', 'Normal'),
            'category': data.get('category', 'Productivity')
        },
        'flags': {
            'interactive': data.get('is_interactive', False),
            'requires_restart': data.get('requires_restart', False),
            'create_shortcut': data.get('create_shortcut', True)
        }
    }
    return json.dumps(package, indent=2)

# ============================================================================
# UI COMPONENTS
# ============================================================================
def render_header():
    """Render application header"""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">📦 PackPilot Pro</h1>
        <p class="hero-subtitle">Intelligent Software Packaging Platform for Enterprise</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar with tools"""
    with st.sidebar:
        st.markdown("## 🛠️ Tools & Options")
        
        deployment_mode = st.selectbox(
            "Deployment Mode",
            ['Standard', 'Silent', 'Interactive'],
            help="Select the deployment mode for your package"
        )
        
        st.divider()
        
        st.markdown("### Quick Actions")
        if st.button("🔄 Reset Application", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if st.button("📚 View Documentation", use_container_width=True):
            st.info("Documentation will open in a new tab")
        
        st.divider()
        
        st.markdown("### Recent Packages")
        if st.session_state.deployment_history:
            for item in st.session_state.deployment_history[-3:]:
                st.markdown(f"• {item['app']} ({item['date']})")
        else:
            st.markdown("*No recent packages*")

def render_upload_section():
    """Render file upload section"""
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">📁</span>
            <span class="card-title">Step 1: Upload Installation Files</span>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload installer files and supporting documents",
        accept_multiple_files=True,
        type=['exe', 'msi', 'msix', 'ps1', 'bat', 'json', 'xml'],
        help="Drag and drop your files here or click to browse"
    )
    
    primary_installer = None
    
    if uploaded_files:
        installers = [f for f in uploaded_files if f.name.endswith(('.exe', '.msi', '.msix'))]
        
        if installers:
            primary_installer = installers[0]
            st.session_state.primary_installer = primary_installer
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Files", len(uploaded_files))
            with col2:
                st.metric("Installers", len(installers))
            with col3:
                total_size = sum(f.size for f in uploaded_files) / (1024*1024)
                st.metric("Total Size", f"{total_size:.2f} MB")
            
            st.success(f"✅ Primary installer: **{primary_installer.name}**")
            st.session_state.step_number = 2
    
    st.markdown("</div>", unsafe_allow_html=True)
    return primary_installer

def render_parse_section():
    """Render PowerShell parsing section"""
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">⚙️</span>
            <span class="card-title">Step 2: Import Metadata</span>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📖 Instructions", expanded=False):
        st.markdown("""
        1. Run `readData.ps1` script with your installer
        2. Copy the complete output
        3. Paste it below and click Parse
        """)
    
    ps_output = st.text_area(
        "Paste PowerShell output:",
        height=150,
        placeholder="AppName : Application Name\nPublisher : Company Name\nVersion : 1.0.0"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Parse Data", use_container_width=True):
            if ps_output:
                parsed = parse_powershell_output(ps_output)
                if parsed:
                    st.session_state.parsed_data = parsed
                    st.success(f"Parsed {len(parsed)} fields successfully!")
                    st.session_state.step_number = 3
            else:
                st.warning("Please paste the PowerShell output first")
    
    with col2:
        if st.button("📝 Use Sample Data", use_container_width=True):
            st.session_state.parsed_data = {
                'AppName': 'Sample Application',
                'Publisher': 'Sample Company',
                'Version': '1.0.0',
                'Architecture': '64-bit',
                'InstallContext': 'System'
            }
            st.success("Sample data loaded!")
            st.session_state.step_number = 3
    
    if st.session_state.parsed_data:
        st.markdown("**Parsed Data:**")
        for key, value in st.session_state.parsed_data.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"• **{key}:** {value}")
            with col2:
                display_code_with_copy(value, "text", f"parsed_{key}")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_configuration_section(primary_installer):
    """Render configuration section"""
    if not st.session_state.parsed_data or not primary_installer:
        return False
    
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">🔧</span>
            <span class="card-title">Step 3: Configure Package</span>
        </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.parsed_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        app_name = st.text_input("Application Name", value=data.get('AppName', ''))
        vendor = st.text_input("Vendor", value=data.get('Publisher', ''))
        version = st.text_input("Version", value=data.get('Version', ''))
    
    with col2:
        architecture = st.selectbox("Architecture", ['64-bit', '32-bit', 'Any'])
        install_context = st.selectbox("Install Context", ['System', 'User'])
        category = st.selectbox("Category", ['Productivity', 'Development', 'Security', 'Utilities'])
    
    with st.expander("Advanced Options"):
        col1, col2, col3 = st.columns(3)
        with col1:
            is_interactive = st.checkbox("Interactive Installation")
            requires_restart = st.checkbox("Requires Restart")
            create_shortcut = st.checkbox("Create Desktop Shortcut", value=True)
        with col2:
            timeout = st.number_input("Timeout (minutes)", min_value=5, max_value=120, value=30)
            priority = st.selectbox("Priority", ['Low', 'Normal', 'High'])
        with col3:
            icon_style = st.selectbox("Icon Style", ['modern', 'flat', 'gradient'])
    
    configs = load_configuration_files()
    rules = configs.get('rules', {})
    
    if is_interactive:
        installer_type_key = 'interactive'
    else:
        file_ext = os.path.splitext(primary_installer.name)[1].lower()
        if file_ext == '.msi':
            installer_type_key = 'msi'
        else:
            installer_type_key = 'exe_nsis'
    
    if st.button("🚀 Generate Recipe", use_container_width=True):
        if all([app_name, vendor, version]):
            st.session_state.recipe_data = {
                'app_name': app_name,
                'vendor': vendor,
                'version': version,
                'architecture': architecture,
                'install_context': install_context,
                'category': category,
                'installer_type_key': installer_type_key,
                'uploaded_filename': primary_installer.name,
                'is_interactive': is_interactive,
                'requires_restart': requires_restart,
                'create_shortcut': create_shortcut,
                'timeout': timeout,
                'priority': priority,
                'icon_style': icon_style
            }
            st.session_state.recipe_generated = True
            st.session_state.step_number = 4
            
            st.session_state.deployment_history.append({
                'app': app_name,
                'date': datetime.now().strftime('%m/%d/%Y')
            })
            
            st.success("Recipe generated successfully!")
        else:
            st.error("Please fill all required fields")
    
    st.markdown("</div>", unsafe_allow_html=True)
    return True

def render_recipe_output():
    """Render the generated recipe with copy functionality"""
    if not st.session_state.recipe_generated or not st.session_state.recipe_data:
        return
    
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">📋</span>
            <span class="card-title">Step 4: Generated Recipe</span>
        </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.recipe_data
    configs = load_configuration_files()
    rules = configs.get('rules', {})
    
    recipe_rules = rules.get(data.get('installer_type_key', 'exe_nsis'), {})
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚙️ Commands", "🔍 Detection", "📥 Export"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {data['app_name']}")
            st.markdown(f"**Version:** {data['version']}")
            st.markdown(f"**Vendor:** {data['vendor']}")
            st.markdown(f"**Category:** {data['category']}")
            
            desc = fetch_app_description(data['app_name'])
            st.info(desc)
        
        with col2:
            st.markdown("### Icon")
            icon = generate_high_quality_icon(data['app_name'], data.get('icon_style', 'modern'))
            st.image(icon, width=150)
            
            buf = io.BytesIO()
            icon.save(buf, format='PNG')
            st.download_button(
                "Download Icon",
                buf.getvalue(),
                f"{data['app_name']}_icon.png",
                "image/png"
            )
    
    with tab2:
        st.markdown("### Installation Commands")
        
        # Safe formatting for install command
        install_cmd = recipe_rules.get('install_command', '"{filename}" /S')
        try:
            install_cmd = install_cmd.format(filename=data['uploaded_filename'])
        except:
            install_cmd = install_cmd.replace('{filename}', data['uploaded_filename'])
        
        display_code_with_copy(install_cmd, 'powershell', 'install_cmd')
        
        # Safe formatting for uninstall command
        if 'uninstall_command' in recipe_rules:
            st.markdown("### Uninstall Command")
            uninstall_cmd = recipe_rules['uninstall_command']
            
            # Safe replacement of placeholders
            uninstall_cmd = uninstall_cmd.replace('{uninstall_string}', '{UNINSTALL_STRING}')
            uninstall_cmd = uninstall_cmd.replace('{product_code}', '{PRODUCT_CODE}')
            
            display_code_with_copy(uninstall_cmd, 'powershell', 'uninstall_cmd')
        
        # Additional PowerShell script
        st.markdown("### Complete Installation Script")
        ps_complete = f"""
# {data['app_name']} Installation Script
# Generated by PackPilot Pro

$AppName = "{data['app_name']}"
$Version = "{data['version']}"
$Vendor = "{data['vendor']}"
$Installer = "{data['uploaded_filename']}"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installing $AppName v$Version" -ForegroundColor Green
Write-Host "Vendor: $Vendor" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{{
    Write-Host "This script requires Administrator privileges!" -ForegroundColor Red
    Exit 1
}}

# Installation
try {{
    Write-Host "Starting installation..." -ForegroundColor Yellow
    {install_cmd}
    
    if ($LASTEXITCODE -eq 0) {{
        Write-Host "Installation completed successfully!" -ForegroundColor Green
    }} else {{
        Write-Host "Installation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        Exit $LASTEXITCODE
    }}
}} catch {{
    Write-Host "Installation error: $_" -ForegroundColor Red
    Exit 1
}}
"""
        display_code_with_copy(ps_complete, 'powershell', 'complete_script')
    
    with tab3:
        st.markdown("### Detection Method")
        detection_method = recipe_rules.get('detection_method', 'Registry Key Detection')
        st.info(f"Method: {detection_method}")
        
        st.markdown("### Registry Paths")
        reg_paths = """
# 64-bit Registry Path
HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall

# 32-bit Registry Path
HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall

# User Registry Path
HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall
"""
        display_code_with_copy(reg_paths, 'powershell', 'registry_paths')
        
        st.markdown("### Detection Script")
        detection_script = f"""
# Detection script for {data['app_name']}
$AppName = "{data['app_name']}"
$Version = "{data['version']}"

$RegistryPaths = @(
    "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
    "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
    "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
)

foreach ($Path in $RegistryPaths) {{
    if (Test-Path $Path) {{
        $Apps = Get-ChildItem -Path $Path | Get-ItemProperty | 
                Where-Object {{ $_.DisplayName -like "*$AppName*" }}
        
        if ($Apps) {{
            Write-Host "Application found:" -ForegroundColor Green
            $Apps | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate
            Exit 0
        }}
    }}
}}

Write-Host "Application not found" -ForegroundColor Yellow
Exit 1
"""
        display_code_with_copy(detection_script, 'powershell', 'detection_script')
    
    with tab4:
        st.markdown("### Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            json_data = create_deployment_json(data)
            st.download_button(
                "📄 Export as JSON",
                json_data,
                f"{data['app_name']}_recipe.json",
                "application/json",
                use_container_width=True
            )
        
        with col2:
            ps_script = f"""
# {data['app_name']} Installation Script
# Generated by PackPilot Pro

$AppName = "{data['app_name']}"
$Version = "{data['version']}"
$Installer = "{data['uploaded_filename']}"

Write-Host "Installing $AppName v$Version..."
{install_cmd}

Write-Host "Installation complete!"
"""
            st.download_button(
                "📜 Export PowerShell",
                ps_script,
                f"{data['app_name']}_install.ps1",
                "text/plain",
                use_container_width=True
            )
        
        with col3:
            # YAML export
            yaml_data = f"""
# {data['app_name']} Package Configuration
# Generated by PackPilot Pro

application:
  name: {data['app_name']}
  version: {data['version']}
  vendor: {data['vendor']}
  
deployment:
  installer: {data['uploaded_filename']}
  architecture: {data['architecture']}
  context: {data['install_context']}
  category: {data['category']}
  
options:
  interactive: {data['is_interactive']}
  requires_restart: {data['requires_restart']}
  create_shortcut: {data['create_shortcut']}
  timeout: {data['timeout']}
  priority: {data['priority']}
  
commands:
  install: {install_cmd}
  detection_method: {detection_method}
"""
            st.download_button(
                "📝 Export YAML",
                yaml_data,
                f"{data['app_name']}_config.yaml",
                "text/yaml",
                use_container_width=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    """Main application entry point"""
    
    # Set background
    set_background_image()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Progress indicator
    if st.session_state.step_number > 1:
        progress = (st.session_state.step_number - 1) / 3
        st.progress(progress)
    
    # Main workflow
    primary_installer = render_upload_section()
    
    if primary_installer:
        render_parse_section()
        
        if st.session_state.parsed_data:
            if render_configuration_section(primary_installer):
                render_recipe_output()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666;">
        <p><strong>PackPilot Pro v3.0</strong> © 2024 | Enterprise Packaging Platform</p>
        <p style="font-size: 0.9rem;">Enhanced with Copy Functions & High-Quality Icons</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
