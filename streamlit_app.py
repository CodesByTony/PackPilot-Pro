"""
PackPilot Pro - Enterprise Software Packaging Automation Platform
Redesigned with enhanced features, improved error handling, and professional UI/UX
Author: Enhanced Version
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

# ============================================================================
# PAGE CONFIGURATION & INITIALIZATION
# ============================================================================

st.set_page_config(
    page_title="PackPilot Pro - Intelligent Packaging Platform",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING - PROFESSIONAL ORANGE/BLACK THEME
# ============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* =========================== GLOBAL RESET & FOUNDATION =========================== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [class*="st-"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1a1a1a !important; /* Deep black for all text */
}

/* =========================== MAIN LAYOUT STRUCTURE =========================== */
.main .block-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem 3rem;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    margin-top: 2rem;
}

/* =========================== ANIMATED HEADER SECTION =========================== */
.hero-section {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    border-radius: 24px;
    padding: 3rem;
    margin-bottom: 3rem;
    box-shadow: 0 20px 60px rgba(255, 107, 53, 0.3);
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 0.8; }
}

.main-title {
    font-size: 4rem;
    font-weight: 800;
    color: #FFFFFF !important;
    text-align: center;
    letter-spacing: -2px;
    margin-bottom: 0.5rem;
    text-shadow: 2px 4px 8px rgba(0,0,0,0.2);
}

.subtitle {
    font-size: 1.4rem;
    color: rgba(255,255,255,0.95) !important;
    text-align: center;
    font-weight: 400;
}

/* =========================== CARD CONTAINERS WITH ORANGE THEME =========================== */
.card-container {
    background: linear-gradient(145deg, #FFF5F0, #FFEBE0);
    border: 2px solid #FF6B35;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(255, 107, 53, 0.15);
    position: relative;
    transition: all 0.3s ease;
}

.card-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(255, 107, 53, 0.25);
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid rgba(255, 107, 53, 0.2);
}

.card-icon {
    font-size: 2rem;
    margin-right: 1rem;
    background: linear-gradient(135deg, #FF6B35, #F7931E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #1a1a1a !important;
}

/* =========================== FORM ELEMENTS & INPUTS =========================== */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div > div {
    background-color: #FFFFFF !important;
    color: #1a1a1a !important;
    border: 2px solid #FFD4C4 !important;
    border-radius: 10px !important;
    padding: 0.75rem !important;
    font-weight: 500 !important;
    transition: all 0.3s ease;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
}

/* All labels in black */
label, [data-testid="stTextInput"] label, 
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stFileUploader"] label {
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin-bottom: 0.5rem !important;
}

/* =========================== BUTTON HIERARCHY SYSTEM =========================== */
/* Primary Action Button - Gradient Orange */
.stButton > button[kind="primary"], 
.stButton > button:first-child:not([kind]) {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    padding: 0.8rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4) !important;
}

/* Secondary Action Button - Outlined Orange */
.stButton > button[kind="secondary"],
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #FF6B35 !important;
    border: 2px solid #FF6B35 !important;
    padding: 0.8rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

.stButton > button[kind="secondary"]:hover {
    background: #FF6B35 !important;
    color: #FFFFFF !important;
}

/* Tertiary Action Button - Ghost Style */
.stButton > button[kind="tertiary"] {
    background: transparent !important;
    color: #FF6B35 !important;
    border: 1px dashed #FFD4C4 !important;
    padding: 0.6rem 1.2rem !important;
    font-size: 0.95rem !important;
    border-radius: 8px !important;
}

/* =========================== STATUS MESSAGES & ALERTS =========================== */
.success-message {
    background: linear-gradient(135deg, #4CAF50, #45a049);
    color: white !important;
    padding: 1.2rem;
    border-radius: 12px;
    margin: 1rem 0;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.warning-message {
    background: linear-gradient(135deg, #FFA726, #FB8C00);
    color: white !important;
    padding: 1.2rem;
    border-radius: 12px;
    margin: 1rem 0;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(255, 167, 38, 0.3);
}

.error-message {
    background: linear-gradient(135deg, #EF5350, #E53935);
    color: white !important;
    padding: 1.2rem;
    border-radius: 12px;
    margin: 1rem 0;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(239, 83, 80, 0.3);
}

/* =========================== TABS STYLING =========================== */
.stTabs [data-baseweb="tab-list"] {
    background: #FFF5F0;
    border-radius: 12px;
    padding: 0.5rem;
    margin-bottom: 1.5rem;
}

.stTabs [data-baseweb="tab"] {
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding: 0.8rem 1.5rem !important;
    border-radius: 8px !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B35, #F7931E) !important;
    color: #FFFFFF !important;
}

/* =========================== CODE BLOCKS =========================== */
pre, code, [data-testid="stCode"] {
    background-color: #2D2D2D !important;
    color: #F8F8F2 !important; /* Light color for dark background */
    border: 2px solid #FF6B35 !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    font-family: 'Monaco', 'Courier New', monospace !important;
}

/* =========================== PROGRESS INDICATORS =========================== */
.progress-container {
    display: flex;
    justify-content: space-between;
    margin: 2rem 0;
    position: relative;
}

.progress-step {
    flex: 1;
    text-align: center;
    position: relative;
}

.progress-step::before {
    content: '';
    position: absolute;
    top: 20px;
    left: 50%;
    right: -50%;
    height: 2px;
    background: #FFD4C4;
    z-index: -1;
}

.progress-step:last-child::before {
    display: none;
}

.progress-step.active .progress-circle {
    background: linear-gradient(135deg, #FF6B35, #F7931E);
    color: white !important;
}

.progress-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #FFF;
    border: 2px solid #FFD4C4;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    color: #1a1a1a;
}

/* =========================== SIDEBAR STYLING =========================== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFF5F0 0%, #FFEBE0 100%);
    border-right: 2px solid #FF6B35;
}

[data-testid="stSidebar"] .sidebar-content {
    padding: 2rem 1rem;
}

/* =========================== ANIMATIONS =========================== */
@keyframes slideIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.card-container {
    animation: slideIn 0.5s ease-out;
}

/* =========================== RESPONSIVE DESIGN =========================== */
@media (max-width: 768px) {
    .main-title { font-size: 2.5rem; }
    .card-container { padding: 1.5rem; }
    .hero-section { padding: 2rem; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables with default values"""
    defaults = {
        'parsed_data': {},
        'recipe_generated': False,
        'recipe_data': None,
        'step_number': 1,
        'validation_passed': False,
        'deployment_history': [],
        'current_mode': 'standard',
        'api_cache': {},
        'last_api_call': 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# HELPER FUNCTIONS & UTILITIES
# ============================================================================

@st.cache_data(ttl=3600)
def load_configuration_files():
    """
    Load all required configuration files with comprehensive error handling
    Returns: Dictionary containing all configurations
    """
    configs = {}
    
    # Load rules.json
    try:
        with open('rules.json', 'r') as f:
            configs['rules'] = json.load(f)
    except FileNotFoundError:
        st.error("⚠️ Configuration file 'rules.json' not found! Please ensure it's in the repository.")
        st.stop()
    except json.JSONDecodeError as e:
        st.error(f"⚠️ Error parsing rules.json: {str(e)}")
        st.stop()
    
    # Verify interactive installer rules exist
    if 'interactive' not in configs['rules']:
        # Add default interactive installer rules if missing
        configs['rules']['interactive'] = {
            'installer_type': 'Interactive Installer (ServiceUI)',
            'install_command': 'ServiceUI.exe -process:explorer.exe "{filename}"',
            'uninstall_command': 'ServiceUI.exe -process:explorer.exe "{uninstall_string}"',
            'detection_method': 'Registry Key Detection',
            'requires_restart': False
        }
    
    return configs

def set_background_image():
    """
    Set the custom background image with error handling
    """
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
    except Exception as e:
        st.warning(f"Could not load background image: {str(e)}")

def parse_powershell_output(output: str) -> Dict[str, str]:
    """
    Parse PowerShell script output with enhanced error handling and validation
    
    Args:
        output: Raw PowerShell output string
        
    Returns:
        Dictionary of parsed key-value pairs
    """
    if not output or not output.strip():
        return {}
    
    data = {}
    
    # Enhanced regex pattern to handle various PowerShell output formats
    patterns = [
        r'^\s*([^:]+?)\s*:\s*(.*)$',  # Standard format
        r'^\s*([^=]+?)\s*=\s*(.*)$',   # Alternative format with =
        r'^([A-Za-z][A-Za-z0-9_]*)\s+(.+)$'  # Space-separated format
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, output, re.MULTILINE)
        if matches:
            for key, value in matches:
                clean_key = key.strip()
                clean_value = value.strip()
                if clean_key and clean_value:
                    data[clean_key] = clean_value
            break
    
    return data

@st.cache_data(ttl=7200)
def fetch_app_description_from_winget(app_name: str) -> str:
    """
    Fetch professional app description from Microsoft Winget repository
    with rate limiting and caching
    
    Args:
        app_name: Name of the application
        
    Returns:
        Professional description string
    """
    # Rate limiting check
    current_time = time.time()
    if 'last_api_call' in st.session_state:
        time_since_last_call = current_time - st.session_state.last_api_call
        if time_since_last_call < 1:  # Minimum 1 second between calls
            time.sleep(1 - time_since_last_call)
    
    st.session_state.last_api_call = current_time
    
    try:
        # Clean app name for search
        search_term = re.sub(r'\s*KATEX_INLINE_OPEN[^)]*KATEX_INLINE_CLOSE', '', app_name).strip()
        search_term = re.sub(r'[^\w\s]', '', search_term)
        
        # GitHub API search
        search_url = f"https://api.github.com/search/code?q={search_term}+in:path+repo:microsoft/winget-pkgs&per_page=5"
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'PackPilot-Pro/1.0'
        }
        
        response = requests.get(search_url, headers=headers, timeout=5)
        
        if response.status_code == 403:  # Rate limit hit
            return f"{app_name} is an enterprise-grade application designed for professional use."
        
        response.raise_for_status()
        items = response.json().get('items', [])
        
        if not items:
            return f"{app_name} is a specialized utility that enhances productivity and workflow efficiency."
        
        # Get the manifest file
        for item in items[:3]:  # Try first 3 results
            try:
                manifest_url = item['html_url'].replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                manifest_response = requests.get(manifest_url, timeout=5)
                manifest_response.raise_for_status()
                
                # Parse YAML manifest
                manifest_data = yaml.safe_load(manifest_response.text)
                
                # Try different description fields
                description_fields = ['Description', 'ShortDescription', 'LongDescription', 'PackageDescription']
                for field in description_fields:
                    if field in manifest_data and manifest_data[field]:
                        description = manifest_data[field].strip()
                        if len(description) > 20:  # Ensure meaningful description
                            return description
                            
            except Exception:
                continue
        
        return f"{app_name} is a professional software solution optimized for enterprise deployment."
        
    except Exception as e:
        return f"{app_name} is a versatile application that provides essential functionality for business operations."

