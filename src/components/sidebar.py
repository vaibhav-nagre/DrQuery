import streamlit as st
from utils.database import init_database

def render_sidebar():
    """Render ChatGPT-like sidebar"""
    
    with st.sidebar:
        # Simple Logo Header
        st.markdown("""
        <div class="logo-header" style="text-align: center; padding: 0.75rem 0; margin: -1rem -1rem 0.5rem -1rem;">
            <div class="logo-container" style="position: relative; display: inline-block;">
                <div class="logo-glow" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: radial-gradient(circle, rgba(16, 163, 127, 0.3) 0%, transparent 70%); border-radius: 50%; animation: pulse 2s ease-in-out infinite;"></div>
                <h2 class="logo-text" style="margin: 0; font-weight: 800; font-size: 1.6rem; color: var(--primary-color); font-family: 'Poppins', sans-serif; position: relative; z-index: 2; animation: textShine 3s ease-in-out infinite;">⚡ DrQuery</h2>
            </div>
            <p style="color: var(--text-muted); margin: 0.75rem 0 0 0; font-size: 0.9rem; font-family: 'Poppins', sans-serif; opacity: 0.8;">AI Data Assistant</p>
            <div class="logo-line" style="width: 40px; height: 2px; background: linear-gradient(90deg, transparent, var(--primary-color), transparent); margin: 1rem auto 0; border-radius: 1px; animation: lineGlow 2s ease-in-out infinite;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Connection Status
        connection_status = "db" in st.session_state
        status_color = "#10a37f" if connection_status else "#ef4444"
        status_text = "Connected" if connection_status else "Disconnected"
        
        st.markdown(f"""
        <div style="background: var(--background-card); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; border: 1px solid var(--border-color);">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: {status_color};"></div>
                <span style="color: var(--text-primary); font-weight: 500; font-size: 0.9rem; font-family: 'Poppins', sans-serif;">Database Status</span>
            </div>
            <p style="color: {status_color}; margin: 0.5rem 0 0 0; font-size: 0.85rem; font-family: 'Poppins', sans-serif;">{status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Database Connection Section
        with st.expander("🔗 Database Connection", expanded=not connection_status):
            st.text_input("Host", value="localhost", key="Host", help="Database host address")
            st.text_input("Port", value="3306", key="Port", help="Database port")
            st.text_input("User", value="root", key="User", help="Database username")
            st.text_input("Password", type="password", value="admin", key="Password", help="Database password")
            st.text_input("Database", value="drqueryDB", key="Database", help="Database name")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Connect", use_container_width=True):
                    with st.spinner("Connecting..."):
                        try:
                            db = init_database(
                                st.session_state["User"],
                                st.session_state["Password"],
                                st.session_state["Host"],
                                st.session_state["Port"],
                                st.session_state["Database"]
                            )
                            st.session_state.db = db
                            st.success("Connected successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Connection failed: {str(e)}")
            
            with col2:
                if st.button("Disconnect", use_container_width=True, disabled=not connection_status):
                    if "db" in st.session_state:
                        del st.session_state.db
                    st.success("Disconnected!")
                    st.rerun()
        
        # Query History Section
        if "chat_history" in st.session_state and len(st.session_state.chat_history) > 1:
            with st.expander("📝 Recent Queries"):
                human_messages = [msg for msg in st.session_state.chat_history if hasattr(msg, 'content') and not msg.content.startswith("Hello")]
                
                for i, msg in enumerate(human_messages[-5:]):  # Show last 5 queries
                    if hasattr(msg, 'content'):
                        query_preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                        if st.button(f"💬 {query_preview}", key=f"history_{i}", use_container_width=True):
                            st.session_state.selected_query = msg.content
        
        # Quick Actions
        with st.expander("⚡ Quick Actions"):
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = [st.session_state.chat_history[0]]  # Keep welcome message
                st.rerun()
            
            if st.button("📊 Show Tables", use_container_width=True, disabled=not connection_status):
                if connection_status:
                    st.session_state.show_tables = True
    