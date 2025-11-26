# 🎨 Capturas de Pantalla: Selector de Fecha Meteorológica

## Vista del Formulario de Fecha

Cuando estés en el **Análisis Completo**, verás esto en la parte superior:

```
┌────────────────────────────────────────────────────────────────┐
│ 📅 Fecha para Datos Meteorológicos:  [12/11/2025]  [🔄 Actualizar] │
│ 💡 Deja vacío para usar la fecha del CSV                        │
└────────────────────────────────────────────────────────────────┘
```

## Flujo Visual

### 1️⃣ Estado Inicial (Sin Fecha Seleccionada)

```
URL: http://127.0.0.1:8000/analyze/file/1/?analysis=complete

┌─────────────────────────────────────────────┐
│  📈 Análisis Básico                         │
│  🚀 Análisis Completo (Todos los Req.) ✓   │
└─────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ 📅 Fecha para Datos Meteorológicos: [___________]   │
│     💡 Deja vacío para usar la fecha del CSV        │
└──────────────────────────────────────────────────────┘

┌─ 1.2 🌐 Dashboard Ambiental ─────────────────┐
│                                               │
│ 📅 Fecha consultada: 2025-11-26 14:30:00     │  ← Fecha del CSV
│                                               │
│ ┌─────────────────┐  ┌──────────────────┐   │
│ │ 📡 Datos Sensor │  │ 🌤️ Meteorológico │   │
│ │ Temp: 20.33°C   │  │ Temp: 22.00°C    │   │
│ │ Pres: 80.87 kPa │  │ Pres: 81.30 kPa  │   │
│ └─────────────────┘  └──────────────────┘   │
└───────────────────────────────────────────────┘
```

### 2️⃣ Después de Seleccionar Fecha Específica

```
Usuario selecciona: 12 de noviembre de 2025
↓
Clic en "🔄 Actualizar Datos Meteorológicos"
↓
URL: http://127.0.0.1:8000/analyze/file/1/?analysis=complete&weather_date=2025-11-12

┌─────────────────────────────────────────────┐
│  📈 Análisis Básico                         │
│  🚀 Análisis Completo (Todos los Req.) ✓   │
└─────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ 📅 Fecha para Datos Meteorológicos: [12/11/2025] ✓  │
│     💡 Deja vacío para usar la fecha del CSV        │
└──────────────────────────────────────────────────────┘

┌─ 1.2 🌐 Dashboard Ambiental ─────────────────┐
│                                               │
│ 📅 Fecha consultada: 2025-11-12 00:00:00     │  ← Fecha seleccionada
│ ⚠️ Usando datos actuales (API histórica...)  │  ← Advertencia
│                                               │
│ ┌─────────────────┐  ┌──────────────────┐   │
│ │ 📡 Datos Sensor │  │ 🌤️ Meteorológico │   │
│ │ Temp: 20.33°C   │  │ Temp: 19.50°C    │   │
│ │ Pres: 80.87 kPa │  │ Pres: 81.10 kPa  │   │
│ └─────────────────┘  └──────────────────┘   │
└───────────────────────────────────────────────┘
```

## Ejemplos de URL

### Sin Fecha (Usa CSV)
```
http://127.0.0.1:8000/analyze/file/1/?analysis=complete
```

### Con Fecha Específica
```
http://127.0.0.1:8000/analyze/file/1/?analysis=complete&weather_date=2025-11-12
```

### Múltiples Parámetros
```
http://127.0.0.1:8000/analyze/file/1/?analysis=complete&weather_date=2025-11-12
                                         └── tipo      └── fecha YYYY-MM-DD
```

## Elementos del Formulario HTML

```html
<form method="get">
  <input type="hidden" name="analysis" value="complete">
  
  <label for="weather_date">📅 Fecha para Datos Meteorológicos:</label>
  <input type="date" 
         name="weather_date" 
         value="2025-11-12"
         max="2025-11-26">  <!-- No permite fechas futuras -->
  
  <button type="submit">🔄 Actualizar Datos Meteorológicos</button>
  
  <small>💡 Deja vacío para usar la fecha del CSV</small>
</form>
```

## Respuesta del Sistema

### Cuando Fecha < 5 días (Datos Actuales)
```json
{
  "query_date": "2025-11-22 14:30:00",
  "is_historical": false,
  "warning": null,
  "external_data": {
    "temperatura_externa": 22.0,
    "presion_externa": 81.3,
    ...
  }
}
```

### Cuando Fecha > 5 días (Requiere API Histórica)
```json
{
  "query_date": "2025-10-12 00:00:00",
  "is_historical": true,
  "warning": "Usando datos meteorológicos actuales (API histórica requiere suscripción)",
  "external_data": {
    "temperatura_externa": 22.0,  // ← Datos actuales, no históricos
    "presion_externa": 81.3,
    ...
  }
}
```

## Comparación Visual Antes/Después

### ANTES (Sin selector de fecha)
```
❌ No podías elegir la fecha
❌ Siempre usaba la fecha del CSV
❌ No sabías qué fecha se consultó
```

### DESPUÉS (Con selector de fecha)
```
✅ Puedes elegir cualquier fecha
✅ Puedes comparar con diferentes días
✅ Ves claramente qué fecha se consultó
✅ Advertencia si la fecha requiere API de pago
```

## Casos de Uso Prácticos

### Caso 1: Vuelo de Ayer
```
1. CSV del 25/11/2025
2. Selector: [dejar vacío]
3. Resultado: Usa 25/11/2025 ✓
```

### Caso 2: Comparar con Día Específico
```
1. CSV del 25/11/2025
2. Selector: [12/11/2025]
3. Resultado: Consulta 12/11/2025
4. Advertencia: "Datos actuales (no históricos)"
```

### Caso 3: Verificar Condiciones de Hoy
```
1. CSV del 12/11/2025 (hace 2 semanas)
2. Selector: [26/11/2025] (hoy)
3. Resultado: Datos actuales precisos ✓
```

## Indicadores Visuales

### ✅ Éxito
```
┌────────────────────────────────────┐
│ 📅 Fecha consultada: 2025-11-26   │
│ ✅ Temperatura precisa (< 2°C)     │
│ ✅ Presión precisa (< 1 kPa)       │
└────────────────────────────────────┘
```

### ⚠️ Advertencia
```
┌────────────────────────────────────────────┐
│ 📅 Fecha consultada: 2025-10-12           │
│ ⚠️ Usando datos actuales (no históricos)  │
│ ⚠️ Diferencia significativa detectada     │
└────────────────────────────────────────────┘
```

### ❌ Error
```
┌────────────────────────────────────┐
│ ❌ Error al obtener datos          │
│ 💡 Verifica tu API key             │
│ 💡 Revisa tu conexión a internet   │
└────────────────────────────────────┘
```

## Flujo de Datos

```
Usuario → [Selector de Fecha] → Django View → utils.py
                    ↓
              weather_date='2025-11-12'
                    ↓
        environmental_dashboard(target_date='2025-11-12')
                    ↓
        OpenWeatherMap API (con fecha específica)
                    ↓
             [Datos Meteorológicos]
                    ↓
        Template HTML con fecha consultada
                    ↓
              Navegador del Usuario
```

---

**¡Ahora tienes control total sobre qué fecha usar para la comparación meteorológica!** 🎯
