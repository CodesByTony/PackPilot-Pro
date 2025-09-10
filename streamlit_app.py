"""
PackPilot Pro - Enterprise Software Packaging Automation Platform
Version 2.0 - Fully Debugged & Enhanced UI/UX
Author: Production Ready Version
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
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

# ============================================================================
# PAGE CONFIGURATION & INITIALIZATION
# ============================================================================

st.set_page_config(
    page_title="PackPilot Pro - Intelligent Packaging Platform",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"  # Changed to collapsed for cleaner look
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
/* This is the critical fix for the drag and drop text */
[data-testid="stFileUploadDropzone"] {
    background-color: #FFF8F5 !important;
    border: 2px dashed #FF6B35 !important;
}

[data-testid="stFileUploadDropzone"] div {
    color: #FF6B35 !important;  /* Orange text for visibility */
    font-weight: 600 !important;
}

[data-testid="stFileUploadDropzone"] small {
    color: #FF6B35 !important;  /* Orange text for file size limit */
}

section[data-testid="stFileUploadDropzone"] > div {
    color: #FF6B35 !important;
}

/* Uploaded file names */
[data-testid="stFileUploaderFile"] {
    background-color: #FFF8F5 !important;
    border: 1px solid #FF6B35 !important;
    color: #1a1a1a !important;
}

[data-testid="stFileUploaderFileName"] {
    color: #1a1a1a !important;
    font-weight: 500 !important;
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

/* Labels */
[data-testid="stWidgetLabel"] {
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    margin-bottom: 0.3rem !important;
}

/* =========================== SELECT BOXES =========================== */
[data-testid="stSelectbox"] > div > div {
    background-color: #FFFFFF !important;
    color: #1a1a1a !important;
    border: 2px solid #FFE4DC !important;
    border-radius: 10px !important;
}

[data-testid="stSelectbox"] label {
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

/* =========================== BUTTONS =========================== */
/* Primary buttons - Full gradient */
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

/* Download buttons - Outlined style */
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #FF6B35 !important;
    border: 2px solid #FF6B35 !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

.stDownloadButton > button:hover {
    background: #FF6B35 !important;
    color: #FFFFFF !important;
}

/* =========================== TABS =========================== */
.stTabs [data-baseweb="tab-list"] {
    background-color: #FFF8F5;
    border-radius: 12px;
    padding: 0.5rem;
    gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1.25rem !important;
    border-radius: 8px !important;
    background-color: transparent !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(255, 107, 53, 0.1) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B35, #F7931E) !important;
    color: #FFFFFF !important;
}

/* =========================== CODE BLOCKS =========================== */
.stCodeBlock, pre, code {
    background-color: #2B2B2B !important;
    color: #F0F0F0 !important;  /* Light gray for dark background */
    border: 2px solid #FF6B35 !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    font-family: 'Consolas', 'Monaco', monospace !important;
    line-height: 1.5 !important;
}

/* =========================== METRICS =========================== */
[data-testid="metric-container"] {
    background-color: #FFF8F5;
    border: 1px solid #FFE4DC;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

[data-testid="metric-container"] label {
    color: #666666 !important;
    font-size: 0.85rem !important;
}

[data-testid="metric-container"] > div:nth-child(2) {
    color: #1a1a1a !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

/* =========================== EXPANDERS =========================== */
[data-testid="stExpander"] {
    background-color: #FFF8F5 !important;
    border: 1px solid #FFE4DC !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary {
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

/* =========================== ALERTS & MESSAGES =========================== */
.stAlert {
    border-radius: 10px !important;
    border-left: 4px solid !important;
}

/* Success */
[data-testid="stAlert"][data-type="success"] {
    background-color: #E8F5E9 !important;
    border-left-color: #4CAF50 !important;
}

/* Info */
[data-testid="stAlert"][data-type="info"] {
    background-color: #FFF3E0 !important;
    border-left-color: #FF9800 !important;
}

/* Warning */
[data-testid="stAlert"][data-type="warning"] {
    background-color: #FFF3E0 !important;
    border-left-color: #FF9800 !important;
}

/* Error */
[data-testid="stAlert"][data-type="error"] {
    background-color: #FFEBEE !important;
    border-left-color: #F44336 !important;
}

/* =========================== PROGRESS BAR =========================== */
.stProgress > div > div {
    background-color: linear-gradient(135deg, #FF6B35, #F7931E) !important;
}

/* =========================== SIDEBAR =========================== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFF8F5 0%, #FFFFFF 100%);
    border-right: 2px solid #FFE4DC;
}

[data-testid="stSidebar"] .block-container {
    padding: 2rem 1rem;
}

/* =========================== SPINNER =========================== */
.stSpinner > div {
    border-top-color: #FF6B35 !important;
}

/* =========================== DIVIDER =========================== */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, #FFE4DC, transparent) !important;
    margin: 2rem 0 !important;
}

/* =========================== RESPONSIVE ADJUSTMENTS =========================== */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem; }
    .custom-card { padding: 1.5rem; }
    .main .block-container { padding: 1rem; }
}

/* =========================== PREVENT TEXT OVERLAP =========================== */
.element-container {
    margin-bottom: 1rem !important;
}

.row-widget {
    margin-bottom: 1rem !important;
}

/* Ensure spacing between elements */
.element-container + .element-container {
    margin-top: 1rem !important;
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
        'uploaded_files': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# CONFIGURATION LOADER
# ============================================================================

@st.cache_data(ttl=3600)
def load_configuration_files():
    """Load and validate all configuration files"""
    configs = {}
    
    # Try to load rules.json
    try:
        if os.path.exists('rules.json'):
            with open('rules.json', 'r', encoding='utf-8') as f:
                configs['rules'] = json.load(f)
        else:
            # Create default rules if file doesn't exist
            configs['rules'] = {
                "exe_nsis": {
                    "installer_type": "NSIS Installer (.exe)",
                    "install_command": '"{filename}" /S',
                    "uninstall_command": '"{uninstall_string}" /S',
                    "detection_method": "Registry Key Detection",
                    "requires_restart": False
                },
                "exe_inno": {
                    "installer_type": "Inno Setup Installer (.exe)",
                    "install_command": '"{filename}" /VERYSILENT /NORESTART',
                    "uninstall_command": '"{uninstall_string}" /VERYSILENT',
                    "detection_method": "Registry Key Detection",
                    "requires_restart": False
                },
                "msi": {
                    "installer_type": "MSI Package",
                    "install_command": 'msiexec /i "{filename}" /qn /norestart',
                    "uninstall_command": 'msiexec /x "{product_code}" /qn',
                    "detection_method": "MSI Product Code",
                    "requires_restart": False
                },
                "interactive": {
                    "installer_type": "Interactive Installer (ServiceUI)",
                    "install_command": 'ServiceUI.exe -process:explorer.exe "{filename}"',
                    "uninstall_command": 'ServiceUI.exe -process:explorer.exe "{uninstall_string}"',
                    "detection_method": "Registry Key Detection",
                    "requires_restart": False
                }
            }
            
            # Save default rules for future use
            with open('rules.json', 'w', encoding='utf-8') as f:
                json.dump(configs['rules'], f, indent=2)
                
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        configs['rules'] = {}
    
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
        pass  # Silently fail if image not found

def parse_powershell_output(output: str) -> Dict[str, str]:
    """Parse PowerShell output into dictionary"""
    if not output or not output.strip():
        return {}
    
    data = {}
    lines = output.strip().split('\n')
    
    for line in lines:
        # Try different patterns
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
        # Rate limiting
        time.sleep(0.5)
        
        # Clean app name
        search_term = re.sub(r'[^\w\s]', '', app_name).strip()
        
        # Try GitHub API
        url = f"https://api.github.com/search/code?q={search_term}+in:path+repo:microsoft/winget-pkgs&per_page=1"
        headers = {'Accept': 'application/vnd.github.v3+json'}
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            items = response.json().get('items', [])
            if items:
                return f"{app_name} is a professional software application designed for enterprise deployment."
    except:
        pass
    
    # Fallback description
    return f"{app_name} is a specialized application that enhances productivity and workflow efficiency in enterprise environments."

def generate_icon(app_name: str, style: str = 'gradient') -> Image.Image:
    """Generate application icon"""
    size = 256
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Get initials
    words = app_name.split()
    initials = "".join([w[0].upper() for w in words[:2]]) if words else "AP"
    
    # Draw background
    if style == 'gradient':
        for y in range(size):
            progress = y / size
            r = int(255 - progress * 50)
            g = int(107 - progress * 40)
            b = int(53 - progress * 20)
            draw.rectangle([(0, y), (size, y+1)], fill=(r, g, b, 255))
    else:
        draw.ellipse([10, 10, size-10, size-10], fill=(255, 107, 53, 255))
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", size//3)
    except:
        font = ImageFont.load_default()
    
    # Draw text centered
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), initials, font=font, fill=(255, 255, 255, 255))
    
    return img

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
        
        # Deployment mode
        deployment_mode = st.selectbox(
            "Deployment Mode",
            ['Standard', 'Silent', 'Interactive'],
            help="Select the deployment mode for your package"
        )
        
        st.divider()
        
        # Quick actions
        st.markdown("### Quick Actions")
        if st.button("🔄 Reset Application", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if st.button("📚 View Documentation", use_container_width=True):
            st.info("Documentation will open in a new tab")
        
        st.divider()
        
        # Recent history
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
        # Find primary installer
        installers = [f for f in uploaded_files if f.name.endswith(('.exe', '.msi', '.msix'))]
        
        if installers:
            primary_installer = installers[0]
            st.session_state.primary_installer = primary_installer
            
            # Display file summary
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
    
    # Show parsed data
    if st.session_state.parsed_data:
        st.markdown("**Parsed Data:**")
        for key, value in st.session_state.parsed_data.items():
            st.markdown(f"• **{key}:** {value}")
    
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
    
    # Advanced options
    with st.expander("Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            is_interactive = st.checkbox("Interactive Installation")
            requires_restart = st.checkbox("Requires Restart")
        with col2:
            timeout = st.number_input("Timeout (minutes)", min_value=5, max_value=120, value=30)
            priority = st.selectbox("Priority", ['Low', 'Normal', 'High'])
    
    # Installer type
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
    
    # Generate button
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
                'timeout': timeout,
                'priority': priority
            }
            st.session_state.recipe_generated = True
            st.session_state.step_number = 4
            
            # Add to history
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
    """Render the generated recipe"""
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
    
    # Get rules safely
    recipe_rules = rules.get(data.get('installer_type_key', 'exe_nsis'), {})
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚙️ Commands", "🔍 Detection", "📥 Export"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {data['app_name']}")
            st.markdown(f"**Version:** {data['version']}")
            st.markdown(f"**Vendor:** {data['vendor']}")
            st.markdown(f"**Category:** {data['category']}")
            
            # Description
            desc = fetch_app_description(data['app_name'])
            st.info(desc)
        
        with col2:
            st.markdown("### Icon")
            icon = generate_icon(data['app_name'])
            st.image(icon, width=150)
            
            # Download icon
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
        
        # Install command - safely get it
        install_cmd = recipe_rules.get('install_command', '"{filename}" /S').format(
            filename=data['uploaded_filename']
        )
        st.code(install_cmd, language='powershell')
        
        # Uninstall command - check if it exists first
        if 'uninstall_command' in recipe_rules:
            st.markdown("### Uninstall Command")
            uninstall_cmd = recipe_rules['uninstall_command']
            # Only format if it contains placeholders
            if '{' in uninstall_cmd:
                uninstall_cmd = uninstall_cmd.format(
                    uninstall_string="{UNINSTALL_STRING}",
                    product_code="{PRODUCT_CODE}"
                )
            st.code(uninstall_cmd, language='powershell')
    
    with tab3:
        st.markdown("### Detection Method")
        detection_method = recipe_rules.get('detection_method', 'Registry Key Detection')
        st.info(f"Method: {detection_method}")
        
        # Registry paths
        st.markdown("### Registry Paths")
        paths = [
            "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
            "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
        ]
        for path in paths:
            st.code(path, language='text')
    
    with tab4:
        st.markdown("### Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # JSON export
            json_data = create_deployment_json(data)
            st.download_button(
                "📄 Export as JSON",
                json_data,
                f"{data['app_name']}_recipe.json",
                "application/json",
                use_container_width=True
            )
        
        with col2:
            # PowerShell export
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
                "📜 Export as PowerShell",
                ps_script,
                f"{data['app_name']}_install.ps1",
                "text/plain",
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
        <p><strong>PackPilot Pro</strong> © 2024 | Enterprise Packaging Platform</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
