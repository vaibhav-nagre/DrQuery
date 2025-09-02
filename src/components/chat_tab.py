import streamlit as st
import pandas as pd
import time
from langchain_core.messages import AIMessage, HumanMessage
from utils.ai_engine import get_response

def render_custom_chat_message(role, content, avatar="👤"):
    """Render a custom chat message with proper alignment and embedded visualizations"""
    
    # Debug: Print what we're getting
    print(f"DEBUG render_custom_chat_message: role={role}, content type={type(content)}")
    
    # Check if this is an AI message that might contain data or visualization requests
    should_render_viz = False
    df_data = None
    
    if role == "assistant":
        print(f"DEBUG: AI message detected")
        if hasattr(st.session_state, 'cross_tab_data') and st.session_state.cross_tab_data is not None:
            print(f"DEBUG: cross_tab_data available, shape: {st.session_state.cross_tab_data.shape}")
            # Check if the user's last message requested graphs or tables
            for msg in reversed(st.session_state.chat_history):
                if hasattr(msg, 'content') and isinstance(msg.content, str):
                    print(f"DEBUG: Checking message: {msg.content[:50]}...")
                    if any(word in msg.content.lower() for word in ['graph', 'chart', 'plot', 'visualize', 'table', 'tabular', 'data', 'show data', 'display data', 'tabular format', 'table format']):
                        print(f"DEBUG: Visualization keyword found!")
                        should_render_viz = True
                        df_data = st.session_state.cross_tab_data
                        break
        else:
            print(f"DEBUG: No cross_tab_data available")
    
    # Render the text part of the message
    if role == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
            <div style="background: #5865f2; color: white; padding: 12px 16px; border-radius: 12px; max-width: 70%; word-wrap: break-word;">
                {content}
            </div>
            <div style="width: 32px; height: 32px; background: #5865f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-left: 8px; flex-shrink: 0;">
                {avatar}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # AI message with potential visualizations
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
            <div style="width: 32px; height: 32px; background: #40444b; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 8px; flex-shrink: 0;">
                {avatar}
            </div>
            <div style="background: #36393f; color: #dcddde; padding: 12px 16px; border-radius: 12px; max-width: 70%; border: 1px solid #40444b; word-wrap: break-word;">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add visualizations if requested and data is available
        if should_render_viz and df_data is not None:
            print(f"DEBUG: Rendering visualizations...")
            render_chat_visualizations(df_data)
        else:
            print(f"DEBUG: Not rendering viz - should_render_viz={should_render_viz}, df_data available={df_data is not None}")


