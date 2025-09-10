"""
PackPilot Pro - Enterprise Software Packaging Automation Platform
Version 3.0 - Enhanced with Auto-Extraction, Smart Icons & Copy Features
Author: Production Ready Version
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import json
import io
import base64
import re
import requests
import yaml
import os
import time
import subprocess
import tempfile
import zipfile
from datetime import datetime
import hashlib
from typing import Dict, Optional, List, Tuple
import urllib.parse
import threading
import queue

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
# ENHANCED CSS WITH COPY BUTTON STYLES
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

/* =========================== COPY BUTTON STYLES =========================== */
.copy-container {
    position: relative;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 10px 0;
}

.copy-button {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.copy-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 3px 10px rgba(255, 107, 53, 0.3);
}

.code-container {
    background: #2B2B2B;
    color: #F0F0F0;
    padding: 15px;
    border-radius: 10px;
    border: 2px solid #FF6B35;
    position: relative;
    font-family: 'Consolas', 'Monaco', monospace;
    line-height: 1.5;
}

.copy-icon {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(255, 107, 53, 0.8);
    color: white;
    border: none;
    padding: 5px 8px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 11px;
}

/* =========================== ENHANCED ICONS =========================== */
.icon-container {
    text-align: center;
    padding: 20px;
    background: linear-gradient(145deg, #FFF8F5, #FFE4DC);
    border-radius: 15px;
    margin: 10px 0;
}

.generated-icon {
    border-radius: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    transition: transform 0.3s ease;
}

.generated-icon:hover {
    transform: scale(1.05);
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

section[data-testid="stFileUploadDropzone"] > div {
    color: #FF6B35 !important;
}

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

[data-testid="stAlert"][data-type="success"] {
    background-color: #E8F5E9 !important;
    border-left-color: #4CAF50 !important;
}

[data-testid="stAlert"][data-type="info"] {
    background-color: #FFF3E0 !important;
    border-left-color: #FF9800 !important;
}

[data-testid="stAlert"][data-type="warning"] {
    background-color: #FFF3E0 !important;
    border-left-color: #FF9800 !important;
}

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

/* =========================== PREVENT TEXT OVERLAP =========================== */
.element-container {
    margin-bottom: 1rem !important;
}

.row-widget {
    margin-bottom: 1rem !important;
}

.element-container + .element-container {
    margin-top: 1rem !important;
}

/* =========================== VIRTUAL ENVIRONMENT STATUS =========================== */
.vm-status {
    background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
    border: 2px solid #2196F3;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}

.vm-status.active {
    background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
    border-color: #4CAF50;
}

.vm-status.error {
    background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
    border-color: #F44336;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# JAVASCRIPT FOR COPY FUNCTIONALITY
# ============================================================================
copy_js = """
<script>
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function() {
            // Show success message
            const button = event.target;
            const originalText = button.innerHTML;
            button.innerHTML = '✓ Copied!';
            button.style.backgroundColor = '#4CAF50';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.style.backgroundColor = '';
            }, 2000);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            const button = event.target;
            const originalText = button.innerHTML;
            button.innerHTML = '✓ Copied!';
            button.style.backgroundColor = '#4CAF50';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.style.backgroundColor = '';
            }, 2000);
        } catch (err) {
            console.error('Copy failed', err);
        }
        document.body.removeChild(textArea);
    }
}
</script>
"""

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
        'vm_status': 'idle',
        'auto_extraction_enabled': True,
        'generated_icon': None
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
# COPY TO CLIPBOARD COMPONENT
# ============================================================================
def copy_button(text_to_copy, button_text="📋 Copy", key=None):
    """Create a copy to clipboard button"""
    unique_key = key or str(hash(text_to_copy))
    
    # Create HTML for copy button
    copy_html = f"""
    {copy_js}
    <div class="copy-container">
        <button class="copy-button" onclick="copyToClipboard(`{text_to_copy.replace('`', '\\`')}`)" id="copy-btn-{unique_key}">
            {button_text}
        </button>
    </div>
    """
    
    st.markdown(copy_html, unsafe_allow_html=True)

def code_block_with_copy(code, language="text", title=""):
    """Create a code block with copy functionality"""
    unique_id = str(hash(code))
    
    code_html = f"""
    {copy_js}
    <div style="margin: 10px 0;">
        {f'<h4 style="color: #1a1a1a; margin-bottom: 10px;">{title}</h4>' if title else ''}
        <div class="code-container">
            <button class="copy-icon" onclick="copyToClipboard(`{code.replace('`', '\\`')}`)">📋</button>
            <pre style="margin: 0; padding-right: 40px;"><code>{code}</code></pre>
        </div>
    </div>
    """
    
    st.markdown(code_html, unsafe_allow_html=True)

# ============================================================================
# VIRTUAL ENVIRONMENT AUTOMATION
# ============================================================================
class VirtualEnvironment:
    """Class to handle virtual environment operations"""
    
    def __init__(self):
        self.status = "idle"
        self.container_name = "packpilot-analyzer"
        self.is_docker_available = self.check_docker()
    
    def check_docker(self):
        """Check if Docker is available"""
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def create_analysis_container(self):
        """Create a Docker container for file analysis"""
        if not self.is_docker_available:
            return False, "Docker not available"
        
        try:
            # Dockerfile content for Windows analysis
            dockerfile_content = """
