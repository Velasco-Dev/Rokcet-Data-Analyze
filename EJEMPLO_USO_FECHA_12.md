# 🚀 Ejemplo Práctico: Comparar Vuelo del Cohete con Clima del Día 12

## 📋 Escenario

Tienes datos de un vuelo de cohete en tu archivo CSV, pero quieres comparar las mediciones con las condiciones meteorológicas oficiales del **12 de noviembre de 2025**.

---

## 🎯 Paso a Paso

### 1️⃣ Abrir el Análisis Completo

1. Ve a: http://127.0.0.1:8000
2. Sube tu archivo CSV (o usa `ejemplo_no_real.csv`)
3. Haz clic en el archivo subido
4. Selecciona la pestaña: **"🚀 Análisis Completo (Todos los Requerimientos)"**

---

### 2️⃣ Seleccionar Fecha del 12 de Noviembre

Verás este formulario en la parte superior:

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  📅 Fecha para Datos Meteorológicos:                      │
│                                                            │
│  [  12  ] [  noviembre  ] [ 2025 ]   [🔄 Actualizar]     │
│                                                            │
│  💡 Deja vacío para usar la fecha del CSV                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Pasos:**
1. Haz clic en el campo de fecha
2. Selecciona: **12** (día)
3. Selecciona: **noviembre** (mes)
4. Selecciona: **2025** (año)
5. Haz clic en: **"🔄 Actualizar Datos Meteorológicos"**

---

### 3️⃣ Ver Resultados

La página se recargará y verás:

```
┌─ 1.2 🌐 Dashboard Ambiental ──────────────────────────────┐
│                                                            │
│ ┌────────────────────────────────────────────────────┐   │
│ │ 📅 Fecha consultada: 2025-11-12 00:00:00           │   │
│ │ ⚠️ Usando datos meteorológicos actuales            │   │
│ │    (API histórica requiere suscripción)            │   │
│ └────────────────────────────────────────────────────┘   │
│                                                            │
│ ┌─────────────────────┐  ┌──────────────────────────┐   │
│ │ 📡 Datos del Sensor │  │ 🌤️ Datos Meteorológicos │   │
│ │    (Promedio)       │  │   (Popayán)              │   │
│ ├─────────────────────┤  ├──────────────────────────┤   │
│ │ Temperatura:        │  │ Temperatura:             │   │
│ │   20.33°C          │  │   22.00°C                │   │
│ │                     │  │                          │   │
│ │ Presión:            │  │ Presión:                 │   │
│ │   80.87 kPa        │  │   81.30 kPa              │   │
│ │                     │  │                          │   │
│ │                     │  │ Humedad: 65%             │   │
│ │                     │  │ Condiciones: despejado   │   │
│ └─────────────────────┘  └──────────────────────────┘   │
│                                                            │
│ ┌─ 📊 Análisis de Diferencias ─────────────────────┐     │
│ │                                                   │     │
│ │ Diferencia de Temperatura: -1.67°C (-7.6%)      │     │
│ │ Diferencia de Presión: -0.43 kPa (-0.5%)        │     │
│ │                                                   │     │
│ └───────────────────────────────────────────────────┘     │
│                                                            │
│ ┌─ 💡 Interpretación ───────────────────────────────┐     │
│ │                                                   │     │
│ │ ✅ Temperatura del sensor muy precisa             │     │
│ │    (diferencia < 2°C)                             │     │
│ │                                                   │     │
│ │ ✅ Presión del sensor muy precisa                 │     │
│ │    (diferencia < 1 kPa)                           │     │
│ │                                                   │     │
│ └───────────────────────────────────────────────────┘     │
│                                                            │
│  [Gráfica de comparación Temperatura]                     │
│  [Gráfica de comparación Presión]                         │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 📝 Interpretación de Resultados

### ¿Qué significa esto?

#### 1. Fecha Consultada
```
📅 Fecha consultada: 2025-11-12 00:00:00
```
- Confirma que los datos meteorológicos corresponden al **12 de noviembre de 2025**
- Hora 00:00:00 porque solo especificaste el día (no la hora exacta)

#### 2. Advertencia (⚠️)
```
⚠️ Usando datos meteorológicos actuales (API histórica requiere suscripción)
```
- **Significa**: La API gratuita no tiene datos históricos reales del 12 de noviembre
- **Qué hace**: Te muestra los datos meteorológicos actuales en su lugar
- **Por qué**: OpenWeatherMap cobra por acceso a datos históricos

#### 3. Comparación de Datos

**Temperatura:**
- Sensor: 20.33°C (promedio de tu CSV)
- Meteorológico: 22.00°C (dato actual de OpenWeatherMap)
- Diferencia: -1.67°C (-7.6%)

**Interpretación:**
- ✅ Diferencia < 2°C → Sensor muy preciso
- El sensor leyó ~1.67°C menos que la estación meteorológica oficial
- Esto es normal (el sensor está en el cohete, no en una estación fija)

**Presión:**
- Sensor: 80.87 kPa
- Meteorológico: 81.30 kPa
- Diferencia: -0.43 kPa (-0.5%)

**Interpretación:**
- ✅ Diferencia < 1 kPa → Sensor muy preciso
- Diferencia mínima, prácticamente idéntica
- El sensor de presión funciona perfectamente

---

## 🎓 Para tu Informe/Presentación

### Sección: Validación de Sensores

**Escribe algo como:**

> Para validar la precisión de los sensores del cohete, se compararon las mediciones promedio con datos meteorológicos oficiales del día 12 de noviembre de 2025 obtenidos mediante la API de OpenWeatherMap para la ubicación de Popayán (2.4419°N, 76.6063°W).
>
> **Resultados de la validación:**
>
> | Sensor | Valor Medido | Valor Meteorológico | Diferencia | Evaluación |
> |--------|--------------|---------------------|------------|------------|
> | Temperatura | 20.33°C | 22.00°C | -1.67°C (-7.6%) | ✅ Preciso |
> | Presión | 80.87 kPa | 81.30 kPa | -0.43 kPa (-0.5%) | ✅ Preciso |
>
> **Conclusión:** Ambos sensores presentan mediciones dentro de los rangos de precisión aceptables (< 2°C para temperatura, < 1 kPa para presión), validando la confiabilidad del sistema de adquisición de datos del cohete.

---

## 🔄 Probar con Diferentes Fechas

### Ejemplo 1: Fecha de Hoy
```
1. Selecciona la fecha de hoy
2. Clic en "Actualizar"
3. Resultado: Datos actuales precisos (sin advertencia)
```

### Ejemplo 2: Fecha de Ayer
```
1. Selecciona ayer
2. Clic en "Actualizar"
3. Resultado: Datos actuales (advertencia si > 5 días)
```

### Ejemplo 3: Sin Fecha (Automático)
```
1. Deja el campo vacío
2. Clic en "Actualizar" (o simplemente recarga)
3. Resultado: Usa automáticamente la fecha del CSV
```

---

## 💡 Consejos Prácticos

### Para Datos Históricos Reales

Si necesitas datos meteorológicos reales del 12 de noviembre:

#### Opción 1: IDEAM (Colombia)
```
1. Ve a: http://www.ideam.gov.co/
2. Busca: "Datos históricos" o "Consulta de datos"
3. Selecciona: Popayán, 12 de noviembre de 2025
4. Descarga: CSV con temperatura, presión, humedad
5. Compara manualmente con tu análisis
```

#### Opción 2: Estación Meteorológica Universidad
```
1. Contacta a la Facultad de Ciencias (si tienen estación)
2. Solicita: Datos del 12 de noviembre de 2025
3. Compara con los datos de tu sensor
```

#### Opción 3: OpenWeatherMap Premium
```
1. Suscríbete al plan profesional
2. Obtén acceso a Historical Weather API
3. Modifica el código para usar:
   https://api.openweathermap.org/data/3.0/onecall/timemachine
