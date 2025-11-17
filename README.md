# Rokcet-Data-Analyze

Proyecto Django para analizar datos de sensores (temperatura, presión, altura) desde CSVs y generar visualizaciones interactivas y estáticas.

---

## ✅ Requisitos previos

- Tener instalado **Python**  
  👉 Recomendado: última versión estable desde [python.org](https://www.python.org/)

---

## Instalación (Windows)

1. Clonar el repositorio y situarse en la raíz del proyecto:
   git clone <repo-url>
   cd Rokcet-Data-Analyze

2. Crear y activar un entorno virtual (PowerShell):

   - Creamos el entorno virtual para aislar las dependencias del proyecto.
      ```bash
      python -m venv rocketDataEnv
      ```

   - Activamos el entorno virtual según el sistema operativo:
     - **Windows:** `menuEnv\Scripts\activate`
     - **Linux/MacOS:** `source menuEnv/bin/activate`

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Aplicar migraciones:

   ```bash
   python manage.py make migrations
   python manage.py migrate
   ```

5. (Opcional) Crear superusuario:

   ```bash
   python manage.py createsuperuser
   ```

### ▶️ Para ejecutar la app:

Finalmente tenemos el proyecto creado y ejecutamos el servidor de desarrollo:

```bash
python manage.py runserver
```

El servidor estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Uso

- Subir archivos CSV desde la interfaz para generar análisis y visualizaciones.
- Las gráficas interactivas usan Plotly; las imágenes estáticas usan Matplotlib/Seaborn.

## Archivos relevantes

- `requirements.txt` — dependencias del proyecto
- `manage.py` — comandos Django (en la raíz)
- `<project_folder>/settings.py` — configuración Django (zona horaria, MEDIA_URL, etc.)
- `analyze/` — app de análisis (modelos, vistas, templates, utils)
- `csv_files/` — ejemplos de CSV (si están incluidos)

---

## Solución de problemas

- Errores al instalar dependencias: asegurarse de usar la versión de Python recomendada y ejecutar pip dentro del entorno virtual.
- Errores de migraciones: eliminar archivos .pyc y volver a ejecutar `python manage.py migrate`.
- Problemas con timestamps: revisar la columna de tiempo en los CSV y la configuración de zona horaria en settings.py.
- Archivos estáticos/media no sirven en desarrollo: comprobar `MEDIA_URL`, `MEDIA_ROOT` y las rutas en `urls.py`.

## Notas

- Ejecutar comandos desde la carpeta raíz donde está `manage.py`.
- Ajustar permisos y rutas de guardado si se usa en producción.

---

## ✍️ Autor

- Creado por Rubén Velasco (Velasco-Dev)
- 📅 Fecha de creación: 16/11/2025
