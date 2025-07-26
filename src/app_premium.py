import streamlit as st
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface, render_query_suggestions
from components.result_display import render_data_table, render_chart_options, render_query_insights

def load_custom_css():
    """Load custom CSS for premium styling"""
    css_path = os.path.join(os.path.dirname(__file__), "styles", "main.css")
    try:
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Using default styling.")

def main():
    """Main application function"""
    
    # Page configuration
    st.set_page_config(
        page_title="DrQuery",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom styling
    load_custom_css()
    
    # Hide Streamlit default elements
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    main_container = st.container()
    
    with main_container:
        # Premium welcome section for new users
        if "db" not in st.session_state:
            st.markdown("""
            <div class="welcome-section" style="text-align: center; padding: 3rem 2rem; background: linear-gradient(145deg, rgba(42, 42, 42, 0.8), rgba(51, 51, 51, 0.6), rgba(68, 68, 68, 0.4)); border-radius: 24px; border: 1px solid rgba(85, 85, 85, 0.5); margin: 2rem 0; box-shadow: 0 20px 80px rgba(0, 0, 0, 0.8), 0 8px 32px rgba(16, 163, 127, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.05); position: relative; overflow: hidden; font-family: 'Poppins', sans-serif;">
                <div style="position: relative; z-index: 2;">
                    <div class="logo-container" style="margin-bottom: 1.5rem;">
                        <div class="logo-glow" style="width: 80px; height: 80px; background: radial-gradient(circle, rgba(16, 163, 127, 0.4) 0%, transparent 70%);"></div>
                        <h1 class="logo-text" style="margin: 0; font-size: 3rem; font-weight: 900; letter-spacing: -0.04em; background: linear-gradient(135deg, #10a37f, #16a085); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Poppins', sans-serif;">⚡ DrQuery</h1>
                    </div>
                    <div style="width: 100px; height: 2px; background: linear-gradient(90deg, transparent, #10a37f, #16a085, transparent); margin: 0 auto 2rem; border-radius: 2px; animation: textShine 3s ease-in-out infinite;"></div>
                    <p style="color: #ffffff; font-size: 1.4rem; margin-bottom: 2rem; font-weight: 600; text-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); font-family: 'Poppins', sans-serif;">Your AI Data Assistant</p>
                    <p style="color: #e0e0e0; max-width: 600px; margin: 0 auto; line-height: 1.6; font-size: 1.1rem; font-weight: 300; opacity: 0.9; font-family: 'Poppins', sans-serif;">
                        Connect to your database and start asking questions in natural language. 
                        DrQuery will generate SQL queries, fetch results, and provide insights automatically.
                    </p>
                    <div style="margin-top: 2.5rem; padding: 1.5rem 2rem; background: linear-gradient(145deg, rgba(42, 42, 42, 0.6), rgba(51, 51, 51, 0.4)); border-radius: 16px; border: 1px solid rgba(85, 85, 85, 0.3); backdrop-filter: blur(20px); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);">
                        <p style="color: #888888; font-weight: 700; font-size: 1.1rem; margin: 0; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5); font-family: 'Poppins', sans-serif;">👈 Get started by connecting to your database in the sidebar</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            

        
        else:
            # Chat interface for connected users
            render_chat_interface()
            
            # Show tables option
            if st.session_state.get("show_tables", False):
                with st.expander("📋 Database Tables", expanded=True):
                    try:
                        tables_info = st.session_state.db.get_table_info()
                        st.code(tables_info, language="sql")
                        st.session_state.show_tables = False
                    except Exception as e:
                        st.error(f"Error fetching table information: {str(e)}")
            
            # Add bottom padding for fixed search bar
            st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()