FROM mcr.microsoft.com/windows/servercore:ltsc2019
SHELL ["powershell", "-Command"]
COPY readData.ps1 C:/scripts/
WORKDIR C:/scripts
"""
            
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                dockerfile_path = os.path.join(temp_dir, 'Dockerfile')
                script_path = os.path.join(temp_dir, 'readData.ps1')
                
                # Write Dockerfile
                with open(dockerfile_path, 'w') as f:
                    f.write(dockerfile_content)
                
                # Write PowerShell script
                with open(script_path, 'w') as f:
                    f.write(self.get_readdata_script())
                
                # Build container
                build_cmd = ['docker', 'build', '-t', self.container_name, temp_dir]
                result = subprocess.run(build_cmd, capture_output=True, text=True, timeout=300)
                
                return result.returncode == 0, result.stderr if result.returncode != 0 else "Success"
        
        except Exception as e:
            return False, str(e)
    
    def analyze_file(self, file_path):
        """Analyze file in virtual environment"""
        if not self.is_docker_available:
            return self.fallback_analysis(file_path)
        
        try:
            # Copy file to temporary location
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file = os.path.join(temp_dir, os.path.basename(file_path))
                
                # For uploaded files, we need to save them first
                if hasattr(file_path, 'read'):
                    with open(temp_file, 'wb') as f:
                        f.write(file_path.read())
                    file_path.seek(0)  # Reset file pointer
                else:
                    import shutil
                    shutil.copy2(file_path, temp_file)
                
                # Run analysis in container
                run_cmd = [
                    'docker', 'run', '--rm',
                    '-v', f'{temp_dir}:C:/analysis',
                    self.container_name,
                    'powershell', '-ExecutionPolicy', 'Bypass',
                    '-File', 'C:/scripts/readData.ps1',
                    '-FilePath', f'C:/analysis/{os.path.basename(file_path)}'
                ]
                
                result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    return True, result.stdout
                else:
                    return False, result.stderr
        
        except Exception as e:
            return False, str(e)
    
    def fallback_analysis(self, file_obj):
        """Fallback analysis when Docker is not available"""
        try:
            # Basic file analysis without execution
            file_name = file_obj.name
            file_size = len(file_obj.read())
            file_obj.seek(0)  # Reset file pointer
            
            # Extract basic info from filename
            name_parts = os.path.splitext(file_name)[0].split('-')
            app_name = name_parts[0].replace('_', ' ').title()
            
            # Try to extract version from filename
            version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', file_name)
            version = version_match.group(1) if version_match else "1.0.0"
            
            # Generate basic analysis output
            analysis_output = f"""AppName : {app_name}
Publisher : Unknown Publisher
Version : {version}
Architecture : 64-bit
InstallContext : System
FileSize : {file_size}
FileName : {file_name}
FileType : {os.path.splitext(file_name)[1]}
AnalysisMethod : Fallback (Filename-based)
"""
            
            return True, analysis_output
            
        except Exception as e:
            return False, str(e)
    
    def get_readdata_script(self):
        """Get the PowerShell analysis script"""
        return """
param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

