# Simulacion de operaciones, flujo de aeronaves y sistemas auxiliares en un aeropuerto


## Características clave
* **Motor de Simulación:** Basado en `Simpy` para la gestión eficiente del tiempo y eventos.

* **Data-Driven:** Alimentado a base de datos reales mediante un archivo CSV (`data/ciudades.csv`)

* **Escenarios de Prueba:**
    * **Escenario Base:** Es un escenario con la operativa estándar del simulador.
    * **Escenario de Estrés:** Situación operativa de alta densidad de tráfico para probar la saturación del sistema.
    * **Escenario Adverso:** Simulación de un escenario con condiciones meteorológicas extremas
    * **Escenario Crítico:** El escenario con mayor densidad de tráfico de todos para comprobar la estabilidad del sistema.

## Estructura del Trabajo

```text
|── csv/                    
|── graficosfinales/
|── memoria/
|   |── build/
|   |── portada/
|   |── secciones
|   |── datos_tfg.tex
|   |── README.md
|   └── tfg_etsiinf_plantilla.tex
|── src/
|   |── Aeronaves.py
|   |── Dashboard.py
|   |── FactoresExternos.py
|   |── GeneradorAeronaves.py
|   |── Gráficas.py
|   |── Input.py
|   |── Launch.py
|   |── Main.py 
|   |── ServiciosAuxiliares.py 
|   └── TorreDeControl.py
|── .gitignore
|── README.md
└── requirements.txt
```

## Instalación y Ejecución
### Clonar el Repositorio
```bash
git clone https://github.com/Furio14/TFG.git
```
### Instalar Dependencias
```bash
pip install -r requirements.txt
```
### Ejecutar la Simulación
```bash
python Main.py
```

### Parametrós de Entrada 
Al ejecutar el `Main.py` se abre una consola interactiva que solicita parámetros para iniciar la simulación.

* **Duración:** Horas totales a simular | `0-168` (Default:24)
* **Tráfico:** Tasa media de vuelos diarios | `100-500` (Default:200)
* **Estacionalidad:** Mes de inicio | `Enero-Diciembre`(Default:Enero)
* **Turnos:** Hora de inicio de la jornada | `Madrugada-Noche` (Default: Madrugada)
* **Iteraciones:** Número de ejecuciones para el análisis estadístico | `1-75` (Default: 50)

### Dashboard
Una vez finalizadas todas las iteraciones, el sistema procesa los logs y ejecutando este comando:

```bash
python Launch.py
```
se mostrará el dashboard de la simulación en otra pantalla distinta.

El dashboard puede avanzar a todo tipo de tiempos que el usuario desee ajustar, y muestra como se ve una simulación y como cambian los datos durante el transcurso de la simulación.

