"""
PackPilot Pro - Enterprise Software Packaging Automation Platform
Version 3.0 - Enhanced with Auto-Extraction & Better UI
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
import subprocess
import tempfile
import zipfile
import struct
import platform

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

/* =========================== COPY BUTTON STYLES =========================== */
.copy-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 5px 12px;
    font-size: 12px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-left: 10px;
}

.copy-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.copy-button.copied {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
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

/* =========================== OUTPUT VALUE CONTAINER =========================== */
.output-value-container {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 12px;
    margin: 8px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.output-value {
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 14px;
    color: #495057;
    flex-grow: 1;
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
    color: #F0F0F0 !important;
    border: 2px solid #FF6B35 !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    font-family: 'Consolas', 'Monaco', monospace !important;
    line-height: 1.5 !important;
}

/* =========================== RESPONSIVE ADJUSTMENTS =========================== */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem; }
    .custom-card { padding: 1.5rem; }
    .main .block-container { padding: 1rem; }
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
        'auto_extracted_data': {},
        'extraction_method': 'manual'
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# ENHANCED ICON GENERATION WITH HIGH QUALITY
# ============================================================================

def generate_high_quality_icon(app_name: str, style: str = 'modern') -> Image.Image:
    """Generate high-quality application icon with modern design"""
    size = 512  # Higher resolution for better quality
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    if style == 'modern':
        # Create circular gradient
        center_x, center_y = size // 2, size // 2
        max_radius = size // 2
        
        for radius in range(max_radius, 0, -2):
            progress = (max_radius - radius) / max_radius
            
            # Gradient colors
            r = int(255 - progress * 50)
            g = int(107 - progress * 40) 
            b = int(53 - progress * 20)
            alpha = int(255 - progress * 30)
            
            draw.ellipse(
                [center_x - radius, center_y - radius, 
                 center_x + radius, center_y + radius],
                fill=(r, g, b, alpha)
            )
    
    # Add glass effect overlay
    overlay = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Top highlight
    overlay_draw.ellipse(
        [size//4, size//6, 3*size//4, size//2],
        fill=(255, 255, 255, 50)
    )
    
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # Get initials with better logic
    words = app_name.split()
    if len(words) >= 2:
        initials = words[0][0].upper() + words[1][0].upper()
    elif len(words) == 1 and len(words[0]) >= 2:
        initials = words[0][:2].upper()
    else:
        initials = app_name[:2].upper() if app_name else "AP"
    
    # Add text with shadow effect
    try:
        # Try to use a better font
        font_size = size // 3
        try:
            # Try different font paths
            font_paths = [
                "C:/Windows/Fonts/Arial.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            ]
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    break
            if not font:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
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
        
    except Exception as e:
        # Fallback to simple text
        draw.text((size//3, size//3), initials, fill=(255, 255, 255, 255))
    
    # Apply subtle blur for smoothness
    img = img.filter(ImageFilter.SMOOTH_MORE)
    
    # Resize to standard icon size with high quality
    img = img.resize((256, 256), Image.Resampling.LANCZOS)
    
    return img

# ============================================================================
# COPY TO CLIPBOARD FUNCTIONALITY
# ============================================================================

def create_copy_button(text: str, button_key: str) -> None:
    """Create a copy to clipboard button with JavaScript"""
    copy_js = f"""
    <script>
    function copyToClipboard_{button_key}() {{
        const text = `{text}`;
        navigator.clipboard.writeText(text).then(function() {{
            document.getElementById('btn_{button_key}').classList.add('copied');
            document.getElementById('btn_{button_key}').innerText = '✓ Copied!';
            setTimeout(function() {{
                document.getElementById('btn_{button_key}').classList.remove('copied');
                document.getElementById('btn_{button_key}').innerText = '📋 Copy';
            }}, 2000);
        }});
    }}
    </script>
    <button id="btn_{button_key}" class="copy-button" onclick="copyToClipboard_{button_key}()">📋 Copy</button>
    """
    st.markdown(copy_js, unsafe_allow_html=True)

def display_copiable_output(label: str, value: str, key: str) -> None:
    """Display output with copy button"""
    st.markdown(f"""
    <div class="output-value-container">
        <div>
            <strong>{label}:</strong>
            <span class="output-value">{value}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    create_copy_button(value, key)

