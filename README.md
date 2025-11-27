# 🚀 Rocket Data Analyzer

Proyecto Django avanzado para análisis exhaustivo de datos de cohetes experimentales. Incluye **detección automática de vuelo real**, validación multi-sensor, diagnóstico de eventos, detección de anomalías y optimización basada en evidencia.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Características Principales

### 🧠 Detección Inteligente de Datos
- 🆕 **Detección automática de vuelo real vs. sensor en reposo**
- 🆕 **Warnings contextuales para datos de prueba**
- 🆕 **Análisis adaptativo según tipo de datos**
- 🆕 **Indicadores visuales claros (gráficas grises para reposo, coloreadas para vuelo)**

### 📊 Análisis Básico
- Estadísticas descriptivas completas
- Visualizaciones interactivas (Plotly)
- Gráficas estáticas de alta calidad (Matplotlib)
- Dashboard intuitivo y responsivo

### 🔬 Análisis Avanzado (3 Requerimientos Completos)

#### **Requerimiento 1: Validación Multi-Sensor**
- ✅ Validación altura teórica vs real (Fórmula de Littlewood)
- ✅ Curva altitud vs presión comparada con ecuación barométrica
- ✅ Cálculo de errores (RMSE, error porcentual)
- ✅ Dashboard ambiental con API meteorológica (OpenWeatherMap)

#### **Requerimiento 2: Diagnóstico de Eventos**
- ✅ Identificación automática de fases del vuelo (ascenso, apogeo, descenso)
- ✅ Análisis de despliegue de paracaídas con detección de cambio brusco
- ✅ Cálculo de densidad del aire durante el vuelo
- ✅ Detección inteligente de anomalías (distingue ruido de eventos reales)
- 📈 Interpretación de impacto en rendimiento

#### **Requerimiento 3: Optimización**
- ✅ Identificación de condiciones óptimas ("Fórmula del Éxito")
- ✅ Recomendaciones para futuros lanzamientos
- 📐 Blueprint para mejoras del cohete v2.0

---

## 📦 Tecnologías Utilizadas

### Backend
- **Django 5.2.8** - Framework web
- **Pandas 2.3.3** - Análisis de datos
- **NumPy 2.3.4** - Cálculos numéricos
- **SciPy 1.16.3** - Algoritmos científicos (detección de picos)

### Visualización
- **Plotly 6.4.0** - Gráficas interactivas
- **Matplotlib 3.10.7** - Gráficas estáticas
- **Seaborn 0.13.2** - Visualizaciones estadísticas

### Frontend
- **Bootstrap 5** - UI responsivo
- **JavaScript** - Interactividad

### API Externa
- **OpenWeatherMap API** - Datos meteorológicos históricos

---

## ✅ Requisitos Previos

- **Python 3.13** o superior (probado en 3.13)
- **pip** (gestor de paquetes)
- **Git** (opcional, para clonar el repositorio)
- **Clave API de OpenWeatherMap** (opcional, para Req 1.2)

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Velasco-Dev/Rokcet-Data-Analyze.git
cd Rokcet-Data-Analyze
```

### 2. Crear Entorno Virtual

**Windows (PowerShell):**
```bash
python -m venv rocketDataEnv
```

**Activar entorno Virtual:**
```bash
source .\rocketDataEnv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar Servidor

```bash
cd rocketDataAnalyze
python manage.py runserver
```

El servidor estará disponible en: **http://127.0.0.1:8000**

---

## 📖 Uso

### 1. Subir Archivo CSV

1. Accede al Dashboard principal (http://127.0.0.1:8000)
2. Haz clic en **"Subir Archivo"** aunque ya está el archivo de muestra expuesto en clase
3. Selecciona un archivo CSV con el formato estándar:

```csv
id,temperatura,presion,altura,timestamp
1,24.96,81.43,160.76,2025-11-13 03:25:08
2,25.26,81.44,159.95,2025-11-13 03:25:09
3,25.15,81.38,165.23,2025-11-13 03:25:10
```