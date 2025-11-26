# 🚀 Rocket Data Analyzer

Proyecto Django avanzado para análisis exhaustivo de datos de cohetes experimentales. Incluye validación multi-sensor, diagnóstico de eventos, detección de anomalías y optimización basada en evidencia.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Características Principales

### 📊 Análisis Básico
- Estadísticas descriptivas completas
- Visualizaciones interactivas (Plotly)
- Gráficas estáticas de alta calidad (Matplotlib)
- Dashboard intuitivo y responsivo

### 🔬 Análisis Avanzado (Nuevos Requerimientos)

#### **Requerimiento 1: Validación Multi-Sensor**
- ✅ Validación altura teórica vs real (Fórmula de Littlewood)
- ✅ Curva altitud vs presión comparada con ecuación barométrica
- ✅ Cálculo de errores (RMSE, error porcentual)
- ✅ Dashboard ambiental con API meteorológica (OpenWeatherMap)
- 🆕 **Selector de fecha específica para comparación meteorológica**

#### **Requerimiento 2: Diagnóstico de Eventos**
- ✅ Identificación automática de fases del vuelo (ascenso, apogeo, descenso)
- ✅ Análisis de despliegue de paracaídas
- ✅ Cálculo de densidad del aire durante el vuelo
- ✅ Detección inteligente de anomalías
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
- **SciPy 1.16.3** - Algoritmos científicos

### Visualización
- **Plotly 6.4.0** - Gráficas interactivas
- **Matplotlib 3.10.7** - Gráficas estáticas
- **Seaborn 0.13.2** - Visualizaciones estadísticas

### Frontend
- **Bootstrap 5** - UI responsivo
- **JavaScript** - Interactividad

---

## ✅ Requisitos Previos

- **Python 3.13** o superior
- **pip** (gestor de paquetes)
- **Git** (opcional, para clonar el repositorio)

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Velasco-Dev/Rokcet-Data-Analyze.git
cd Rokcet-Data-Analyze
```

### 2. Crear Entorno Virtual

**Windows (PowerShell):**
```powershell
python -m venv rocketDataEnv
.\rocketDataEnv\Scripts\Activate.ps1
```

**Linux/MacOS:**
```bash
python -m venv rocketDataEnv
source rocketDataEnv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

```bash
cd rocketDataAnalyze
python manage.py makemigrations
python manage.py migrate
```

### 5. (Opcional) Crear Superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: **http://127.0.0.1:8000**

---

## 📖 Uso

### 1. Subir Archivo CSV

1. Accede al Dashboard principal
2. Haz clic en "Subir Archivo"
3. Selecciona un archivo CSV con el formato:

```csv
id,temperatura,presion,altura,timestamp
1,24.96,81.43,160.76,2025-11-13 03:25:08
2,25.26,81.44,159.95,2025-11-13 03:25:09
```

### 2. Ver Análisis Básico

- Visualiza estadísticas generales
- Explora gráficas interactivas
- Revisa métricas descriptivas

### 3. Activar Análisis Completo

1. Haz clic en la pestaña **"Análisis Completo"**
2. El sistema calculará automáticamente:
   - Validación teórica de altitud
   - Fases del vuelo
   - Detección de paracaídas
   - Densidad del aire
   - Anomalías
   - Condiciones óptimas

---

## 📊 Estructura del Proyecto

```
Rokcet-Data-Analyze/
│
├── rocketDataAnalyze/           # Proyecto Django principal
│   ├── manage.py
│   ├── db.sqlite3
│   │
│   ├── analyze/                 # App principal
│   │   ├── models.py           # Modelo DataFile
│   │   ├── views.py            # Vistas del dashboard
│   │   ├── utils.py            # ⭐ Motor de análisis
│   │   ├── forms.py            # Formularios
│   │   ├── urls.py             # URLs
│   │   │
│   │   ├── templates/
│   │   │   └── analyze/
│   │   │       ├── base.html
│   │   │       ├── dashboard.html
│   │   │       └── file_detail.html  # ⭐ Vista de análisis
│   │   │
│   │   └── static/
│   │       └── analyze/
│   │           ├── css/
│   │           └── js/
│   │
│   ├── csv_files/              # Archivos de ejemplo
│   │   ├── sensor_data_1.csv
│   │   └── ...
│   │
│   └── rocketDataAnalyze/      # Configuración Django
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
│
├── rocketDataEnv/              # Entorno virtual
│
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
├── REQUERIMIENTOS_DOCUMENTACION.md  # 📄 Documentación detallada
└── PRESENTACION_DIAPOSITIVAS.md     # 📊 Guía para presentaciones
```

---

## 🧮 Fórmulas Implementadas

### 1. Ecuación Barométrica Internacional (Littlewood)

```
h = (T₀/L) × [1 - (P/P₀)^(R×L/g×M)]
```