# ============================================================================
# AUTOMATIC INSTALLER DATA EXTRACTION
# ============================================================================

class InstallerExtractor:
    """Automatic extraction of installer metadata without Windows Sandbox"""
    
    @staticmethod
    def extract_msi_info(file_content: bytes) -> Dict[str, str]:
        """Extract information from MSI files"""
        try:
            import tempfile
            import subprocess
            
            # Save MSI temporarily
            with tempfile.NamedTemporaryFile(suffix='.msi', delete=False) as tmp:
                tmp.write(file_content)
                tmp_path = tmp.name
            
            extracted_data = {}
            
            # Try to use msiexec to query the MSI
            if platform.system() == 'Windows':
                # PowerShell command to extract MSI properties
                ps_script = f"""
                $msi = New-Object -ComObject WindowsInstaller.Installer
                $database = $msi.GetType().InvokeMember('OpenDatabase', 'InvokeMethod', $null, $msi, @('{tmp_path}', 0))
                $query = "SELECT Property, Value FROM Property WHERE Property IN ('ProductName', 'Manufacturer', 'ProductVersion', 'ProductCode')"
                $view = $database.GetType().InvokeMember('OpenView', 'InvokeMethod', $null, $database, $query)
                $view.GetType().InvokeMember('Execute', 'InvokeMethod', $null, $view, $null)
                
                while ($record = $view.GetType().InvokeMember('Fetch', 'InvokeMethod', $null, $view, $null)) {{
                    $prop = $record.GetType().InvokeMember('StringData', 'GetProperty', $null, $record, 1)
                    $val = $record.GetType().InvokeMember('StringData', 'GetProperty', $null, $record, 2)
                    Write-Output "$prop=$val"
                }}
                """
                
                result = subprocess.run(['powershell', '-Command', ps_script], 
                                      capture_output=True, text=True)
                
                for line in result.stdout.split('\n'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        extracted_data[key.strip()] = value.strip()
            
            # Clean up
            os.unlink(tmp_path)
            
            return {
                'AppName': extracted_data.get('ProductName', 'Unknown'),
                'Publisher': extracted_data.get('Manufacturer', 'Unknown'),
                'Version': extracted_data.get('ProductVersion', '1.0.0'),
                'ProductCode': extracted_data.get('ProductCode', ''),
                'InstallerType': 'MSI'
            }
            
        except Exception as e:
            return {'Error': str(e)}
    
    @staticmethod
    def extract_exe_info(file_content: bytes) -> Dict[str, str]:
        """Extract information from EXE files using various methods"""
        try:
            extracted_data = {}
            
            # Try to identify installer type by signature
            if b'Nullsoft' in file_content[:10000]:
                extracted_data['InstallerType'] = 'NSIS'
            elif b'Inno Setup' in file_content[:10000]:
                extracted_data['InstallerType'] = 'Inno Setup'
            elif b'InstallShield' in file_content[:10000]:
                extracted_data['InstallerType'] = 'InstallShield'
            else:
                extracted_data['InstallerType'] = 'Generic EXE'
            
            # Try to extract version info (Windows only)
            if platform.system() == 'Windows':
                import tempfile
                
                with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as tmp:
                    tmp.write(file_content)
                    tmp_path = tmp.name
                
                ps_script = f"""
                $file = Get-Item '{tmp_path}'
                $versionInfo = $file.VersionInfo
                Write-Output "ProductName=$($versionInfo.ProductName)"
                Write-Output "CompanyName=$($versionInfo.CompanyName)"
                Write-Output "FileVersion=$($versionInfo.FileVersion)"
                Write-Output "ProductVersion=$($versionInfo.ProductVersion)"
                """
                
                result = subprocess.run(['powershell', '-Command', ps_script],
                                      capture_output=True, text=True)
                
                for line in result.stdout.split('\n'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if key == 'ProductName':
                            extracted_data['AppName'] = value.strip()
                        elif key == 'CompanyName':
                            extracted_data['Publisher'] = value.strip()
                        elif key in ['FileVersion', 'ProductVersion']:
                            extracted_data['Version'] = value.strip()
                
                os.unlink(tmp_path)
            
            return extracted_data or {
                'AppName': 'Unknown Application',
                'Publisher': 'Unknown Publisher',
                'Version': '1.0.0',
                'InstallerType': extracted_data.get('InstallerType', 'Generic EXE')
            }
            
        except Exception as e:
            return {'Error': str(e)}
    
    @staticmethod
    def extract_from_filename(filename: str) -> Dict[str, str]:
        """Extract basic info from filename patterns"""
        data = {}
        
        # Try to extract version from filename
        version_patterns = [
            r'v?(\d+\.\d+\.\d+)',
            r'v?(\d+\.\d+)',
            r'_(\d+\.\d+\.\d+)',
            r'-(\d+\.\d+\.\d+)'
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                data['Version'] = match.group(1)
                break
        
        # Try to extract app name
        app_name = filename.split('.')[0]
        app_name = re.sub(r'[-_]?v?\d+\.\d+.*', '', app_name)
        app_name = re.sub(r'[-_]', ' ', app_name)
        data['AppName'] = app_name.strip()
        
        # Architecture detection
        if 'x64' in filename or '64bit' in filename or 'amd64' in filename:
            data['Architecture'] = '64-bit'
        elif 'x86' in filename or '32bit' in filename or 'i386' in filename:
            data['Architecture'] = '32-bit'
        
        return data

# ============================================================================
# CONFIGURATION LOADER
# ============================================================================

@st.cache_data(ttl=3600)
def load_configuration_files():
    """Load and validate all configuration files"""
    configs = {}
    
    try:
        if os.path.exists('rules.json'):
            with open('rules.json', 'r', encoding='utf-8') as f:
                configs['rules'] = json.load(f)
        else:
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
            
            with open('rules.json', 'w', encoding='utf-8') as f:
                json.dump(configs['rules'], f, indent=2)
                
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        configs['rules'] = {}
    
    return configs

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_header():
    """Render application header"""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">📦 PackPilot Pro</h1>
        <p class="hero-subtitle">Intelligent Software Packaging Platform with Auto-Extraction</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar with tools"""
    with st.sidebar:
        st.markdown("## 🛠️ Tools & Options")
        
        # Extraction method
        extraction_method = st.selectbox(
            "Data Extraction Method",
            ['Automatic (Recommended)', 'Manual (PowerShell)', 'Hybrid'],
            help="Choose how to extract installer metadata"
        )
        st.session_state.extraction_method = extraction_method
        
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
    """Render file upload section with auto-extraction"""
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
            
            # Auto-extraction if enabled
            if st.session_state.extraction_method in ['Automatic (Recommended)', 'Hybrid']:
                with st.spinner("🔍 Extracting installer metadata automatically..."):
                    extractor = InstallerExtractor()
                    
                    # Read file content
                    file_content = primary_installer.read()
                    primary_installer.seek(0)  # Reset file pointer
                    
                    # Extract based on file type
                    if primary_installer.name.endswith('.msi'):
                        extracted = extractor.extract_msi_info(file_content)
                    else:
                        extracted = extractor.extract_exe_info(file_content)
                    
                    # Also extract from filename
                    filename_data = extractor.extract_from_filename(primary_installer.name)
                    
                    # Merge data
                    final_data = {**filename_data, **extracted}
                    
                    if 'Error' not in final_data:
                        st.session_state.auto_extracted_data = final_data
                        st.session_state.parsed_data = final_data
                        st.success("✅ Metadata extracted automatically!")
                        
                        # Display extracted data with copy buttons
                        st.markdown("### Extracted Information")
                        for key, value in final_data.items():
                            display_copiable_output(key, str(value), f"extract_{key}")
                        
                        st.session_state.step_number = 3
                    else:
                        st.warning("⚠️ Automatic extraction failed. Please use manual method.")
                        st.session_state.step_number = 2
            else:
                st.session_state.step_number = 2
    
    st.markdown("</div>", unsafe_allow_html=True)
    return primary_installer

def render_parse_section():
    """Render PowerShell parsing section for manual extraction"""
    if st.session_state.extraction_method == 'Automatic (Recommended)' and st.session_state.auto_extracted_data:
        return  # Skip if auto-extraction succeeded
    
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">⚙️</span>
            <span class="card-title">Step 2: Import Metadata (Manual)</span>
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
                    
                    # Display with copy buttons
                    for key, value in parsed.items():
                        display_copiable_output(key, str(value), f"parse_{key}")
                    
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
        architecture = st.selectbox("Architecture", 
                                   ['64-bit', '32-bit', 'Any'],
                                   index=['64-bit', '32-bit', 'Any'].index(data.get('Architecture', '64-bit')))
        install_context = st.selectbox("Install Context", 
                                      ['System', 'User'],
                                      index=['System', 'User'].index(data.get('InstallContext', 'System')))
        category = st.selectbox("Category", ['Productivity', 'Development', 'Security', 'Utilities'])
    
    # Advanced options
    with st.expander("Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            is_interactive = st.checkbox("Interactive Installation")
            requires_restart = st.checkbox("Requires Restart")
            create_shortcut = st.checkbox("Create Desktop Shortcut", value=True)
        with col2:
            timeout = st.number_input("Timeout (minutes)", min_value=5, max_value=120, value=30)
            priority = st.selectbox("Priority", ['Low', 'Normal', 'High'])
    
    # Installer type detection
    configs = load_configuration_files()
    rules = configs.get('rules', {})
    
    if is_interactive:
        installer_type_key = 'interactive'
    else:
        # Check auto-extracted installer type first
        auto_type = st.session_state.auto_extracted_data.get('InstallerType', '')
        
        if 'MSI' in auto_type:
            installer_type_key = 'msi'
        elif 'NSIS' in auto_type:
            installer_type_key = 'exe_nsis'
        elif 'Inno' in auto_type:
            installer_type_key = 'exe_inno'
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
                'create_shortcut': create_shortcut,
                'timeout': timeout,
                'priority': priority,
                'product_code': data.get('ProductCode', '')
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
    
    # Get rules with defaults
    default_rules = {
        'installer_type': 'Generic Installer',
        'install_command': '"{filename}" /S',
        'uninstall_command': '"{uninstall_string}" /S',
        'detection_method': 'Registry Key Detection',
        'requires_restart': False
    }
    
    recipe_rules = rules.get(data.get('installer_type_key', 'exe_nsis'), default_rules)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚙️ Commands", "🔍 Detection", "📥 Export"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {data['app_name']}")
            display_copiable_output("Version", data['version'], "recipe_version")
            display_copiable_output("Vendor", data['vendor'], "recipe_vendor")
            display_copiable_output("Category", data['category'], "recipe_category")
            
            # Generate and display description
            desc = f"{data['app_name']} is a professional software application designed for enterprise deployment."
            st.info(desc)
        
        with col2:
            st.markdown("### Icon")
            icon = generate_high_quality_icon(data['app_name'])
            st.image(icon, width=200)
            
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
        
        # Install command
        install_cmd = recipe_rules.get('install_command', '"{filename}" /S')
        install_cmd = install_cmd.replace('{filename}', data['uploaded_filename'])
        
        st.code(install_cmd, language='powershell')
        create_copy_button(install_cmd, "install_cmd")
        
        # Uninstall command
        if 'uninstall_command' in recipe_rules:
            st.markdown("### Uninstall Command")
            uninstall_cmd = recipe_rules['uninstall_command']
            
            if data.get('product_code'):
                uninstall_cmd = uninstall_cmd.replace('{product_code}', data['product_code'])
            else:
                uninstall_cmd = uninstall_cmd.replace('{uninstall_string}', '{UNINSTALL_STRING}')
                uninstall_cmd = uninstall_cmd.replace('{product_code}', '{PRODUCT_CODE}')
            
            st.code(uninstall_cmd, language='powershell')
            create_copy_button(uninstall_cmd, "uninstall_cmd")
        
        # Additional commands
        if data.get('create_shortcut'):
            st.markdown("### Create Shortcut Command")
            shortcut_cmd = f'$WshShell = New-Object -comObject WScript.Shell\n$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\\Desktop\\{data["app_name"]}.lnk")'
            st.code(shortcut_cmd, language='powershell')
            create_copy_button(shortcut_cmd, "shortcut_cmd")
    
    with tab3:
        st.markdown("### Detection Method")
        detection_method = recipe_rules.get('detection_method', 'Registry Key Detection')
        st.info(f"Method: {detection_method}")
        
        # Registry paths
        st.markdown("### Registry Paths")
        reg_paths = [
            "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
            "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
        ]
        
        for i, path in enumerate(reg_paths):
            st.code(path, language='text')
            create_copy_button(path, f"reg_path_{i}")
        
        # Product code if available
        if data.get('product_code'):
            st.markdown("### Product Code")
            display_copiable_output("Product Code", data['product_code'], "product_code")
    
    with tab4:
        st.markdown("### Export Options")
        
        col1, col2, col3 = st.columns(3)
        
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
# Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

$AppName = "{data['app_name']}"
$Version = "{data['version']}"
$Installer = "{data['uploaded_filename']}"

Write-Host "Installing $AppName v$Version..." -ForegroundColor Green

# Installation
{install_cmd}

# Verification
$installed = Get-WmiObject -Class Win32_Product | Where-Object {{$_.Name -like "*$AppName*"}}
if ($installed) {{
    Write-Host "✅ Installation successful!" -ForegroundColor Green
}} else {{
    Write-Host "❌ Installation may have failed. Please verify." -ForegroundColor Red
}}
"""
            st.download_button(
                "📜 Export as PowerShell",
                ps_script,
                f"{data['app_name']}_install.ps1",
                "text/plain",
                use_container_width=True
            )
        
        with col3:
            # Batch file export
            batch_script = f"""
@echo off
title Installing {data['app_name']} v{data['version']}
echo Installing {data['app_name']} v{data['version']}...
{install_cmd.replace('/', '-')}
echo Installation complete!
pause
"""
            st.download_button(
                "📝 Export as Batch",
                batch_script,
                f"{data['app_name']}_install.bat",
                "text/plain",
                use_container_width=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

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

def create_deployment_json(data: Dict) -> str:
    """Create deployment package JSON"""
    package = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'version': '1.0.0',
            'packager': 'PackPilot Pro',
            'extraction_method': st.session_state.extraction_method
        },
        'application': {
            'name': data.get('app_name', ''),
            'vendor': data.get('vendor', ''),
            'version': data.get('version', ''),
            'architecture': data.get('architecture', '64-bit'),
            'context': data.get('install_context', 'System'),
            'product_code': data.get('product_code', '')
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
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Info banner for new features
    if st.session_state.extraction_method == 'Automatic (Recommended)':
        st.info("🎯 **Auto-Extraction Mode**: Upload your installer and metadata will be extracted automatically!")
    
    # Main workflow
    primary_installer = render_upload_section()
    
    if primary_installer:
        # Only show manual parse if not using automatic extraction
        if st.session_state.extraction_method != 'Automatic (Recommended)' or not st.session_state.auto_extracted_data:
            render_parse_section()
        
        if st.session_state.parsed_data:
            if render_configuration_section(primary_installer):
                render_recipe_output()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666;">
        <p><strong>PackPilot Pro v3.0</strong> © 2024 | Enterprise Packaging Platform</p>
        <p>Features: Auto-Extraction | High-Quality Icons | Easy Copy Functions</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
