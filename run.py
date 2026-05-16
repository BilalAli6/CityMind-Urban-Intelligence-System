#!/usr/bin/env python3
"""
CityMind Launcher
Run: python3 run.py
Then open: http://localhost:5555
"""
import subprocess, sys, os, time, threading, webbrowser

DEPS = ["flask", "networkx", "numpy", "scikit-learn"]

def install_deps():
    for dep in DEPS:
        key = dep.replace("-","_").split("==")[0]
        try:
            __import__(key)
        except ImportError:
            print(f"  Installing {dep}...")
            subprocess.run([sys.executable,"-m","pip","install",dep,"--break-system-packages","-q"])

if __name__ == "__main__":
    print("="*52)
    print("  🏙️   CityMind — Urban Intelligence System")
    print("="*52)
    install_deps()
    print("  ✅ Dependencies ready")
    print("  🌐 Server: http://localhost:5555")
    print("  ⌨️  Press Ctrl+C to stop\n")

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def open_browser():
        time.sleep(2)
        try: webbrowser.open("http://localhost:5555")
        except: pass
    threading.Thread(target=open_browser, daemon=True).start()

    # Import and run the app
    import importlib.util
    spec = importlib.util.spec_from_file_location("citymind", "citymind.py")
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.app.run(debug=False, port=5555, host="0.0.0.0")
