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
    datasetRes = pd.read_csv("../csv/resultados.csv")

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
    plt.figure(figsize=(10,6))
    cols = ["TotalMadrugada","TotalMañana","TotalTarde","TotalNoche"]
    dataBoxPlot = datasetRes.melt(value_vars=cols,var_name="Turno",value_name="Operaciones Aereas")
    dataBoxPlot["Turno"] = dataBoxPlot["Turno"].str.replace("Total","")

    sns.boxplot(data=dataBoxPlot,x="Turno",y="Operaciones Aereas",hue="Turno",legend=False,palette="Set2")
    sns.stripplot(data=dataBoxPlot,x="Turno",y="Operaciones Aereas",color="black",size=2,alpha=0.3)
    plt.title("Operaciones Totales por Turno")
    plt.savefig("../graficosfinales/OperacionesTotalesTurno",dpi = 300)

    listaTiempo = []
    tiempoCiclo = datasetRes["MediaTiempoCicloAeronaves"]
    for _ in range(1000):
        muestra = ran.random.choice(tiempoCiclo.values,size = len(tiempoCiclo),replace = True)
        listaTiempo.append(ran.mean(muestra))
    icMin = ran.percentile(listaTiempo,2.5)
    icMax = ran.percentile(listaTiempo,97.5)
    media = ran.mean(tiempoCiclo)
    plt.figure(figsize=(10,6))
    sns.histplot(listaTiempo,kde=True,color="skyblue",bins=30,edgecolor = "white")
    plt.axvline(icMin,color="black",linestyle= '--',label = "IC 2.5%")
    plt.axvline(icMax,color="black",linestyle= '--',label = "IC 97.5%")
    plt.axvline(media,color="red",linewidth = 2,label = "Media")
    plt.title("Estimacion Bootstrap")
    plt.xlabel("Tiempo Medio (Minutos)")
    plt.ylabel("Frecuencia")
    plt.savefig("../graficosfinales/MediaBootstrap.png",dpi=300)