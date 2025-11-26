# ⚡ GUÍA RÁPIDA DE USO

## 🚀 Inicio Rápido (3 pasos)

### 1. Activar y Ejecutar
```powershell
cd C:\Users\marti\Documents\U\fisica\Rokcet-Data-Analyze
.\rocketDataEnv\Scripts\Activate.ps1
cd rocketDataAnalyze
python manage.py runserver
```

### 2. Abrir Navegador
```
http://127.0.0.1:8000
```

### 3. Usar la Aplicación
1. Click en "Subir Archivo"
2. Selecciona tu CSV
3. Click en "Análisis Completo"
4. ¡Explora todos los análisis!

---

## 📊 Qué Hace Cada Análisis

### Requerimiento 1: Validación
- **1.1** ✅ Compara altura real vs teórica
- **1.3** ✅ Verifica consistencia del sensor

### Requerimiento 2: Diagnóstico
- **2.1** ✅ Identifica ascenso, apogeo, descenso
- **2.2** ✅ Detecta despliegue del paracaídas
- **2.3** ✅ Calcula densidad del aire
- **2.4** ✅ Encuentra anomalías

### Requerimiento 3: Optimización
- **3.1** ✅ Identifica mejores condiciones de lanzamiento

---

## 📁 Archivos Importantes

- **Código principal:** `rocketDataAnalyze/analyze/utils.py`
- **Documentación técnica:** `REQUERIMIENTOS_DOCUMENTACION.md`
- **Para presentación:** `PRESENTACION_DIAPOSITIVAS.md`
- **Resumen completo:** `RESUMEN_IMPLEMENTACION.md`

---

## 🎯 Para Crear tu Presentación

1. Abre `PRESENTACION_DIAPOSITIVAS.md`
2. Copia el contenido de cada diapositiva
3. Pégalo en PowerPoint/Miro/Draw.io
4. Agrega las gráficas exportadas de la app

---

## ⚠️ Solución Rápida de Problemas

**El servidor no inicia:**
```powershell
.\rocketDataEnv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
```

**Error con scipy:**
```powershell
pip install scipy
```

**No se ven las gráficas:**
- Refresca la página (Ctrl + F5)
- Verifica que hiciste click en "Análisis Completo"

---

## 📞 Ayuda Adicional

Lee estos archivos en orden:
1. `README.md` - Instalación completa
2. `RESUMEN_IMPLEMENTACION.md` - Todo lo implementado
3. `REQUERIMIENTOS_DOCUMENTACION.md` - Detalles técnicos
4. `PRESENTACION_DIAPOSITIVAS.md` - Para tu presentación

---

**¡Listo para usar! 🎉**
