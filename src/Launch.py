import webview
import os
import threading
import time

def start_streamlit():
    # Ejecuta tu dashboard en segundo plano
    os.system('streamlit run Dashboard.py --server.headless true')

if __name__ == '__main__':
    t = threading.Thread(target=start_streamlit)
    t.daemon = True
    t.start()
    webview.create_window('Dashboard TFG', 'http://localhost:8501')
    webview.start()