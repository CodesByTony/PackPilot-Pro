"""
PackPilot Pro — Intelligent Packaging Copilot
- Theme: all text black (#1a1a1a), orange accent cards/buttons, light code blocks
- Assets expected in repo: rules.json, Generated.png, readData.ps1
- Fixes:
  - No white text anywhere (even in tabs, code blocks, file uploader)
  - No KeyError if 'uninstall_command' missing in rules.json
  - Multi-line PowerShell parsing
  - Robust Winget manifest lookup (timeouts, TTL cache, optional token)
  - Primary installer selection (not auto-picking first)
  - Safer defaults and clear validation
"""

import os
import io
import re
import json
import base64
from typing import Dict, Any, Optional, List, Tuple

import requests
import yaml
import streamlit as st
from PIL import Image, ImageDraw, ImageFont


# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="PackPilot Pro",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =============================================================================
# THEME CONSTANTS
# =============================================================================
COLOR_TEXT = "#1a1a1a"          # Black text everywhere
COLOR_ORANGE = "#FF8C00"        # Orange accent/border
COLOR_BORDER = "#FFB56B"        # Softer orange border
COLOR_CARD_BG = "#FFF7EF"       # Pale orange card background
COLOR_INPUT_BG = "#FFFCF6"      # Extra light background for inputs
COLOR_CODE_BG = "#FFF3E0"       # Light code background


# =============================================================================
# GLOBAL CSS — stable selectors; readable everywhere
# =============================================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

/* Global text and font */
html, body, .stApp, [class^="css"] {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  color: {COLOR_TEXT} !important;
}}

/* Container width */
.main .block-container {{
  max-width: 1100px;
  padding-top: 3vh;
}}

/* Title area */
.title-wrap {{
  text-align: center;
  margin-bottom: 1rem;
}}
.title-wrap .title {{
  font-size: 2.4rem;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: {COLOR_TEXT};
  margin: 0;
}}
.title-wrap .tagline {{
  color: {COLOR_TEXT};
  opacity: 0.85;
  margin-top: .35rem;
}}

/* Card container */
.card {{
  background: {COLOR_CARD_BG};
  border: 2px solid {COLOR_ORANGE};
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 8px 24px rgba(255, 140, 0, .14);
  margin-bottom: 1rem;
}}

/* Step header */
.step-title {{
  font-weight: 800;
  margin-bottom: .5rem;
  display: flex;
  align-items: center;
  gap: .5rem;
}}
.step-badge {{
  background: #FFD9A6;
  border: 2px solid {COLOR_ORANGE};
  border-radius: 999px;
  font-weight: 800;
  padding: .2rem .6rem;
  color: {COLOR_TEXT};
}}