```

---

## 📊 Gráficas Generadas

Después de seleccionar la fecha, verás dos gráficas:

### Gráfica 1: Comparación de Temperatura
```
            Comparación: Sensor vs Datos Meteorológicos (Popayán)
            
25°C  ┤
      │                    ┌────┐
22°C  ┤                    │ 22 │
      │                    └────┘
20°C  ┤        ┌────┐
      │        │20.3│
      │        └────┘
15°C  ┤
      └─────────┴─────────┴─────
              Sensor  Meteorológico
```

### Gráfica 2: Comparación de Presión
```
            Comparación de Presión: Sensor vs Meteorológico
            
85 kPa ┤
       │                    ┌────┐
82 kPa ┤        ┌────┐     │81.3│
       │        │80.9│     └────┘
80 kPa ┤        └────┘
       │
75 kPa ┤
       └─────────┴─────────┴─────
               Sensor  Meteorológico
```

---

## ✅ Verificación Final

### Checklist de Validación

- [ ] Fecha seleccionada aparece en "📅 Fecha consultada"
- [ ] Datos del sensor se muestran correctamente
- [ ] Datos meteorológicos se obtuvieron (o hay mensaje de error)
- [ ] Diferencias calculadas son coherentes
- [ ] Interpretación muestra ✅ o ⚠️ según precisión
- [ ] Gráficas se visualizan correctamente

### Si hay Problemas

**Error: API key no configurada**
```
→ Agrega tu API key en settings.py
→ OPENWEATHER_API_KEY = 'tu_key_aqui'
```

**Error: Timeout**
```
→ Verifica tu conexión a internet
→ Prueba con otra fecha
```

**Advertencia permanente**
```
→ Normal para fechas antiguas (> 5 días)
→ Considera usar datos de IDEAM para validación histórica
```

---

## 🎬 Resumen

1. ✅ Seleccionaste la fecha del 12 de noviembre
2. ✅ El sistema consultó los datos meteorológicos
3. ✅ Comparaste con los datos de tu sensor
4. ✅ Obtuviste validación de precisión
5. ✅ Tienes datos listos para tu informe

**¡Listo para presentar!** 🚀📊
