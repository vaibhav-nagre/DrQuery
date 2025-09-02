import time
import re
from typing import Dict, Any
from langchain_community.utilities import SQLDatabase

def estimate_query_performance(query: str, db: SQLDatabase) -> Dict[str, Any]:
    """Estimate query performance and provide warnings"""
    
    performance_info = {
        'estimated_time': 'unknown',
        'warning': False,
        'message': '',
        'complexity_score': 0
    }
    
    try:
        # Analyze query complexity
        complexity_score = _calculate_complexity_score(query)
        performance_info['complexity_score'] = complexity_score
        
        # Get table information for size estimation
        table_info = _get_table_sizes(query, db)
        
        # Estimate performance based on complexity and data size
        if complexity_score < 3:
            performance_info['estimated_time'] = 'Fast (< 1 second)'
            performance_info['message'] = 'Query should execute quickly'
            performance_info['warning'] = False
        elif complexity_score < 6:
            performance_info['estimated_time'] = 'Medium (1-5 seconds)'
            performance_info['message'] = 'Query may take a few seconds to complete'
            performance_info['warning'] = False
        elif complexity_score < 9:
            performance_info['estimated_time'] = 'Slow (5-30 seconds)'
            performance_info['message'] = 'Query may take some time to complete. Consider optimization.'
            performance_info['warning'] = True
        else:
            performance_info['estimated_time'] = 'Very Slow (> 30 seconds)'
            performance_info['message'] = 'Query may be very slow. Strong recommendation to optimize.'
            performance_info['warning'] = True
        
        # Check for specific performance killers
        performance_killers = _check_performance_killers(query)
        if performance_killers:
            performance_info['warning'] = True
            performance_info['message'] += f" Issues detected: {', '.join(performance_killers)}"
    
    except Exception as e:
        performance_info['message'] = f"Unable to estimate performance: {str(e)}"
        performance_info['warning'] = False
    
    return performance_info

def _calculate_complexity_score(query: str) -> int:
    """Calculate query complexity score (0-10)"""
    
    score = 0
    query_lower = query.lower()
    
    # Base complexity for different query types
    if query_lower.strip().startswith('select'):
        score += 1
    elif query_lower.strip().startswith(('insert', 'update', 'delete')):
        score += 2
    elif query_lower.strip().startswith(('create', 'alter', 'drop')):
        score += 3
    
    # Count JOINs
    join_count = len(re.findall(r'\bjoin\b', query_lower))
    score += join_count * 1.5
    
    # Count subqueries
    subquery_count = query_lower.count('select') - 1
    score += subquery_count * 2
    
    # Check for GROUP BY
    if 'group by' in query_lower:
        score += 1
    
    # Check for ORDER BY
    if 'order by' in query_lower:
        score += 0.5
    
    # Check for DISTINCT
    if 'distinct' in query_lower:
        score += 1
    
    # Check for LIKE with wildcards
    if re.search(r"like\s+['\"]%.*%['\"]", query_lower):
        score += 2
    elif re.search(r"like\s+['\"]%", query_lower):
        score += 1.5
    
    # Check for OR conditions
    or_count = len(re.findall(r'\bor\b', query_lower))
    score += or_count * 0.5
    
    # Check for functions in WHERE clause
    if re.search(r'where.*\b(upper|lower|substring|concat)\s*\(', query_lower):
        score += 1
    
    # Bonus for no LIMIT
    if 'limit' not in query_lower and 'count(' not in query_lower:
        score += 1
    
    return min(int(score), 10)  # Cap at 10

def _get_table_sizes(query: str, db: SQLDatabase) -> Dict[str, int]:
    """Get approximate table sizes mentioned in the query"""
    
    table_sizes = {}
    
    try:
        # Extract table names from query
        table_names = _extract_table_names(query)
        
        for table in table_names:
            try:
                # Get row count for each table
                count_query = f"SELECT COUNT(*) FROM {table}"
                result = db.run(count_query)
                
                # Parse count from result
                import re
                count_match = re.search(r'\((\d+),?\)', str(result))
                if count_match:
                    table_sizes[table] = int(count_match.group(1))
                else:
                    table_sizes[table] = 0
            except:
                table_sizes[table] = 0
    
    except Exception:
        pass
    
    return table_sizes

def _extract_table_names(query: str) -> list:
    """Extract table names from SQL query"""
    
    table_names = []
    query_lower = query.lower()
    
    # Simple regex patterns to find table names
    patterns = [
        r'from\s+(\w+)',
        r'join\s+(\w+)',
        r'update\s+(\w+)',
        r'insert\s+into\s+(\w+)',
        r'delete\s+from\s+(\w+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, query_lower)
        table_names.extend(matches)
    
    return list(set(table_names))  # Remove duplicates

def _check_performance_killers(query: str) -> list:
    """Check for specific performance issues"""
    
    issues = []
    query_lower = query.lower()
    
    # SELECT *
    if 'select *' in query_lower:
        issues.append("SELECT * usage")
    
    # LIKE with leading wildcard
    if re.search(r"like\s+['\"]%", query_lower):
        issues.append("LIKE with leading wildcard")
    
    # No WHERE clause on potentially large tables
    if ('from' in query_lower and 
        'where' not in query_lower and 
        'limit' not in query_lower and
        'count(' not in query_lower):
        issues.append("No filtering conditions")
    
    # Functions in WHERE clause
    if re.search(r'where.*\b(upper|lower|substring|concat)\s*\(', query_lower):
        issues.append("Functions in WHERE clause")
    
    # Multiple OR conditions
    or_count = len(re.findall(r'\bor\b', query_lower))
    if or_count > 3:
        issues.append(f"Many OR conditions ({or_count})")
    
    # Cartesian products (JOIN without ON)
    if 'join' in query_lower and 'on' not in query_lower:
        issues.append("Potential cartesian product")
    
    return issues

def monitor_query_execution(query: str, db: SQLDatabase) -> Dict[str, Any]:
    """Monitor actual query execution time and performance"""
    
    start_time = time.time()
    
    try:
        result = db.run(query)
        execution_time = time.time() - start_time
        
        return {
            'success': True,
            'execution_time': execution_time,
            'result': result,
            'performance_rating': _get_performance_rating(execution_time),
            'message': f"Query executed in {execution_time:.2f} seconds"
        }
    
    except Exception as e:
        execution_time = time.time() - start_time
        
        return {
            'success': False,
            'execution_time': execution_time,
            'error': str(e),
            'performance_rating': 'failed',
            'message': f"Query failed after {execution_time:.2f} seconds: {str(e)}"
        }

def _get_performance_rating(execution_time: float) -> str:
    """Get performance rating based on execution time"""
    
    if execution_time < 1:
        return 'excellent'
    elif execution_time < 3:
        return 'good'
    elif execution_time < 10:
        return 'fair'
    elif execution_time < 30:
        return 'poor'
    else:
        return 'very_poor'