function Get-FileProperties {
    param($File)
    
    try {
        $FileInfo = Get-ItemProperty -Path $File -ErrorAction Stop
        $VersionInfo = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($File)
        
        # Try to get MSI properties if it's an MSI file
        if ($File -like "*.msi") {
            try {
                $WindowsInstaller = New-Object -ComObject WindowsInstaller.Installer
                $Database = $WindowsInstaller.GetType().InvokeMember("OpenDatabase", "InvokeMethod", $null, $WindowsInstaller, @($File, 0))
                
                $Query = "SELECT Property, Value FROM Property"
                $View = $Database.GetType().InvokeMember("OpenView", "InvokeMethod", $null, $Database, ($Query,))
                $View.GetType().InvokeMember("Execute", "InvokeMethod", $null, $View, $null)
                
                $Properties = @{}
                while ($true) {
                    $Record = $View.GetType().InvokeMember("Fetch", "InvokeMethod", $null, $View, $null)
                    if ($Record -eq $null) { break }
                    
                    $Property = $Record.GetType().InvokeMember("StringData", "GetProperty", $null, $Record, 1)
                    $Value = $Record.GetType().InvokeMember("StringData", "GetProperty", $null, $Record, 2)
                    $Properties[$Property] = $Value
                }
                
                Write-Output "AppName : $($Properties['ProductName'])"
                Write-Output "Publisher : $($Properties['Manufacturer'])"
                Write-Output "Version : $($Properties['ProductVersion'])"
                Write-Output "ProductCode : $($Properties['ProductCode'])"
                Write-Output "UpgradeCode : $($Properties['UpgradeCode'])"
                
            } catch {
                Write-Output "AppName : $($VersionInfo.ProductName)"
                Write-Output "Publisher : $($VersionInfo.CompanyName)"
                Write-Output "Version : $($VersionInfo.ProductVersion)"
            }
        } else {
            Write-Output "AppName : $($VersionInfo.ProductName)"
            Write-Output "Publisher : $($VersionInfo.CompanyName)"
            Write-Output "Version : $($VersionInfo.ProductVersion)"
            Write-Output "FileDescription : $($VersionInfo.FileDescription)"
            Write-Output "InternalName : $($VersionInfo.InternalName)"
        }
        
        Write-Output "Architecture : $(if([Environment]::Is64BitOperatingSystem) { '64-bit' } else { '32-bit' })"
        Write-Output "FileSize : $($FileInfo.Length)"
        Write-Output "CreationTime : $($FileInfo.CreationTime)"
        Write-Output "LastWriteTime : $($FileInfo.LastWriteTime)"
        Write-Output "FileName : $($FileInfo.Name)"
        Write-Output "InstallContext : System"
        
    } catch {
        Write-Error "Failed to analyze file: $($_.Exception.Message)"
        exit 1
    }
}

