# Simulador de Vuelo de Cohete de Agua

Proyecto que genera simulaciones realistas de vuelos de cohetes de agua en CSV, a partir de la presión de lanzamiento (PSI), volumen de agua (mL) y estado del paracaídas. Incluye un modelo físico independiente para predecir la altura máxima.

## Requisitos
- Python 3.9+ (probado con 3.13)
- Windows PowerShell 5.1 (comandos a continuación)
- Paquetes: `numpy`, `scipy`

## Instalación
1. Clona o abre la carpeta del proyecto (contiene `flight_simulator.py` y `requirements.txt`).
2. Crea y activa un entorno virtual e instala dependencias:

```powershell
# Desde la raíz del proyecto
python -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

> Nota: Si ya tienes un entorno `.venv` configurado, solo actívalo y omite la instalación.

## Ejecución
Ejecuta el simulador interactivo:
```powershell
& ".\.venv\Scripts\Activate.ps1"
python .\flight_simulator.py
```
Luego responde a las preguntas:
- `PSI`: Presión de lanzamiento (recomendado 47–50).
- `mL`: Volumen de agua (recomendado 480–520).
- Paracaídas (`s/n`): Define si se abre durante el descenso.
- Nombre base del archivo: Prefijo para el CSV generado.

## Qué genera
- Un archivo CSV en la raíz del proyecto con nombre: `NOMBRE_BASE_<PSI>PSI_<mL>mL.csv`.
- Columnas: `id, temperatura, presion, altura, timestamp`.
- Frecuencia de muestreo: 40 Hz (cada registro avanza 25 ms).
- Duración:
  - Con paracaídas: ~8–10 s totales (vuelo 6–8 s).
  - Sin paracaídas: ~6–8 s totales (vuelo ~5 s).

## Modelo de predicción
El script muestra una predicción independiente de la altura máxima basada en energía del aire comprimido y factores empíricos. También compara la altura predicha con la ganancia de altura observada en la simulación.

## Consejos de uso
- Si ingresas valores fuera de los rangos recomendados (PSI 20–80, agua 200–800 mL), el programa avisará, pero seguirá generando la simulación.
- Para reducir ruido en las señales, el simulador usa una tasa de muestreo menor (40 Hz) y niveles de ruido ajustados.

## Problemas comunes
- "No se encuentran paquetes": Asegúrate de activar el entorno virtual antes de ejecutar (`& ".\\.venv\\Scripts\\Activate.ps1"`).
- "Permisos de ejecución": Si PowerShell bloquea scripts, habilita la ejecución local (requiere permisos de administrador):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Estructura
```
/ (raíz)
├─ flight_simulator.py      # Script principal
├─ requirements.txt         # Dependencias
└─ README.md                # Este archivo
```

## Licencia
Uso educativo. Ajusta y reutiliza libremente en tu contexto académico.
