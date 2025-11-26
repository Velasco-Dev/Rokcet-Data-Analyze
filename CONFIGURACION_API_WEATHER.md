# 🌐 GUÍA: Configuración del Dashboard Ambiental (OpenWeatherMap API)

## ¿Dónde agregar la API Key?

### 📍 Ubicación: `rocketDataAnalyze/rocketDataAnalyze/settings.py`

**Líneas 127-136** (al final del archivo):

```python
# ===== CONFIGURACIÓN DE API EXTERNA =====
# API Key para OpenWeatherMap (para Dashboard Ambiental - Requerimiento 1.2)
# Obtén tu API key gratis en: https://openweathermap.org/api
OPENWEATHER_API_KEY = 'TU_API_KEY_AQUI'  # ← REEMPLAZA AQUÍ

# Coordenadas por defecto (puedes cambiarlas según tu ubicación)
DEFAULT_LATITUDE = 40.4168  # Madrid, España (ejemplo)
DEFAULT_LONGITUDE = -3.7038
```

---

## 🚀 Pasos para Activar el Dashboard Ambiental

### Paso 1: Obtener API Key Gratuita

1. Ve a **https://openweathermap.org/api**
2. Haz click en "Sign Up" (Registrarse)
3. Crea una cuenta gratuita
4. Ve a tu perfil → "API keys"
5. Copia tu API key (algo como: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

**Nota:** La activación puede tardar unos minutos después de registrarte.

---

### Paso 2: Configurar la API Key

**Opción A: Directamente en settings.py** (Para desarrollo/pruebas)

```python
# En settings.py línea 130
OPENWEATHER_API_KEY = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'  # Tu key aquí
```

**Opción B: Usando Variables de Entorno** (Recomendado para producción)

1. Crea un archivo `.env` en la raíz del proyecto:
```bash
OPENWEATHER_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

2. Instala python-decouple:
```bash
pip install python-decouple
```

3. Modifica settings.py:
```python
from decouple import config

OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY', default='TU_API_KEY_AQUI')
```

---

### Paso 3: Configurar Coordenadas (Opcional)

Si quieres usar tu ubicación específica, cambia las coordenadas:

```python
# Ejemplo: Ciudad de México
DEFAULT_LATITUDE = 19.4326
DEFAULT_LONGITUDE = -99.1332

# Ejemplo: Buenos Aires
DEFAULT_LATITUDE = -34.6037
DEFAULT_LONGITUDE = -58.3816

# Ejemplo: Barcelona
DEFAULT_LATITUDE = 41.3851
DEFAULT_LONGITUDE = 2.1734
```

**¿Cómo encontrar tus coordenadas?**
- Ve a Google Maps
- Haz click derecho en tu ubicación
- Aparecerán las coordenadas (latitud, longitud)

---

### Paso 4: Reiniciar el Servidor

Después de configurar la API key:

```powershell
# Detén el servidor (Ctrl + C)
# Reinicia:
cd rocketDataAnalyze
python manage.py runserver
```

---

### Paso 5: Verificar que Funciona

1. Abre http://127.0.0.1:8000
2. Sube un archivo CSV
3. Click en "Análisis Completo"
4. Ve a la sección **"1.2 Dashboard Ambiental"**

**Si está configurado correctamente verás:**
- ✅ Datos del sensor
- ✅ Datos meteorológicos de tu ubicación
- ✅ Comparación entre ambos
- ✅ Gráficas comparativas

**Si NO está configurado verás:**
- ⚠️ Mensaje: "API key no configurada"
- 📝 Instrucciones para activar

---

## 🎯 ¿Qué hace el Dashboard Ambiental?

### Comparaciones que realiza:

1. **Temperatura**
   - Sensor vs Datos meteorológicos
   - Diferencia absoluta y porcentual
   - Evaluación de precisión

2. **Presión Atmosférica**
   - Sensor vs Estación meteorológica
   - Análisis de desviaciones
   - Verificación de calibración

3. **Condiciones Ambientales**
   - Clima durante el vuelo
   - Humedad
   - Descripción del tiempo

---

## 📊 Interpretación de Resultados

### Temperatura:
- **✅ Diferencia < 2°C:** Sensor muy preciso
- **⚠️ Diferencia 2-5°C:** Precisión aceptable
- **❌ Diferencia > 5°C:** Posible problema de calibración

### Presión:
- **✅ Diferencia < 1 kPa:** Sensor muy preciso
- **⚠️ Diferencia 1-2 kPa:** Precisión aceptable
- **❌ Diferencia > 2 kPa:** Posible problema de calibración

---

## 🔒 Seguridad

### ⚠️ NUNCA subas tu API key a GitHub

**Si usas Git, agrega al `.gitignore`:**

```bash
# .gitignore
.env
**/settings_local.py
```

**Alternativa:** Usa settings_local.py

1. Crea `rocketDataAnalyze/rocketDataAnalyze/settings_local.py`:
```python
OPENWEATHER_API_KEY = 'tu_key_secreta_aqui'
```

2. En `settings.py` al final:
```python
try:
    from .settings_local import *
except ImportError:
    pass
```

3. Agrega `settings_local.py` al `.gitignore`

---

## 📈 Plan Gratuito de OpenWeatherMap

**Límites del plan gratuito:**
- ✅ 1,000 llamadas por día
- ✅ 60 llamadas por minuto
- ✅ Datos actuales del tiempo
- ❌ Sin datos históricos precisos

**Para este proyecto es más que suficiente** 👍

---

## 🐛 Solución de Problemas

### Error: "API key no válida"
```
Solución: Espera 10-15 minutos después del registro
La activación de la API key puede tardar un poco
```

### Error: "ModuleNotFoundError: No module named 'requests'"
```bash
pip install requests
```

### Error: "Timeout al conectar"
```
Solución: Verifica tu conexión a internet
Intenta nuevamente en unos minutos
```

### No aparece la sección 1.2
```
Solución: 
1. Verifica que hiciste click en "Análisis Completo"
2. Recarga la página (Ctrl + F5)
3. Revisa la consola del servidor por errores
```

---

## ✅ Checklist de Configuración

- [ ] Cuenta creada en OpenWeatherMap
- [ ] API key obtenida
- [ ] API key agregada en `settings.py`
- [ ] Coordenadas configuradas (opcional)
- [ ] `requests` instalado (`pip install requests`)
- [ ] Servidor reiniciado
- [ ] Dashboard funciona (prueba con un CSV)

---

## 📚 Documentación Adicional

**OpenWeatherMap API Docs:**
- https://openweathermap.org/api

**API Endpoint usado:**
```
https://api.openweathermap.org/data/2.5/weather
```

**Parámetros:**
- `lat`: Latitud
- `lon`: Longitud
- `appid`: Tu API key
- `units=metric`: Unidades métricas (°C, m/s)

---

## 🎉 ¡Listo!

Una vez configurado, el Dashboard Ambiental comparará automáticamente tus datos del sensor con información meteorológica real, validando la precisión de tus mediciones.

**Esto completa el Requerimiento 1.2 al 100%** ✅
