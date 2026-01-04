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
|   |── ciudades.csv                    # [INPUT] Contiene los datos reales de distancias entre aeropuertos con sus IDs
|   |── estadisticas.csv                # [OUTPUT] Contiene el cálculo total de métricas clave de todas las iteraciones
|   |── log.csv                         # [OUTPUT] Traza detallada evento a evento del simulador
|   └── resultados.csv                  # [OUTPUT] Contiene información y métricas de cada iteración y semilla que se realiza en una simulación          
|── graficosfinales/                    # Cada vez que termina la simulación se generan distintas gráficas para poder analizar visualmente los datos y comparar cambios en distintos escenarios
|   |── EvolucionColaAterrizaje.png
|   |── Hexbin.png
|   |── MediaBoostrap.png
|   |── MediaPasajeros.png
|   |── PasajerosIters.png
|   |── PasajerosvolumenEntero.png
|   |── Regresion.png
|   |── TasaLlegadaPorTurno.png
|   |── TasaSalidaPorTurno.png
|   └── TotalPorTurno.png
|── memoria/
|   |── build/
|   |── portada/
|   |── secciones
|   |── datos_tfg.tex
|   |── README.md
|   └── tfg_etsiinf_plantilla.tex
|── src/
|   |── Aeronaves.py                    # Define la clase `Aeronave`, sus atributos y métodos de registro
|   |── Dashboard.py                    # Panel de Control para la visualización de los datos a tiempo real
|   |── FactoresExternos.py             # Configuración del clima, retrasos y condiciones externas
|   |── GeneradorAeronaves.py           # Genera aeronaves combinando datos de `ciudades.csv` con generación ectocástica
|   |── Graficas.py                     # Generación automática de gráficas al finalizar la simulación
|   |── Input.py                        # Módulo que contiene la configuración interactiva de escenarios
|   |── Launch.py                       # Lanzador de la aplicación del dashboard
|   |── Main.py                         # Script de ejecución que controla las iteraciones y el flujo del programa
|   |── ServiciosAuxiliares.py          # Gestión de operaciones y servicios de pista
|   └── TorreDeControl.py               # Es el núcleo de la simulación. Controla el flujo de eventos y asignación de recursos
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

