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
if st.sidebar.button("Play"):
    st.session_state.simulando = True
if st.sidebar.button("Pausa"):
    st.session_state.simulando = False
if st.sidebar.button("Stop"):
    st.session_state.simulando = False
    st.session_state.i = 0
    st.rerun()

velocidad = st.sidebar.slider("Velocidad", 0.01, 1.0, 0.1, format="%f s")

# Barra de progreso del dia
if not dataset.empty:
    progreso_dia = st.session_state.i/len(dataset)
    st.sidebar.progress(min(progreso_dia, 1.0), text="Progreso del Dia")
def emergencia(fila):
    valor = str(fila.get('Emergencia','False')).strip()
    if valor == 'True':
        return ['background-color: #8B0000; color: white'] * len(fila)
    else:
        return[''] * len(fila)
    
def operativa(fila,colas,datasetHistory):
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
    if 'aterrizaje' not in st.session_state:
        st.session_state.aterrizaje = None
    if 'parking' not in st.session_state:
        st.session_state.parking = None
    if 'despegue' not in st.session_state:
        st.session_state.despegue = None
    
    if fila['Estado'] == "Aterrizaje":
        st.session_state.aterrizaje = fila
    if fila['Estado'] == "Estacionado":
        st.session_state.parking = fila
    if fila['Estado'] == "Despegando":
        st.session_state.despegue = fila
        
    st.markdown("Ultimos eventos registrados")
    filas = []
    if st.session_state.aterrizaje is not None:
        filas.append(st.session_state.aterrizaje)
    if st.session_state.parking is not None:
        filas.append(st.session_state.parking)
    if st.session_state.despegue is not None:
        filas.append(st.session_state.despegue)

    if filas:
        resumen = pd.DataFrame(filas)
        st.dataframe(resumen.style.apply(emergencia, axis=1),use_container_width=True,hide_index=True)


def tactica(datasetHistory,fila):
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
    if not datasetHistory.empty:
        fig = px.area(datasetHistory, x="Reloj", y=["Aeronaves_En_Cola_Llegada", "Aeronaves_En_Cola_Salida"],
                      title="Evolucion de Colas (Ultimas 2 horas)", height=300,
                      color_discrete_sequence=["#FFC107", "#FF4B4B"])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"               ")
        st.markdown(f"               ")
        st.markdown(f"               ")

def alerta(fila,colas):
    motivo = "SATURACION DE PISTA" if colas['llegada'] > 7 else "PARKING COMPLETO"
    st.markdown(f"<div class='alerta'>ALERTA CRITICA: {motivo} ({fila['Reloj']})</div>", unsafe_allow_html=True)
    st.error(f"Llegadas: {colas['llegada']} | Parking: {colas['parking']}/50")

def averia(estado):
    motivo = "OBJETO EN PISTA DE ATERRIZAJE" if estado['pistaAterrizaje'] == "Cerrada" else "OBJETO EN PISTA DE DESPEGUE"
    st.markdown(f"<div class='averia'>AVERIA: {motivo} ({fila['Reloj']})</div>", unsafe_allow_html=True)
    st.error(f"Llegadas: {colas['llegada']} | Parking: {colas['parking']}/50")


if st.session_state.i >= len(dataset):
    st.session_state.i = len(dataset) - 1 
    st.session_state.simulando = False 

idx = st.session_state.i
fila = dataset.iloc[idx]

inicio_hist = max(0,idx - 60)
datasetH = dataset.iloc[inicio_hist:idx+1]

colas = {
    'llegada': int(fila['Aeronaves_En_Cola_Llegada']),
    'parking': int(fila['Aeronaves_En_Estacionamiento']),
    'salida': int(fila['Aeronaves_En_Cola_Salida'])
}
estado = {
    'pistaDespegue': fila['Estado_Pista_Despegue'],
    'pistaAterrizaje':fila['Estado_Pista_Aterrizaje']  
}

container = st.container()
with container:
    if colas['llegada'] > 7 or colas['parking'] >= 45:
        alerta(fila,colas)

    if estado['pistaDespegue'] == "Cerrada" or estado['pistaAterrizaje'] == "Cerrada":
        averia(estado)
    
    elif modo == "Vista Operativa":
        operativa(fila,colas,datasetH)
    
    elif modo == "Vista Tactica":
        tactica(datasetH,fila)
    
    else:
        if (idx // 50) % 2 == 0:
            operativa(fila,colas,datasetH)
        else:
            tactica(datasetH,fila)

if st.session_state.simulando:
    time.sleep(velocidad)
    st.session_state.i += 1
    st.rerun() 

############################FUNCIONES AUXILIARES############################