import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.ai_engine import get_response
from utils.chart_generator import ChartGenerator
from components.export_modal import show_export_modal

def parse_sql_result_to_dataframe(sql_result):
    """Parse SQL result string into a pandas DataFrame"""
    try:
        if not sql_result:
            return None
            
        # Handle different result formats
        if isinstance(sql_result, list):
            # If it's already a list (like [('Cardiology', 2), ('Neurology', 1), ...])
            if len(sql_result) > 0 and isinstance(sql_result[0], tuple):
                df = pd.DataFrame(sql_result)
                # Give generic column names
                df.columns = [f'Column_{i+1}' for i in range(len(df.columns))]
                return df
        
        # Convert to string if needed and try original parsing
        result_str = str(sql_result).strip()
        
        # Check if it looks like a list representation
        if result_str.startswith('[') and result_str.endswith(']'):
            # Try to evaluate it safely
            try:
                import ast
                parsed_list = ast.literal_eval(result_str)
                if isinstance(parsed_list, list) and len(parsed_list) > 0:
                    if isinstance(parsed_list[0], tuple):
                        df = pd.DataFrame(parsed_list)
                        df.columns = [f'Column_{i+1}' for i in range(len(df.columns))]
                        return df
            except:
                pass
        
        # Split into lines for tuple format parsing
        lines = result_str.split('\n')
        if len(lines) < 1:
            return None
        
        # Parse tuple-like format: (value1, value2, value3)
        data = []
        for line in lines:
            line = line.strip()
            if line.startswith('(') and line.endswith(')'):
                # Remove parentheses and split by comma
                values = line[1:-1].split(', ')
                # Clean up quotes and whitespace
                cleaned_values = []
                for val in values:
                    val = val.strip().strip('"').strip("'")
                    # Try to convert to number if possible
                    try:
                        if '.' in val:
                            cleaned_values.append(float(val))
                        else:
                            cleaned_values.append(int(val))
                    except:
                        cleaned_values.append(val)
                data.append(cleaned_values)
        
        if data:
            df = pd.DataFrame(data)
            # Give generic column names
            df.columns = [f'Column_{i+1}' for i in range(len(df.columns))]
            return df
        
        return None
    except Exception as e:
        print(f"Error parsing SQL result: {e}")
        return None

def improve_column_names(df, sql_query):
    """Try to extract better column names from the SQL query"""
    try:
        if sql_query and 'SELECT' in sql_query.upper():
            # Extract the SELECT part
            select_part = sql_query.split('FROM')[0].replace('SELECT', '', 1).strip()
            
            # Handle common patterns
            if 'department_name' in select_part.lower() and 'count' in select_part.lower():
                if len(df.columns) >= 2:
                    df.columns = ['Department', 'Count']
            elif 'first_name' in select_part.lower() and 'last_name' in select_part.lower():
                if len(df.columns) >= 2:
                    df.columns = ['First_Name', 'Last_Name'] + [f'Column_{i+3}' for i in range(len(df.columns)-2)]
            # Add more patterns as needed
            
        return df
    except:
        return df

