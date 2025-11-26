# 📅 Guía: Seleccionar Fecha Específica para Datos Meteorológicos

## 🎯 Objetivo

Esta funcionalidad te permite comparar los datos de tu cohete con las condiciones meteorológicas **de un día específico**, por ejemplo, el día 12 de noviembre si tu vuelo fue ese día.

## 🚀 Cómo Usar

### Paso 1: Acceder al Análisis Completo

1. Sube tu archivo CSV con los datos del cohete
2. Haz clic en el archivo subido
3. Selecciona la pestaña **"🚀 Análisis Completo (Todos los Requerimientos)"**

### Paso 2: Seleccionar la Fecha

Una vez en el análisis completo, verás un formulario en la parte superior:

```
📅 Fecha para Datos Meteorológicos: [selector de fecha] 🔄 Actualizar Datos Meteorológicos
💡 Deja vacío para usar la fecha del CSV
```

**Opciones:**

#### Opción A: Usar Fecha del CSV (Por Defecto)
- Si no seleccionas ninguna fecha, el sistema automáticamente usa la fecha del primer registro de tu archivo CSV
- Ejemplo: Si tu CSV tiene datos del 12 de noviembre de 2025, usará esa fecha

#### Opción B: Seleccionar Fecha Específica
1. Haz clic en el campo de fecha
2. Selecciona el día específico (ej: 12 de noviembre de 2025)
3. Haz clic en **"🔄 Actualizar Datos Meteorológicos"**
4. La página se recargará con los datos meteorológicos de ese día

### Paso 3: Verificar los Datos

Después de seleccionar la fecha, verás en la sección **"1.2 🌐 Dashboard Ambiental"**:

```
📅 Fecha consultada: 2025-11-12 14:30:00
```

Esto confirma qué fecha se usó para obtener los datos meteorológicos.

## 🌐 Ejemplo de URL

Puedes también usar la URL directamente:

```
http://127.0.0.1:8000/analyze/file/1/?analysis=complete&weather_date=2025-11-12
```

Donde:
- `analysis=complete` → activa el análisis completo
- `weather_date=2025-11-12` → fecha específica en formato YYYY-MM-DD

## 📊 Qué Verás

Después de seleccionar la fecha, el dashboard mostrará:

### 1. Fecha Consultada
```
📅 Fecha consultada: 2025-11-12 14:30:00
```

### 2. Comparación de Datos

**Sensor vs Meteorológico:**
- Temperatura del sensor vs temperatura meteorológica
- Presión del sensor vs presión meteorológica
- Humedad y condiciones climáticas del día

### 3. Análisis de Diferencias

```
📊 Análisis de Diferencias:
Diferencia de Temperatura: +2.5 °C (12.3%)
Diferencia de Presión: -0.8 kPa (1.2%)
```

### 4. Interpretación Automática

```
💡 Interpretación:
✅ Temperatura del sensor muy precisa (diferencia < 2°C)
✅ Presión del sensor muy precisa (diferencia < 1 kPa)
```

## ⚠️ Notas Importantes

### API Gratuita vs Histórica

**OpenWeatherMap API Gratuita:**
- Solo permite datos **actuales**
- No puede acceder a datos históricos de fechas pasadas

**Si consultas una fecha antigua (> 5 días):**
```
⚠️ Usando datos meteorológicos actuales (API histórica requiere suscripción)
```

**Para datos históricos reales:**
1. Necesitas suscribirte al plan de pago de OpenWeatherMap
2. Incluye acceso a la API de datos históricos
3. Más información: https://openweathermap.org/price

### Solución para Fechas Pasadas

Si necesitas comparar con datos de fechas pasadas sin pagar:

1. **Consulta el día del vuelo**: Si tu vuelo fue hoy o hace pocos días, los datos serán precisos
2. **Usa registros meteorológicos locales**: IDEAM, estaciones meteorológicas de tu universidad
3. **Compara manualmente**: Anota los datos meteorológicos del día y compáralos con el análisis

## 🔧 Configuración Requerida

Asegúrate de tener tu API key configurada en `settings.py`:

```python
# rocketDataAnalyze/settings.py (línea ~130)
OPENWEATHER_API_KEY = 'tu_api_key_aqui'  # Obtener en https://openweathermap.org/api

OPENWEATHER_LOCATION = {
    'lat': 2.4419,   # Popayán
    'lon': -76.6063
}
```

## 📝 Ejemplos de Uso

### Ejemplo 1: Vuelo del 12 de noviembre
```
1. CSV tiene datos del 12/11/2025
2. Deja el campo de fecha vacío
3. Sistema usa automáticamente 12/11/2025
```

### Ejemplo 2: Comparar con fecha específica
```
1. CSV tiene datos del 15/11/2025
2. Quieres comparar con clima del 12/11/2025
3. Selecciona 12/11/2025 en el formulario
4. Haz clic en "Actualizar"
```

### Ejemplo 3: Verificar clima actual
```
1. Selecciona la fecha de hoy
2. Compara con los datos del sensor
3. Verifica precisión en tiempo real
```

## 🎓 Aplicaciones

### Para tu Presentación:
- Muestra que validaste con datos meteorológicos reales
- Demuestra la precisión del sensor comparando con estación meteorológica
- Explica las diferencias entre sensor y clima oficial

### Para el Informe:
- Documenta las condiciones climáticas del día del lanzamiento
- Justifica desviaciones en los datos del sensor
- Valida que el sensor funcionó correctamente

### Para Análisis:
- Identifica si las condiciones climáticas afectaron el vuelo
- Compara múltiples vuelos en diferentes días
- Encuentra el mejor día para lanzar según condiciones

## ❓ Preguntas Frecuentes

**P: ¿Por qué aparece una advertencia de "datos actuales"?**  
R: Tu fecha seleccionada es antigua. La API gratuita solo tiene datos actuales.

**P: ¿Puedo comparar vuelos de hace 1 mes?**  
R: Necesitas la API de pago para datos históricos, o usar datos de IDEAM/estaciones locales.

**P: ¿Qué fecha usa si dejo el campo vacío?**  
R: Usa automáticamente la fecha del primer registro de tu CSV.

**P: ¿Puedo cambiar la ubicación (coordenadas)?**  
R: Sí, edita `OPENWEATHER_LOCATION` en `settings.py`.

## 📞 Soporte

Si tienes problemas:
1. Verifica que tu API key esté configurada
2. Revisa que la fecha esté en formato YYYY-MM-DD
3. Comprueba tu conexión a internet
4. Consulta los logs del servidor Django

---

**¡Listo!** Ahora puedes comparar tus datos del cohete con las condiciones meteorológicas exactas del día que quieras. 🚀🌤️