def render_chat_visualizations(df):
    """Render visualizations and tables within the chat interface"""
    
    print(f"DEBUG render_chat_visualizations: DataFrame shape = {df.shape}")
    print(f"DEBUG render_chat_visualizations: DataFrame columns = {df.columns.tolist()}")
    
    # Get the last user message to determine what type of visualization to show
    last_user_message = ""
    for msg in reversed(st.session_state.chat_history):
        if hasattr(msg, 'content') and isinstance(msg.content, str):
            last_user_message = msg.content.lower()
            print(f"DEBUG: Found user message: {last_user_message}")
            break
    
    # Instead of HTML containers, use a simple expander for better compatibility
    # Use container instead of expander to avoid nesting issues
        try:
            # Check what type of visualization is requested
            print(f"DEBUG: Checking for table keywords in: '{last_user_message}'")
            
            # Simplified table detection - prioritize table keywords
            if 'table' in last_user_message or 'tabular' in last_user_message:
                print(f"DEBUG: Table keywords found! Displaying table.")
                # Display table only
                st.subheader("📋 Data Table")
                st.dataframe(df, use_container_width=True, height=400)
                st.info(f"Showing {len(df)} rows × {len(df.columns)} columns")
                
            elif 'data' in last_user_message and not any(word in last_user_message for word in ['graph', 'chart', 'plot', 'visualize']):
                print(f"DEBUG: Data keyword found without chart keywords! Displaying table.")
                # Display table when data is requested without charts
                st.subheader("📋 Data Table")
                st.dataframe(df, use_container_width=True, height=400)
                st.info(f"Showing {len(df)} rows × {len(df.columns)} columns")
                
            elif any(word in last_user_message for word in ['graph', 'chart', 'plot', 'visualize']):
                # Display charts
                st.subheader("📈 Data Visualization")
                
                try:
                    import plotly.express as px
                    
                    # Get numeric and categorical columns
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                    
                    print(f"DEBUG: Numeric columns: {numeric_cols}")
                    print(f"DEBUG: Categorical columns: {categorical_cols}")
                    
                    if len(numeric_cols) >= 2:
                        # Scatter plot for two numeric columns
                        st.write(f"**Scatter Plot: {numeric_cols[0]} vs {numeric_cols[1]}**")
                        fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], 
                                       title=f"{numeric_cols[0]} vs {numeric_cols[1]}")
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Also show data table
                        st.markdown("**📋 Data Table**")
                        st.dataframe(df, use_container_width=True, height=300)
                        
                    elif len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
                        # Bar chart
                        st.write(f"**Bar Chart: {numeric_cols[0]} by {categorical_cols[0]}**")
                        chart_data = df.head(15)  # Limit for readability
                        fig = px.bar(chart_data, x=categorical_cols[0], y=numeric_cols[0],
                                   title=f"{numeric_cols[0]} by {categorical_cols[0]}")
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Also show data table
                        st.markdown("**📋 Data Table**")
                        st.dataframe(df, use_container_width=True, height=300)
                        
                    elif len(numeric_cols) >= 1:
                        # Histogram
                        st.write(f"**Distribution: {numeric_cols[0]}**")
                        fig = px.histogram(df, x=numeric_cols[0], 
                                         title=f"Distribution of {numeric_cols[0]}")
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Also show data table
                        st.markdown("**📋 Data Table**")
                        st.dataframe(df, use_container_width=True, height=300)
                        
                    else:
                        # Fallback to table if no suitable columns for charts
                        st.warning("No suitable numeric data for charts. Showing data table:")
                        st.dataframe(df, use_container_width=True, height=400)
                        
                except Exception as e:
                    st.error(f"Could not generate chart: {str(e)}")
                    st.dataframe(df, use_container_width=True, height=400)
            
            else:
                # Default: show both table and chart if possible
                st.subheader("📊 Query Results")
                
                # Show data table
                st.dataframe(df.head(20), use_container_width=True, height=300)
                if len(df) > 20:
                    st.info(f"Showing first 20 rows of {len(df)} total rows")
                
                # Try to show a simple chart
                try:
                    import plotly.express as px
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    if len(numeric_cols) >= 1:
                        st.subheader("📈 Quick Chart")
                        fig = px.histogram(df, x=numeric_cols[0])
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                except:
                    pass  # No chart if it fails
            
        except Exception as e:
            st.error(f"Error rendering visualization: {str(e)}")
            st.dataframe(df, use_container_width=True)


