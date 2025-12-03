import streamlit as st
import pandas as pd
import time
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border: 1px solid #dce1e6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .alerta {
        background-color: #ff4b4b;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

if 'i' not in st.session_state:
    st.session_state.i = 0

if 'simulando' not in st.session_state:
    st.session_state.simulando = False

dataset = pd.read_csv("../csv/log.csv", sep=',', decimal=',')
st.sidebar.title("Centro de Control")
modo = st.sidebar.radio(
    "Seleccionar Pantalla:",
    ["Automatico", "Vista Operativa", "Vista Tactica"],
    index=0
)
if st.sidebar.button("Empezar"):
    st.session_state.simulando = True
if st.sidebar.button("Pausar"):
    st.session_state.simulando = False
if st.sidebar.button("Parar"):
    st.session_state.simulando = False
    st.session_state.i = 0
    st.rerun()

velocidad = st.sidebar.slider("Velocidad", 0.01, 1.0, 0.1, format="%f s")

# Barra de progreso del dia
if not dataset.empty:
    progreso_dia = st.session_state.i/len(dataset)
    st.sidebar.progress(min(progreso_dia, 1.0), text="Progreso del Dia")

def render_operativa(fila,colas):
    st.subheader(f"VISTA OPERATIVA | {fila['Reloj']}")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("LLEGADAS")
        n = colas['llegada']
        iconos = "✈️ " * n if n > 0 else "Libre"
        st.markdown(f"### {n}")
        st.markdown(f"<div style='font-size:20px'>{iconos}</div>", unsafe_allow_html=True)

    with c2:
        st.success("GATES")
        n = colas['parking']
        st.metric("Ocupacion", f"{n}/50")
        st.progress(n/50)

    with c3:
        st.warning("SALIDAS")
        n = colas['salida']
        iconos = "✈️ " * n if n > 0 else "Libre"
        st.markdown(f"### {n}")
        st.markdown(f"<div style='font-size:20px'>{iconos}</div>", unsafe_allow_html=True)

    st.divider()
    if 'val1' not in st.session_state:
        st.session_state.val1 = ""
    if 'val2' not in st.session_state:
        st.session_state.val2 = ""
    if 'val3' not in st.session_state:
        st.session_state.val3 = ""
    mensaje1 = st.empty()
    mensaje2 = st.empty()
    mensaje3 = st.empty()
    
    if fila['Estado'] == "Aterrizaje":
        st.session_state.val1 = f"Ultimo Aterrizaje registrado: Vuelo {fila['ID_Vuelo']} ({fila['Hora_Salida_Origen']}|{fila['Origen']} -> {fila['Hora_Llegada_Destino']}|{fila['Destino']}) aterrizo"
    if fila['Estado'] == "Estacionado":
        st.session_state.val2 =f"Ultimo Estacionamiento registrado: Vuelo {fila['ID_Vuelo']} ({fila['Hora_Salida_Origen']}|{fila['Origen']} -> {fila['Hora_Llegada_Destino']}|{fila['Destino']}) estaciono"
    if fila['Estado'] == "Despegando":
        st.session_state.val3 =f"Ultimo Despegue registrado: Vuelo {fila['ID_Vuelo']} ({fila['Hora_Salida_Origen']}|{fila['Origen']} -> {fila['Hora_Llegada_Destino']}|{fila['Destino']}) despego"
    mensaje1.caption(st.session_state.val1)
    mensaje2.caption(st.session_state.val2)
    mensaje3.caption(st.session_state.val3)


def render_tactica(dataset_hist,fila):
    st.subheader(f"VISTA TACTICA | {fila['Reloj']}")
    c4, c5, c6 = st.columns(3)
    with c4:
        st.info("Pasajeros")
        datast = dataset.iloc[:st.session_state.i+1]
        datast = datast[datast['Estado'] == 'Llegando']
        pasajeros= datast['Pasajeros'].sum()
        st.metric("Pasajeros Procesados", f"{int(pasajeros):,}")   
        st.markdown(f"               ")
        st.markdown(f"               ")
        st.markdown(f"               ")
    with c5:
        st.info("Clima")
        st.metric("Clima Actual", fila['Clima'])
        st.markdown(f"               ")
        st.markdown(f"               ")
        st.markdown(f"               ")
        
    with c6:
        st.info("Estado")
        st.metric("Estado del Sistema", "ACTIVO", delta="OK")
        st.markdown(f"               ")
        st.markdown(f"               ")

    # Tendencia de Colas
    if not dataset_hist.empty:
        fig = px.area(dataset_hist, x="Reloj", y=["Aeronaves_En_Cola_Llegada", "Aeronaves_En_Cola_Salida"],
                      title="Evolucion de Colas (Ultimas 2 horas)", height=300,
                      color_discrete_sequence=["#FFC107", "#FF4B4B"])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"               ")
        st.markdown(f"               ")
        st.markdown(f"               ")

def render_alerta(fila,colas):
    motivo = "SATURACION DE PISTA" if colas['llegada'] > 7 else "PARKING COMPLETO"
    st.markdown(f"<div class='alerta'>ALERTA CRITICA: {motivo} ({fila['Reloj']})</div>", unsafe_allow_html=True)
    st.error(f"Llegadas: {colas['llegada']} | Parking: {colas['parking']}/50")


if st.session_state.i >= len(dataset):
    st.session_state.i = len(dataset) - 1 
    st.session_state.simulando = False 

idx = st.session_state.i
fila = dataset.iloc[idx]

inicio_hist = max(0,idx - 60)
dataset_history = dataset.iloc[inicio_hist:idx+1]

colas = {
    'llegada': int(fila['Aeronaves_En_Cola_Llegada']),
    'parking': int(fila['Aeronaves_En_Estacionamiento']),
    'salida': int(fila['Aeronaves_En_Cola_Salida'])
}

container = st.container()
with container:
    if colas['llegada'] > 7 or colas['parking'] >= 45:
        render_alerta(fila,colas)
    
    elif modo == "Vista Operativa":
        render_operativa(fila,colas)
    
    elif modo == "Vista Tactica":
        render_tactica(dataset_history,fila)
    
    else:
        if (idx // 50) % 2 == 0:
            render_operativa(fila,colas)
        else:
            render_tactica(dataset_history,fila)

if st.session_state.simulando:
    time.sleep(velocidad)
    st.session_state.i += 1
    st.rerun() 