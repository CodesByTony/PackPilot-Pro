# PackPilot Pro — Redesigned for your theme and robustness
# ---------------------------------------------------------
# - Uses black text everywhere (no white text)
# - Orange cards/accents and differentiated buttons
# - Robust GitHub Winget lookup with timeouts and optional token
# - Safer parsing for readData.ps1 output (supports multi-line values)
# - Defensive rules.json validation (clear errors)
# - Primary installer selection if multiple found
# - Icon generation (black text), downloads, recipe export (JSON + Markdown)
# - Clean layout, comments explaining each section

import os
import io
import re
import json
import base64
from typing import Dict, Any, List, Optional

import requests
import yaml
import streamlit as st
from PIL import Image, ImageDraw, ImageFont


# -------------------------------
# Page configuration and theming
# -------------------------------
st.set_page_config(
    page_title="PackPilot Pro",
    page_icon="🧰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global constants for theme colors (black text + orange UI)
COLOR_TEXT = "#212529"          # Black/dark text everywhere
COLOR_ORANGE = "#FF8C00"        # Orange accents
COLOR_ORANGE_SOFT = "#FFE8CC"   # Light orange fill
COLOR_ORANGE_SOFTER = "#FFF2DF" # Lighter orange for code areas/cards
COLOR_CARD_BG = "#FFF3E0"       # Pale orange background for cards
COLOR_INPUT_BG = "#FFF9F0"      # Very light orange input background
COLOR_BORDER = "#FFB347"        # Orange-ish border

# -------------------------------
# Global CSS (stable selectors)
# -------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

/* Global typography and colors */
html, body, .stApp, [class^="css"] {{
  font-family: 'Inter', sans-serif !important;
  color: {COLOR_TEXT} !important;
}}

/* Keep links readable and consistent */
a, a:visited {{ color: {COLOR_TEXT} !important; text-decoration: underline; }}

/* Main container width + spacing */
.main .block-container {{ max-width: 1000px; padding-top: 4vh; }}

/* Card style blocks */
.card {{
  background: {COLOR_CARD_BG};
  border: 2px solid {COLOR_ORANGE};
  border-radius: 16px;
  padding: 1.5rem 1.75rem;
  box-shadow: 0 8px 28px rgba(0,0,0,0.08);
  margin-bottom: 1.25rem;
}}

/* Title + tagline */
.title-wrap {{ text-align: center; margin-bottom: 1.25rem; }}
.title-wrap .title {{
  font-size: 3.2rem; font-weight: 800; letter-spacing: -1px; margin: 0;
  color: {COLOR_TEXT};
}}
.title-wrap .tagline {{
  font-size: 1.05rem; color: {COLOR_TEXT}; opacity: 0.8; margin-top: 0.35rem;
}}

/* Step headers */
.step-title {{
  font-weight: 700; font-size: 1.1rem; margin: 0 0 0.5rem 0;
  display: flex; align-items: center; gap: 0.5rem;
}}
.step-badge {{
  background: {COLOR_ORANGE};
  color: {COLOR_TEXT};
  border: 2px solid {COLOR_BORDER};
  font-weight: 700; font-size: 0.9rem; line-height: 1;
  padding: 0.25rem 0.5rem; border-radius: 999px;
}}

/* Inputs (text, select, textarea) — readable on light background */
label {{ color: {COLOR_TEXT} !important; font-weight: 600; }}
input, textarea, select {{
  background: {COLOR_INPUT_BG} !important;
  color: {COLOR_TEXT} !important;
  border: 1.5px solid {COLOR_BORDER} !important;
  border-radius: 8px !important;
}}
textarea::placeholder, input::placeholder {{ color: #6b6b6b; }}

/* Code blocks — light orange with black text (no white anywhere) */
pre, code, .stCode, .stMarkdown code {{
  background: {COLOR_ORANGE_SOFTER} !important;
  color: {COLOR_TEXT} !important;
  border-radius: 10px !important;
  border: 1px solid {COLOR_BORDER} !important;
}}
/* Some highlighters color individual spans; force them readable */
pre code span, code span {{ color: {COLOR_TEXT} !important; }}

/* Buttons: differentiated but with black text */
.stButton>button {{
  color: {COLOR_TEXT} !important;
  border-radius: 10px;
  padding: 0.6rem 1.1rem;
  font-weight: 700;
  border: 2px solid {COLOR_ORANGE};
  background: {COLOR_ORANGE_SOFT};
}}
/* Primary button: bold orange fill */
.stButton>button[kind="primary"] {{
  background: linear-gradient(90deg, #FF9F0A 0%, #FF6A00 100%) !important;
  border: 2px solid {COLOR_BORDER} !important;
  color: {COLOR_TEXT} !important;
}}
/* Secondary + download: outlined/light */
.stButton>button[kind="secondary"], .stDownloadButton>button {{
  background: {COLOR_ORANGE_SOFT} !important;
  border: 2px solid {COLOR_ORANGE} !important;
  color: {COLOR_TEXT} !important;
}}

/* Info/success/warning/error boxes — ensure black text */
.stAlert, .stAlert p, .stAlert span {{ color: {COLOR_TEXT} !important; }}

/* Divider subtler */
hr {{ border-top: 1px solid {COLOR_BORDER}; }}

/* Hide Streamlit default menu/footer for a cleaner look */
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# Background image (white) + soft tint overlay for readability
# -------------------------------
@st.cache_data(show_spinner=False)
def _get_base64_of_image(file_path: str) -> Optional[str]:
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

def set_background(image_file: str = "Generated.png") -> None:
    """
    Sets a soft-tinted background image using the white 'Generated.png'.
    Keeps text readable by overlaying a subtle orange-tinted gradient.
    """
    b64 = _get_base64_of_image(image_file)
    if not b64:
        # If missing, show a gentle note but don't break the app
        st.info("Background image 'Generated.png' not found in repo; continuing without it.")
        return
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 165, 0, 0.04), rgba(255, 165, 0, 0.04)),
                    url("data:image/png;base64,{b64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """, unsafe_allow_html=True)

set_background("Generated.png")


# -------------------------------
# Utility: Load and validate rules.json
# -------------------------------
@st.cache_data(show_spinner=False)
def load_rules() -> Dict[str, Any]:
    """
    Loads rules.json from the repo and performs basic schema validation.
    Each installer-type key should at least define:
        - installer_type (display string)
        - install_command (format string, supports {filename})
        - detection_method (string)
    """
    try:
        with open("rules.json", "r", encoding="utf-8") as f:
            rules = json.load(f)
    except FileNotFoundError:
        st.error("Fatal Error: 'rules.json' not found in the repository.")
        st.stop()
    except json.JSONDecodeError as e:
        st.error(f"Fatal Error: rules.json is not valid JSON. Details: {e}")
        st.stop()

    # Validate schema
    required_fields = {"installer_type", "install_command", "detection_method"}
    errors: List[str] = []
    for key, cfg in rules.items():
        if not isinstance(cfg, dict):
            errors.append(f"Key '{key}': value must be a JSON object.")
            continue
        missing = required_fields - set(cfg.keys())
        if missing:
            errors.append(f"'{key}' is missing fields: {', '.join(sorted(missing))}")

    if errors:
        st.error("rules.json validation failed:\n- " + "\n- ".join(errors))
        st.stop()

    return rules

RULES = load_rules()


# -------------------------------
# Utility: Parse readData.ps1 output safely (multi-line aware)
# -------------------------------
def parse_ps_output(output: str) -> Dict[str, str]:
    """
    Parses PowerShell 'Key: Value' style output, supporting multi-line values.
    Continues collecting lines for a key until a new 'Key:' line is found.
    """
    data: Dict[str, str] = {}
    key_pat = re.compile(r'^\s*([A-Za-z0-9._&() \-```math
```/\```+?)\s*:\s*(.*)$')

    current_key: Optional[str] = None
    buffer: List[str] = []

    for raw_line in output.splitlines():
        line = raw_line.rstrip("\r")
        m = key_pat.match(line)
        if m:
            # Store previous key/value
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

    # Optional normalization for common fields
    # (Use these keys if your readData.ps1 matches)
    # data['AppName'] = data.get('AppName') or data.get('DisplayName', '')
    # data['Publisher'] = data.get('Publisher') or data.get('Vendor', '')
    # data['Version'] = data.get('Version') or data.get('ProductVersion', '')

    return data


# -------------------------------
# Utility: Get Winget description with GitHub Code Search
# -------------------------------
def _get_github_token() -> Optional[str]:
    """
    Reads GitHub token from environment or Streamlit secrets to avoid rate limits.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        try:
            token = st.secrets.get("GITHUB_TOKEN")  # type: ignore[attr-defined]
        except Exception:
            token = None
    return token

@st.cache_data(ttl=86400, show_spinner=False)
def get_info_from_winget(app_name: str) -> str:
    """
    Searches microsoft/winget-pkgs for the app's manifest and returns Description/ShortDescription.
    More robust: timeouts, optional auth, narrow search, checks top matches.
    """
    try:
        # Sanitize the search term a bit
        search_term = app_name.split(" (")[0].strip()
        if not search_term:
            return f"{app_name} is a widely-used application."

        headers = {"Accept": "application/vnd.github.v3+json"}
        token = _get_github_token()
        if token:
            headers["Authorization"] = f"token {token}"

        # Narrow search to YAML manifests under /manifests
        q = f'{search_term} in:file repo:microsoft/winget-pkgs path:/manifests language:yaml'
        url = "https://api.github.com/search/code"
        params = {"q": q, "per_page": 5}
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        items = r.json().get("items", [])[:5]
        if not items:
            return f"{app_name} is a versatile utility designed to enhance productivity."

        # Look through a few matches until we find a good description
        for it in items:
            raw_url = it["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            m = requests.get(raw_url, headers=headers, timeout=10)
            m.raise_for_status()

            # Some manifests contain multiple docs
            docs = list(yaml.safe_load_all(m.text)) if m.text.strip().startswith("---") else [yaml.safe_load(m.text)]
            for doc in docs:
                if isinstance(doc, dict):
                    desc = doc.get("Description") or doc.get("ShortDescription")
                    if desc:
                        text = str(desc).strip()
                        # Make sure we don’t return empty
                        if text:
                            return text

        # Fallback if none found
        return f"{app_name} is a widely-used application."
    except Exception:
        # Never block the app on network hiccups
        return f"{app_name} is a versatile utility designed to enhance productivity."


# -------------------------------
# Utility: Generate a professional icon (PNG bytes) with black initials
# -------------------------------
def _build_icon_image(app_name: str, width: int = 256, height: int = 256) -> Image.Image:
    """
    Creates an orange gradient square with black initials in the center.
    """
    # Soft orange gradient background
    top_color = (255, 204, 153)   # light orange
    bottom_color = (255, 153, 51) # deeper orange
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / height)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * y / height)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Initials in black
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 100)
    except IOError:
        font = ImageFont.load_default()

    words = re.findall(r"[A-Z][a-z]*|\d+", app_name) or [app_name]
    initials = "".join([w[0] for w in words[:2]]).upper()
    if not initials:
        initials = app_name[:2].upper() if len(app_name) else "A"

    bbox = draw.textbbox((0, 0), initials, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) / 2
    y = (height - text_h) / 2
    draw.text((x, y), initials, font=font, fill=COLOR_TEXT)

    # Subtle border
    draw.rounded_rectangle([(2, 2), (width - 3, height - 3)], radius=28, outline=(255, 140, 0), width=4)
    return img

@st.cache_data(show_spinner=False)
def generate_icon_bytes(app_name: str) -> bytes:
    img = _build_icon_image(app_name)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# -------------------------------
# Helper: Guess installer type by filename extension
# -------------------------------
def guess_type_from_filename(filename: str) -> str:
    """
    Simple heuristic: .msi -> 'msi', .exe -> default to 'exe_nsis' unless rules specify otherwise.
    """
    low = filename.lower()
    if low.endswith(".msi"):
        return "msi"
    if low.endswith(".exe"):
        # prefer whichever exists in RULES in expected order
        for candidate in ("exe_nsis", "exe_inno", "exe"):
            if candidate in RULES:
                return candidate
        return "exe_nsis"
    return next(iter(RULES.keys()))  # fallback to first available


# -------------------------------
# Helper: Build exportable recipe content
# -------------------------------
def build_recipe_json(data: Dict[str, Any], install_cmd: str, description: str) -> Dict[str, Any]:
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
    md.append("## Detection Rules")
    md.append(f"- Recommended: {detection_method}")
    md.append("  - HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
    md.append("  - HKLM\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
    return "\n".join(md)


# -------------------------------
# Title Section
# -------------------------------
st.markdown("""
<div class="title-wrap">
  <div class="title">PackPilot Pro</div>
  <div class="tagline">Your intelligent packaging copilot — clean, consistent, and fast.</div>
</div>
""", unsafe_allow_html=True)


# -------------------------------
# Step 1: Upload installers (choose primary)
# -------------------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title"><span class="step-badge">1</span> Upload package files (.exe/.msi)</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload all relevant files for this package",
        accept_multiple_files=True,
        key="multi_uploader"
    )

    primary_installer = None
    installer_names: List[str] = []
    if uploaded_files:
        installers = [f for f in uploaded_files if f.name.lower().endswith((".exe", ".msi"))]
        if installers:
            installer_names = [f.name for f in installers]
            selected_name = st.selectbox("Choose primary installer", installer_names, index=0, key="primary_installer_select")
            primary_installer = next((f for f in installers if f.name == selected_name), None)
            if primary_installer:
                st.success(f"Primary installer: {primary_installer.name}")
        else:
            st.warning("No .exe or .msi files detected. Please add at least one installer.")
    else:
        st.info("Tip: You can drag & drop multiple files here.")

    st.markdown('</div>', unsafe_allow_html=True)


# -------------------------------
# Step 2: Paste readData.ps1 output (parse)
# -------------------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title"><span class="step-badge">2</span> Paste output from readData.ps1</div>', unsafe_allow_html=True)

    ps_output_text = st.text_area(
        "Paste the PowerShell script output (Key: Value per line; multi-line values supported)",
        height=160,
        key="ps_output"
    )

    col_parse, col_clear = st.columns([1, 1])
    with col_parse:
        if st.button("Parse Data", key="parse_btn", type="secondary"):
            if ps_output_text.strip():
                st.session_state.parsed_data = parse_ps_output(ps_output_text)
                if st.session_state.parsed_data:
                    st.success("Data parsed successfully.")
                else:
                    st.warning("No key/value pairs detected. Please verify the script output format.")
            else:
                st.error("Please paste the script output first.")
    with col_clear:
        if st.button("Clear Parsed Data", key="clear_btn", type="secondary"):
            st.session_state.pop("parsed_data", None)
            st.experimental_rerun()

    # Optional preview of parsed data keys
    if st.session_state.get("parsed_data"):
        with st.expander("Preview parsed keys"):
            st.json(st.session_state.parsed_data, expanded=False)

    st.markdown('</div>', unsafe_allow_html=True)


# -------------------------------
# Step 3: Verify auto-filled details and options
# -------------------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title"><span class="step-badge">3</span> Verify and confirm details</div>', unsafe_allow_html=True)

    ready_for_recipe = False
    if primary_installer and st.session_state.get("parsed_data"):
        parsed = st.session_state.parsed_data

        # Autofill from parsed data where available
        default_app_name = parsed.get("AppName", parsed.get("DisplayName", ""))
        default_vendor = parsed.get("Publisher", parsed.get("Vendor", ""))
        default_version = parsed.get("Version", parsed.get("ProductVersion", ""))
        default_arch = parsed.get("Architecture", "64-bit")
        default_context = parsed.get("InstallContext", "System")
        default_aafn = parsed.get("AppsAndFeaturesName", default_app_name or "Unknown")

        app_name = st.text_input("Application Name", value=default_app_name, key="app_name_input")
        vendor = st.text_input("Vendor", value=default_vendor, key="vendor_input")
        version = st.text_input("Version", value=default_version, key="version_input")

        # Installer type logic (interactive wins over type)
        col_type, col_interactive = st.columns([2, 1])
        with col_type:
            guessed_type = guess_type_from_filename(primary_installer.name)
            type_options = list(RULES.keys())
            default_idx = type_options.index(guessed_type) if guessed_type in type_options else 0
            installer_type_key = st.selectbox(
                "Installer Type",
                options=type_options,
                index=default_idx,
                format_func=lambda x: RULES[x]["installer_type"]
            )
        with col_interactive:
            is_interactive = st.checkbox("Requires user interaction (ServiceUI)", value=False, help="Use interactive rules if defined in rules.json")

        # If interactive is checked and rules contain an 'interactive' profile, use it; otherwise use selected type
        if is_interactive and "interactive" in RULES:
            final_type_key = "interactive"
        else:
            final_type_key = installer_type_key

        # Environment/metadata details
        col_ctx, col_arch = st.columns([1, 1])
        with col_ctx:
            install_context = st.text_input("Install Context", value=default_context)
        with col_arch:
            architecture = st.text_input("Architecture", value=default_arch)

        apps_and_features_name = st.text_input("Apps & Features Name", value=default_aafn)

        # Validate rules presence and install template
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

        if st.button("Generate Recipe 🚀", use_container_width=True, type="primary", key="generate_btn"):
            if not app_name or not vendor or not version:
                st.error("Please fill in Application Name, Vendor, and Version.")
            elif not ready_for_recipe:
                st.error("Please fix the missing rules before generating.")
            else:
                st.session_state.generate = True
                st.session_state.recipe_data = {
                    "app_name": app_name,
                    "vendor": vendor,
                    "version": version,
                    "installer_type_key": final_type_key,
                    "uploaded_filename": primary_installer.name,
                    "apps_and_features_name": apps_and_features_name,
                    "architecture": architecture,
                    "install_context": install_context,
                }

    else:
        st.info("Select a primary installer and parse data to continue.")

    st.markdown('</div>', unsafe_allow_html=True)


# -------------------------------
# Step 4: Deployment Recipe — details, commands, detection, exports
# -------------------------------
if st.session_state.get("generate") and st.session_state.get("recipe_data"):
    data = st.session_state.recipe_data
    recipe_rules = RULES[data["installer_type_key"]]

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="step-title"><span class="step-badge">4</span> Deployment Recipe</div>', unsafe_allow_html=True)

        # Build install command from template
        install_cmd = recipe_rules["install_command"].format(filename=data["uploaded_filename"])

        # Fetch description from Winget (with spinner)
        with st.spinner("Fetching app description from Winget manifests..."):
            description = get_info_from_winget(data["app_name"])

        # Tabs: Overview, Config, Detection, Exports
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "⚙️ Configuration", "🔍 Detection", "⬇️ Exports"])

        # Overview tab
        with tab1:
            st.text_input("App Name", value=data["app_name"], disabled=True)
            st.text_input("Vendor", value=data["vendor"], disabled=True)
            st.text_input("Version", value=data["version"], disabled=True)
            st.text_area("Description (Winget)", value=description, height=120, disabled=True)

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

        # Config tab
        with tab2:
            st.text_input("Installer Type", value=data["installer_type_key"], disabled=True)
            st.text_input("Install Context", value=data["install_context"], disabled=True)
            st.text_input("Architecture", value=data["architecture"], disabled=True)
            st.text_input("Apps & Features Name", value=data["apps_and_features_name"], disabled=True)

            st.subheader("Install Command")
            st.code(install_cmd, language="powershell")

        # Detection tab
        with tab3:
            st.info(f"Recommended Method: {recipe_rules['detection_method']}")
            st.write("Common registry locations to check:")
            st.code(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", language="text")
            st.code(r"HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall", language="text")

        # Exports tab
        with tab4:
            recipe_json = build_recipe_json(data, install_cmd, description)
            recipe_md = build_recipe_markdown(recipe_json, recipe_rules["detection_method"])

            st.subheader("Download Recipe (JSON)")
            st.download_button(
                "Download recipe.json",
                data=json.dumps(recipe_json, indent=2).encode("utf-8"),
                file_name=f"{data['app_name'].replace(' ', '_')}_recipe.json",
                mime="application/json",
                type="secondary"
            )

            st.subheader("Download Readme (Markdown)")
            st.download_button(
                "Download README.md",
                data=recipe_md.encode("utf-8"),
                file_name=f"{data['app_name'].replace(' ', '_')}_README.md",
                mime="text/markdown",
                type="secondary"
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # Keep state so user can navigate tabs; if you want to reset after export:
    # st.session_state.pop("generate", None)


# -------------------------------
# Footer: Light guidance
# -------------------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("Need changes to rules.json structure or new installer types? Add them in the repo, and this app will adapt automatically.")
    st.markdown('</div>', unsafe_allow_html=True)
