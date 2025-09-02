import streamlit as st
from utils.database import init_database

def render_sidebar():
    """Render ChatGPT-like sidebar"""
    
    with st.sidebar:
        # Simple Logo Header with Dark Theme
        st.markdown("""
        <div class="logo-header" style="text-align: center; padding: 0; margin: -3rem -1rem 0.5rem -1rem;">
            <div class="logo-container" style="position: relative; display: inline-block;">
                <div class="logo-glow" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: radial-gradient(circle, rgba(8, 145, 178, 0.3) 0%, transparent 70%); border-radius: 50%; animation: pulse 2s ease-in-out infinite;"></div>
                <h2 class="logo-text" style="margin: 0; font-weight: 800; font-size: 1.6rem; color: #0891b2; font-family: 'Poppins', sans-serif; position: relative; z-index: 2; animation: textShine 3s ease-in-out infinite;">⚡ DrQuery</h2>
            </div>
            <p style="color: #94a3b8; margin: 0.75rem 0 0 0; font-size: 0.9rem; font-family: 'Poppins', sans-serif; opacity: 0.8;">AI Data Assistant</p>
            <div class="logo-line" style="width: 40px; height: 2px; background: linear-gradient(90deg, transparent, #0891b2, transparent); margin: 1rem auto 0; border-radius: 1px; animation: lineGlow 2s ease-in-out infinite;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Connection Status - Check actual database connection
        connection_status = False
        if "db" in st.session_state and st.session_state.db is not None:
            try:
                # Test the connection by running a simple query
                result = st.session_state.db.run("SELECT 1 as test")
                # Also verify we can get table names
                tables = st.session_state.db.get_usable_table_names()
                connection_status = True
            except Exception as e:
                # Connection exists but is not working, remove it
                if "db" in st.session_state:
                    del st.session_state.db
                connection_status = False
        
        status_color = "#10a37f" if connection_status else "#ef4444"
        status_text = "Connected" if connection_status else "Disconnected"
        
        # Show additional info when connected
        additional_info = ""
        if connection_status and "db" in st.session_state:
            try:
                tables = st.session_state.db.get_usable_table_names()
                additional_info = f"<br><small style='color: #94a3b8; font-size: 0.75rem;'>{len(tables)} tables available</small>"
            except:
                pass
        
        st.markdown(f"""
        <div style="background: #2d3748; padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid #475569; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: {status_color}; box-shadow: 0 0 10px {status_color}40;"></div>
                <span style="color: #f1f5f9; font-weight: 500; font-size: 0.9rem; font-family: 'Poppins', sans-serif;">Database Status</span>
            </div>
            <p style="color: {status_color}; margin: 0.5rem 0 0 0; font-size: 0.85rem; font-family: 'Poppins', sans-serif; font-weight: 500;">{status_text}{additional_info}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Database Connection Section - Always expanded by default
        with st.expander("🔗 Database Connection", expanded=True):
            st.text_input("Host", value="localhost", key="Host", help="Database host address")
            st.text_input("Port", value="3306", key="Port", help="Database port")
            st.text_input("User", value="root", key="User", help="Database username")
            st.text_input("Password", type="password", value="admin", key="Password", help="Database password")
            st.text_input("Database Schema", value="drqueryDB", key="Database", help="Database name")
            
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
        with st.expander("Quick Actions"):
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.chat_history = [st.session_state.chat_history[0]]  # Keep welcome message
                st.rerun()
            
            if st.button("Show Tables", use_container_width=True, disabled=not connection_status):
                if connection_status:
                    st.session_state.show_tables = True
    