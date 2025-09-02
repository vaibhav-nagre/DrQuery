#!/usr/bin/env python3
"""
DrQuery - Intelligent Database Query Assistant
Main entry point for Streamlit Community Cloud deployment
Created by Vaibhav Nagre
"""

import streamlit as st
import sys
import os

# Add the src directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Change working directory to project root
os.chdir(current_dir)

# Import and run the main application
if __name__ == "__main__":
    # Import the main application
    import src.main
