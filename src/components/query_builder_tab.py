import streamlit as st
import pandas as pd
from utils.ai_engine import get_sql_chain
from utils.query_optimizer import QueryOptimizer
from utils.performance_monitor import estimate_query_performance

def render_query_builder_tab():
    """Render the query builder interface tab"""
    
    # Use visual containers and formatting to highlight headings
    st.markdown("")  # Add some space

    
    # Create another highlighted section for the input prompt
    with st.container():
        st.markdown("#### **DESCRIBE YOUR QUERY**")
    
    # Initialize session state for query builder
    if "generated_sql" not in st.session_state:
        st.session_state.generated_sql = ""
    if "query_results" not in st.session_state:
        st.session_state.query_results = None
    
    query_description = st.text_area(
        "*Build SQL queries using natural language, then review and edit before execution*",
        placeholder="e.g., 'Get all patients who had appointments in the last 30 days with their doctor names'",
        height=80,
        key="query_description"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        generate_sql = st.button("Generate SQL", use_container_width=True)
    
    with col2:
        clear_all = st.button("Clear All", use_container_width=True)
    
    if clear_all:
        st.session_state.generated_sql = ""
        st.session_state.query_results = None
        st.rerun()
    
    if generate_sql and query_description.strip():
        if "db" not in st.session_state or st.session_state.db is None:
            st.error("Please connect to the database first using the sidebar.")
            return
        
        with st.spinner("Generating SQL query..."):
            try:
                sql_chain = get_sql_chain(st.session_state.db)
                generated_query = sql_chain.invoke({
                    "question": query_description,
                    "chat_history": []
                })
                
                # Clean up the query
                import re
                generated_query = re.sub(r'\bd\.department_name\b', 'de.department_name', generated_query)
                generated_query = generated_query.strip()
                
                st.session_state.generated_sql = generated_query
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating SQL: {str(e)}")
    
    # SQL Editor Section
    if st.session_state.generated_sql:
        st.markdown("#### 📝 SQL Query Editor:")
        
        # Performance estimation
        if st.session_state.generated_sql:
            performance_info = estimate_query_performance(st.session_state.generated_sql, st.session_state.db)
            
            if performance_info['warning']:
                st.warning(f"⚠️ {performance_info['message']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🚀 Optimize Query"):
                        optimizer = QueryOptimizer(st.session_state.db)
                        optimized = optimizer.optimize_query(st.session_state.generated_sql)
                        if optimized != st.session_state.generated_sql:
                            st.session_state.generated_sql = optimized
                            st.success("Query optimized!")
                            st.rerun()
                        else:
                            st.info("Query is already optimized.")
                
                with col2:
                    run_anyway = st.button("▶️ Run Anyway")
            else:
                st.success(f"✅ {performance_info['message']}")
                run_anyway = False
        
        # SQL code editor with syntax highlighting - responsive height
        edited_sql = st.text_area(
            "Edit your SQL query:",
            value=st.session_state.generated_sql,
            height=150,
            key="sql_editor",
            help="You can edit the generated SQL query before execution"
        )
        
        # Auto-completion helper
        if "db" in st.session_state:
            with st.expander("📋 Database Schema Helper"):
                try:
                    schema_info = st.session_state.db.get_table_info()
                    st.text(schema_info)
                except:
                    st.error("Could not load schema information")
        
        # Execute query
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            execute_query = st.button("▶️ Execute Query", use_container_width=True) or run_anyway
        
        with col2:
            validate_sql = st.button("✅ Validate", use_container_width=True)
        
        with col3:
            save_query = st.button("💾 Save Query", use_container_width=True)
        
        if validate_sql:
            # Basic SQL validation
            if validate_sql_syntax(edited_sql):
                st.success("✅ SQL syntax appears valid")
            else:
                st.error("❌ SQL syntax issues detected")
        
        if save_query:
            # Save to session state for future use
            if "saved_queries" not in st.session_state:
                st.session_state.saved_queries = []
            
            query_name = st.text_input("Query name:", key="save_query_name")
            if query_name:
                st.session_state.saved_queries.append({
                    "name": query_name,
                    "sql": edited_sql,
                    "description": query_description
                })
                st.success(f"Query '{query_name}' saved!")
        
        if execute_query and edited_sql.strip():
            with st.spinner("Executing query..."):
                try:
                    result = st.session_state.db.run(edited_sql)
                    
                    # Parse results into DataFrame
                    if result:
                        # Simple parsing for display
                        lines = str(result).strip().split('\n')
                        if len(lines) > 1:
                            data = []
                            for line in lines:
                                if line.strip().startswith('(') and line.strip().endswith(')'):
                                    values = line.strip()[1:-1].split(', ')
                                    values = [v.strip("'\"") for v in values]
                                    data.append(values)
                            
                            if data:
                                df = pd.DataFrame(data)
                                st.session_state.query_results = df
                                
                                st.markdown("#### 📊 Query Results:")
                                st.dataframe(df, use_container_width=True)
                                st.caption(f"Returned {len(df)} rows")
                                
                                # Cross-tab integration
                                col1, col2, col3 = st.columns([2, 1, 1])
                                with col2:
                                    if st.button("📊 Visualize Results"):
                                        st.session_state.cross_tab_data = df
                                        st.info("💡 Switch to Visualization tab to create charts!")
                                
                                with col3:
                                    if st.button("💬 Discuss Results"):
                                        st.session_state.cross_tab_data = df
                                        st.info("💡 Switch to Chat tab to ask questions about this data!")
                            else:
                                st.info("Query executed successfully but returned no data.")
                        else:
                            st.info(f"Query result: {result}")
                    else:
                        st.info("Query executed successfully (no data returned).")
                        
                except Exception as e:
                    st.error(f"Query execution failed: {str(e)}")
                    
                    # Suggest fixes
                    st.markdown("**💡 Common fixes:**")
                    st.markdown("- Check table and column names")
                    st.markdown("- Verify JOIN conditions")  
                    st.markdown("- Check data types in WHERE clauses")
    
    # Saved queries section
    if "saved_queries" in st.session_state and st.session_state.saved_queries:
        st.markdown("---")
        st.markdown("#### 💾 Saved Queries:")
        
        for i, saved_query in enumerate(st.session_state.saved_queries):
            with st.expander(f"📋 {saved_query['name']}"):
                st.markdown(f"**Description:** {saved_query['description']}")
                st.code(saved_query['sql'], language="sql")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📝 Load Query", key=f"load_{i}"):
                        st.session_state.generated_sql = saved_query['sql']
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_{i}"):
                        st.session_state.saved_queries.pop(i)
                        st.rerun()

def validate_sql_syntax(sql_query):
    """Basic SQL syntax validation"""
    if not sql_query.strip():
        return False
    
    # Basic checks
    sql_lower = sql_query.lower().strip()
    
    # Check for basic SQL keywords
    sql_keywords = ['select', 'insert', 'update', 'delete', 'create', 'alter', 'drop']
    has_keyword = any(sql_lower.startswith(keyword) for keyword in sql_keywords)
    
    # Check for balanced parentheses
    open_parens = sql_query.count('(')
    close_parens = sql_query.count(')')
    balanced_parens = open_parens == close_parens
    
    # Check for quotes balance
    single_quotes = sql_query.count("'") % 2 == 0
    double_quotes = sql_query.count('"') % 2 == 0
    
    return has_keyword and balanced_parens and single_quotes and double_quotes