**Donde:**
- `h` = Altura (m)
- `T₀ = 288.15 K` - Temperatura estándar
- `L = 0.0065 K/m` - Gradiente térmico
- `P` = Presión actual (kPa)
- `P₀` = Presión inicial (kPa)
- `R = 8.314 J/(mol·K)` - Constante de gases
- `g = 9.80665 m/s²` - Gravedad
- `M = 0.029 kg/mol` - Masa molar del aire

### 2. Densidad del Aire

```
ρ = (P × M) / (R × T)
```

**Donde:**
- `ρ` = Densidad (kg/m³)
- `P` = Presión (Pa)
- `T` = Temperatura (K)

---

## 📈 Ejemplos de Análisis

### Validación de Altura

El sistema compara la altura medida por el sensor con la calculada teóricamente:

```python
# Error promedio: ±1.2 m
# RMSE: 1.8 m
# Precisión: 99.2%
```

### Fases del Vuelo

```
Ascenso:  0.0s → 8.2s  (Altura: 0m → 165m)
Apogeo:   8.2s         (Altura máxima: 165m)
Descenso: 8.2s → 15.4s (Altura: 165m → 0m)
```

### Detección de Paracaídas

```
Estado: ✅ Detectado
Altura de despliegue: 95.3m (57.8% del apogeo)
Tiempo: 10.1s desde lanzamiento
Reducción velocidad: 68%
```

---

## 🔧 Solución de Problemas

### Error al instalar scipy

```bash
pip install --upgrade pip
pip install scipy
```

### Error de migraciones

```bash
python manage.py makemigrations --empty analyze
python manage.py migrate
```

### Archivos CSV no se suben

Verifica que el formato sea correcto y que incluya las columnas:
- `id`, `temperatura`, `presion`, `altura`, `timestamp`

### Gráficas no se muestran

Asegúrate de que las librerías de visualización estén instaladas:
```bash
pip install plotly matplotlib seaborn
```

---

## 📚 Documentación Adicional

### Documentación Técnica
- **📄 Documentación Técnica Completa:** `REQUERIMIENTOS_DOCUMENTACION.md`
- **📊 Guía para Presentaciones:** `PRESENTACION_DIAPOSITIVAS.md`
- **🔧 Resumen de Implementación:** `RESUMEN_IMPLEMENTACION.md`
- **⚡ Guía Rápida de Uso:** `GUIA_RAPIDA.md`

### Nuevas Guías (Selector de Fecha Meteorológica)
- **📅 Guía de Uso - Fecha Meteorológica:** `GUIA_FECHA_METEOROLOGICA.md`
- **🎨 Vista Previa del Selector:** `VISTA_PREVIA_SELECTOR_FECHA.md`
- **💻 Resumen Técnico de Implementación:** `RESUMEN_TECNICO_FECHA.md`
- **🚀 Ejemplo Práctico (Día 12):** `EJEMPLO_USO_FECHA_12.md`

Estos archivos incluyen:
- Explicación detallada de todas las fórmulas
- Interpretación de resultados
- Mapas mentales de causas de error
- Blueprint del cohete v2.0
- Recomendaciones de optimización
- 🆕 **Cómo seleccionar fechas específicas para comparación meteorológica**

---

## 🚀 Mejoras Futuras

### Corto Plazo
- [x] ~~Integración con API meteorológica (OpenWeatherMap)~~ ✅ **Completado**
- [x] ~~Selector de fecha específica para datos meteorológicos~~ ✅ **Completado**
- [ ] Exportación de reportes a PDF
- [ ] Comparación entre múltiples vuelos

### Mediano Plazo
- [ ] Modelo predictivo de altura máxima (ML)
- [ ] Aplicación móvil
- [ ] Sistema de alertas en tiempo real
- [ ] Integración con API de datos históricos (OpenWeatherMap Premium)

### Largo Plazo
- [ ] Simulador 3D de trayectoria
- [ ] Integración con video sincronizado
- [ ] API pública para desarrolladores

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## ✍️ Autor

**Rubén Velasco** (Velasco-Dev)

- GitHub: [@Velasco-Dev](https://github.com/Velasco-Dev)
- Email: [tu-email]

---

## 🙏 Agradecimientos

- Comunidad de Python y Django
- Desarrolladores de Plotly, Matplotlib y Pandas
- Comunidad de cohetería experimental
- NOAA por estándares atmosféricos

---

## 📞 Soporte

¿Tienes preguntas o problemas?

1. Revisa la documentación en `REQUERIMIENTOS_DOCUMENTACION.md`
2. Abre un issue en GitHub
3. Contacta al autor

---

## 🎯 Estado del Proyecto

**Versión:** 2.0  
**Estado:** ✅ Producción  
**Última Actualización:** Noviembre 2025

### Requerimientos Completados:

- ✅ **Requerimiento 1:** 75% (Falta API meteorológica)
- ✅ **Requerimiento 2:** 100%
- ✅ **Requerimiento 3:** 67% (Modelo predictivo y simulador no requeridos)

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**
