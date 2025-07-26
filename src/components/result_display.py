import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_sql_preview(query: str):
    """Render SQL query preview with syntax highlighting"""
    
    with st.expander("🔍 View Generated SQL", expanded=False):
        st.code(query, language="sql")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy Query", use_container_width=True):
                st.write("Query copied to clipboard!")
        with col2:
            if st.button("✏️ Edit Query", use_container_width=True):
                st.session_state.edit_mode = True

def render_data_table(data, title="Query Results"):
    """Render data table with premium styling"""
    
    if not data or len(data) == 0:
        st.info("No data returned from the query.")
        return
    
    st.markdown(f"### 📊 {title}")
    
    # Convert to DataFrame if not already
    if not isinstance(data, pd.DataFrame):
        try:
            df = pd.DataFrame(data)
        except:
            st.error("Unable to display data in table format.")
            return
    else:
        df = data
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        if len(df.select_dtypes(include=['number']).columns) > 0:
            numeric_cols = df.select_dtypes(include=['number']).columns
            st.metric("Numeric Columns", len(numeric_cols))
    
    # Display table
    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )
    
    # Export options
    col1, col2, col3 = st.columns(3)
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            "query_results.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("📈 Create Chart", use_container_width=True):
            st.session_state.show_chart_options = True
    
    with col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()

def render_chart_options(df):
    """Render chart creation options"""
    
    if "show_chart_options" not in st.session_state:
        return
    
    with st.expander("📈 Chart Options", expanded=True):
        chart_type = st.selectbox(
            "Chart Type",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram"]
        )
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if chart_type in ["Bar Chart", "Line Chart"]:
            x_col = st.selectbox("X-axis", categorical_cols + numeric_cols)
            y_col = st.selectbox("Y-axis", numeric_cols)
            
            if st.button("Generate Chart"):
                if chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                else:
                    fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
                
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Pie Chart":
            if categorical_cols and numeric_cols:
                names_col = st.selectbox("Categories", categorical_cols)
                values_col = st.selectbox("Values", numeric_cols)
                
                if st.button("Generate Chart"):
                    fig = px.pie(df, names=names_col, values=values_col, title=f"{values_col} by {names_col}")
                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(fig, use_container_width=True)

def render_query_insights(df):
    """Render automatic insights about the query results"""
    
    if df is None or len(df) == 0:
        return
    
    with st.expander("🧠 Data Insights", expanded=False):
        insights = []
        
        # Basic insights
        insights.append(f"📊 Dataset contains {len(df)} rows and {len(df.columns)} columns")
        
        # Numeric column insights
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols[:3]:  # Show insights for first 3 numeric columns
                mean_val = df[col].mean()
                max_val = df[col].max()
                min_val = df[col].min()
                insights.append(f"📈 {col}: Average = {mean_val:.2f}, Range = {min_val:.2f} to {max_val:.2f}")
        
        # Categorical insights
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            for col in categorical_cols[:2]:  # Show insights for first 2 categorical columns
                unique_count = df[col].nunique()
                most_common = df[col].mode().iloc[0] if len(df[col].mode()) > 0 else "N/A"
                insights.append(f"🏷️ {col}: {unique_count} unique values, most common = '{most_common}'")
        
        for insight in insights:
            st.markdown(f"• {insight}")

def render_error_display(error_message: str):
    """Render error message with helpful suggestions"""
    
    st.error(f"❌ Query Error: {error_message}")
    
    with st.expander("💡 Troubleshooting Tips"):
        st.markdown("""
        **Common issues and solutions:**
        
        • **Table not found**: Check if the table name is correct and exists in your database
        • **Column not found**: Verify column names match exactly (case-sensitive)
        • **Syntax error**: Review the SQL syntax, especially quotes and commas
        • **Permission denied**: Ensure your database user has the required permissions
        • **Connection timeout**: Check your database connection and network
        
        **Need help?** Try rephrasing your question or ask for available tables first.
        """)
        
        if st.button("🔄 Try Again", use_container_width=True):
            st.rerun()