def render_chat_tab():
    """Render the main chat interface"""
    
    # Initialize session state for chat interface
    if "chat_input_key" not in st.session_state:
        st.session_state.chat_input_key = 0
    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False
    
    # Professional Chatbot CSS
    st.markdown("""
    <style>
    /* Main container with proper spacing - responsive */
    .main .block-container {
        padding-bottom: 80px !important;
        max-width: 100% !important;
        min-height: 100vh !important;
        padding-top: 1rem !important;
    }
    
    /* Chat container - responsive design for all screen sizes */
        /* ========== CUSTOM DISCORD/SLACK STYLE CHAT INTERFACE ========== */
    
    /* Chat Container - Responsive Height */
    [data-testid="stVerticalBlock"] > div > div > div[style*="height"] {
        height: calc(100vh - 250px) !important;
        max-height: calc(100vh - 250px) !important;
        min-height: 300px !important;
        overflow-y: auto !important;
        padding: 1rem !important;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border-radius: 12px !important;
        margin-bottom: 0 !important;
        scrollbar-width: thin;
        scrollbar-color: #475569 transparent;
    }
    
    [data-testid="stVerticalBlock"] > div > div > div[style*="height"]::-webkit-scrollbar {
        width: 6px;
    }
    
    [data-testid="stVerticalBlock"] > div > div > div[style*="height"]::-webkit-scrollbar-track {
        background: transparent;
    }
    
    [data-testid="stVerticalBlock"] > div > div > div[style*="height"]::-webkit-scrollbar-thumb {
        background-color: #475569;
        border-radius: 3px;
    }
    
    /* ========== CUSTOM CHAT MESSAGES ========== */
    
    /* Main message container */
    .custom-chat-message {
        width: 100%;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        animation: messageSlideIn 0.3s ease-out;
    }
    
    /* Message wrapper for alignment */
    .message-wrapper {
        display: flex;
        align-items: flex-end;
        gap: 8px;
        max-width: 100%;
    }
    
    /* User messages - Right aligned */
    .chat-message-user .message-wrapper {
        justify-content: flex-end;
        margin-left: 20%;
    }
    
    /* AI messages - Left aligned */
    .chat-message-assistant .message-wrapper {
        justify-content: flex-start;
        margin-right: 20%;
    }
    
    /* ========== MESSAGE BUBBLES ========== */
    
    /* Base bubble styling */
    .message-bubble {
        border-radius: 12px;
        padding: 12px 16px;
        max-width: 70%;
        min-width: 60px;
        word-wrap: break-word;
        position: relative;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        transition: all 0.2s ease;
    }
    
    .message-bubble:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* User bubble - Discord/Slack blue style */
    .user-bubble {
        background: linear-gradient(135deg, #5865f2 0%, #4f46e5 100%);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    /* AI bubble - Discord/Slack gray style */
    .ai-bubble {
        background: #36393f;
        color: #dcddde;
        border: 1px solid #40444b;
        border-bottom-left-radius: 4px;
    }
    
    /* Message content */
    .message-content {
        font-size: 14px;
        line-height: 1.4;
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* ========== AVATARS ========== */
    
    .avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: 600;
        flex-shrink: 0;
        border: 2px solid transparent;
        transition: all 0.2s ease;
    }
    
    .avatar:hover {
        transform: scale(1.05);
    }
    
    /* User avatar */
    .user-avatar {
        background: linear-gradient(135deg, #5865f2, #4f46e5);
        color: white;
        border-color: #4f46e5;
    }
    
    /* AI avatar */
    .ai-avatar {
        background: #40444b;
        color: #dcddde;
        border-color: #36393f;
    }
    
    /* ========== ANIMATIONS ========== */
    
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* ========== CODE BLOCKS IN MESSAGES ========== */
    
    .message-content pre {
        background: rgba(0, 0, 0, 0.2) !important;
        border-radius: 6px !important;
        padding: 8px 10px !important;
        margin: 8px 0 4px 0 !important;
        font-size: 13px !important;
        overflow-x: auto !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .user-bubble .message-content pre {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    .message-content code {
        background: rgba(0, 0, 0, 0.2) !important;
        padding: 2px 4px !important;
        border-radius: 3px !important;
        font-size: 13px !important;
    }
    
    /* ========== CHAT VISUALIZATION STYLING ========== */
    
    /* Visualization containers in chat */
    .chat-viz-container {
        background: #2d3748 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin: 10px 0 !important;
        border: 1px solid #40444b !important;
        max-width: 80% !important;
    }
    
    /* Plotly charts in chat */
    .chat-viz-container .plotly-graph-div {
        background: transparent !important;
    }
    
    /* DataFrames in chat */
    .chat-viz-container .stDataFrame {
        background: transparent !important;
    }
    
    .chat-viz-container .stDataFrame > div {
        background: #1a202c !important;
        border-radius: 8px !important;
    }
    
    /* Table styling in chat */
    .chat-viz-container table {
        background: #1a202c !important;
        color: #f1f5f9 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    .chat-viz-container table th {
        background: #374151 !important;
        color: #f1f5f9 !important;
        border-bottom: 1px solid #475569 !important;
    }
    
    .chat-viz-container table td {
        border-bottom: 1px solid #374151 !important;
        color: #e5e7eb !important;
    }
    
    .chat-viz-container table tr:hover {
        background: #374151 !important;
    }
    
    /* ========== TYPING INDICATOR ========== */
    
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #dcddde;
        font-size: 14px;
    }
    
    .typing-dots {
        display: flex;
        gap: 3px;
    }
    
    .typing-dot {
        width: 6px;
        height: 6px;
        background: #dcddde;
        border-radius: 50%;
        animation: typingDot 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typingDot {
        0%, 60%, 100% {
            transform: scale(1);
            opacity: 0.5;
        }
        30% {
            transform: scale(1.2);
            opacity: 1;
        }
    }
    
    /* Custom scrollbar for chat container */
    [data-testid="stVerticalBlock"] > div > div > div[style*="height"]::-webkit-scrollbar {
        width: 6px;
    }
    
    [data-testid="stVerticalBlock"] > div > div > div[style*="height"]::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 10px;
    }
    
    [data-testid="stVerticalBlock"] > div > div > div[style*="height"]::-webkit-scrollbar-thumb {
        background: var(--primary-ocean);
        border-radius: 10px;
    }
    
    [data-testid="stVerticalBlock"] > div > div > div[style*="height"]::-webkit-scrollbar-thumb:hover {
        background: var(--accent-teal);
    }
    
    /* Fixed bottom input - perfectly positioned */
    .fixed-bottom-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
        border-top: 2px solid var(--border-accent);
        padding: 8px 20px 8px 20px;
        z-index: 1000;
        box-shadow: 0 -8px 32px rgba(0, 0, 0, 0.2);
    }
    
    /* Input form container with proper alignment */
    .fixed-bottom-input .stForm {
        margin: 0 !important;
        background: transparent !important;
        max-width: 1200px;
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Form columns alignment */
    .fixed-bottom-input .stForm > div {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        width: 100% !important;
    }
    
    /* Text area container alignment */
    .fixed-bottom-input .stTextArea {
        margin-bottom: 0 !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Button container alignment */
    .fixed-bottom-input .stButton {
        margin-bottom: 0 !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Text input styling - COMPLETELY STATIC with NO scrollbar */
    .fixed-bottom-input .stTextArea > div > div > textarea {
        border-radius: 25px !important;
        border: 2px solid var(--border-color) !important;
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        padding: 0 12px !important;
        font-size: 15px !important;
        height: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        resize: none !important;
        overflow: hidden !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
        line-height: 40px !important;
        word-wrap: break-word !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
    }
    
    /* Focus state - still no scrollbar, just visual feedback */
    .fixed-bottom-input .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-ocean) !important;
        box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.15), 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        outline: none !important;
        overflow: hidden !important;
    }
    
    /* Force height on the container as well */
    .fixed-bottom-input .stTextArea > div > div {
        height: 40px !important;
    }
    
    /* Force height on the parent container */
    .fixed-bottom-input .stTextArea > div {
        height: 40px !important;
    }
    
    /* Additional overrides for Streamlit's default styles - NO SCROLLBARS */
    .stTextArea textarea[data-baseweb="textarea"] {
        height: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        padding: 8px 12px !important;
        overflow: hidden !important;
        resize: none !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
    }
    
    /* Even more specific override - NO SCROLLBARS */
    div[data-testid="stForm"] .stTextArea textarea {
        height: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        overflow: hidden !important;
        resize: none !important;
        white-space: nowrap !important;
        line-height: 40px !important;
        padding: 0 12px !important;
        text-align: left !important;
        vertical-align: middle !important;
    }
    
    /* Force center placeholder text */
    div[data-testid="stForm"] .stTextArea textarea::placeholder {
        line-height: 40px !important;
        vertical-align: middle !important;
    }
    
    /* Additional specific targeting */
    .stTextArea textarea[data-baseweb="textarea"] {
        line-height: 40px !important;
        padding: 0 12px !important;
        text-align: left !important;
        vertical-align: middle !important;
    }
    
    .stTextArea textarea[data-baseweb="textarea"]::placeholder {
        line-height: 40px !important;
        vertical-align: middle !important;
        text-overflow: ellipsis !important;
    }
    
    .fixed-bottom-input .stTextArea > div > div > textarea::placeholder {
        color: var(--text-muted) !important;
        font-style: normal !important;
    }
    
    /* Send button - FORCED height override */
    .fixed-bottom-input .stButton > button {
        background: linear-gradient(135deg, var(--primary-ocean) 0%, var(--accent-teal) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        height: 37px !important;
        max-height: 37px !important;
        min-height: 37px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(8, 145, 178, 0.3) !important;
        min-width: 120px !important;
        padding: 0 !important;
        line-height: 37px !important;
    }
    
    /* Additional button override with higher specificity */
    div[data-testid="stForm"] .stButton button {
        height: 37px !important;
        max-height: 37px !important;
        min-height: 37px !important;
        line-height: 37px !important;
    }
    
    .fixed-bottom-input .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(8, 145, 178, 0.4) !important;
        background: linear-gradient(135deg, var(--accent-teal) 0%, var(--primary-ocean) 100%) !important;
    }
    
    .fixed-bottom-input .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Message containers - Enhanced bubble layout with maximum specificity */
    .stChatMessage {
        margin-bottom: 1rem !important;
        animation: messageSlideIn 0.4s ease-out !important;
        max-width: 100% !important;
        display: flex !important;
        align-items: flex-end !important;
        padding: 0 1rem !important;
        clear: both !important;
        width: 100% !important;
    }
    
    /* ULTRA HIGH SPECIFICITY - Force user messages RIGHT */
    div[data-testid="stVerticalBlock"] div[data-testid="chat-message-user"],
    .stChatMessage[data-testid="chat-message-user"],
    [data-testid="chat-message-user"].stChatMessage {
        display: flex !important;
        flex-direction: row-reverse !important;
        justify-content: flex-start !important;
        margin-left: 30% !important;
        margin-right: 0 !important;
        text-align: right !important;
        width: 100% !important;
        float: right !important;
    }
    
    /* ULTRA HIGH SPECIFICITY - Force AI messages LEFT */
    div[data-testid="stVerticalBlock"] div[data-testid="chat-message-assistant"],
    .stChatMessage[data-testid="chat-message-assistant"],
    [data-testid="chat-message-assistant"].stChatMessage {
        display: flex !important;
        flex-direction: row !important;
        justify-content: flex-start !important;
        margin-right: 30% !important;
        margin-left: 0 !important;
        text-align: left !important;
        width: 100% !important;
        float: left !important;
    }
    
    /* User messages (right side) - Blue bubbles with MAXIMUM SPECIFICITY */
    div[data-testid="stVerticalBlock"] div[data-testid="chat-message-user"],
    .stChatMessage[data-testid="chat-message-user"],
    [data-testid="chat-message-user"].stChatMessage {
        flex-direction: row-reverse !important;
        justify-content: flex-start !important;
        margin-left: 25% !important;
        margin-right: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] div[data-testid="chat-message-user"] .stChatMessageContent,
    .stChatMessage[data-testid="chat-message-user"] .stChatMessageContent,
    [data-testid="chat-message-user"] .stChatMessageContent {
        background: linear-gradient(135deg, #0891b2 0%, #14b8a6 100%) !important;
        color: white !important;
        border-radius: 20px 20px 5px 20px !important;
        padding: 12px 16px !important;
        max-width: 70% !important;
        min-width: fit-content !important;
        box-shadow: 0 2px 12px rgba(8, 145, 178, 0.25) !important;
        margin-left: 8px !important;
        margin-right: 0 !important;
        font-weight: 400 !important;
        word-wrap: break-word !important;
        position: relative !important;
        border: none !important;
        float: right !important;
    }
    
    /* User bubble tail with maximum specificity */
    div[data-testid="stVerticalBlock"] div[data-testid="chat-message-user"] .stChatMessageContent::after,
    .stChatMessage[data-testid="chat-message-user"] .stChatMessageContent::after,
    [data-testid="chat-message-user"] .stChatMessageContent::after {
        content: '' !important;
        position: absolute !important;
        right: -8px !important;
        bottom: 0px !important;
        width: 0 !important;
        height: 0 !important;
        border: 8px solid transparent !important;
        border-left-color: #14b8a6 !important;
        border-bottom: none !important;
        border-right: none !important;
    }
    
    /* AI messages (left side) - Gray bubbles with MAXIMUM SPECIFICITY */
    div[data-testid="stVerticalBlock"] div[data-testid="chat-message-assistant"],
    .stChatMessage[data-testid="chat-message-assistant"],
    [data-testid="chat-message-assistant"].stChatMessage {
        flex-direction: row !important;
        justify-content: flex-start !important;
        margin-right: 25% !important;
        margin-left: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] div[data-testid="chat-message-assistant"] .stChatMessageContent,
    .stChatMessage[data-testid="chat-message-assistant"] .stChatMessageContent,
    [data-testid="chat-message-assistant"] .stChatMessageContent {
        background: #334155 !important;
        color: #f1f5f9 !important;
        border-radius: 20px 20px 20px 5px !important;
        padding: 12px 16px !important;
        max-width: 70% !important;
        min-width: fit-content !important;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15) !important;
        margin-right: 8px !important;
        margin-left: 0 !important;
        word-wrap: break-word !important;
        position: relative !important;
        border: 1px solid #475569 !important;
        float: left !important;
    }
    
    /* AI bubble tail */
    .stChatMessage[data-testid="chat-message-assistant"] .stChatMessageContent::after {
        content: '';
        position: absolute !important;
        left: -8px !important;
        bottom: 0px !important;
        width: 0 !important;
        height: 0 !important;
        border: 8px solid transparent !important;
        border-right-color: #334155 !important;
        border-bottom: none !important;
        border-left: none !important;
    }
    
    /* Avatar styling - Smaller, cleaner for bubble chat */
    .stChatMessage .stChatMessageAvatar {
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 16px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
        flex-shrink: 0 !important;
        margin-bottom: 4px !important;
    }
    
    .stChatMessage[data-testid="chat-message-user"] .stChatMessageAvatar {
        background: linear-gradient(135deg, #0891b2 0%, #14b8a6 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: 2px solid white !important;
    }
    
    .stChatMessage[data-testid="chat-message-assistant"] .stChatMessageAvatar {
        background: #475569 !important;
        border: 2px solid #64748b !important;
        font-size: 18px !important;
        color: #f1f5f9 !important;
    }
    
    /* Message text styling - Optimized for bubbles */
    .stChatMessage .stChatMessageContent p {
        margin: 0 !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    /* Code blocks within messages */
    .stChatMessage .stChatMessageContent pre {
        background: rgba(0, 0, 0, 0.1) !important;
        border-radius: 8px !important;
        padding: 8px !important;
        margin: 8px 0 !important;
        font-size: 13px !important;
        overflow-x: auto !important;
    }
    
    /* Links in messages */
    .stChatMessage .stChatMessageContent a {
        color: inherit !important;
        text-decoration: underline !important;
        opacity: 0.9 !important;
    }
    
    .stChatMessage[data-testid="chat-message-user"] .stChatMessageContent a {
        color: #e0f2fe !important;
    }
    
    /* Typing animation - three bouncing dots */
    .typing-indicator {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        color: var(--text-muted) !important;
        font-size: 15px !important;
    }
    
    .typing-dots {
        display: flex !important;
        gap: 4px !important;
    }
    
    .typing-dot {
        width: 8px !important;
        height: 8px !important;
        border-radius: 50% !important;
        background: var(--text-muted) !important;
        animation: typingBounce 1.4s infinite ease-in-out !important;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s !important; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s !important; }
    .typing-dot:nth-child(3) { animation-delay: 0s !important; }
    
    /* Animations */
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(15px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes typingBounce {
        0%, 80%, 100% {
            transform: scale(0.8) translateY(0);
            opacity: 0.5;
        }
        40% {
            transform: scale(1.2) translateY(-8px);
            opacity: 1;
        }
    }
    
    /* Responsive design - adaptive bubble chat for all screen sizes */
    @media (max-width: 768px) {
        [data-testid="stVerticalBlock"] > div > div > div[style*="height"] {
            height: calc(100vh - 280px) !important;
            max-height: calc(100vh - 280px) !important;
            min-height: 250px !important;
            padding: 1rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .fixed-bottom-input {
            padding: 15px !important;
        }
        
        /* Mobile bubble adjustments */
        .stChatMessage[data-testid="chat-message-user"] {
            margin-left: 15% !important;
        }
        
        .stChatMessage[data-testid="chat-message-assistant"] {
            margin-right: 15% !important;
        }
        
        .stChatMessage[data-testid="chat-message-user"] .stChatMessageContent,
        .stChatMessage[data-testid="chat-message-assistant"] .stChatMessageContent {
            max-width: 85% !important;
            padding: 10px 14px !important;
            font-size: 14px !important;
            border-radius: 16px 16px 4px 16px !important;
        }
        
        .stChatMessage[data-testid="chat-message-assistant"] .stChatMessageContent {
            border-radius: 16px 16px 16px 4px !important;
        }
        
        .stChatMessage .stChatMessageAvatar {
            width: 28px !important;
            height: 28px !important;
            font-size: 14px !important;
        }
        
        .main .block-container {
            padding-bottom: 100px !important;
            padding-top: 0.5rem !important;
        }
        
        .stChatMessage .stChatMessageAvatar {
            width: 36px !important;
            height: 36px !important;
            font-size: 18px !important;
        }
    }
    
    @media (max-height: 600px) {
        [data-testid="stVerticalBlock"] > div > div > div[style*="height"] {
            height: calc(100vh - 250px) !important;
            max-height: calc(100vh - 250px) !important;
            min-height: 200px !important;
        }
        
        .main .block-container {
            padding-bottom: 90px !important;
        }
        
        .fixed-bottom-input {
            padding: 10px !important;
        }
    }
    
    @media (max-height: 500px) {
        [data-testid="stVerticalBlock"] > div > div > div[style*="height"] {
            height: calc(100vh - 220px) !important;
            max-height: calc(100vh - 220px) !important;
            min-height: 150px !important;
        }
    }
    
    /* High resolution screens */
    @media (min-height: 900px) {
        [data-testid="stVerticalBlock"] > div > div > div[style*="height"] {
            height: calc(100vh - 350px) !important;
            max-height: calc(100vh - 350px) !important;
        }
    }
    
    /* Very wide screens */
    @media (min-width: 1400px) {
        .main .block-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a responsive chat container that adapts to viewport height
    chat_container = st.container(height=600)
    
    # Keep track of message count for auto-scroll triggering
    current_message_count = len(st.session_state.chat_history)
    if "last_message_count" not in st.session_state:
        st.session_state.last_message_count = 0
    
    # Trigger scroll if new messages were added
    new_messages_added = current_message_count > st.session_state.last_message_count
    st.session_state.last_message_count = current_message_count
    
    with chat_container:
        # Display chat messages using custom Discord/Slack style interface
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                render_custom_chat_message("assistant", message.content, "🤖")
            elif isinstance(message, HumanMessage):
                render_custom_chat_message("user", message.content, "👤")
        
        # Show typing indicator with bouncing dots at bottom of chat
        if st.session_state.is_typing:
            st.markdown('''
            <div class="custom-chat-message chat-message-assistant">
                <div class="message-wrapper">
                    <div class="avatar ai-avatar">🤖</div>
                    <div class="message-bubble ai-bubble">
                        <div class="typing-indicator">
                            <span>DrQuery is thinking</span>
                            <div class="typing-dots">
                                <div class="typing-dot"></div>
                                <div class="typing-dot"></div>
                                <div class="typing-dot"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Auto-scroll to bottom and enforce static textarea height
    st.markdown("""
    <script>
    function scrollToBottom() {
        // Scroll main window
        window.scrollTo(0, document.body.scrollHeight);
        
        // Also scroll the chat container if it exists
        const chatContainer = document.querySelector('[data-testid="stVerticalBlock"] > div > div > div[style*="height"]');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Alternative: find any scrollable containers and scroll them
        const scrollableContainers = document.querySelectorAll('[style*="overflow-y: auto"], [style*="overflow: auto"]');
        scrollableContainers.forEach(container => {
            container.scrollTop = container.scrollHeight;
        });
    }
    
    function enforceStaticTextareaHeight() {
        const textareas = document.querySelectorAll('.fixed-bottom-input textarea, div[data-testid="stForm"] textarea, .stTextArea textarea');
        textareas.forEach(textarea => {
            textarea.style.height = '40px';
            textarea.style.minHeight = '40px';
            textarea.style.maxHeight = '40px';
            textarea.style.resize = 'none';
            textarea.style.overflow = 'hidden';
            textarea.style.whiteSpace = 'nowrap';
            textarea.style.textOverflow = 'ellipsis';
            textarea.style.lineHeight = '40px';
            textarea.style.padding = '0 12px';
            textarea.style.textAlign = 'left';
            textarea.style.verticalAlign = 'middle';
            textarea.style.setProperty('line-height', '40px', 'important');
            textarea.style.setProperty('padding', '0 12px', 'important');
        });
    }
    
    function enforceButtonHeight() {
        const buttons = document.querySelectorAll('.fixed-bottom-input button');
        buttons.forEach(button => {
            button.style.height = '37px';
            button.style.minHeight = '37px';
            button.style.maxHeight = '37px';
            button.style.lineHeight = '37px';
            button.style.padding = '0';
        });
    }
    
    // Scroll to bottom after content loads - multiple attempts for reliability
    setTimeout(scrollToBottom, 100);
    setTimeout(scrollToBottom, 300);
    setTimeout(scrollToBottom, 500);
    
    // Continuous scrolling for new messages
    setInterval(function() {
        const shouldScroll = sessionStorage.getItem('autoScroll');
        if (shouldScroll !== 'false') {
            scrollToBottom();
        }
    }, 200);
    
    # Mark that auto-scroll should happen
    sessionStorage.setItem('autoScroll', 'true');
    """, unsafe_allow_html=True)
    
    # Additional scroll trigger for new messages
    if new_messages_added:
        st.markdown("""
        <script>
        // Immediate scroll for new message
        setTimeout(function() {
            const chatContainer = document.querySelector('[data-testid="stVerticalBlock"] > div > div > div[style*="height"]');
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            window.scrollTo(0, document.body.scrollHeight);
        }, 50);
        </script>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <script>
    
    // Enforce static heights
    setTimeout(enforceStaticTextareaHeight, 100);
    setTimeout(enforceButtonHeight, 100);
    setTimeout(enforceStaticTextareaHeight, 500);
    setTimeout(enforceButtonHeight, 500);
    
    // Monitor for changes and re-enforce
    setInterval(enforceStaticTextareaHeight, 1000);
    setInterval(enforceButtonHeight, 1000);
    </script>
    """, unsafe_allow_html=True)
    
    # Fixed bottom input container - perfectly positioned
    st.markdown('<div class="fixed-bottom-input">', unsafe_allow_html=True)
    
    # Input form with proper styling
    with st.form(key=f"chat_form_{st.session_state.chat_input_key}", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_query = st.text_area(
                "",
                placeholder="Type your message",
                height=10,
                max_chars=300,
                key=f"chat_input_{st.session_state.chat_input_key}",
                label_visibility="collapsed"
            )
        
        with col2:
            send_clicked = st.form_submit_button(
                "Send", 
                use_container_width=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle message sending
    if send_clicked and user_query and user_query.strip():
        if "db" not in st.session_state or st.session_state.db is None:
            st.error("Please connect to the database first using the sidebar.")
            return
        
        # Add user message to history
        st.session_state.chat_history.append(HumanMessage(content=user_query.strip()))
        
        # Show typing indicator
        st.session_state.is_typing = True
        st.session_state.chat_input_key += 1
        st.rerun()
    
    # Process AI response if typing
    if st.session_state.is_typing:
        try:
            # Get the last user message
            last_user_message = None
            for msg in reversed(st.session_state.chat_history):
                if isinstance(msg, HumanMessage):
                    last_user_message = msg.content
                    break
            
            if last_user_message:
                print(f"DEBUG: Processing user message: {last_user_message}")
                print(f"DEBUG: Database connection: {st.session_state.db is not None}")
                
                # Get AI response
                response, df, sql_query = get_response(
                    last_user_message, 
                    st.session_state.db, 
                    st.session_state.chat_history[:-1]  # Exclude the current message
                )
                
                print(f"DEBUG: AI Response: {response[:100]}...")
                print(f"DEBUG: DataFrame returned: {df is not None}")
                print(f"DEBUG: SQL Query: {sql_query}")
                
                if df is not None:
                    print(f"DEBUG: DataFrame shape: {df.shape}")
                    print(f"DEBUG: DataFrame columns: {df.columns.tolist()}")
                
                # Check if user requested visualizations
                viz_keywords = ['graph', 'chart', 'plot', 'visualize', 'visualization', 'show chart', 'create graph']
                table_keywords = ['table', 'tabular', 'data table', 'show data', 'display data', 'tabular format', 'in table', 'table format', 'rows', 'columns']
                
                user_wants_viz = any(keyword in last_user_message.lower() for keyword in viz_keywords)
                user_wants_table = any(keyword in last_user_message.lower() for keyword in table_keywords)
                
                print(f"DEBUG: User wants viz: {user_wants_viz}, User wants table: {user_wants_table}")
                
                # Enhance response based on user request
                if df is not None:
                    if user_wants_viz:
                        response += f"\n\n**📈 I'll create a visualization for you with the data below.**"
                    elif user_wants_table:
                        response += f"\n\n**📊 Here's the data in table format as requested.**"
                    else:
                        response += f"\n\n**📊 Query executed successfully! Found {len(df)} rows.**"
                
                # Add SQL query if relevant
                if sql_query and ('sql' in last_user_message.lower() or 'query' in last_user_message.lower()):
                    response += f"""
                    
**🔍 SQL Query:**
```sql
{sql_query}
```
                    """
                
                # Add AI response to history
                st.session_state.chat_history.append(AIMessage(content=response))
                
                # Store data for cross-tab integration AND chat visualizations
                if df is not None:
                    st.session_state.cross_tab_data = df
                    st.session_state.cross_tab_query = sql_query
                    st.session_state.latest_query_data = df  # Additional storage for chat viz
                    print(f"DEBUG: Stored data with shape {df.shape} for visualizations")
                else:
                    print(f"DEBUG: No data to store")
                    
                    # For testing purposes, create some sample data if user asks for viz
                    if user_wants_viz or user_wants_table:
                        print(f"DEBUG: Creating sample data for testing...")
                        import pandas as pd
                        import numpy as np
                        
                        # Create sample data
                        sample_data = pd.DataFrame({
                            'Product': ['A', 'B', 'C', 'D', 'E'],
                            'Sales': np.random.randint(100, 1000, 5),
                            'Revenue': np.random.randint(1000, 10000, 5),
                            'Category': ['Electronics', 'Clothing', 'Electronics', 'Books', 'Clothing']
                        })
                        
                        st.session_state.cross_tab_data = sample_data
                        st.session_state.latest_query_data = sample_data
                        print(f"DEBUG: Created sample data with shape {sample_data.shape}")
                        
                        response += f"\n\n**📊 Using sample data for demonstration (no database query returned data).**"
                
        except Exception as e:
            error_response = f"❌ An error occurred: {str(e)}"
            st.session_state.chat_history.append(AIMessage(content=error_response))
        
        finally:
            # Stop typing indicator
            st.session_state.is_typing = False
            st.rerun()
