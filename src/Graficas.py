import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

PATH_DATASET = "../log.csv"                 # Ruta del archivo CSV
EJEX   = "Reloj"                      # Columna eje X (hh:mm)
EJEY    = "Aeronaves_En_Cola_Llegada"  # Columna eje Y
FREQ_TICKS   = "2H"
HORA_INICIO  = "00:00"
HORA_FIN     = "23:59"

dataset = pd.read_csv(PATH_DATASET)
dataset["Reloj_dt"] = pd.to_datetime(dataset[EJEX], format='%H:%M')

plt.figure(figsize=(12,6))

sns.lineplot(data=dataset,x="Reloj_dt",y=EJEY,color="red", linewidth=1.5)
sns.despine(offset=10, trim=False)

plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.title("Evolución de la Cola de Aterrizaje", weight='bold', pad=20) 
plt.xlabel("Hora del día", labelpad=10)
plt.ylabel("Nº Aeronaves", labelpad=10)


ax = plt.gca()
base_date = dataset["Reloj_dt"].iloc[0].date()
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
plt.savefig("EvolucionColaAterrizaje.png", dpi=300)
plt.show()