def render_visualization_tab():
    """Render the visualization interface tab"""
    
    # Use visual containers and formatting to highlight headings
    st.markdown("")  # Add some space
    
    
    # Create another highlighted section for the input prompt
    with st.container():
        st.markdown("#### **DESCRIBE WHAT YOU WANT TO VISUALIZE**")
    
    viz_query = st.text_area(
        "*Generate intelligent visualizations from your data using natural language*",
        placeholder="e.g., 'Show me a bar chart of patient count by department' or 'Create a line graph of appointments over time'",
        height=80
    )
    
    col1 = st.columns(1)[0]
    
    with col1:
        generate_viz = st.button("Generate Visualization", use_container_width=True)
    
    if generate_viz and viz_query.strip():
        if "db" not in st.session_state or st.session_state.db is None:
            st.error("Please connect to the database first using the sidebar.")
            return
            
        with st.spinner("Generating visualization..."):
            try:
                # Get data using AI with explicit instruction for tabular data
                response, df, sql_query = get_response(
                    viz_query + " (please return data in tabular format suitable for visualization)",
                    st.session_state.db,
                    []
                )
                
                if df is not None and not df.empty:
                    # Store data in session state for persistence
                    st.session_state.viz_data = df
                    st.session_state.viz_query = viz_query
                    st.session_state.viz_sql_query = sql_query
                    process_visualization_data(df, viz_query, sql_query)
                elif sql_query:
                    # Try to execute the SQL directly if we have a query but no DataFrame
                    try:
                        raw_result = st.session_state.db.run(sql_query)
                        
                        # Try to parse the raw result into a DataFrame
                        df_from_sql = parse_sql_result_to_dataframe(raw_result)
                        if df_from_sql is not None and not df_from_sql.empty:
                            # Try to give better column names based on the SQL query
                            df_from_sql = improve_column_names(df_from_sql, sql_query)
                            # Store data in session state for persistence
                            st.session_state.viz_data = df_from_sql
                            st.session_state.viz_query = viz_query
                            st.session_state.viz_sql_query = sql_query
                            process_visualization_data(df_from_sql, viz_query, sql_query)
                        else:
                            st.error("Could not parse SQL result into DataFrame")
                    except Exception as sql_error:
                        st.error(f"SQL execution failed: {str(sql_error)}")
                else:
                    st.error("Could not generate visualization data. Please try rephrasing your request.")
                    if response:
                        st.info(f"AI Response: {response}")
                    
            except Exception as e:
                st.error(f"Error generating visualization: {str(e)}")
    
    # Check if we have existing visualization data to redisplay
    elif hasattr(st.session_state, 'viz_data') and st.session_state.viz_data is not None:
        process_visualization_data(
            st.session_state.viz_data, 
            st.session_state.viz_query, 
            st.session_state.viz_sql_query
        )
def process_visualization_data(df, query, sql_query=None):
    """Process and visualize the data"""
    
    # Get chart suggestions
    chart_generator = ChartGenerator(df)
    suggested_charts = chart_generator.suggest_charts(query)
    
    if not suggested_charts:
        st.error("Unable to suggest appropriate charts for this data.")
        return
    
    st.markdown("#### 🎯 Recommended Chart:")
    recommended = suggested_charts[0]
    st.info(f"**{recommended['type']}** - {recommended['reason']}")
    
    # Chart type selection with persistence
    col1, col2 = st.columns([2, 1])
    
    # Initialize selected chart in session state if not exists
    chart_key = f"selected_chart_{hash(str(df.values.tobytes()))}"
    if chart_key not in st.session_state:
        st.session_state[chart_key] = None
    
    with col1:
        chart_options = [chart['type'] for chart in suggested_charts]
        selected_chart = st.selectbox(
            "Choose chart type:",
            chart_options,
            index=0,
            key=f"chart_selector_{hash(str(df.values.tobytes()))}"
        )
        
        # Store the selected chart type
        st.session_state[chart_key] = selected_chart
    
    with col2:
        export_clicked = st.button("📤 Export Chart", key=f"export_chart_{id(df)}")
        
    # Generate and display chart
    try:
        chart = chart_generator.create_chart(selected_chart, query)
        if chart:
            # Store chart in session state for export
            st.session_state.current_chart = chart
            
            st.plotly_chart(chart, use_container_width=True)
            
            # Handle export if button was clicked
            if export_clicked:
                st.markdown("---")
                show_export_modal()
            
            # Data preview below the chart
            st.markdown("#### 📋 Data Preview:")
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"Showing first 10 rows of {len(df)} total rows")
            
            # Chart insights
            insights = chart_generator.get_insights(df, selected_chart)
            if insights:
                with st.expander("🔍 Data Insights"):
                    for insight in insights:
                        st.markdown(f"• {insight}")
            
            # Show SQL query if available
            if sql_query:
                with st.expander("🔍 SQL Query Used"):
                    st.code(sql_query, language="sql")
                    
    except Exception as e:
        st.error(f"Error generating chart: {str(e)}")
        st.info("Try selecting a different chart type or modifying your data query.")
        
        # Always show raw data as fallback
        st.markdown("**📊 Raw Data:**")
        st.dataframe(df, use_container_width=True)
