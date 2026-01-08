import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import numpy as ran

def generadorGraficas():
    EJEX   = "Reloj"
    EJEY    = "Aeronaves_En_Cola_Llegada" 
    FREQ_TICKS   = "2H"
    HORA_INICIO  = "00:00"
    HORA_FIN     = "23:59"

    datasetLog = pd.read_csv("../csv/log.csv")
    datasetLog["Reloj_dt"] = pd.to_datetime(datasetLog[EJEX], format='%H:%M')
    datasetRes = pd.read_csv("../csv/resultados.csv",sep = ',',decimal = ',',thousands = '.')
    #########################################Graficas Log#########################################
    plt.figure(figsize=(12,6))
    sns.lineplot(data=datasetLog,x="Reloj_dt",y=EJEY,color="red", linewidth=1.5)
    sns.despine(offset=10, trim=False)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.title("Evolución de la Cola de Aterrizaje", weight='bold', pad=20) 
    plt.xlabel("Hora del día", labelpad=10)
    plt.ylabel("Nº Aeronaves", labelpad=10)

    ax = plt.gca()
    base_date = datasetLog["Reloj_dt"].iloc[0].date()
    start_limit = pd.Timestamp.combine(base_date, pd.to_datetime(HORA_INICIO).time())
    end_limit   = pd.Timestamp.combine(base_date, pd.to_datetime(HORA_FIN).time())

    ax.set_xlim(start_limit, end_limit)

    ticks = pd.date_range(start=start_limit, end=end_limit, freq=FREQ_TICKS)
    if ticks[-1] != end_limit:
        ticks = ticks.union([end_limit])

    ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("../graficosfinales/EvolucionColaAterrizaje.png", dpi=300)
    #plt.show()

    #########################################Graficas Resultados#########################################
    graficasBoxPlot(["TotalMadrugada","TotalMañana","TotalTarde","TotalNoche"],datasetRes,"Total","Operaciones Aereas")
    graficasBoxPlot(["TasaLlegadaMadrugada","TasaLlegadaMañana","TasaLlegadaTarde","TasaLlegadaNoche"],datasetRes,"TasaLlegada","Tasa Llegadas")
    graficasBoxPlot(["TasaSalidaMadrugada","TasaSalidaMañana","TasaSalidaTarde","TasaSalidaNoche"],datasetRes,"TasaSalida","Tasa Salidas")

    graficasBootstrap(datasetRes,"MediaTiempoCicloAeronaves")
    plt.title("Estimacion Tiempo Media Aeronaves")
    plt.xlabel("Tiempo Medio (Minutos)")
    plt.ylabel("Frecuencia")
    plt.savefig("../graficosfinales/MediaBootstrap.png",dpi=300)
    graficasBootstrap(datasetRes,"MediaPasajerosAeronave")
    plt.title("Estimacion Media Pasajeros por Aeronave")
    plt.xlabel("Numero Medio de Pasajeros")
    plt.ylabel("Frecuencia")
    plt.savefig("../graficosfinales/MediaPasajeros.png",dpi=300)

    plt.figure(figsize=(10,6))
    sns.regplot(data=datasetRes,x="TotalOperacionesAereas",y="MediaTiempoCicloAeronaves",scatter_kws={'alpha':0.5},line_kws={'color':'black'})
    plt.title("Operaciones Aereas vs Eficiencia")
    plt.xlabel("Número diario de Operaciones Aereas")
    plt.ylabel("Tiempo Medio De Ciclo (Minutos)")
    plt.savefig("../graficosfinales/Regresion.png")

    plt.figure(figsize=(10,6))
    g = sns.jointplot(
        data = datasetRes,
        x="TotalOperacionesAereas",
        y="MediaTiempoCicloAeronaves",
        kind="kde",
        fill=True,
        color="#4CB391",
        height=8
    )
    g.set_axis_labels("Número diario de Operaciones Aereas","Tiempo Medio De Ciclo (Minutos)",fontsize=12)
    g.fig.suptitle("Densidad vs eficiencia", y=1.02,fontsize=15)
    plt.savefig("../graficosfinales/Hexbin.png",bbox_inches='tight')

    graficasPasajeros(datasetRes.head(10).copy(),"PasajerosIters",rotar=False)
    graficasPasajeros(datasetRes,"PasajerosvolumenEntero",rotar=True)

def graficasBoxPlot(cols,dataset,mode,name):
    plt.figure(figsize=(10,6))
    dataBoxPlot = dataset.melt(value_vars=cols,var_name="Turno",value_name=name)
    dataBoxPlot["Turno"] = dataBoxPlot["Turno"].str.replace(mode,"")

    sns.boxplot(data=dataBoxPlot,x="Turno",y=name,hue="Turno",legend=False,palette="Set2")
    sns.stripplot(data=dataBoxPlot,x="Turno",y=name,color="black",size=2,alpha=0.3)
    plt.title(f"{name} por Turno")
    plt.savefig(f"../graficosfinales/{mode}PorTurno",dpi = 300)

def graficasBootstrap(datasetRes,mode):
    lista = []
    parametro = datasetRes[mode]
    for _ in range(1000): #bootstrap
        muestra = ran.random.choice(parametro.values,size = len(parametro),replace = True)
        lista.append(ran.mean(muestra))
    icMin = ran.percentile(lista,2.5)
    icMax = ran.percentile(lista,97.5)
    media = ran.mean(parametro)
    plt.figure(figsize=(10,6))
    sns.histplot(lista,kde=True,color="skyblue",bins=30,edgecolor = "white")
    plt.axvline(icMin,color="black",linestyle= '--',label = "IC 2.5%")
    plt.axvline(icMax,color="black",linestyle= '--',label = "IC 97.5%")
    plt.axvline(media,color="red",linewidth = 2,label = "Media")

def graficasPasajeros(dataset,nombre,rotar=False):
    dataPlot = dataset.sort_values('PasajerosTotales', ascending=False).copy()
    iters = dataPlot['Semilla'].astype(str)
    fig,(ej1,ej2) = plt.subplots(2,1,figsize=(14,7),sharex=True)
    datos = dataPlot['PasajerosTotales']/1000
    ej1.bar(iters,datos,color='skyblue',label='Total Pasajeros', alpha=0.8)

    ej1.set_ylabel('Total Pasajeros (Miles)',color='tab:blue',fontsize=18)
    ej1.set_title(f'Resultados por semilla', fontsize=16, fontweight='bold')
    ej1.grid(axis='y',alpha=0.3,linestyle='--')
    ej1.set_ylim(0,datos.max()*1.1)

    ej2.scatter(iters, dataPlot['MediaPasajerosAeronave'], color='tab:red', s=100, label='Media por Avión',zorder=3)
    ej2.vlines(iters,0,dataPlot['MediaPasajerosAeronave'],color='tab:red',alpha=0.3,linewidth=1)

    ej2.set_ylabel('Media Pasajeros / Avión', color='tab:red', fontsize=18)
    ej2.set_xlabel('Semilla', fontsize=18)
    ej2.grid(axis='both',alpha=0.3,linestyle='--')
    miny = dataPlot['MediaPasajerosAeronave'].min() * 0.98
    maxy = dataPlot['MediaPasajerosAeronave'].max() * 1.02
    ej2.set_ylim(miny, maxy)
    plt.xticks(rotation=90,fontsize=10)
    plt.tight_layout()
    plt.savefig(f"../graficosfinales/{nombre}",dpi = 300)