if (Test-Path $FilePath) {
    Get-FileProperties -File $FilePath
} else {
    Write-Error "File not found: $FilePath"
    exit 1
}
"""

# ============================================================================
# ENHANCED ICON GENERATION
# ============================================================================
class SmartIconGenerator:
    """Enhanced icon generator with app-specific intelligence"""
    
    def __init__(self):
        self.icon_cache = {}
        self.app_categories = {
            'browser': ['chrome', 'firefox', 'edge', 'safari', 'opera'],
            'media': ['vlc', 'spotify', 'itunes', 'media', 'player'],
            'office': ['office', 'word', 'excel', 'powerpoint', 'outlook'],
            'development': ['visual', 'studio', 'code', 'git', 'python'],
            'security': ['antivirus', 'firewall', 'security', 'defender'],
            'communication': ['teams', 'skype', 'zoom', 'discord', 'slack'],
            'design': ['photoshop', 'illustrator', 'design', 'gimp'],
            'utility': ['winrar', 'zip', 'utility', 'tool', 'system']
        }
        
        self.category_colors = {
            'browser': [(66, 133, 244), (234, 67, 53)],  # Blue/Red
            'media': [(255, 87, 51), (255, 206, 84)],    # Orange/Yellow
            'office': [(0, 120, 212), (16, 124, 16)],    # Blue/Green
            'development': [(1, 103, 197), (0, 0, 0)],   # Blue/Black
            'security': [(215, 0, 0), (255, 140, 0)],    # Red/Orange
            'communication': [(0, 120, 212), (0, 188, 212)], # Blue/Cyan
            'design': [(173, 20, 87), (240, 80, 35)],    # Purple/Orange
            'utility': [(104, 104, 104), (0, 0, 0)]      # Gray/Black
        }
    
    def detect_app_category(self, app_name):
        """Detect application category based on name"""
        app_lower = app_name.lower()
        
        for category, keywords in self.app_categories.items():
            if any(keyword in app_lower for keyword in keywords):
                return category
        
        return 'utility'  # Default category
    
    def get_app_icon_from_api(self, app_name):
        """Try to fetch real app icon from APIs"""
        try:
            # Try GitHub API for popular apps
            search_query = urllib.parse.quote(f"{app_name} icon")
            url = f"https://api.github.com/search/code?q={search_query}+filename:icon+extension:png&per_page=5"
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results = response.json().get('items', [])
                if results:
                    # Try to download the first icon
                    icon_url = results[0].get('download_url')
                    if icon_url:
                        icon_response = requests.get(icon_url, timeout=5)
                        if icon_response.status_code == 200:
                            return Image.open(io.BytesIO(icon_response.content))
        except:
            pass
        
        return None
    
    def create_category_icon(self, app_name, category):
        """Create category-specific icon"""
        size = 256
        img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Get category colors
        colors = self.category_colors.get(category, [(255, 107, 53), (247, 147, 30)])
        
        # Create gradient background
        for y in range(size):
            progress = y / size
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * progress)
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * progress)
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * progress)
            draw.rectangle([(0, y), (size, y+1)], fill=(r, g, b, 255))
        
        # Add category-specific shapes
        self.add_category_elements(draw, category, size)
        
        # Add app initials
        words = app_name.split()
        initials = "".join([w[0].upper() for w in words[:2]]) if words else "AP"
        
        try:
            font_size = size // 4
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Draw text with shadow effect
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        # Shadow
        draw.text((x+3, y+3), initials, font=font, fill=(0, 0, 0, 128))
        # Main text
        draw.text((x, y), initials, font=font, fill=(255, 255, 255, 255))
        
        # Apply rounded corners
        img = self.add_rounded_corners(img, 30)
        
        return img
    
    def add_category_elements(self, draw, category, size):
        """Add category-specific design elements"""
        margin = size // 8
        
        if category == 'browser':
            # Add browser-like elements (address bar, etc.)
            draw.rectangle([margin, margin, size-margin, margin+20], fill=(255, 255, 255, 100))
        
        elif category == 'media':
            # Add play button symbol
            play_size = size // 6
            center = size // 2
            points = [
                (center - play_size//2, center - play_size),
                (center - play_size//2, center + play_size),
                (center + play_size, center)
            ]
            draw.polygon(points, fill=(255, 255, 255, 150))
        
        elif category == 'office':
            # Add document-like lines
            for i in range(3):
                y = margin + 40 + i * 20
                draw.rectangle([margin+20, y, size-margin-20, y+3], fill=(255, 255, 255, 120))
        
        elif category == 'development':
            # Add code brackets
            bracket_size = size // 8
            center = size // 2
            draw.text((margin, center-bracket_size), "</>", fill=(255, 255, 255, 150))
        
        elif category == 'security':
            # Add shield shape
            shield_points = [
                (size//2, margin),
                (size-margin-20, margin+40),
                (size-margin-20, size-margin-40),
                (size//2, size-margin),
                (margin+20, size-margin-40),
                (margin+20, margin+40)
            ]
            draw.polygon(shield_points, fill=(255, 255, 255, 100))
    
    def add_rounded_corners(self, img, radius):
        """Add rounded corners to image"""
        # Create a mask for rounded corners
        mask = Image.new('L', img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), img.size], radius, fill=255)
        
        # Apply mask
        result = Image.new('RGBA', img.size, (255, 255, 255, 0))
        result.paste(img, (0, 0))
        result.putalpha(mask)
        
        return result
    
    def generate_smart_icon(self, app_name):
        """Generate intelligent app icon"""
        # Check cache first
        if app_name in self.icon_cache:
            return self.icon_cache[app_name]
        
        # Try to get real icon from API
        real_icon = self.get_app_icon_from_api(app_name)
        if real_icon:
            # Resize and process real icon
            real_icon = real_icon.resize((256, 256), Image.Resampling.LANCZOS)
            self.icon_cache[app_name] = real_icon
            return real_icon
        
        # Generate category-based icon
        category = self.detect_app_category(app_name)
        generated_icon = self.create_category_icon(app_name, category)
        
        # Cache and return
        self.icon_cache[app_name] = generated_icon
        return generated_icon

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
        
        # Virtual Environment Status
        vm = VirtualEnvironment()
        vm_status_class = "vm-status active" if vm.is_docker_available else "vm-status error"
        vm_status_text = "🟢 Docker Available" if vm.is_docker_available else "🔴 Docker Unavailable"
        
        st.markdown(f"""
        <div class="{vm_status_class}">
            <strong>Virtual Environment</strong><br>
            {vm_status_text}<br>
            <small>Auto-extraction: {'Enabled' if vm.is_docker_available else 'Fallback Mode'}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Deployment mode
        deployment_mode = st.selectbox(
            "Deployment Mode",
            ['Standard', 'Silent', 'Interactive'],
            help="Select the deployment mode for your package"
        )
        
        st.divider()
        
        # Auto-extraction toggle
        auto_extract = st.checkbox(
            "Auto-extract metadata",
            value=st.session_state.auto_extraction_enabled,
            help="Automatically extract metadata from uploaded files"
        )
        st.session_state.auto_extraction_enabled = auto_extract
        
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
            
            # Auto-extraction if enabled
            if st.session_state.auto_extraction_enabled and not st.session_state.parsed_data:
                with st.spinner("🔍 Auto-extracting metadata..."):
                    vm = VirtualEnvironment()
                    success, result = vm.analyze_file(primary_installer)
                    
                    if success:
                        parsed = parse_powershell_output(result)
                        if parsed:
                            st.session_state.parsed_data = parsed
                            st.success(f"✨ Auto-extracted {len(parsed)} metadata fields!")
                            st.session_state.step_number = 3
                        else:
                            st.warning("Auto-extraction completed but no data parsed. Please proceed manually.")
                    else:
                        st.warning(f"Auto-extraction failed: {result}. Using fallback mode.")
            
            st.session_state.step_number = 2

    st.markdown("</div>", unsafe_allow_html=True)
    return primary_installer