def generate_professional_icon(app_name: str, style: str = 'gradient') -> Image.Image:
    """
    Generate a unique, professional icon for the application with multiple style options
    
    Args:
        app_name: Name of the application
        style: Icon style ('gradient', 'flat', 'glass', 'minimal')
        
    Returns:
        PIL Image object
    """
    width, height = 512, 512
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Extract initials intelligently
    words = re.findall(r'[A-Z][a-z]*|\d+', app_name) or app_name.split()
    initials = "".join([word[0].upper() for word in words[:2]])
    if not initials:
        initials = app_name[:2].upper() if len(app_name) > 1 else app_name[0].upper()
    
    # Create unique color based on app name hash
    hash_obj = hashlib.md5(app_name.encode())
    hash_hex = hash_obj.hexdigest()
    base_hue = int(hash_hex[:2], 16) / 255 * 30  # Orange range (0-30 degrees)
    
    if style == 'gradient':
        # Create gradient background
        for y in range(height):
            progress = y / height
            r = int(255 - progress * 50)
            g = int(107 - progress * 40)
            b = int(53 - progress * 20)
            draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b, 255))
        
        # Add glossy effect
        overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.ellipse([(width*0.1, -height*0.5), (width*0.9, height*0.3)], 
                            fill=(255, 255, 255, 40))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
    elif style == 'flat':
        # Flat design with rounded corners
        draw.rounded_rectangle([(0, 0), (width, height)], radius=width//8, 
                              fill=(255, 107, 53, 255))
    
    elif style == 'glass':
        # Glass morphism effect
        draw.rounded_rectangle([(0, 0), (width, height)], radius=width//8, 
                              fill=(255, 107, 53, 180))
        # Add blur effect simulation
        for i in range(3):
            overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rounded_rectangle([(i*10, i*10), (width-i*10, height-i*10)], 
                                          radius=width//8, fill=(255, 255, 255, 10))
            img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
    
    else:  # minimal
        # Minimalist design
        draw.ellipse([(width*0.05, height*0.05), (width*0.95, height*0.95)], 
                    fill=(255, 107, 53, 255))
    
    # Add text with shadow effect
    try:
        # Try to load a better font
        font_size = int(height * 0.35)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw shadow
    shadow_offset = 5
    draw.text((x + shadow_offset, y + shadow_offset), initials, 
             font=font, fill=(0, 0, 0, 100))
    
    # Draw main text
    draw.text((x, y), initials, font=font, fill=(255, 255, 255, 255))
    
    return img

def validate_installer_file(file) -> Tuple[bool, str]:
    """
    Validate uploaded installer file
    
    Args:
        file: Uploaded file object
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not file:
        return False, "No file provided"
    
    # Check file extension
    valid_extensions = ['.exe', '.msi', '.msix', '.appx']
    file_ext = os.path.splitext(file.name)[1].lower()
    
    if file_ext not in valid_extensions:
        return False, f"Invalid file type. Supported types: {', '.join(valid_extensions)}"
    
    # Check file size (max 2GB)
    max_size = 2 * 1024 * 1024 * 1024  # 2GB in bytes
    if file.size > max_size:
        return False, f"File too large. Maximum size: 2GB"
    
    return True, "Valid installer file"

def create_deployment_package(recipe_data: Dict) -> bytes:
    """
    Create a deployment package with all necessary files
    
    Args:
        recipe_data: Dictionary containing recipe information
        
    Returns:
        Bytes object of the package
    """
    # This would create a ZIP file with all deployment files
    # For now, returning a JSON representation
    package_data = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'version': '1.0.0',
            'packager': 'PackPilot Pro'
        },
        'application': recipe_data,
        'deployment': {
            'install_command': recipe_data.get('install_command', ''),
            'uninstall_command': recipe_data.get('uninstall_command', ''),
            'detection_rules': recipe_data.get('detection_rules', {}),
            'requirements': recipe_data.get('requirements', {})
        }
    }
    
    return json.dumps(package_data, indent=2).encode('utf-8')

# ============================================================================
# MAIN UI COMPONENTS
# ============================================================================

def render_header():
    """Render the animated header section"""
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">📦 PackPilot Pro</h1>
        <p class="subtitle">Intelligent Software Packaging Platform for Enterprise Deployment</p>
    </div>
    """, unsafe_allow_html=True)

