#!/usr/bin/env python3
"""
DrQuery Premium Launcher
Launch the premium version of DrQuery with enhanced UI/UX
"""

import subprocess
import sys
import os

def main():
    """Launch the premium DrQuery application"""
    
    # Change to src directory
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    
    # Launch streamlit app
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'app_premium.py',
            '--server.headless=true',
            '--server.enableCORS=false',
            '--server.enableXsrfProtection=false'
        ], cwd=src_dir, check=True)
    except KeyboardInterrupt:
        print("\n👋 Thanks for using DrQuery Premium!")
    except Exception as e:
        print(f"❌ Error launching DrQuery: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()