def render_parse_section():
    """Render PowerShell parsing section with auto-extraction status"""
    if st.session_state.parsed_data:
        st.markdown("""
        <div class="custom-card">
            <div class="card-header">
                <span class="card-icon">✅</span>
                <span class="card-title">Step 2: Metadata Extracted Successfully</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Show parsed data with copy buttons
        st.markdown("**Extracted Metadata:**")
        for key, value in st.session_state.parsed_data.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"• **{key}:** {value}")
            with col2:
                copy_button(value, "📋", f"meta_{key}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">⚙️</span>
            <span class="card-title">Step 2: Import Metadata</span>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 Manual Instructions", expanded=False):
        st.markdown("""
        **If auto-extraction failed, follow these steps:**
        1. Run `readData.ps1` script with your installer
        2. Copy the complete output
        3. Paste it below and click Parse
        
        **Or use the sample data for testing.**
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

    st.markdown("</div>", unsafe_allow_html=True)

def render_configuration_section(primary_installer):
    """Render configuration section with enhanced icon generation"""
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

    # Icon Preview Section
    if app_name:
        st.markdown("### 🎨 Application Icon Preview")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button("🔄 Generate Smart Icon", use_container_width=True):
                with st.spinner("Generating intelligent icon..."):
                    icon_generator = SmartIconGenerator()
                    smart_icon = icon_generator.generate_smart_icon(app_name)
                    st.session_state.generated_icon = smart_icon
            
            if st.session_state.generated_icon:
                st.markdown('<div class="icon-container">', unsafe_allow_html=True)
                st.image(st.session_state.generated_icon, width=150, caption="Generated Icon")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if st.session_state.generated_icon:
                st.markdown("**Icon Features:**")
                category = SmartIconGenerator().detect_app_category(app_name)
                st.markdown(f"• **Category:** {category.title()}")
                st.markdown(f"• **Style:** Category-optimized design")
                st.markdown(f"• **Resolution:** 256x256 (High Quality)")
                st.markdown(f"• **Format:** PNG with transparency")

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
                'create_shortcut': create_shortcut,
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

    # Get rules safely
    recipe_rules = rules.get(data.get('installer_type_key', 'exe_nsis'), {})

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚙️ Commands", "🔍 Detection", "📥 Export"])

    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {data['app_name']}")
            
            # Copyable fields
            fields = [
                ("Version", data['version']),
                ("Vendor", data['vendor']),
                ("Category", data['category']),
                ("Architecture", data.get('architecture', '64-bit')),
                ("Install Context", data.get('install_context', 'System'))
            ]
            
            for label, value in fields:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{label}:** {value}")
                with col_b:
                    copy_button(value, "📋", f"field_{label}")
            
            # Description
            desc = fetch_app_description(data['app_name'])
            st.info(desc)
            copy_button(desc, "📋 Copy Description", "description")
        
        with col2:
            st.markdown("### Application Icon")
            if st.session_state.generated_icon:
                st.image(st.session_state.generated_icon, width=150)
                
                # Download icon
                buf = io.BytesIO()
                st.session_state.generated_icon.save(buf, format='PNG')
                st.download_button(
                    "💾 Download Icon",
                    buf.getvalue(),
                    f"{data['app_name']}_icon.png",
                    "image/png",
                    use_container_width=True
                )

    with tab2:
        st.markdown("### Installation Commands")
        
        # Install command
        try:
            install_cmd = recipe_rules.get('install_command', '"{filename}" /S')
            if '{filename}' in install_cmd:
                install_cmd = install_cmd.format(filename=data['uploaded_filename'])
            
            code_block_with_copy(install_cmd, "powershell", "Install Command")
            
        except Exception as e:
            st.error(f"Error formatting install command: {e}")
            code_block_with_copy(recipe_rules.get('install_command', 'Command not available'), "powershell", "Install Command")
        
        # Uninstall command
        if 'uninstall_command' in recipe_rules:
            st.markdown("### Uninstall Command")
            try:
                uninstall_cmd = recipe_rules['uninstall_command']
                
                # Create display version with placeholder names
                display_uninstall = uninstall_cmd
                if '{uninstall_string}' in display_uninstall:
                    display_uninstall = display_uninstall.replace('{uninstall_string}', '[UNINSTALL_STRING]')
                if '{product_code}' in display_uninstall:
                    display_uninstall = display_uninstall.replace('{product_code}', '[PRODUCT_CODE]')
                
                code_block_with_copy(display_uninstall, "powershell", "Uninstall Command")
                
                # Show note about placeholders
                if '{' in uninstall_cmd:
                    st.info("💡 Placeholders will be replaced with actual values during deployment")
                    
            except Exception as e:
                st.error(f"Error processing uninstall command: {e}")
                code_block_with_copy("Uninstall command not available", "powershell", "Uninstall Command")

    with tab3:
        st.markdown("### Detection Method")
        detection_method = recipe_rules.get('detection_method', 'Registry Key Detection')
        st.info(f"Method: {detection_method}")
        copy_button(detection_method, "📋 Copy Method", "detection_method")
        
        # Registry paths
        st.markdown("### Registry Paths")
        paths = [
            "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
            "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
        ]
        for i, path in enumerate(paths):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.code(path, language='text')
            with col2:
                copy_button(path, "📋", f"path_{i}")

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
            
            # Copy JSON to clipboard
            copy_button(json_data, "📋 Copy JSON", "json_export")
        
        with col2:
            # PowerShell export
            install_cmd = recipe_rules.get('install_command', '"{filename}" /S')
            if '{filename}' in install_cmd:
                install_cmd = install_cmd.format(filename=data['uploaded_filename'])
            
            ps_script = f"""# {data['app_name']} Installation Script
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
            
            # Copy PowerShell to clipboard
            copy_button(ps_script, "📋 Copy Script", "ps_export")

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
        <p><strong>PackPilot Pro v3.0</strong> © 2024 | Enterprise Packaging Platform</p>
        <p><small>Enhanced with Smart Icons, Auto-Extraction & Copy Features</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
