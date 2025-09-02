import re
from typing import Dict, Any
from langchain_community.utilities import SQLDatabase

class QueryOptimizer:
    def __init__(self, db: SQLDatabase):
        self.db = db
    
    def optimize_query(self, sql_query: str) -> str:
        """Optimize SQL query for better performance"""
        
        optimized_query = sql_query.strip()
        
        # Basic optimizations
        optimizations = [
            self._add_limit_if_missing,
            self._optimize_select_star,
            self._optimize_joins,
            self._add_indexes_hints,
            self._optimize_where_clauses
        ]
        
        for optimization in optimizations:
            optimized_query = optimization(optimized_query)
        
        return optimized_query
    
    def _add_limit_if_missing(self, query: str) -> str:
        """Add LIMIT clause if missing to prevent large result sets"""
        
        query_lower = query.lower().strip()
        
        # Don't add LIMIT to queries that already have it, or to aggregation queries
        if ('limit' in query_lower or 
            'count(' in query_lower or 
            'sum(' in query_lower or 
            'avg(' in query_lower or 
            'max(' in query_lower or 
            'min(' in query_lower or
            'group by' in query_lower):
            return query
        
        # Add LIMIT 1000 for potentially large result sets
        if query.rstrip().endswith(';'):
            return query.rstrip()[:-1] + ' LIMIT 1000;'
        else:
            return query + ' LIMIT 1000'
    
    def _optimize_select_star(self, query: str) -> str:
        """Warn about SELECT * usage but don't change it automatically"""
        # This is just for analysis - we won't change SELECT * automatically
        # as it might be what the user wants
        return query
    
    def _optimize_joins(self, query: str) -> str:
        """Optimize JOIN conditions"""
        
        # Ensure proper JOIN syntax
        query = re.sub(r'\bINNER JOIN\b', 'JOIN', query, flags=re.IGNORECASE)
        
        return query
    
    def _add_indexes_hints(self, query: str) -> str:
        """Add index hints where appropriate"""
        # For MySQL, we could add USE INDEX hints, but this requires
        # knowledge of existing indexes, which we'll skip for now
        return query
    
    def _optimize_where_clauses(self, query: str) -> str:
        """Optimize WHERE clauses"""
        
        # Move more selective conditions first (basic heuristic)
        # This is a simplified optimization
        return query
    
    def analyze_query_complexity(self, query: str) -> Dict[str, Any]:
        """Analyze query complexity and potential performance issues"""
        
        analysis = {
            'complexity': 'low',
            'issues': [],
            'suggestions': [],
            'estimated_rows': 'unknown'
        }
        
        query_lower = query.lower()
        
        # Check for SELECT *
        if 'select *' in query_lower:
            analysis['issues'].append("Using SELECT * - consider selecting only needed columns")
            analysis['complexity'] = 'medium'
        
        # Check for missing LIMIT
        if ('limit' not in query_lower and 
            'count(' not in query_lower and
            'group by' not in query_lower):
            analysis['issues'].append("No LIMIT clause - may return large result set")
            analysis['suggestions'].append("Add LIMIT clause to control result size")
        
        # Check for multiple JOINs
        join_count = len(re.findall(r'\bjoin\b', query_lower))
        if join_count > 3:
            analysis['complexity'] = 'high'
            analysis['issues'].append(f"Multiple JOINs ({join_count}) may impact performance")
            analysis['suggestions'].append("Consider breaking into smaller queries or adding indexes")
        
        # Check for subqueries
        if '(' in query and 'select' in query_lower:
            subquery_count = query_lower.count('select') - 1
            if subquery_count > 0:
                analysis['complexity'] = 'medium' if subquery_count == 1 else 'high'
                analysis['issues'].append(f"Contains {subquery_count} subquery(ies)")
        
        # Check for LIKE with leading wildcard
        if re.search(r"like\s+['\"]%", query_lower):
            analysis['issues'].append("LIKE with leading wildcard - may be slow on large tables")
            analysis['suggestions'].append("Consider full-text search or alternative approaches")
        
        # Check for OR conditions
        or_count = len(re.findall(r'\bor\b', query_lower))
        if or_count > 2:
            analysis['issues'].append(f"Multiple OR conditions ({or_count}) may impact performance")
            analysis['suggestions'].append("Consider using IN clause or UNION instead")
        
        return analysis

def get_query_recommendations(query: str, db: SQLDatabase) -> Dict[str, Any]:
    """Get recommendations for query improvement"""
    
    optimizer = QueryOptimizer(db)
    analysis = optimizer.analyze_query_complexity(query)
    
    recommendations = {
        'original_query': query,
        'optimized_query': optimizer.optimize_query(query),
        'analysis': analysis,
        'performance_tips': []
    }
    
    # Add general performance tips
    recommendations['performance_tips'] = [
        "Use specific column names instead of SELECT *",
        "Add appropriate LIMIT clauses",
        "Ensure JOIN conditions use indexed columns",
        "Consider adding WHERE clauses to filter data early",
        "Use EXPLAIN to analyze query execution plan"
    ]
    
    return recommendations