/* Inputs and selects */
label {{
  color: {COLOR_TEXT} !important;
  font-weight: 700 !important;
}}
input, textarea, select {{
  background: {COLOR_INPUT_BG} !important;
  color: {COLOR_TEXT} !important;
  border: 1.5px solid {COLOR_BORDER} !important;
  border-radius: 10px !important;
}}
textarea::placeholder, input::placeholder {{ color: #6b6b6b !important; }}

/* File uploader dropzone (readable, light) */
[data-testid="stFileUploader"] div[role="button"] {{
  background: {COLOR_INPUT_BG} !important;
  color: {COLOR_TEXT} !important;
  border: 2px dashed {COLOR_ORANGE} !important;
  border-radius: 12px !important;
}}
[data-testid="stFileUploader"] label {{
  color: {COLOR_TEXT} !important;
  font-weight: 700 !important;
}}

/* Buttons: differentiated, readable (black text) */
.stButton > button {{
  color: {COLOR_TEXT} !important;
  border-radius: 10px !important;
  padding: 0.65rem 1.1rem !important;
  font-weight: 800 !important;
  border: 2px solid {COLOR_ORANGE} !important;
  background: #FFE8CC !important;
}}
.stButton > button[kind="primary"] {{
  background: linear-gradient(90deg, #FFC27A 0%, #FF8C00 100%) !important;
  border: 2px solid {COLOR_BORDER} !important;
  color: {COLOR_TEXT} !important;
}}
.stButton > button[kind="secondary"], .stDownloadButton > button {{
  background: #FFE8CC !important;
  border: 2px solid {COLOR_ORANGE} !important;
  color: {COLOR_TEXT} !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
  background: #FFF3E0;
  border-radius: 12px;
  padding: .4rem;
  margin-bottom: 1rem;
}}
.stTabs [data-baseweb="tab"] {{
  color: {COLOR_TEXT} !important;
  font-weight: 700 !important;
}}
.stTabs [aria-selected="true"] {{
  background: #FFD9A6 !important;
  color: {COLOR_TEXT} !important;
}}

/* Code blocks — light background, black text */
pre, code, [data-testid="stCode"] {{
  background-color: {COLOR_CODE_BG} !important;
  color: {COLOR_TEXT} !important;
  border: 1px solid {COLOR_BORDER} !important;
  border-radius: 10px !important;
}}
pre code span, code span {{ color: {COLOR_TEXT} !important; }}

/* Alerts: ensure black text */
.stAlert, .stAlert p, .stAlert span {{ color: {COLOR_TEXT} !important; }}

/* Hide Streamlit footer/menu */
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# BACKGROUND IMAGE (white image with a subtle tint overlay for readability)
# =============================================================================
@st.cache_data(show_spinner=False)
def _get_base64(path: str) -> Optional[str]:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

def set_background(image_file: str = "Generated.png") -> None:
    b64 = _get_base64(image_file)
    if not b64:
        st.info("Note: 'Generated.png' not found. Continuing without background.")
        return
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 165, 0, 0.035), rgba(255, 165, 0, 0.035)),
                    url("data:image/png;base64,{b64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """, unsafe_allow_html=True)

set_background("Generated.png")


# =============================================================================
# RULES LOADER + VALIDATION (no KeyError for uninstall_command)
# =============================================================================
@st.cache_data(show_spinner=False)
def load_rules() -> Dict[str, Any]:
    try:
        with open("rules.json", "r", encoding="utf-8") as f:
            rules = json.load(f)
    except FileNotFoundError:
        st.error("Fatal: 'rules.json' not found in the repository.")
        st.stop()
    except json.JSONDecodeError as e:
        st.error(f"Fatal: rules.json is invalid JSON. {e}")
        st.stop()

    # Minimal schema validation and safe defaults
    required = {"installer_type", "install_command", "detection_method"}
    for key, cfg in list(rules.items()):
        if not isinstance(cfg, dict):
            st.error(f"rules.json -> '{key}' must be an object.")
            st.stop()
        missing = required - set(cfg.keys())
        if missing:
            st.error(f"rules.json -> '{key}' missing fields: {', '.join(sorted(missing))}")
            st.stop()
        # Ensure uninstall_command exists (fallback to parsed UninstallString)
        if not cfg.get("uninstall_command"):
            cfg["uninstall_command"] = "{uninstall_string}"

    # Ensure interactive rules exist
    rules.setdefault("interactive", {
        "installer_type": "Interactive (ServiceUI)",
        "install_command": 'ServiceUI.exe -process:explorer.exe "{filename}"',
        "uninstall_command": 'ServiceUI.exe -process:explorer.exe "{uninstall_string}"',
        "detection_method": "Registry"
    })

    return rules

RULES = load_rules()


# =============================================================================
# PARSE POWERSHELL OUTPUT (multi-line aware)
# =============================================================================
def parse_ps_output(output: str) -> Dict[str, str]:
    """
    Parses PowerShell 'Key: Value' style output, supporting multi-line values.
    Accumulates lines under the last seen key until a new 'Key:' line appears.
    """
    if not output or not output.strip():
        return {}
    data: Dict[str, str] = {}
    key_pat = re.compile(r'^\s*([A-Za-z0-9._&() \-```math
```/\```+?)\s*:\s*(.*)$')
    current_key: Optional[str] = None
    buffer: List[str] = []

    for raw_line in output.splitlines():
        line = raw_line.rstrip("\r")
        m = key_pat.match(line)
        if m:
            if current_key is not None:
                data[current_key] = "\n".join(buffer).strip()
            current_key = m.group(1).strip()
            first_value = m.group(2).strip()
            buffer = [first_value] if first_value else []
        else:
            if current_key is not None:
                buffer.append(line)

    if current_key is not None:
        data[current_key] = "\n".join(buffer).strip()
    return data


# =============================================================================
# WINGET DESCRIPTION LOOKUP (robust, cached, optional token)
# =============================================================================
def _get_github_token() -> Optional[str]:
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token
    try:
        return st.secrets.get("GITHUB_TOKEN")  # type: ignore[attr-defined]
    except Exception:
        return None

@st.cache_data(ttl=86400, show_spinner=False)
def get_info_from_winget(app_name: str) -> str:
    try:
        term = app_name.split(" (")[0].strip()
        if not term:
            return f"{app_name} is a widely-used application."
        headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "PackPilot-Pro/1.0"}
        token = _get_github_token()
        if token:
            headers["Authorization"] = f"token {token}"

        # Narrow to manifests in winget-pkgs and YAML files
        params = {"q": f'{term} in:file repo:microsoft/winget-pkgs path:/manifests language:yaml', "per_page": 5}
        r = requests.get("https://api.github.com/search/code", headers=headers, params=params, timeout=10)
        r.raise_for_status()
        items = r.json().get("items", [])[:5]
        if not items:
            return f"{app_name} is a versatile utility designed to enhance productivity."

        for it in items:
            raw_url = it["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            m = requests.get(raw_url, headers=headers, timeout=10)
            m.raise_for_status()
            text = m.text.strip()
            docs = list(yaml.safe_load_all(text)) if text.startswith("---") else [yaml.safe_load(text)]
            for doc in docs:
                if isinstance(doc, dict):
                    desc = doc.get("Description") or doc.get("ShortDescription")
                    if desc and str(desc).strip():
                        return str(desc).strip()

        return f"{app_name} is a widely-used application."
    except Exception:
        return f"{app_name} is a versatile utility designed to enhance productivity."


# =============================================================================
# ICON GENERATION (black initials on orange gradient) + caching
# =============================================================================
def _build_icon_image(app_name: str, width: int = 256, height: int = 256) -> Image.Image:
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # Soft vertical gradient
    top = (255, 204, 153)
    bottom = (255, 153, 51)
    for y in range(height):
        r = int(top[0] + (bottom[0] - top[0]) * y / height)
        g = int(top[1] + (bottom[1] - top[1]) * y / height)
        b = int(top[2] + (bottom[2] - top[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Initials
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 100)
    except Exception:
        font = ImageFont.load_default()

    words = re.findall(r"[A-Z][a-z]*|\d+", app_name) or app_name.split()
    initials = "".join([w[0] for w in words[:2]]).upper() or (app_name[:2].upper() if app_name else "A")
    bbox = draw.textbbox((0, 0), initials, font=font)
    x = (width - (bbox[2] - bbox[0])) / 2
    y = (height - (bbox[3] - bbox[1])) / 2
    draw.text((x, y), initials, font=font, fill=COLOR_TEXT)

    # Subtle rounded border
    draw.rounded_rectangle([(2, 2), (width - 3, height - 3)], radius=28, outline=(255, 140, 0), width=3)
    return img

@st.cache_data(show_spinner=False)
def generate_icon_bytes(app_name: str) -> bytes:
    img = _build_icon_image(app_name)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# =============================================================================
# INSTALLER TYPE GUESSER
# =============================================================================
def guess_type_from_filename(filename: str) -> str:
    low = filename.lower()
    if low.endswith(".msi"):
        return "msi" if "msi" in RULES else next(iter(RULES.keys()))
    if low.endswith(".exe"):
        for cand in ("exe_nsis", "exe_inno", "exe"):
            if cand in RULES:
                return cand
    return next(iter(RULES.keys()))


# =============================================================================
# UNINSTALL COMMAND HELPERS (no KeyError; safe fallbacks)
# =============================================================================
GUID_RE = re.compile(r"\{[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}\}")

def extract_product_code(uninstall_string: str) -> Optional[str]:
    if not uninstall_string:
        return None
    m = GUID_RE.search(uninstall_string)
    return m.group(0) if m else None

def sanitize_uninstall_string(uninstall_string: str) -> str:
    if not uninstall_string:
        return ""
    s = uninstall_string.strip().strip('"')
    low = s.lower()

    # MSI (prefer GUID)
    if "msiexec" in low:
        guid = extract_product_code(s)
        return f"msiexec /x {guid} /qn /norestart" if guid else "msiexec /x {PRODUCT_CODE} /qn /norestart"

    # Inno Setup
    if "unins" in low and s.endswith(".exe"):
        return f'"{s}" /VERYSILENT /NORESTART'

    # NSIS or generic uninstall.exe
    if "uninstall" in low and s.endswith(".exe"):
        return f'"{s}" /S'

    # Fallback
    return f'"{s}"'

def build_uninstall_command(data: Dict[str, Any], recipe_rules: Dict[str, Any]) -> Tuple[str, str]:
    """
    Returns (uninstall_cmd, source) where source is one of: template|parsed|fallback-msi|missing
    """
    uninstall_template = (recipe_rules.get("uninstall_command") or "").strip()
    uninstall_string = (data.get("uninstall_string")
                        or data.get("UninstallString")
                        or data.get("uninstallString")
                        or "")
    product_code = extract_product_code(uninstall_string) if uninstall_string else None

    if uninstall_template:
        cmd = uninstall_template.format(
            filename=data.get("uploaded_filename", ""),
            uninstall_string=sanitize_uninstall_string(uninstall_string),
            product_code=product_code or "{PRODUCT_CODE}"
        )
        return cmd, "template"

    if uninstall_string:
        return sanitize_uninstall_string(uninstall_string), "parsed"

    # File-based fallback
    ext = os.path.splitext(data.get("uploaded_filename", ""))[1].lower()
    if ext == ".msi":
        return "msiexec /x {PRODUCT_CODE} /qn /norestart", "fallback-msi"

    return "Please provide an UninstallString or add uninstall_command in rules.json.", "missing"


# =============================================================================
# RECIPE BUILDERS
# =============================================================================
def build_recipe_json(data: Dict[str, Any], install_cmd: str, uninstall_cmd: str, description: str) -> Dict[str, Any]:
    return {
        "app_name": data["app_name"],
        "vendor": data["vendor"],
        "version": data["version"],
        "installer_type_key": data["installer_type_key"],
        "uploaded_filename": data["uploaded_filename"],
        "apps_and_features_name": data.get("apps_and_features_name", data["app_name"]),
        "architecture": data.get("architecture", "64-bit"),
        "install_context": data.get("install_context", "System"),
        "install_command": install_cmd,
        "uninstall_command": uninstall_cmd,
        "description": description,
    }

def build_recipe_markdown(recipe: Dict[str, Any], detection_method: str) -> str:
    md = []
    md.append(f"# Deployment Recipe — {recipe['app_name']}")
    md.append("")
    md.append(f"- Vendor: {recipe['vendor']}")
    md.append(f"- Version: {recipe['version']}")
    md.append(f"- Installer Type: {recipe['installer_type_key']}")
    md.append(f"- Install Context: {recipe['install_context']}")
    md.append(f"- Architecture: {recipe['architecture']}")
    md.append("")
    md.append("## Description")
    md.append(recipe.get("description", "").strip() or "N/A")
    md.append("")
    md.append("## Install Command")
    md.append("```powershell")
    md.append(recipe["install_command"])
    md.append("```")
    md.append("")
    md.append("## Uninstall Command")
    md.append("```powershell")
    md.append(recipe["uninstall_command"])
    md.append("```")
    md.append("")
    md.append("## Detection Rules")
    md.append(f"- Recommended: {detection_method}")
    md.append("  - HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
    md.append("  - HKLM\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
    return "\n".join(md)


# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<div class="title-wrap">
  <div class="title">PackPilot Pro</div>
  <div class="tagline">Packaging copilot with clean design, robust logic, and safe defaults.</div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# STEP 1 — UPLOAD FILES
# =============================================================================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title"><span class="step-badge">1</span> Upload package files (.exe/.msi)</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload installers and related files",
        accept_multiple_files=True,
        type=['exe', 'msi', 'msix', 'appx', 'ps1', 'bat', 'cmd', 'txt', 'json', 'xml']
    )

    primary_installer = None
    if uploaded_files:
        installers = [f for f in uploaded_files if f.name.lower().endswith((".exe", ".msi", ".msix", ".appx"))]
        if installers:
            names = [f.name for f in installers]
            choice = st.selectbox("Choose primary installer", names, index=0)
            primary_installer = next(f for f in installers if f.name == choice)
            st.success(f"Primary installer: {primary_installer.name}")
        else:
            st.warning("No installer files (.exe/.msi/.msix/.appx) detected.")
    else:
        st.info("Tip: Drag and drop multiple files above.")

    st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# STEP 2 — PASTE POWERSHELL OUTPUT
# =============================================================================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title"><span class="step-badge">2</span> Paste output from readData.ps1</div>', unsafe_allow_html=True)

    with st.expander("How to use readData.ps1", expanded=False):
        st.markdown("""
        1) Run: ./readData.ps1 -Path "installer.exe"
        2) Copy the output (Key: Value lines)
        3) Paste below and click 'Parse Data'
        """)
        st.code("""AppName : Example Application
Publisher : Example Corp
Version : 1.2.3
Architecture : 64-bit
InstallContext : System
AppsAndFeaturesName : Example Application
UninstallString : MsiExec.exe /X{GUID-HERE}""", language="powershell")

    ps_output_text = st.text_area(
        "Paste PowerShell script output here",
        height=160,
        placeholder="AppName : Microsoft Teams\nPublisher : Microsoft\nVersion : 1.0.0\n..."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Parse Data", type="primary"):
            if ps_output_text.strip():
                st.session_state.parsed_data = parse_ps_output(ps_output_text)
                if st.session_state.parsed_data:
                    st.success(f"Parsed {len(st.session_state.parsed_data)} fields.")
                else:
                    st.warning("No key/value pairs detected. Check the format.")
            else:
                st.error("Please paste the PowerShell output first.")
    with col2:
        if st.button("Clear Parsed Data", type="secondary"):
            st.session_state.pop("parsed_data", None)
            st.rerun()

    # Preview parsed data
    if st.session_state.get("parsed_data"):
        with st.expander("Preview parsed data"):
            st.json(st.session_state.parsed_data)

    st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# STEP 3 — VERIFY DETAILS / OPTIONS
# =============================================================================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title"><span class="step-badge">3</span> Verify and confirm details</div>', unsafe_allow_html=True)

    ready_for_recipe = False
    if primary_installer and st.session_state.get("parsed_data"):
        parsed = st.session_state.parsed_data

        # Defaults from parsed data
        default_app_name = parsed.get("AppName", parsed.get("DisplayName", ""))
        default_vendor = parsed.get("Publisher", parsed.get("Vendor", ""))
        default_version = parsed.get("Version", parsed.get("ProductVersion", ""))
        default_arch = parsed.get("Architecture", "64-bit")
        default_context = parsed.get("InstallContext", "System")
        default_aafn = parsed.get("AppsAndFeaturesName", default_app_name or "Unknown")

        colA, colB = st.columns(2)
        with colA:
            app_name = st.text_input("Application Name", value=default_app_name, key="app_name_input")
            vendor = st.text_input("Vendor/Publisher", value=default_vendor, key="vendor_input")
            version = st.text_input("Version", value=default_version, key="version_input")
        with colB:
            arch_options = ["64-bit", "32-bit", "Any"]
            try:
                arch_index = arch_options.index(default_arch)
            except ValueError:
                arch_index = 0
            architecture = st.selectbox("Architecture", options=arch_options, index=arch_index)

            context_options = ["System", "User"]
            try:
                ctx_index = context_options.index(default_context)
            except ValueError:
                ctx_index = 0
            install_context = st.selectbox("Install Context", options=context_options, index=ctx_index)

        apps_and_features_name = st.text_input("Apps & Features Name", value=default_aafn)

        # Installer type
        col1, col2 = st.columns([2, 1])
        with col1:
            guessed = guess_type_from_filename(primary_installer.name)
            type_options = list(RULES.keys())
            idx = type_options.index(guessed) if guessed in type_options else 0
            installer_type_key = st.selectbox(
                "Installer Type",
                options=type_options,
                index=idx,
                format_func=lambda x: RULES[x]["installer_type"]
            )
        with col2:
            is_interactive = st.checkbox("Requires user interaction (ServiceUI)")

        final_type_key = "interactive" if is_interactive and "interactive" in RULES else installer_type_key

        # Validate rules and install template presence
        if final_type_key not in RULES:
            st.error(f"'{final_type_key}' is missing from rules.json.")
        else:
            recipe_rules = RULES[final_type_key]
            install_tmpl = recipe_rules.get("install_command", "").strip()
            if not install_tmpl:
                st.error(f"'install_command' missing in rules.json for '{final_type_key}'.")
            else:
                ready_for_recipe = True

        st.divider()
        if st.button("Generate Recipe 🚀", use_container_width=True, type="primary"):
            if not app_name or not vendor or not version:
                st.error("Please fill Application Name, Vendor, and Version.")
            elif not ready_for_recipe:
                st.error("Please resolve rules.json issues.")
            else:
                st.session_state.recipe_data = {
                    "app_name": app_name,
                    "vendor": vendor,
                    "version": version,
                    "installer_type_key": final_type_key,
                    "uploaded_filename": primary_installer.name,
                    "apps_and_features_name": apps_and_features_name,
                    "architecture": architecture,
                    "install_context": install_context,
                    # persist uninstall string if provided by PS output
                    "uninstall_string": parsed.get("UninstallString", ""),
                }
                st.session_state.generate = True
                st.success("Recipe data captured, proceed to review below.")
    else:
        st.info("Select a primary installer and parse readData.ps1 output to continue.")

    st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# STEP 4 — RECIPE OUTPUT
# =============================================================================
if st.session_state.get("generate") and st.session_state.get("recipe_data"):
    data = st.session_state.recipe_data
    recipe_rules = RULES[data["installer_type_key"]]

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="step-title"><span class="step-badge">4</span> Deployment Recipe</div>', unsafe_allow_html=True)

        # Build commands
        install_cmd = recipe_rules["install_command"].format(filename=data["uploaded_filename"])
        uninstall_cmd, source = build_uninstall_command(data, recipe_rules)

        # Get description (cached)
        with st.spinner("Fetching app description (Winget)…"):
            description = get_info_from_winget(data["app_name"])

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "⚙️ Configuration", "🔍 Detection", "⬇️ Export"])

        with tab1:
            st.text_input("App Name", value=data["app_name"], disabled=True)
            st.text_input("Vendor", value=data["vendor"], disabled=True)
            st.text_input("Version", value=data["version"], disabled=True)
            st.text_area("Description (Winget)", value=description, height=110, disabled=True)

            st.subheader("Generated Icon")
            png_bytes = generate_icon_bytes(data["app_name"])
            st.image(png_bytes, width=128, caption="Smart initials icon (black text)")
            st.download_button(
                "Download Icon (.png)",
                data=png_bytes,
                file_name=f"{data['app_name'].replace(' ', '_')}_icon.png",
                mime="image/png",
                type="secondary"
            )

        with tab2:
            st.text_input("Installer Type", value=data["installer_type_key"], disabled=True)
            st.text_input("Install Context", value=data["install_context"], disabled=True)
            st.text_input("Architecture", value=data["architecture"], disabled=True)
            st.text_input("Apps & Features Name", value=data["apps_and_features_name"], disabled=True)

            st.subheader("Install Command")
            st.code(install_cmd, language="powershell")

            st.subheader(f"Uninstall Command (source: {source})")
            st.code(uninstall_cmd, language="powershell")

        with tab3:
            st.info(f"Recommended method: {recipe_rules['detection_method']}")
            st.write("Common registry locations:")
            st.code(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", language="text")
            st.code(r"HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall", language="text")
            if data["install_context"] == "User":
                st.code(r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", language="text")

            st.subheader("PowerShell detection script")
            detection_script = f"""
$AppName = "{data['apps_and_features_name']}"
$Version = "{data['version']}"

$Paths = @(
  "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
  "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
)

foreach ($Path in $Paths) {{
  $App = Get-ChildItem -Path $Path -ErrorAction SilentlyContinue |
         Get-ItemProperty |
         Where-Object {{ $_.DisplayName -like "*$AppName*" -and $_.DisplayVersion -eq $Version }}
  if ($App) {{
    Write-Output "Detected: $($App.DisplayName) v$($App.DisplayVersion)"
    exit 0
  }}
}}

Write-Output "Not Detected"
exit 1
""".strip("\n")
            st.code(detection_script, language="powershell")

        with tab4:
            recipe_json = build_recipe_json(data, install_cmd, uninstall_cmd, description)
            recipe_md = build_recipe_markdown(recipe_json, recipe_rules["detection_method"])

            st.subheader("Download Recipe (JSON)")
            st.download_button(
                "Download recipe.json",
                data=json.dumps(recipe_json, indent=2).encode("utf-8"),
                file_name=f"{data['app_name'].replace(' ', '_')}_recipe.json",
                mime="application/json",
                type="secondary"
            )

            st.subheader("Download README (Markdown)")
            st.download_button(
                "Download README.md",
                data=recipe_md.encode("utf-8"),
                file_name=f"{data['app_name'].replace(' ', '_')}_README.md",
                mime="text/markdown",
                type="secondary"
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # Keep state so users can still download. To auto-reset after showing, uncomment:
    # st.session_state.pop("generate", None)


# =============================================================================
# FOOTER / UTILITIES
# =============================================================================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Reset All", type="secondary"):
            keys = list(st.session_state.keys())
            for k in keys:
                del st.session_state[k]
            st.rerun()
    with col2:
        st.markdown("Need new installer types? Update rules.json — the app validates and adapts automatically.")
    st.markdown('</div>', unsafe_allow_html=True)
