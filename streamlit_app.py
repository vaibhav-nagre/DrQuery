#!/usr/bin/env python3
"""
DrQuery - Intelligent Database Query Assistant
Main entry point for Streamlit Community Cloud deployment
Created by Vaibhav Nagre
"""

import streamlit as st
import sys
import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)
sys.path.insert(0, current_dir)

load_dotenv()

from src.components.sidebar import render_sidebar
from src.components.chat_tab import render_chat_tab
from src.components.visualization_tab import render_visualization_tab
from src.components.query_builder_tab import render_query_builder_tab

st.set_page_config(
    page_title="DrQuery",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
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
    
    .stApp {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        color: var(--text-primary) !important;
    }
    
    .main .block-container {
        background: transparent !important;
        padding-top: 1rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 0.5rem !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
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
</style>
""", unsafe_allow_html=True)

from langchain.schema import AIMessage

if "messages" not in st.session_state:
    st.session_state.messages = [
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

render_sidebar()

if st.session_state.db is None:
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, rgba(8, 145, 178, 0.05) 0%, rgba(20, 184, 166, 0.05) 100%); border-radius: 24px; border: 1px solid rgba(8, 145, 178, 0.2); margin: 2rem 0; box-shadow: 0 8px 32px rgba(8, 145, 178, 0.1);">
        <h1 style="font-size: 4rem; font-weight: 800; background: linear-gradient(135deg, #0891b2, #14b8a6, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">DrQuery ⚡</h1>
        <p style="font-size: 1.2rem; color: #94a3b8; margin-bottom: 3rem;">Intelligent Database Query Assistant</p>
        
        <div style="background: rgba(8, 145, 178, 0.1); border: 1px solid rgba(8, 145, 178, 0.3); border-radius: 16px; padding: 2rem; margin: 2rem auto; max-width: 400px;">
            <p style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">Created by</p>
            <h2 style="font-size: 1.8rem; font-weight: 700; color: #0891b2; margin: 0;">Vaibhav Nagre</h2>
        </div>
        
        <p style="margin-top: 3rem; padding: 1.5rem; background: rgba(20, 184, 166, 0.1); border: 1px solid rgba(20, 184, 166, 0.3); border-radius: 12px; color: #5eead4;">
            👈 Connect to your database using the sidebar to get started
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    tab1, tab2, tab3 = st.tabs(["Chat", "Visualization", "Query Builder"])
    
    with tab1:
        render_chat_tab()
    
    with tab2:
        render_visualization_tab()
    
    with tab3:
        render_query_builder_tab()
