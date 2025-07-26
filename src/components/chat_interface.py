import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from utils.database import get_response
import time

def render_chat_interface():
    """Render the premium chat interface"""
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm your AI data assistant. Ask me anything about your database.")
        ]
    
    # Display chat messages with animations
    for i, message in enumerate(st.session_state.chat_history):
        if isinstance(message, AIMessage):
            st.markdown(f"""
            <div class="message-ai" style="animation-delay: {i * 0.1}s;">
                <div class="message-content">
                    <div class="avatar-ai">🤖</div>
                    <div class="text-content" style="font-family: 'Poppins', sans-serif;">{message.content}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif isinstance(message, HumanMessage):
            st.markdown(f"""
            <div class="message-user" style="animation-delay: {i * 0.1}s;">
                <div class="message-content">
                    <div class="text-content" style="font-family: 'Poppins', sans-serif;">{message.content}</div>
                    <div class="avatar-user">👤</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Add minimal bottom spacing for search bar
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Auto-scroll to bottom
    st.markdown("""
    <script>
    setTimeout(function() {
        window.scrollTo(0, document.body.scrollHeight);
    }, 100);
    </script>
    """, unsafe_allow_html=True)
    
    # Fixed Chat Input at Bottom
    if prompt := st.chat_input("      💭 Type your question here...", key="chat_input"):
        handle_user_input(prompt)

def handle_user_input(user_query: str):
    """Handle user input and generate response with enhanced animations"""
    
    if "db" not in st.session_state:
        st.error("🔌 Please connect to your database first using the sidebar.")
        return
    
    # Add user message to history
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    # Create placeholders for smooth animation
    message_container = st.empty()
    typing_container = st.empty()
    
    # Show user message with send animation
    message_container.markdown(f"""
    <div class="message-user message-sending">
        <div class="message-content">
            <div class="text-content" style="font-family: 'Poppins', sans-serif;">{user_query}</div>
            <div class="avatar-user">👤</div>
            <div class="message-status">📤</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(0.3)  # Brief pause for send effect
    
    # Update to sent status
    message_container.markdown(f"""
    <div class="message-user message-sent">
        <div class="message-content">
            <div class="text-content" style="font-family: 'Poppins', sans-serif;">{user_query}</div>
            <div class="avatar-user">👤</div>
            <div class="message-status">✓</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show enhanced typing indicator
    typing_container.markdown("""
    <div class="typing-indicator-enhanced">
        <div class="ai-avatar-typing">🤖</div>
        <div class="typing-content">
            <div class="typing-dots-enhanced">
                <span></span><span></span><span></span>
            </div>
            <div class="typing-text-enhanced">AI is analyzing your query...</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Simulate processing with status updates
        time.sleep(0.8)
        typing_container.markdown("""
        <div class="typing-indicator-enhanced">
            <div class="ai-avatar-typing">🤖</div>
            <div class="typing-content">
                <div class="typing-dots-enhanced">
                    <span></span><span></span><span></span>
                </div>
                <div class="typing-text-enhanced">Generating SQL query...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.8)
        typing_container.markdown("""
        <div class="typing-indicator-enhanced">
            <div class="ai-avatar-typing">🤖</div>
            <div class="typing-content">
                <div class="typing-dots-enhanced">
                    <span></span><span></span><span></span>
                </div>
                <div class="typing-text-enhanced">Fetching results...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        response = get_response(
            user_query, 
            st.session_state.db, 
            st.session_state.chat_history
        )
        
        # Clear typing indicator
        typing_container.empty()
        
        # Show AI response with receive animation
        typing_container.markdown(f"""
        <div class="message-ai message-receiving">
            <div class="message-content">
                <div class="avatar-ai">🤖</div>
                <div class="text-content" style="font-family: 'Poppins', sans-serif;">{response}</div>
                <div class="message-pulse"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.5)  # Brief pause for receive effect
        
        # Add response to chat history and rerun
        st.session_state.chat_history.append(AIMessage(content=response))
        st.rerun()
        
    except Exception as e:
        typing_container.empty()
        error_message = f"Sorry, I encountered an error: {str(e)}"
        
        # Show error with animation
        typing_container.markdown(f"""
        <div class="message-ai message-error">
            <div class="message-content">
                <div class="avatar-ai">⚠️</div>
                <div class="text-content" style="font-family: 'Poppins', sans-serif;">{error_message}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.5)
        st.session_state.chat_history.append(AIMessage(content=error_message))
        st.rerun()

def render_query_suggestions():
    """Render suggested queries for better UX"""
    # Removed as requested
    pass