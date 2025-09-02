import streamlit as st
import plotly.graph_objects as go
import io
import base64
from datetime import datetime

def show_export_modal():
    """Show export modal using expander instead of dialog"""
    
    with st.expander("📤 Export Chart", expanded=True):
        st.markdown("### Export Options")
        
        # Format selection
        export_format = st.selectbox(
            "Export Format:",
            ["PNG", "PDF", "SVG", "HTML", "JSON"],
            index=0
        )
        
        # Size options for image formats
        if export_format in ["PNG", "PDF", "SVG"]:
            col1, col2 = st.columns(2)
            with col1:
                width = st.number_input("Width (px):", min_value=400, max_value=3000, value=1200, step=100)
            with col2:
                height = st.number_input("Height (px):", min_value=300, max_value=2000, value=800, step=100)
            
            scale = st.slider("Scale (quality):", min_value=1, max_value=4, value=2)
        else:
            width, height, scale = 1200, 800, 1
        
        # File naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"drquery_chart_{timestamp}"
        
        filename = st.text_input(
            "Filename (without extension):",
            value=default_filename,
            help="The file extension will be added automatically"
        )
        
        # Export button
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("📤 Export", use_container_width=True):
                if 'current_chart' in st.session_state and st.session_state.current_chart is not None:
                    try:
                        # Export the chart using the current chart from session state
                        exported_data, exported_filename = export_chart_data(
                            st.session_state.current_chart,
                            export_format,
                            filename,
                            width=width,
                            height=height,
                            scale=scale
                        )
                        
                        if exported_data:
                            # Create download button
                            st.download_button(
                                label=f"💾 Download {exported_filename}",
                                data=exported_data,
                                file_name=exported_filename,
                                mime=get_mime_type(export_format)
                            )
                            st.success(f"Chart ready for download as {exported_filename}")
                        else:
                            st.error("Failed to export chart")
                            
                    except Exception as e:
                        st.error(f"Export failed: {str(e)}")
                else:
                    st.error("No chart available to export. Please generate a chart first.")
        
        with col2:
            if st.button("❌ Close", use_container_width=True):
                st.info("Export dialog closed. Generate a new chart to export again.")

def export_chart_data(chart: go.Figure, format: str, filename: str, **kwargs):
    """Export chart in specified format"""
    
    try:
        if format.upper() == "PNG":
            try:
                img_bytes = chart.to_image(
                    format="png",
                    width=kwargs.get('width', 1200),
                    height=kwargs.get('height', 800),
                    scale=kwargs.get('scale', 2)
                )
                return img_bytes, f"{filename}.png"
            except Exception as e:
                st.error("PNG export requires 'kaleido' package. Install with: pip install kaleido")
                # Fallback to HTML
                html_string = chart.to_html(include_plotlyjs=True)
                return html_string.encode(), f"{filename}_fallback.html"
        
        elif format.upper() == "PDF":
            try:
                img_bytes = chart.to_image(
                    format="pdf",
                    width=kwargs.get('width', 1200),
                    height=kwargs.get('height', 800)
                )
                return img_bytes, f"{filename}.pdf"
            except Exception as e:
                st.error("PDF export requires 'kaleido' package. Install with: pip install kaleido")
                # Fallback to HTML
                html_string = chart.to_html(include_plotlyjs=True)
                return html_string.encode(), f"{filename}_fallback.html"
        
        elif format.upper() == "SVG":
            try:
                svg_string = chart.to_image(format="svg")
                return svg_string, f"{filename}.svg"
            except Exception as e:
                st.error("SVG export requires 'kaleido' package. Install with: pip install kaleido")
                # Fallback to HTML
                html_string = chart.to_html(include_plotlyjs=True)
                return html_string.encode(), f"{filename}_fallback.html"
        
        elif format.upper() == "HTML":
            html_string = chart.to_html(
                include_plotlyjs=True,
                div_id=f"chart_{filename}"
            )
            return html_string.encode(), f"{filename}.html"
        
        elif format.upper() == "JSON":
            json_string = chart.to_json()
            return json_string.encode(), f"{filename}.json"
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    except Exception as e:
        st.error(f"Export failed: {str(e)}")
        # Final fallback - always try HTML
        try:
            html_string = chart.to_html(include_plotlyjs=True)
            return html_string.encode(), f"{filename}_emergency_fallback.html"
        except:
            return None, None

def create_download_link(file_data, filename: str, file_format: str):
    """Create a download link for the exported file"""
    
    if file_data is None:
        return None
    
    # Determine MIME type
    mime_types = {
        'png': 'image/png',
        'pdf': 'application/pdf',
        'svg': 'image/svg+xml',
        'html': 'text/html',
        'json': 'application/json'
    }
    
    mime_type = mime_types.get(file_format.lower(), 'application/octet-stream')
    
    # Create base64 encoded data
    if isinstance(file_data, str):
        file_data = file_data.encode()
    
    b64_data = base64.b64encode(file_data).decode()
    
    # Create download link
    href = f'<a href="data:{mime_type};base64,{b64_data}" download="{filename}" style="text-decoration: none;">'
    href += f'<button style="background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">'
    href += f'📥 Download {filename}</button></a>'
    
    return href

def get_mime_type(format: str) -> str:
    """Get MIME type for the given format"""
    mime_types = {
        "PNG": "image/png",
        "PDF": "application/pdf", 
        "SVG": "image/svg+xml",
        "HTML": "text/html",
        "JSON": "application/json"
    }
    return mime_types.get(format.upper(), "application/octet-stream")
