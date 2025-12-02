import webview
import os
import threading
import time

def start_streamlit():
    # Ejecuta tu dashboard en segundo plano
    os.system('streamlit run Dashboard.py --server.headless true')

if __name__ == '__main__':
    # 1. Arranca el servidor de Streamlit en un hilo aparte
    t = threading.Thread(target=start_streamlit)
    t.daemon = True
    t.start()
    
    # Dale unos segundos para que arranque
    time.sleep(3)
    
    # 2. Abre una ventana nativa apuntando al local
    webview.create_window('Simulador Aeroportuario TFG', 'http://localhost:8501')
    webview.start()