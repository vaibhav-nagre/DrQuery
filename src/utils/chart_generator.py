import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import List, Dict, Any

class ChartGenerator:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        # More robust column type detection
        self.numeric_columns = []
        self.categorical_columns = []
        self.datetime_columns = []
        
        for col in data.columns:
            try:
                # Try to convert to numeric
                pd.to_numeric(data[col], errors='raise')
                self.numeric_columns.append(col)
            except (ValueError, TypeError):
                try:
                    # Try to convert to datetime
                    pd.to_datetime(data[col], errors='raise')
                    self.datetime_columns.append(col)
                except (ValueError, TypeError):
                    # Default to categorical
                    self.categorical_columns.append(col)
        
        # If no numeric columns found, treat first few columns as potential numeric
        if not self.numeric_columns and len(data.columns) > 1:
            # Check if any columns contain numbers as strings
            for col in data.columns:
                sample_values = data[col].dropna().head(10)
                numeric_count = 0
                for val in sample_values:
                    try:
                        float(str(val))
                        numeric_count += 1
                    except:
                        pass
                if numeric_count > len(sample_values) * 0.7:  # If 70% are numeric
                    self.numeric_columns.append(col)
                    if col in self.categorical_columns:
                        self.categorical_columns.remove(col)
    
    def suggest_charts(self, query: str = "") -> List[Dict[str, Any]]:
        """Suggest appropriate chart types based on data characteristics and query"""
        suggestions = []
        
        # Analyze data structure
        num_numeric = len(self.numeric_columns)
        num_categorical = len(self.categorical_columns)
        num_datetime = len(self.datetime_columns)
        total_rows = len(self.data)
        
        # Query-based suggestions
        query_lower = query.lower()
        
        # Specific chart type requests
        if 'bar' in query_lower or 'column' in query_lower:
            suggestions.append({
                'type': 'Bar Chart',
                'reason': 'Requested in query',
                'priority': 1
            })
        elif 'line' in query_lower or 'trend' in query_lower or 'time' in query_lower:
            suggestions.append({
                'type': 'Line Chart',
                'reason': 'Time series or trend analysis requested',
                'priority': 1
            })
        elif 'pie' in query_lower or 'proportion' in query_lower or 'percentage' in query_lower:
            suggestions.append({
                'type': 'Pie Chart',
                'reason': 'Proportional data requested',
                'priority': 1
            })
        elif 'scatter' in query_lower or 'correlation' in query_lower or 'relationship' in query_lower:
            suggestions.append({
                'type': 'Scatter Plot',
                'reason': 'Relationship analysis requested',
                'priority': 1
            })
        elif 'histogram' in query_lower or 'distribution' in query_lower:
            suggestions.append({
                'type': 'Histogram',
                'reason': 'Distribution analysis requested',
                'priority': 1
            })
        
        # Data-driven suggestions
        if num_datetime > 0 and num_numeric > 0:
            suggestions.append({
                'type': 'Line Chart',
                'reason': 'Time series data detected',
                'priority': 2
            })
        
        if num_categorical > 0 and num_numeric > 0:
            suggestions.append({
                'type': 'Bar Chart',
                'reason': 'Categorical and numeric data combination',
                'priority': 2
            })
            
            if len(self.data[self.categorical_columns[0]].unique()) <= 10:
                suggestions.append({
                    'type': 'Pie Chart',
                    'reason': 'Small number of categories suitable for pie chart',
                    'priority': 3
                })
        
        if num_numeric >= 2:
            suggestions.append({
                'type': 'Scatter Plot',
                'reason': 'Multiple numeric columns available for correlation analysis',
                'priority': 3
            })
        
        if num_numeric > 0:
            suggestions.append({
                'type': 'Histogram',
                'reason': 'Numeric data available for distribution analysis',
                'priority': 4
            })
        
        if num_categorical >= 2 and num_numeric > 0:
            suggestions.append({
                'type': 'Heatmap',
                'reason': 'Multiple categorical variables for cross-tabulation',
                'priority': 4
            })
        
        if total_rows > 100 and num_numeric > 0:
            suggestions.append({
                'type': 'Box Plot',
                'reason': 'Large dataset suitable for statistical summary',
                'priority': 5
            })
        
        # Remove duplicates and sort by priority
        seen_types = set()
        unique_suggestions = []
        for suggestion in sorted(suggestions, key=lambda x: x['priority']):
            if suggestion['type'] not in seen_types:
                seen_types.add(suggestion['type'])
                unique_suggestions.append(suggestion)
        
        return unique_suggestions[:5] if unique_suggestions else [
            {'type': 'Bar Chart', 'reason': 'Default visualization', 'priority': 10}
        ]
    
    def create_chart(self, chart_type: str, query: str = "") -> go.Figure:
        """Create a chart based on the specified type"""
        try:
            if chart_type == "Bar Chart":
                return self._create_bar_chart()
            elif chart_type == "Line Chart":
                return self._create_line_chart()
            elif chart_type == "Pie Chart":
                return self._create_pie_chart()
            elif chart_type == "Scatter Plot":
                return self._create_scatter_plot()
            elif chart_type == "Histogram":
                return self._create_histogram()
            elif chart_type == "Box Plot":
                return self._create_box_plot()
            elif chart_type == "Heatmap":
                return self._create_heatmap()
            else:
                return self._create_bar_chart()  # Default
        except Exception as e:
            print(f"Error creating {chart_type}: {str(e)}")
            return None
    
    def _create_bar_chart(self) -> go.Figure:
        """Create a bar chart"""
        if not self.categorical_columns or not self.numeric_columns:
            return None
        
        x_col = self.categorical_columns[0]
        y_col = self.numeric_columns[0]
        
        # Group by categorical column and sum numeric values
        grouped_data = self.data.groupby(x_col)[y_col].sum().reset_index()
        
        fig = px.bar(
            grouped_data,
            x=x_col,
            y=y_col,
            title=f"{y_col} by {x_col}",
            color=y_col,
            color_continuous_scale="viridis"
        )
        
        fig.update_layout(
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            showlegend=False
        )
        
        return fig
    
    def _create_line_chart(self) -> go.Figure:
        """Create a line chart"""
        if self.datetime_columns and self.numeric_columns:
            x_col = self.datetime_columns[0]
            y_col = self.numeric_columns[0]
        elif len(self.numeric_columns) >= 2:
            x_col = self.numeric_columns[0]
            y_col = self.numeric_columns[1]
        elif self.categorical_columns and self.numeric_columns:
            # Sort categorical data if it looks like it might be ordered
            x_col = self.categorical_columns[0]
            y_col = self.numeric_columns[0]
        else:
            return None
        
        if x_col in self.datetime_columns:
            sorted_data = self.data.sort_values(x_col)
        else:
            sorted_data = self.data
        
        fig = px.line(
            sorted_data,
            x=x_col,
            y=y_col,
            title=f"{y_col} over {x_col}",
            markers=True
        )
        
        fig.update_layout(
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title()
        )
        
        return fig
    
    def _create_pie_chart(self) -> go.Figure:
        """Create a pie chart"""
        if not self.categorical_columns:
            return None
        
        cat_col = self.categorical_columns[0]
        
        if self.numeric_columns:
            # Use numeric column for values
            grouped_data = self.data.groupby(cat_col)[self.numeric_columns[0]].sum()
        else:
            # Use count of categories
            grouped_data = self.data[cat_col].value_counts()
        
        fig = px.pie(
            values=grouped_data.values,
            names=grouped_data.index,
            title=f"Distribution of {cat_col}"
        )
        
        return fig
    
    def _create_scatter_plot(self) -> go.Figure:
        """Create a scatter plot"""
        if len(self.numeric_columns) < 2:
            return None
        
        x_col = self.numeric_columns[0]
        y_col = self.numeric_columns[1]
        
        color_col = self.categorical_columns[0] if self.categorical_columns else None
        
        fig = px.scatter(
            self.data,
            x=x_col,
            y=y_col,
            color=color_col,
            title=f"{y_col} vs {x_col}",
            trendline="ols" if len(self.data) > 10 else None
        )
        
        fig.update_layout(
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title()
        )
        
        return fig
    
    def _create_histogram(self) -> go.Figure:
        """Create a histogram"""
        if not self.numeric_columns:
            return None
        
        col = self.numeric_columns[0]
        
        fig = px.histogram(
            self.data,
            x=col,
            title=f"Distribution of {col}",
            marginal="box"
        )
        
        fig.update_layout(
            xaxis_title=col.replace('_', ' ').title(),
            yaxis_title="Frequency"
        )
        
        return fig
    
    def _create_box_plot(self) -> go.Figure:
        """Create a box plot"""
        if not self.numeric_columns:
            return None
        
        if self.categorical_columns:
            # Box plot by category
            x_col = self.categorical_columns[0]
            y_col = self.numeric_columns[0]
            
            fig = px.box(
                self.data,
                x=x_col,
                y=y_col,
                title=f"{y_col} Distribution by {x_col}"
            )
        else:
            # Single box plot
            col = self.numeric_columns[0]
            fig = px.box(
                self.data,
                y=col,
                title=f"{col} Distribution"
            )
        
        return fig
    
    def _create_heatmap(self) -> go.Figure:
        """Create a heatmap"""
        if len(self.categorical_columns) < 2:
            return None
        
        cat1 = self.categorical_columns[0]
        cat2 = self.categorical_columns[1]
        
        # Create crosstab
        if self.numeric_columns:
            # Use numeric values
            pivot_table = self.data.pivot_table(
                values=self.numeric_columns[0],
                index=cat1,
                columns=cat2,
                aggfunc='sum',
                fill_value=0
            )
        else:
            # Use counts
            crosstab = pd.crosstab(self.data[cat1], self.data[cat2])
            pivot_table = crosstab
        
        fig = px.imshow(
            pivot_table,
            title=f"Heatmap: {cat1} vs {cat2}",
            color_continuous_scale="viridis"
        )
        
        return fig
    
    def get_insights(self, data: pd.DataFrame, chart_type: str) -> List[str]:
        """Generate insights about the data and chart"""
        insights = []
        
        # Basic data insights
        insights.append(f"Dataset contains {len(data)} rows and {len(data.columns)} columns")
        
        if self.numeric_columns:
            for col in self.numeric_columns[:2]:  # Top 2 numeric columns
                mean_val = data[col].mean()
                max_val = data[col].max()
                min_val = data[col].min()
                insights.append(f"{col}: Mean = {mean_val:.2f}, Range = {min_val:.2f} to {max_val:.2f}")
        
        if self.categorical_columns:
            for col in self.categorical_columns[:2]:  # Top 2 categorical columns
                unique_count = data[col].nunique()
                top_category = data[col].mode().iloc[0] if len(data[col].mode()) > 0 else "N/A"
                insights.append(f"{col}: {unique_count} unique values, most common = {top_category}")
        
        # Chart-specific insights
        if chart_type == "Scatter Plot" and len(self.numeric_columns) >= 2:
            correlation = data[self.numeric_columns[0]].corr(data[self.numeric_columns[1]])
            insights.append(f"Correlation between {self.numeric_columns[0]} and {self.numeric_columns[1]}: {correlation:.3f}")
        
        return insights
