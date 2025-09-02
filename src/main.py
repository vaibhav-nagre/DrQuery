import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import custom components
from components.sidebar import render_sidebar
from components.chat_tab import render_chat_tab
from components.visualization_tab import render_visualization_tab
from components.query_builder_tab import render_query_builder_tab

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="DrQuery",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Modern Dark Ocean Theme
st.markdown("""
<style>
    /* ========== GLOBAL DARK OCEAN THEME ========== */
    
    /* Root Variables for Consistent Theming */
    :root {
        --primary-ocean: #0891b2;
        --primary-ocean-dark: #0e7490;
        --primary-ocean-light: #06b6d4;
        --accent-teal: #14b8a6;
        --accent-teal-light: #5eead4;
        
        --bg-primary: #1e293b;
        --bg-secondary: #334155;
        --bg-tertiary: #475569;
        --bg-card: #2d3748;
        --bg-sidebar: #1a202c;
        
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --text-accent: #67e8f9;
        
        --border-color: #475569;
        --border-accent: #0891b2;
        --shadow-ocean: 0 4px 20px rgba(8, 145, 178, 0.15);
        --shadow-dark: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* ========== HEADER & TOP AREA STYLING ========== */
    
    /* Streamlit Header */
    .stApp > header {
        background: transparent !important;
        height: 0 !important;
    }
    
    /* Top toolbar/header area */
    .stApp > header[data-testid="stHeader"] {
        background: var(--bg-primary) !important;
        border-bottom: 1px solid var(--border-color) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Menu button */
    .stApp > header button {
        color: var(--text-primary) !important;
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    .stApp > header button:hover {
        background: var(--primary-ocean) !important;
        border-color: var(--accent-teal) !important;
    }
    
    /* Deploy button and other header elements */
    .stApp > header [data-testid="stToolbar"] {
        background: var(--bg-secondary) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
        padding: 4px 8px !important;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        color: var(--text-primary) !important;
    }
    
    /* Global Responsive Container - allow natural expansion */
    html, body, #root, .stApp {
        height: auto !important;
        min-height: 100vh !important;
    }
    
    /* Main Container - responsive width with natural height */
    .main .block-container {
        background: transparent !important;
        padding-top: 1rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
        min-height: 100vh !important;
    }
    
    /* Remove default padding from main content */
    .main {
        background: transparent !important;
        min-height: 100vh !important;
    }
    
    /* Top spacing fix - natural height */
    .stApp .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        min-height: calc(100vh - 1rem) !important;
    }
    
    /* Tab styling improvements - let tabs expand naturally except for specific overrides */
    .stTabs [data-baseweb="tab-panel"] {
        overflow-y: auto !important;
        /* Let content determine height by default */
        height: auto !important;
        max-height: none !important;
        padding: 0.5rem !important;
    }
    
    /* ========== SIDEBAR STYLING ========== */
    
    /* Sidebar Container */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--bg-sidebar) 0%, #2d3748 100%) !important;
        border-right: 2px solid var(--border-accent) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Sidebar Content Text */
    .css-1d391kg .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    /* Sidebar Text Elements */
    .css-1d391kg .stMarkdown p {
        color: var(--text-primary) !important;
    }
    
    /* Sidebar Expander Headers */
    .css-1d391kg .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar Expander Content */
    .css-1d391kg .streamlit-expanderContent {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        color: var(--text-primary) !important;
    }
    
    /* Sidebar Input Fields */
    .css-1d391kg .stTextInput > div > div > input {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
    }
    
    .css-1d391kg .stTextInput > div > div > input:focus {
        border-color: var(--primary-ocean) !important;
        box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.2) !important;
    }
    
    /* Sidebar Text Visibility Fixes */
    .css-1d391kg .stMarkdown, .css-1lcbmhc .stMarkdown, .css-1y4p8pa .stMarkdown, section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    .css-1d391kg .stMarkdown p, .css-1lcbmhc .stMarkdown p, .css-1y4p8pa .stMarkdown p, section[data-testid="stSidebar"] .stMarkdown p {
        color: var(--text-primary) !important;
    }
    
    .css-1d391kg .stMarkdown h1, .css-1d391kg .stMarkdown h2, .css-1d391kg .stMarkdown h3, .css-1d391kg .stMarkdown h4 {
        color: var(--text-primary) !important;
    }
    
    .css-1d391kg .stMarkdown strong, .css-1d391kg .stMarkdown b {
        color: var(--text-accent) !important;
    }
    
    /* Sidebar Expander Text */
    .css-1d391kg .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    
    .css-1d391kg .streamlit-expanderHeader p {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    .css-1d391kg .streamlit-expanderContent {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        color: var(--text-primary) !important;
    }
    
    .css-1d391kg .streamlit-expanderContent .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    .css-1d391kg .streamlit-expanderContent p {
        color: var(--text-primary) !important;
    }
    
    /* Sidebar Input Fields */
    .css-1d391kg .stTextInput > div > div > input {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
    }
    
    .css-1d391kg .stTextInput > div > div > input:focus {
        border-color: var(--primary-ocean) !important;
        box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.2) !important;
    }
    
    .css-1d391kg .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
        opacity: 0.7 !important;
    }
    
    /* Sidebar Input Labels */
    .css-1d391kg .stTextInput label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar Buttons */
    .css-1d391kg .stButton > button {
        background: linear-gradient(135deg, var(--primary-ocean) 0%, var(--accent-teal) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-ocean) !important;
    }
    
    .css-1d391kg .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(8, 145, 178, 0.3) !important;
        background: linear-gradient(135deg, var(--primary-ocean-dark) 0%, var(--primary-ocean) 100%) !important;
    }
    
    /* Sidebar Success/Error Messages */
    .css-1d391kg .stSuccess {
        background: linear-gradient(135deg, rgba(20, 184, 166, 0.15) 0%, rgba(94, 234, 212, 0.15) 100%) !important;
        border: 1px solid var(--accent-teal) !important;
        border-radius: 12px !important;
        color: var(--accent-teal-light) !important;
    }
    
    .css-1d391kg .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(248, 113, 113, 0.15) 100%) !important;
        border: 1px solid #ef4444 !important;
        border-radius: 12px !important;
        color: #fca5a5 !important;
    }
    
    .css-1d391kg .stSuccess p, .css-1d391kg .stError p {
        color: inherit !important;
        margin: 0 !important;
    }
    
    /* Alternative sidebar selectors for different Streamlit versions */
    .css-1lcbmhc, .css-1y4p8pa, section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-sidebar) 0%, #2d3748 100%) !important;
        border-right: 2px solid var(--border-accent) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    .css-1lcbmhc .stMarkdown, .css-1y4p8pa .stMarkdown, section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    /* ========== TEXT VISIBILITY & CONTRAST FIXES ========== */
    
    /* Global text color fixes */
    .stApp, .stApp .main, .main {
        color: var(--text-primary) !important;
    }
    
    /* All paragraphs and text elements */
    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: var(--text-primary) !important;
    }
    
    /* Headers and titles */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* Special blue headers for visualization tab */
    .stTabs [data-baseweb="tab-panel"][aria-label="Visualization"] h3,
    .stTabs [data-baseweb="tab-panel"][aria-label="Visualization"] h4,
    .stTabs [data-baseweb="tab-panel"] .viz-header-blue h3,
    .stTabs [data-baseweb="tab-panel"] .viz-header-blue h4,
    .stTabs [data-baseweb="tab-panel"] h3[data-viz-blue="true"],
    .stTabs [data-baseweb="tab-panel"] h4[data-viz-blue="true"] {
        color: #0891b2 !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Strong and bold text */
    .stMarkdown strong, .stMarkdown b {
        color: var(--text-accent) !important;
        font-weight: 700 !important;
    }
    
    /* Lists */
    .stMarkdown ul, .stMarkdown ol, .stMarkdown li {
        color: var(--text-primary) !important;
    }
    
    /* Code inline */
    .stMarkdown code {
        background: var(--bg-secondary) !important;
        color: var(--text-accent) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Links */
    .stMarkdown a {
        color: var(--primary-ocean-light) !important;
        text-decoration: none !important;
    }
    
    .stMarkdown a:hover {
        color: var(--accent-teal-light) !important;
        text-decoration: underline !important;
    }
    
    /* Captions and small text */
    .caption, .stCaption {
        color: var(--text-muted) !important;
        font-size: 0.875rem !important;
    }
    
    /* Tab content text */
    .stTabs [data-baseweb="tab-panel"] .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] p {
        color: var(--text-primary) !important;
    }
    
    /* Form labels */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }
    
    /* Help text */
    .stTextInput div[data-testid="stMarkdownContainer"] small,
    .stTextArea div[data-testid="stMarkdownContainer"] small,
    .stSelectbox div[data-testid="stMarkdownContainer"] small {
        color: var(--text-muted) !important;
    }
    
    /* Placeholder text */
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
        opacity: 0.7 !important;
    }
    
    /* Main content warning/info text styling */
    .main .stWarning p, .main .stInfo p, .main .stSuccess p, .main .stError p {
        color: var(--text-primary) !important;
        margin: 0 !important;
    }
    
    /* Strong text in messages */
    .main .stInfo strong, .main .stWarning strong, .main .stSuccess strong, .main .stError strong {
        color: var(--text-accent) !important;
    }
    
    /* Specific alert text colors */
    .stSuccess {
        color: var(--accent-teal-light) !important;
    }
    
    .stError {
        color: #fca5a5 !important;
    }
    
    .stWarning {
        color: #fcd34d !important;
    }
    
    .stInfo {
        color: var(--text-accent) !important;
    }
    
    /* Metric values and labels */
    .metric-value {
        color: var(--text-primary) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    .metric-label {
        color: var(--text-secondary) !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Expander text */
    .streamlit-expanderHeader p {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    /* DataFrames text */
    .stDataFrame table {
        color: var(--text-primary) !important;
    }
    
    .stDataFrame th {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    .stDataFrame td {
        color: var(--text-primary) !important;
    }
    
    /* Alternative header selectors for different Streamlit versions */
    header[data-testid="stHeader"], .stApp > header, .css-18ni7ap, .css-vk3wp9 {
        background: var(--bg-primary) !important;
        border-bottom: 1px solid var(--border-color) !important;
        backdrop-filter: blur(10px) !important;
        height: auto !important;
        color: var(--text-primary) !important;
    }
    
    /* Fix any white backgrounds in header area */
    .css-1rs6os, .css-17eq0hr, .css-1kyxreq {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Warning/Info messages in main area */
    .main .stWarning, .main .stInfo, .main .stSuccess, .main .stError {
        background: var(--bg-card) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        box-shadow: var(--shadow-dark) !important;
    }
    
    /* Additional contrast fixes for specific elements */
    
    /* Selectbox dropdown */
    .stSelectbox div[data-baseweb="select"] {
        background: var(--bg-secondary) !important;
        border: 2px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Selectbox options */
    .stSelectbox div[role="listbox"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stSelectbox div[role="option"] {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }
    
    .stSelectbox div[role="option"]:hover {
        background: var(--primary-ocean) !important;
        color: white !important;
    }
    
    /* Multiselect */
    .stMultiSelect div[data-baseweb="select"] {
        background: var(--bg-secondary) !important;
        border: 2px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Date/Time inputs */
    .stDateInput input, .stTimeInput input {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
    }
    
    /* Slider */
    .stSlider .slider-thumb {
        background: var(--primary-ocean) !important;
    }
    
    .stSlider .slider-track {
        background: var(--bg-tertiary) !important;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: var(--text-primary) !important;
    }
    
    /* Checkboxes */
    .stCheckbox label {
        color: var(--text-primary) !important;
    }
    
    /* Progress bars */
    .stProgress .progress-bar {
        background: var(--primary-ocean) !important;
    }
    
    /* Spinner text */
    .stSpinner div {
        color: var(--text-primary) !important;
    }
    
    /* File uploader */
    .stFileUploader label {
        color: var(--text-primary) !important;
    }
    
    .stFileUploader section {
        background: var(--bg-secondary) !important;
        border: 2px dashed var(--border-color) !important;
    }
    
    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(135deg, var(--primary-ocean) 0%, var(--accent-teal) 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    /* Charts and plots */
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* ========== TAB STYLING ========== */
    
    /* Tab List Container */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(90deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%) !important;
        padding: 12px 20px !important;
        border-radius: 16px !important;
        margin-bottom: 24px !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: var(--shadow-dark) !important;
        gap: 16px !important;
    }
    
    /* Individual Tab Buttons */
    .stTabs [data-baseweb="tab-list"] button {
        background: var(--bg-card) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        height: 50px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    /* Tab Button Hover Effect */
    .stTabs [data-baseweb="tab-list"] button:hover {
        background: var(--primary-ocean-dark) !important;
        color: var(--text-primary) !important;
        border-color: var(--accent-teal) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-ocean) !important;
    }
    
    /* Active Tab */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-ocean) 0%, var(--accent-teal) 100%) !important;
        color: white !important;
        border-color: var(--accent-teal-light) !important;
        box-shadow: var(--shadow-ocean) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Tab Text Styling */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px !important;
        font-weight: 600 !important;
        margin: 0 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* ========== CONTENT AREAS ========== */
    
    /* Tab Content Panels */
    .stTabs [data-baseweb="tab-panel"] {
        background: var(--bg-card) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: var(--shadow-dark) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* ========== FORM ELEMENTS ========== */
    
    /* Text Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    /* Input Focus States */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary-ocean) !important;
        box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.2) !important;
        outline: none !important;
    }
    
    /* ========== BUTTONS ========== */
    
    /* Primary Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-ocean) 0%, var(--accent-teal) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-ocean) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    /* Button Hover Effects */
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(8, 145, 178, 0.3) !important;
        background: linear-gradient(135deg, var(--primary-ocean-dark) 0%, var(--primary-ocean) 100%) !important;
    }
    
    /* Button Active State */
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* ========== ALERTS & MESSAGES ========== */
    
    /* Success Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(20, 184, 166, 0.15) 0%, rgba(94, 234, 212, 0.15) 100%) !important;
        border: 1px solid var(--accent-teal) !important;
        border-radius: 12px !important;
        color: var(--accent-teal-light) !important;
    }
    
    /* Error Messages */
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(248, 113, 113, 0.15) 100%) !important;
        border: 1px solid #ef4444 !important;
        border-radius: 12px !important;
        color: #fca5a5 !important;
    }
    
    /* Warning Messages */
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(251, 191, 36, 0.15) 100%) !important;
        border: 1px solid #f59e0b !important;
        border-radius: 12px !important;
        color: #fcd34d !important;
    }
    
    /* Info Messages */
    .stInfo {
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%) !important;
        border: 1px solid var(--primary-ocean) !important;
        border-radius: 12px !important;
        color: var(--text-accent) !important;
    }
    
    /* ========== DATA DISPLAY ========== */
    
    /* DataFrames */
    .stDataFrame {
        background: var(--bg-secondary) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-dark) !important;
    }
    
    /* Code Blocks */
    .stCodeBlock {
        background: var(--bg-sidebar) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        box-shadow: var(--shadow-dark) !important;
    }
    
    /* ========== EXPANDERS ========== */
    
    /* Expander Headers */
    .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    /* Expander Content */
    .streamlit-expanderContent {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* ========== METRICS & CARDS ========== */
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: var(--shadow-dark) !important;
        transition: all 0.3s ease !important;
    }
    
    /* ========== SCROLLBARS ========== */
    
    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary) !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-ocean) !important;
        border-radius: 4px !important;
        transition: all 0.3s ease !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-teal) !important;
    }
    
    /* ========== ANIMATIONS ========== */
    
    @keyframes oceanGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(8, 145, 178, 0.3); }
        50% { box-shadow: 0 0 30px rgba(20, 184, 166, 0.5); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { 
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.7;
        }
        50% { 
            transform: translate(-50%, -50%) scale(1.1);
            opacity: 1;
        }
    }
    
    @keyframes textShine {
        0%, 100% { 
            color: #0891b2;
            text-shadow: 0 0 10px rgba(8, 145, 178, 0.3);
        }
        50% { 
            color: #14b8a6;
            text-shadow: 0 0 20px rgba(20, 184, 166, 0.5);
        }
    }
    
    @keyframes lineGlow {
        0%, 100% { 
            opacity: 0.5;
            box-shadow: 0 0 5px rgba(8, 145, 178, 0.3);
        }
        50% { 
            opacity: 1;
            box-shadow: 0 0 15px rgba(20, 184, 166, 0.6);
        }
    }
    
    /* Apply animations to main containers */
    .stTabs [data-baseweb="tab-panel"] {
        animation: fadeInUp 0.5s ease-out !important;
    }
    
    /* ========== RESPONSIVE DESIGN ========== */
    
    /* Mobile devices */
    @media (max-width: 768px) {
        html, body, #root, .stApp {
            height: 100vh !important;
        }
        
        .main .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            max-width: 98% !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            padding: 8px 12px !important;
            gap: 8px !important;
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            padding: 8px 16px !important;
            font-size: 14px !important;
        }
    }
    
    /* Small screens / tablets */
    @media (max-height: 600px) {
        .main .block-container {
            padding-top: 0.25rem !important;
            padding-bottom: 0.25rem !important;
        }
    }
    
    /* Large screens */
    @media (min-width: 1400px) {
        .main .block-container {
            max-width: 90% !important;
        }
    }
    
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    from langchain_core.messages import AIMessage
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm DrQuery, created by Vaibhav Nagre. I'm your intelligent SQL assistant ready to help you explore and analyze your database."),
    ]

if "db" not in st.session_state:
    st.session_state.db = None

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Chat"

if "cross_tab_data" not in st.session_state:
    st.session_state.cross_tab_data = None

if "cross_tab_query" not in st.session_state:
    st.session_state.cross_tab_query = None

# Sidebar
render_sidebar()

# Main content area
if st.session_state.db is None:
    # Beautiful Welcome Homepage
    st.markdown("""
    <style>
    .homepage-container {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.05) 0%, rgba(20, 184, 166, 0.05) 100%);
        border-radius: 24px;
        border: 1px solid rgba(8, 145, 178, 0.2);
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(8, 145, 178, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .brand-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0891b2, #14b8a6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(8, 145, 178, 0.3);
    }
    
    .brand-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 3rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .creator-section {
        background: rgba(8, 145, 178, 0.1);
        border: 1px solid rgba(8, 145, 178, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 400px;
        backdrop-filter: blur(5px);
    }
    
    .creator-label {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .creator-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0891b2;
        margin-bottom: 0;
        letter-spacing: 0.5px;
    }
    
    .connect-hint {
        margin-top: 3rem;
        padding: 1.5rem;
        background: rgba(20, 184, 166, 0.1);
        border: 1px solid rgba(20, 184, 166, 0.3);
        border-radius: 12px;
        color: #5eead4;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: rgba(8, 145, 178, 0.08);
        border: 1px solid rgba(8, 145, 178, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(8, 145, 178, 0.2);
        border-color: rgba(8, 145, 178, 0.4);
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0891b2;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #94a3b8;
        line-height: 1.5;
    }
    </style>
    
    <div class="homepage-container">
        <div class="brand-title">⚡ DrQuery</div>
        <div class="brand-subtitle">Intelligent Database Query Assistant</div>
        <div class="creator-section">
            <div class="creator-label">Created by</div>
            <div class="creator-name">Vaibhav Nagre</div>
        </div> 
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-title">💬 Natural Language Chat</div>
                <div class="feature-desc">Query your database using plain English</div>
            </div>
            <div class="feature-card">
                <div class="feature-title">📊 Smart Visualizations</div>
                <div class="feature-desc">AI-powered chart generation from your data</div>
            </div>
            <div class="feature-card">
                <div class="feature-title">🛠️ Query Builder</div>
                <div class="feature-desc">Visual SQL query construction and editing</div>
            </div>
        </div>
        <div class="connect-hint">
            👈 Connect to your database using the sidebar to get started
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Chat", "Visualization", "Query Builder"])
    
    with tab1:
        render_chat_tab()
    
    with tab2:
        render_visualization_tab()
    
    with tab3:
        render_query_builder_tab()