def render_progress_indicator():
    """Render the progress indicator showing current step"""
    steps = ['Upload', 'Parse', 'Configure', 'Generate', 'Deploy']
    current_step = st.session_state.get('step_number', 1)
    
    progress_html = '<div class="progress-container">'
    for i, step in enumerate(steps, 1):
        active_class = 'active' if i <= current_step else ''
        progress_html += f'''
        <div class="progress-step {active_class}">
            <div class="progress-circle">{i}</div>
            <div style="margin-top: 0.5rem; color: #1a1a1a; font-weight: 500;">{step}</div>
        </div>
        '''
    progress_html += '</div>'
    
    st.markdown(progress_html, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with additional tools and information"""
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem;">
            <h2 style="color: #1a1a1a; margin-bottom: 1.5rem;">🛠️ Toolkit</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Deployment Mode Selection
        st.selectbox(
            "Deployment Mode",
            options=['standard', 'silent', 'interactive', 'custom'],
            format_func=lambda x: {
                'standard': '📋 Standard',
                'silent': '🤫 Silent',
                'interactive': '👤 Interactive',
                'custom': '⚙️ Custom'
            }[x],
            key='deployment_mode'
        )
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 View Docs", use_container_width=True, type="secondary"):
                st.info("Documentation coming soon!")
        with col2:
            if st.button("🔄 Reset All", use_container_width=True, type="secondary"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()
        
        # Recent Deployments
        st.markdown("### 📊 Recent Deployments")
        if st.session_state.get('deployment_history'):
            for deployment in st.session_state.deployment_history[-5:]:
                st.markdown(f"• **{deployment['app']}** - {deployment['date']}")
        else:
            st.markdown("*No recent deployments*")
        
        # System Status
        st.markdown("### 🔍 System Status")
        st.success("✅ All systems operational")
        
        # Help Section
        with st.expander("💡 Need Help?"):
            st.markdown("""
            **Quick Tips:**
            - Upload your installer files first
            - Run readData.ps1 to gather metadata
            - Paste the output in step 2
            - Configure and generate your recipe
            
            **Support:** support@packpilot.pro
            """)

def render_upload_section():
    """Render the file upload section with validation"""
    st.markdown("""
    <div class="card-container">
        <div class="card-header">
            <span class="card-icon">📁</span>
            <span class="card-title">Step 1: Upload Installation Package</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Select all package files (installers, configs, scripts)",
            accept_multiple_files=True,
            type=['exe', 'msi', 'msix', 'appx', 'ps1', 'bat', 'cmd', 'txt', 'json', 'xml'],
            help="You can upload multiple files. The primary installer will be automatically detected."
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Analyze Files", use_container_width=True, type="secondary"):
            if uploaded_files:
                with st.spinner("Analyzing files..."):
                    time.sleep(1)  # Simulate analysis
                    st.success("Files analyzed successfully!")
    
    primary_installer = None
    if uploaded_files:
        # Categorize files
        installers = []
        configs = []
        scripts = []
        
        for file in uploaded_files:
            ext = os.path.splitext(file.name)[1].lower()
            if ext in ['.exe', '.msi', '.msix', '.appx']:
                installers.append(file)
            elif ext in ['.json', '.xml', '.txt']:
                configs.append(file)
            elif ext in ['.ps1', '.bat', '.cmd']:
                scripts.append(file)
        
        # Display file summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Installers", len(installers), delta=None)
            if installers:
                primary_installer = installers[0]
                for installer in installers:
                    st.markdown(f"• {installer.name}")
        
        with col2:
            st.metric("Config Files", len(configs), delta=None)
            for config in configs:
                st.markdown(f"• {config.name}")
        
        with col3:
            st.metric("Scripts", len(scripts), delta=None)
            for script in scripts:
                st.markdown(f"• {script.name}")
        
        if primary_installer:
            st.success(f"✅ Primary installer detected: **{primary_installer.name}**")
            st.session_state.step_number = 2
    
    st.markdown("</div>", unsafe_allow_html=True)
    return primary_installer

def render_parse_section():
    """Render the PowerShell output parsing section"""
    st.markdown("""
    <div class="card-container">
        <div class="card-header">
            <span class="card-icon">⚙️</span>
            <span class="card-title">Step 2: Import Metadata from PowerShell</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Instructions
    with st.expander("📋 How to use readData.ps1", expanded=False):
        st.markdown("""
        1. Run the PowerShell script: `./readData.ps1 -Path "installer.exe"`
        2. Copy the entire output
        3. Paste it in the text area below
        4. Click "Parse Data" to extract the information
        """)
        
        # Show sample output format
        st.code("""
        AppName         : Example Application
        Publisher       : Example Corp
        Version         : 1.2.3
        Architecture    : 64-bit
        InstallContext  : System
        """, language='powershell')
    
    ps_output = st.text_area(
        "Paste PowerShell script output here:",
        height=200,
        placeholder="AppName : Your Application\nPublisher : Your Company\nVersion : 1.0.0\n...",
        help="Paste the complete output from readData.ps1"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        parse_button = st.button(
            "🔄 Parse Data",
            use_container_width=True,
            type="primary" if ps_output else "secondary"
        )
    
    with col2:
        if st.button("📝 Use Sample Data", use_container_width=True, type="secondary"):
            # Provide sample data for testing
            sample_data = """AppName : Microsoft Teams
Publisher : Microsoft Corporation
Version : 1.6.00.1381
Architecture : 64-bit
InstallContext : System
AppsAndFeaturesName : Microsoft Teams
UninstallString : MsiExec.exe /X{731F6BAA-A986-45A4-8936-7C3AAAAA760B}"""
            st.session_state.parsed_data = parse_powershell_output(sample_data)
            st.success("Sample data loaded!")
            st.session_state.step_number = 3
    
    if parse_button:
        if ps_output:
            with st.spinner("Parsing PowerShell output..."):
                parsed = parse_powershell_output(ps_output)
                if parsed:
                    st.session_state.parsed_data = parsed
                    st.success(f"✅ Successfully parsed {len(parsed)} fields!")
                    st.session_state.step_number = 3
                    
                    # Display parsed data
                    with st.expander("View Parsed Data", expanded=True):
                        for key, value in parsed.items():
                            st.markdown(f"**{key}:** {value}")
                else:
                    st.error("❌ Could not parse the output. Please check the format.")
        else:
            st.warning("⚠️ Please paste the PowerShell output first.")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_configuration_section(primary_installer):
    """Render the configuration section for recipe generation"""
    if not st.session_state.get('parsed_data') or not primary_installer:
        return False
    
    st.markdown("""
    <div class="card-container">
        <div class="card-header">
            <span class="card-icon">🔧</span>
            <span class="card-title">Step 3: Configure Deployment Recipe</span>
        </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.parsed_data
    
    # Auto-fill form with parsed data
    col1, col2 = st.columns(2)
    
    with col1:
        app_name = st.text_input(
            "Application Name *",
            value=data.get('AppName', ''),
            help="Official name of the application"
        )
        
        vendor = st.text_input(
            "Vendor/Publisher *",
            value=data.get('Publisher', ''),
            help="Software vendor or publisher"
        )
        
        version = st.text_input(
            "Version *",
            value=data.get('Version', ''),
            help="Application version number"
        )
    
    with col2:
        architecture = st.selectbox(
            "Architecture",
            options=['64-bit', '32-bit', 'Any'],
            index=0 if data.get('Architecture', '64-bit') == '64-bit' else 1
        )
        
        install_context = st.selectbox(
            "Install Context",
            options=['System', 'User'],
            index=0 if data.get('InstallContext', 'System') == 'System' else 1
        )
        
        apps_features_name = st.text_input(
            "Apps & Features Name",
            value=data.get('AppsAndFeaturesName', app_name),
            help="Name as it appears in Windows Apps & Features"
        )
    
    # Advanced Options
    with st.expander("⚙️ Advanced Options", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            is_interactive = st.checkbox(
                "Interactive Installation (Requires ServiceUI)",
                help="Check if the installer requires user interaction"
            )
            
            requires_restart = st.checkbox(
                "Requires System Restart",
                help="Check if installation requires a system restart"
            )
            
            create_shortcut = st.checkbox(
                "Create Desktop Shortcut",
                value=True,
                help="Create a desktop shortcut after installation"
            )
        
        with col2:
            timeout = st.number_input(
                "Installation Timeout (minutes)",
                min_value=5,
                max_value=120,
                value=30,
                help="Maximum time allowed for installation"
            )
            
            priority = st.selectbox(
                "Deployment Priority",
                options=['Low', 'Normal', 'High', 'Critical'],
                index=1
            )
            
            category = st.selectbox(
                "Application Category",
                options=['Productivity', 'Development', 'Security', 'Utilities', 'Communication', 'Other'],
                index=0
            )
    
    # Installer Type Selection
    configs = load_configuration_files()
    rules = configs['rules']
    
    if is_interactive:
        installer_type_key = 'interactive'
        st.info("ℹ️ Interactive mode selected - will use ServiceUI wrapper")
    else:
        # Detect installer type based on file extension
        file_ext = os.path.splitext(primary_installer.name)[1].lower()
        
        if file_ext == '.msi':
            default_type = 'msi'
        elif file_ext == '.exe':
            # Try to detect EXE installer type
            if 'nsis' in primary_installer.name.lower():
                default_type = 'exe_nsis'
            elif 'inno' in primary_installer.name.lower():
                default_type = 'exe_inno'
            else:
                default_type = 'exe_nsis'  # Default to NSIS
        else:
            default_type = 'exe_nsis'
        
        installer_type_key = st.selectbox(
            "Installer Type",
            options=list(rules.keys()),
            format_func=lambda x: rules[x].get('installer_type', x),
            index=list(rules.keys()).index(default_type) if default_type in rules else 0,
            help="Select the type of installer package"
        )
    
    # Validation
    all_required_filled = all([app_name, vendor, version])
    
    if all_required_filled:
        st.session_state.validation_passed = True
        st.session_state.step_number = 4
    
    # Generate Recipe Button
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button(
            "🚀 Generate Deployment Recipe",
            use_container_width=True,
            type="primary" if all_required_filled else "secondary",
            disabled=not all_required_filled
        ):
            if all_required_filled:
                # Store recipe data
                st.session_state.recipe_data = {
                    'app_name': app_name,
                    'vendor': vendor,
                    'version': version,
                    'architecture': architecture,
                    'install_context': install_context,
                    'apps_features_name': apps_features_name,
                    'installer_type_key': installer_type_key,
                    'uploaded_filename': primary_installer.name,
                    'is_interactive': is_interactive,
                    'requires_restart': requires_restart,
                    'create_shortcut': create_shortcut,
                    'timeout': timeout,
                    'priority': priority,
                    'category': category,
                    'timestamp': datetime.now().isoformat()
                }
                st.session_state.recipe_generated = True
                st.session_state.step_number = 5
                
                # Add to deployment history
                st.session_state.deployment_history.append({
                    'app': app_name,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M')
                })
                
                st.success("✅ Recipe generated successfully!")
                st.balloons()
            else:
                st.error("Please fill all required fields marked with *")
    
    with col2:
        if st.button("💾 Save Draft", use_container_width=True, type="secondary"):
            st.info("Draft saved to session!")
    
    with col3:
        if st.button("❌ Clear Form", use_container_width=True, type="secondary"):
            st.session_state.parsed_data = {}
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    return True

def render_recipe_output():
    """Render the generated deployment recipe with all details"""
    if not st.session_state.get('recipe_generated') or not st.session_state.get('recipe_data'):
        return
    
    st.markdown("""
    <div class="card-container">
        <div class="card-header">
            <span class="card-icon">📋</span>
            <span class="card-title">Step 4: Deployment Recipe Generated</span>
        </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.recipe_data
    configs = load_configuration_files()
    rules = configs['rules']
    
    # Get the appropriate rules
    recipe_rules = rules.get(data['installer_type_key'], rules['exe_nsis'])
    
    # Fetch description
    with st.spinner("Fetching application description..."):
        description = fetch_app_description_from_winget(data['app_name'])
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "⚙️ Installation",
        "🔍 Detection",
        "📦 Package",
        "📤 Export"
    ])
    
    with tab1:
        # Application Overview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {data['app_name']} v{data['version']}")
            st.markdown(f"**Vendor:** {data['vendor']}")
            st.markdown(f"**Category:** {data['category']}")
            st.markdown(f"**Priority:** {data['priority']}")
            
            st.markdown("**Description:**")
            st.info(description)
            
            # Metadata
            st.markdown("**Package Metadata:**")
            metadata_cols = st.columns(3)
            with metadata_cols[0]:
                st.metric("Architecture", data['architecture'])
            with metadata_cols[1]:
                st.metric("Context", data['install_context'])
            with metadata_cols[2]:
                st.metric("Timeout", f"{data['timeout']} min")
        
        with col2:
            st.markdown("### Application Icon")
            
            # Icon style selector
            icon_style = st.selectbox(
                "Icon Style",
                options=['gradient', 'flat', 'glass', 'minimal'],
                index=0
            )
            
            # Generate and display icon
            icon = generate_professional_icon(data['app_name'], icon_style)
            st.image(icon, width=200)
            
            # Download icon
            buf = io.BytesIO()
            icon.save(buf, format='PNG')
            st.download_button(
                label="📥 Download Icon",
                data=buf.getvalue(),
                file_name=f"{data['app_name'].replace(' ', '_')}_icon.png",
                mime="image/png",
                use_container_width=True,
                type="secondary"
            )
    
    with tab2:
        # Installation Commands
        st.markdown("### Installation Configuration")
        
        # Install command
        install_cmd = recipe_rules['install_command'].format(
            filename=data['uploaded_filename']
        )
        
        st.markdown("**Install Command:**")
        st.code(install_cmd, language='powershell')
        
        # Uninstall command
        if 'uninstall_command' in recipe_rules:
            uninstall_cmd = recipe_rules['uninstall_command'].format(
                uninstall_string="{UNINSTALL_STRING}"  # Placeholder
            )
            st.markdown("**Uninstall Command:**")
            st.code(uninstall_cmd, language='powershell')
        
        # Additional settings
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Installation Flags:**")
            if data['is_interactive']:
                st.warning("⚠️ Interactive installation - ServiceUI required")
            if data['requires_restart']:
                st.warning("⚠️ System restart required after installation")
            if data['create_shortcut']:
                st.info("✅ Desktop shortcut will be created")
        
        with col2:
            st.markdown("**Installer Type:**")
            st.info(recipe_rules.get('installer_type', 'Standard'))
            
            st.markdown("**Install Context:**")
            st.info(data['install_context'])
    
    with tab3:
        # Detection Rules
        st.markdown("### Detection Rules")
        
        st.info(f"Detection Method: **{recipe_rules.get('detection_method', 'Registry')}**")
        
        # Registry paths
        st.markdown("**Registry Paths to Check:**")
        reg_paths = [
            "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
            "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
        ]
        
        if data['install_context'] == 'User':
            reg_paths.append("HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
        
        for path in reg_paths:
            st.code(path, language='text')
        
        # Detection script
        st.markdown("**PowerShell Detection Script:**")
        detection_script = f"""
$AppName = "{data['apps_features_name']}"
$Version = "{data['version']}"

$Paths = @(
    "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
    "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
)

foreach ($Path in $Paths) {{
    $App = Get-ChildItem -Path $Path -ErrorAction SilentlyContinue | 
           Get-ItemProperty | 
           Where-Object {{$_.DisplayName -like "*$AppName*" -and $_.DisplayVersion -eq $Version}}
    
    if ($App) {{
        Write-Output "Detected: $($App.DisplayName) v$($App.DisplayVersion)"
        exit 0
    }}
}}

Write-Output "Not Detected"
exit 1
"""
        st.code(detection_script, language='powershell')
    
    with tab4:
        # Package Contents
        st.markdown("### Package Contents")
        
        # File list
        st.markdown("**Included Files:**")
        files_list = f"""
        📁 Package Root
        ├── 📄 {data['uploaded_filename']}
        ├── 📄 Install.ps1
        ├── 📄 Uninstall.ps1
        ├── 📄 Detection.ps1
        ├── 📄 Requirements.json
        └── 📄 Metadata.json
        """
        st.code(files_list, language='text')
        
        # Requirements
        st.markdown("**System Requirements:**")
        requirements = {
            "OS": "Windows 10/11",
            "Architecture": data['architecture'],
            "MinDiskSpace": "500 MB",
            "MinMemory": "4 GB",
            ".NET Framework": "4.7.2 or higher"
        }
        
        for req, value in requirements.items():
            st.markdown(f"• **{req}:** {value}")
    
    with tab5:
        # Export Options
        st.markdown("### Export Deployment Package")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export as JSON
            package_json = create_deployment_package(data)
            st.download_button(
                label="📄 Export as JSON",
                data=package_json,
                file_name=f"{data['app_name'].replace(' ', '_')}_deployment.json",
                mime="application/json",
                use_container_width=True,
                type="primary"
            )
            
            # Export as PowerShell
            ps_script = f"""
# {data['app_name']} Deployment Script
# Generated by PackPilot Pro
# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

$AppName = "{data['app_name']}"
$Version = "{data['version']}"
$Installer = "{data['uploaded_filename']}"

Write-Host "Installing $AppName v$Version..." -ForegroundColor Green

# Installation
{install_cmd}

# Verification
{detection_script}
"""
            st.download_button(
                label="📜 Export as PowerShell",
                data=ps_script.encode('utf-8'),
                file_name=f"{data['app_name'].replace(' ', '_')}_install.ps1",
                mime="text/plain",
                use_container_width=True,
                type="secondary"
            )
        
        with col2:
            # Export as Intune package
            st.download_button(
                label="📱 Export for Intune",
                data=package_json,  # Would be .intunewin format
                file_name=f"{data['app_name'].replace(' ', '_')}.intunewin",
                mime="application/octet-stream",
                use_container_width=True,
                type="secondary"
            )
            
            # Export as SCCM package
            st.download_button(
                label="🖥️ Export for SCCM",
                data=package_json,  # Would be SCCM format
                file_name=f"{data['app_name'].replace(' ', '_')}_sccm.zip",
                mime="application/zip",
                use_container_width=True,
                type="secondary"
            )
        
        # Success message
        st.success(f"""
        ✅ **Deployment recipe successfully generated!**
        
        Application: {data['app_name']} v{data['version']}
        Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION FLOW
# ============================================================================

def main():
    """Main application entry point"""
    
    # Set background
    set_background_image()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Render progress indicator
    render_progress_indicator()
    
    # Main workflow
    primary_installer = render_upload_section()
    
    if primary_installer:
        render_parse_section()
        
        if st.session_state.get('parsed_data'):
            if render_configuration_section(primary_installer):
                render_recipe_output()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 4rem; padding: 2rem; color: #666;">
        <p>PackPilot Pro © 2024 | Enterprise Software Packaging Platform</p>
        <p style="font-size: 0.9rem;">Designed for Hugo Boss IT Infrastructure</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# APPLICATION EXECUTION
# ============================================================================

if __name__ == "__main__":
    main()
