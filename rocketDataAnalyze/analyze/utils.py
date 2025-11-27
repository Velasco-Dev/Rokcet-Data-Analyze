import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI para evitar errores de threading
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import io
import base64
from datetime import datetime
import numpy as np
from scipy.signal import find_peaks
from django.conf import settings
import requests


class RocketDataAnalyzer:
    """
    Analizador de datos del cohete de agua.

    Cobertura de requerimientos:

    REQUERIMIENTO 1 – Análisis Comparativo y Validación Multi-Sensor
      1.1 validate_theoretical_altitude()
      1.2 environmental_dashboard()
      1.3 altitude_pressure_curve()
      (1.4 Mapa mental se hace en presentación, no en código)

    REQUERIMIENTO 2 – Diagnóstico de Eventos y Atmósfera
      2.1 identify_flight_phases()
      2.2 analyze_parachute_deployment()
      2.3 calculate_air_density()
      2.4 detect_anomalies()

    REQUERIMIENTO 3 – Optimización Basada en Evidencia
      3.1 analyze_success_formula()
      3.3 propose_blueprint_v2()
      (3.2 modelo predictivo y 3.4 simulador NO se implementan, por solicitud)
    """

    # Constantes razonables para tu experimento (Popayán)
    ALTURA_POPAYAN_MSNM = getattr(settings, 'CITY_ALTITUDE_MSNM', 1737)  # m
    ALTURA_SENSOR_SUELO = getattr(settings, 'SENSOR_ZERO_ALTITUDE', 163)  # m (offset del sensor)

    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.filename = file_path.split('/')[-1]

        # Altura absoluta sobre el nivel del mar (opcional, útil para explicación)
        # altura_csv se interpreta como "altura relativa respecto al punto de medición"
        self.df['altura_msnm'] = (
            self.df['altura']
            - self.ALTURA_SENSOR_SUELO
            + self.ALTURA_POPAYAN_MSNM
        )

    # ==========================
    # UTILIDADES BÁSICAS / PLOTS
    # ==========================

    def get_basic_stats(self):
        """Retorna estadísticas básicas del dataset"""
        duration_total_seconds = (
            self.df['timestamp'].max() - self.df['timestamp'].min()
        ).total_seconds()
        
        stats = {
            'total_records': len(self.df),
            'time_range': {
                'start': self.df['timestamp'].min(),
                'end': self.df['timestamp'].max()
            },
            'duration_seconds': duration_total_seconds,
            'duration_minutes': duration_total_seconds / 60,
            'temperature_stats': self.df['temperatura'].describe().to_dict(),
            'pressure_stats': self.df['presion'].describe().to_dict(),
            'altitude_stats': self.df['altura'].describe().to_dict(),
            'altitude_msnm_stats': self.df['altura_msnm'].describe().to_dict()
        }
        return stats

    def create_matplotlib_plots(self):
        """Crea gráficas usando matplotlib para visualización rápida"""
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))

        # Temperatura vs Tiempo
        axes[0].plot(self.df['timestamp'], self.df['temperatura'],
                     color='red', linewidth=1)
        axes[0].set_title(f'Temperatura vs Tiempo - {self.filename}')
        axes[0].set_ylabel('Temperatura (°C)')
        axes[0].grid(True, alpha=0.3)

        # Presión vs Tiempo
        axes[1].plot(self.df['timestamp'], self.df['presion'],
                     color='blue', linewidth=1)
        axes[1].set_title(f'Presión vs Tiempo - {self.filename}')
        axes[1].set_ylabel('Presión (kPa)')
        axes[1].grid(True, alpha=0.3)

        # Altura vs Tiempo
        axes[2].plot(self.df['timestamp'], self.df['altura'],
                     color='green', linewidth=1)
        axes[2].set_title(f'Altura vs Tiempo - {self.filename}')
        axes[2].set_ylabel('Altura (m)')
        axes[2].set_xlabel('Tiempo')
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()

        # Convertir a base64 para mostrar en HTML
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode('utf-8')
        plt.close(fig)

        return graphic

    def create_interactive_plots(self):
        """Crea gráficas interactivas usando Plotly"""
        plots = {}

        # Gráfica de temperatura interactiva
        fig_temp = px.line(
            self.df, x='timestamp', y='temperatura',
            title=f'Temperatura vs Tiempo - {self.filename}',
            labels={'temperatura': 'Temperatura (°C)',
                    'timestamp': 'Tiempo'}
        )
        fig_temp.update_traces(line=dict(color='red', width=2))
        plots['temperature'] = plot(fig_temp, output_type='div')

        # Gráfica de presión interactiva
        fig_pressure = px.line(
            self.df, x='timestamp', y='presion',
            title=f'Presión vs Tiempo - {self.filename}',
            labels={'presion': 'Presión (kPa)',
                    'timestamp': 'Tiempo'}
        )
        fig_pressure.update_traces(line=dict(color='blue', width=2))
        plots['pressure'] = plot(fig_pressure, output_type='div')

        # Gráfica de altura interactiva
        fig_altitude = px.line(
            self.df, x='timestamp', y='altura',
            title=f'Altura vs Tiempo - {self.filename}',
            labels={'altura': 'Altura (m)',
                    'timestamp': 'Tiempo'}
        )
        fig_altitude.update_traces(line=dict(color='green', width=2))
        plots['altitude'] = plot(fig_altitude, output_type='div')

        return plots

    def create_combined_plot(self):
        """Crea una gráfica combinada con las tres variables"""
        fig = go.Figure()

        # Agregar las tres series
        fig.add_trace(go.Scatter(
            x=self.df['timestamp'], y=self.df['temperatura'],
            mode='lines', name='Temperatura',
            line=dict(color='red'), yaxis='y1'
        ))

        fig.add_trace(go.Scatter(
            x=self.df['timestamp'], y=self.df['presion'],
            mode='lines', name='Presión',
            line=dict(color='blue'), yaxis='y2'
        ))

        fig.add_trace(go.Scatter(
            x=self.df['timestamp'], y=self.df['altura'],
            mode='lines', name='Altura',
            line=dict(color='green'), yaxis='y3'
        ))

        # Configurar el layout con múltiples ejes Y
        fig.update_layout(
            title=f'Análisis Completo - {self.filename}',
            xaxis=dict(title='Tiempo'),
            yaxis=dict(title='Temperatura (°C)', side='left',
                       color='red', position=0.0),
            yaxis2=dict(title='Presión (kPa)', side='right',
                        color='blue', overlaying='y', position=1.0),
            yaxis3=dict(title='Altura (m)', side='right',
                        color='green', overlaying='y', position=0.9,
                        anchor='free'),
            legend=dict(x=0, y=1.1, orientation='h')
        )

        return plot(fig, output_type='div')

    # =====================================================
    # REQUERIMIENTO 1: ANÁLISIS COMPARATIVO Y VALIDACIÓN
    # =====================================================

    def validate_theoretical_altitude(self, initial_pressure=None, theoretical_height=None, tiempo_vuelo_manual=None):
        """
        Req 1.1 – Análisis de vuelos detectados con métricas individuales
        """
        # Config Littlewood / barométrica
        config = getattr(settings, 'LITTLEWOOD_CONFIG', {
            'T0': 288.15, 'L': 0.0065, 'R': 8.314,
            'g': 9.80665, 'M': 0.029, 'USE_LOCAL_TEMP': False,
            'USE_SIMPLIFIED_FORMULA': False
        })

        threshold = getattr(settings, 'FLIGHT_DETECTION_THRESHOLD', 0.10)
        min_flight_alt = getattr(settings, 'MIN_FLIGHT_ALTITUDE', 1.0)
        base_altitude = getattr(settings, 'ROCKET_BASE_ALTITUDE', float(self.ALTURA_SENSOR_SUELO))

        # PASO 1: punto de lanzamiento
        n_initial = int(len(self.df) * threshold)
        if n_initial < 5:
            n_initial = min(5, len(self.df))

        altura_lanzamiento = self.df['altura'].iloc[:n_initial].mean()
        presion_lanzamiento = self.df['presion'].iloc[:n_initial].mean()
        temperatura_lanzamiento = (
            self.df['temperatura'].iloc[:n_initial].mean()
            if 'temperatura' in self.df.columns else None
        )

        # PASO 2: altura relativa para detectar vuelo
        altura_relativa_temp = self.df['altura'] - altura_lanzamiento

        vuelo_iniciado = altura_relativa_temp > min_flight_alt
        if vuelo_iniciado.any():
            idx_inicio_vuelo = vuelo_iniciado.idxmax()
        else:
            idx_inicio_vuelo = n_initial

        # Parámetros formula
        T0 = config['T0']
        L = config['L']
        R = config['R']
        g = config['g']
        M = config['M']
        use_simplified = config.get('USE_SIMPLIFIED_FORMULA', False)

        if config.get('USE_LOCAL_TEMP', False) and temperatura_lanzamiento:
            T0 = temperatura_lanzamiento + 273.15  # °C → K

        # P0: presión en reposo
        P0 = presion_lanzamiento

        # PASO 5: DETECTAR VUELOS INDIVIDUALES (picos y valles)
        df_vuelo = self.df[idx_inicio_vuelo:].copy()
        
        # Suavizar datos para evitar ruido en detección de picos
        from scipy.signal import find_peaks
        
        altura_suavizada = df_vuelo['altura'].rolling(window=5, center=True).mean().fillna(df_vuelo['altura'])
        
        # Encontrar PICOS (máximos locales) - apogeos de cada vuelo
        picos, _ = find_peaks(altura_suavizada, prominence=2.0, distance=30)
        
        # Encontrar VALLES (mínimos locales) - puntos en el suelo
        valles, _ = find_peaks(-altura_suavizada, prominence=2.0, distance=30)
        
        # Agregar inicio y fin como valles si no están
        indices_vuelo = df_vuelo.index.tolist()
        if len(valles) == 0 or valles[0] > 5:
            valles = np.insert(valles, 0, 0)
        if len(valles) == 0 or valles[-1] < len(indices_vuelo) - 5:
            valles = np.append(valles, len(indices_vuelo) - 1)
        
        # DETECTAR CADA VUELO: valle → pico → valle
        vuelos_detectados = []
        
        for pico_idx in picos:
            # Encontrar valle anterior (inicio del vuelo)
            valles_anteriores = valles[valles < pico_idx]
            if len(valles_anteriores) == 0:
                valle_inicio_idx = 0
            else:
                valle_inicio_idx = valles_anteriores[-1]
            
            # Encontrar valle posterior (fin del vuelo)
            valles_posteriores = valles[valles > pico_idx]
            if len(valles_posteriores) == 0:
                valle_fin_idx = len(indices_vuelo) - 1
            else:
                valle_fin_idx = valles_posteriores[0]
            
            # Obtener índices reales del DataFrame
            idx_inicio = indices_vuelo[valle_inicio_idx]
            idx_pico = indices_vuelo[pico_idx]
            idx_fin = indices_vuelo[valle_fin_idx]
            
            # Extraer datos del vuelo
            # USAR altura_lanzamiento (altura base del reposo) como referencia real
            altura_inicio = altura_lanzamiento  # Altura base desde el CSV
            altura_pico = df_vuelo.loc[idx_pico, 'altura']
            altura_fin = df_vuelo.loc[idx_fin, 'altura']
            
            tiempo_inicio = df_vuelo.loc[idx_inicio, 'timestamp']
            tiempo_pico = df_vuelo.loc[idx_pico, 'timestamp']
            tiempo_fin = df_vuelo.loc[idx_fin, 'timestamp']
            
            # Calcular métricas del vuelo
            altura_ganada = altura_pico - altura_inicio
            duracion_total = (tiempo_fin - tiempo_inicio).total_seconds()
            duracion_ascenso = (tiempo_pico - tiempo_inicio).total_seconds()
            duracion_descenso = (tiempo_fin - tiempo_pico).total_seconds()
            
            # Contar datos del segmento
            n_datos = len(df_vuelo.loc[idx_inicio:idx_fin])
            
            # Solo considerar vuelos con altura ganada significativa (> 1m)
            if altura_ganada > 1.0 and duracion_total > 0.5:
                vuelos_detectados.append({
                    'numero': len(vuelos_detectados) + 1,
                    'idx_inicio': idx_inicio,
                    'idx_pico': idx_pico,
                    'idx_fin': idx_fin,
                    'altura_inicio': float(altura_inicio),
                    'altura_pico': float(altura_pico),
                    'altura_fin': float(altura_fin),
                    'altura_ganada': float(altura_ganada),
                    'duracion_total': float(duracion_total),
                    'duracion_ascenso': float(duracion_ascenso),
                    'duracion_descenso': float(duracion_descenso),
                    'tiempo_inicio': tiempo_inicio,
                    'tiempo_pico': tiempo_pico,
                    'tiempo_fin': tiempo_fin,
                    'n_datos': n_datos,
                    'velocidad_promedio': float(altura_ganada / duracion_total) if duracion_total > 0 else 0
                })
        
        # Calcular tiempo promedio de vuelos individuales
        if vuelos_detectados:
            tiempo_promedio_vuelos = sum(v['duracion_total'] for v in vuelos_detectados) / len(vuelos_detectados)
            altura_promedio_ganada = sum(v['altura_ganada'] for v in vuelos_detectados) / len(vuelos_detectados)
        else:
            tiempo_promedio_vuelos = 0
            altura_promedio_ganada = 0
        
        # Usar tiempo manual si se proporciona, sino usar promedio detectado
        if tiempo_vuelo_manual is not None and tiempo_vuelo_manual > 0:
            tiempo_para_calculo = tiempo_vuelo_manual
            origen_tiempo = 'manual'
        elif tiempo_promedio_vuelos > 0:
            tiempo_para_calculo = tiempo_promedio_vuelos
            origen_tiempo = 'promedio detectado'
        
        # Altura máxima real (del vuelo con mayor pico)
        if vuelos_detectados:
            altura_maxima_real = max(v['altura_pico'] for v in vuelos_detectados)
        else:
            altura_maxima_real = df_vuelo['altura'].max()

        error_stats = {
            'altura_base_configurada': float(base_altitude),
            'altura_lanzamiento': float(altura_lanzamiento),
            'altura_lanzamiento_msnm_aprox': float(
                altura_lanzamiento - self.ALTURA_SENSOR_SUELO + self.ALTURA_POPAYAN_MSNM
            ),
            'presion_lanzamiento': float(presion_lanzamiento),
            'temperatura_lanzamiento': float(temperatura_lanzamiento) if temperatura_lanzamiento else None,
            'n_datos_reposo': n_initial,
            'n_datos_vuelo': len(df_vuelo),
            'porcentaje_datos_reposo': float(threshold * 100),
            'vuelos_detectados': vuelos_detectados,
            'tiempo_promedio_vuelos': float(tiempo_promedio_vuelos) if tiempo_promedio_vuelos > 0 else None,
            'altura_promedio_ganada': float(altura_promedio_ganada) if vuelos_detectados else None,
            'altura_maxima_real': float(altura_maxima_real)
        }

        # Gráfica ENFOCADA solo en vuelos (crestas)
        fig = go.Figure()

        # Calcular tiempo relativo en SEGUNDOS desde el primer vuelo
        if vuelos_detectados:
            tiempo_inicio_primer_vuelo = vuelos_detectados[0]['tiempo_inicio']
            # Convertir timestamps a segundos relativos
            df_vuelo_copy = df_vuelo.copy()
            df_vuelo_copy['segundos_relativos'] = (df_vuelo_copy['timestamp'] - tiempo_inicio_primer_vuelo).dt.total_seconds()
        else:
            df_vuelo_copy = df_vuelo.copy()
            df_vuelo_copy['segundos_relativos'] = 0

        # Línea de altura real solo de vuelos
        fig.add_trace(go.Scatter(
            x=df_vuelo_copy['segundos_relativos'],
            y=df_vuelo_copy['altura'],
            mode='lines',
            name='Altura Real (Sensor)',
            line=dict(color='green', width=3)
        ))

        # MARCADORES de cada vuelo detectado con segundos relativos
        colores_vuelos = ['blue', 'purple', 'red', 'cyan', 'magenta']
        if vuelos_detectados:
            tiempo_inicio_primer_vuelo = vuelos_detectados[0]['tiempo_inicio']
            
            for i, vuelo in enumerate(vuelos_detectados):
                color = colores_vuelos[i % len(colores_vuelos)]
                
                # Calcular segundos relativos para cada evento
                seg_inicio = (vuelo['tiempo_inicio'] - tiempo_inicio_primer_vuelo).total_seconds()
                seg_pico = (vuelo['tiempo_pico'] - tiempo_inicio_primer_vuelo).total_seconds()
                seg_fin = (vuelo['tiempo_fin'] - tiempo_inicio_primer_vuelo).total_seconds()
                
                # Marcador de inicio (despegue)
                fig.add_trace(go.Scatter(
                    x=[seg_inicio],
                    y=[vuelo['altura_inicio']],
                    mode='markers',
                    name=f'Vuelo {vuelo["numero"]} - Despegue',
                    marker=dict(size=10, color=color, symbol='triangle-up'),
                    showlegend=True
                ))
                
                # Marcador de pico (apogeo)
                fig.add_trace(go.Scatter(
                    x=[seg_pico],
                    y=[vuelo['altura_pico']],
                    mode='markers+text',
                    name=f'Vuelo {vuelo["numero"]} - Apogeo',
                    text=[f'V{vuelo["numero"]}: {vuelo["altura_ganada"]:.1f}m'],
                    textposition='top center',
                    marker=dict(size=12, color=color, symbol='star'),
                    showlegend=True
                ))
                
                # Marcador de fin (aterrizaje)
                fig.add_trace(go.Scatter(
                    x=[seg_fin],
                    y=[vuelo['altura_fin']],
                    mode='markers',
                    name=f'Vuelo {vuelo["numero"]} - Aterrizaje',
                    marker=dict(size=10, color=color, symbol='triangle-down'),
                    showlegend=True
                ))

        fig.update_layout(
            title=f'Análisis de Vuelos Detectados - Enfoque en Crestas',
            xaxis_title='Tiempo (segundos)',
            yaxis_title='Altura Absoluta (m)',
            hovermode='x unified',
            xaxis=dict(
                tickformat='.2f',
                ticksuffix=' s'
            ),
            annotations=[
                dict(
                    x=0.02, y=0.98,
                    xref='paper', yref='paper',
                    text=(
                        f'<b>Vuelos detectados:</b> {len(vuelos_detectados)}<br>' +
                        (f'<b>Tiempo promedio:</b> {tiempo_promedio_vuelos:.2f} s<br>' if tiempo_promedio_vuelos > 0 else '') +
                        (f'<b>Altura promedio ganada:</b> {altura_promedio_ganada:.2f} m<br>' if altura_promedio_ganada > 0 else '') +
                        f'<br><b>Condiciones Iniciales:</b><br>'
                        f'h₀ = {altura_lanzamiento:.1f} m<br>'
                        f'P₀ = {presion_lanzamiento:.2f} kPa'
                    ),
                    showarrow=False,
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='black',
                    borderwidth=1,
                    align='left'
                )
            ]
        )

        plot_html = plot(fig, output_type='div')

        # Tabla simple con altura real
        tabla_datos = df_vuelo[['timestamp', 'altura']].head(20).to_dict('records')

        return {
            'error_stats': error_stats,
            'plot': plot_html,
            'data_sample': tabla_datos,
            'explicacion': {
                'metodo': (
                    f'Se usa el promedio de los primeros {threshold * 100:.0f}% '
                    f'de datos ({n_initial} registros) como punto de referencia (cohete en reposo).'
                ),
                'referencia_presion': f'{presion_lanzamiento:.2f} kPa (presión en el lanzamiento)',
                'referencia_altura': (
                    f'{altura_lanzamiento:.1f} m (sensor) ≈ '
                    f'{altura_lanzamiento - self.ALTURA_SENSOR_SUELO + self.ALTURA_POPAYAN_MSNM:.0f} m.s.n.m'
                ),
                'altura_base_config': f'{base_altitude} m (ROCKET_BASE_ALTITUDE)',
                'interpretacion': (
                    'Análisis de vuelos detectados automáticamente mediante detección de picos y valles. '
                    'Cada vuelo muestra: altura inicial, altura máxima (apogeo), altura final, '
                    'altura ganada, duraciones y velocidad promedio.'
                )
            }
        }

    def altitude_pressure_curve(self):
        """
        Req 1.3 – Curva Altitud vs Presión vs ecuación barométrica
        """
        fig = go.Figure()

        # Datos reales
        fig.add_trace(go.Scatter(
            x=self.df['presion'],
            y=self.df['altura'],
            mode='markers',
            name='Datos del Sensor',
            marker=dict(size=4, color='blue', opacity=0.6)
        ))

        # Curva teórica
        P0 = self.df['presion'].max()
        pressure_range = np.linspace(self.df['presion'].min(), self.df['presion'].max(), 100)

        T0 = 288.15
        L = 0.0065
        R = 8.314
        g = 9.80665
        M = 0.029
        exponent = (R * L) / (g * M)

        theoretical_altitude = (T0 / L) * (1 - (pressure_range / P0) ** exponent)

        fig.add_trace(go.Scatter(
            x=pressure_range,
            y=theoretical_altitude,
            mode='lines',
            name='Ecuación Barométrica',
            line=dict(color='red', width=3, dash='dash')
        ))

        fig.update_layout(
            title='Curva Altitud vs Presión: Sensor vs Ecuación Barométrica',
            xaxis_title='Presión (kPa)',
            yaxis_title='Altura (m)',
            hovermode='closest'
        )

        return plot(fig, output_type='div')

    def environmental_dashboard(self, lat=None, lon=None, target_date=None):
        """
        Req 1.2 – Dashboard Ambiental:
        Compara temperatura y presión promedio del sensor
        vs datos meteorológicos externos (OpenWeather).
        """
        # Coordenadas por defecto (Popayán, si está en settings)
        if lat is None:
            lat = getattr(settings, 'DEFAULT_LATITUDE', 2.4456)
        if lon is None:
            lon = getattr(settings, 'DEFAULT_LONGITUDE', -76.6147)

        api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)

        if not api_key or api_key == 'TU_API_KEY_AQUI':
            return {
                'error': True,
                'message': 'API key no configurada. Obtén una gratis en https://openweathermap.org/api',
                'instructions': [
                    '1. Regístrate en OpenWeatherMap',
                    '2. Obtén tu API key gratuita',
                    '3. Agrega en settings.py: OPENWEATHER_API_KEY = "tu_key"',
                    '4. Recarga esta página'
                ]
            }

        try:
            # Fecha de referencia
            if target_date:
                from datetime import datetime as dt
                flight_date = dt.strptime(target_date, '%Y-%m-%d')
            else:
                flight_date = self.df['timestamp'].iloc[0]

            from datetime import datetime as dt, timedelta
            days_ago = (dt.now() - flight_date).days

            # Para simplicidad, usamos API de tiempo actual
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            )
            is_historical = days_ago > 5  # solo para que tú expliques la diferencia

            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                weather_data = response.json()

                external_data = {
                    'temperatura_externa': weather_data['main']['temp'],
                    'presion_externa': weather_data['main']['pressure'] / 10,  # hPa → kPa
                    'humedad': weather_data['main']['humidity'],
                    'descripcion': weather_data['weather'][0]['description'],
                    'ubicacion': weather_data['name']
                }

                sensor_avg = {
                    'temperatura_sensor': self.df['temperatura'].mean(),
                    'presion_sensor': self.df['presion'].mean(),
                }

                comparisons = {
                    'diff_temperatura': sensor_avg['temperatura_sensor'] - external_data['temperatura_externa'],
                    'diff_temperatura_pct': (
                        (sensor_avg['temperatura_sensor'] - external_data['temperatura_externa'])
                        / external_data['temperatura_externa']
                    ) * 100,
                    'diff_presion': sensor_avg['presion_sensor'] - external_data['presion_externa'],
                    'diff_presion_pct': (
                        (sensor_avg['presion_sensor'] - external_data['presion_externa'])
                        / external_data['presion_externa']
                    ) * 100,
                }

                # Gráfica temperatura
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=['Sensor', 'Meteorológico'],
                    y=[sensor_avg['temperatura_sensor'], external_data['temperatura_externa']],
                    name='Temperatura (°C)',
                    marker_color=['blue', 'orange']
                ))
                fig.update_layout(
                    title=f'Comparación: Temperatura Sensor vs Estación ({external_data["ubicacion"]})',
                    yaxis_title='Temperatura (°C)',
                    showlegend=True
                )
                plot_temp = plot(fig, output_type='div')

                # Gráfica presión
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    x=['Sensor', 'Meteorológico'],
                    y=[sensor_avg['presion_sensor'], external_data['presion_externa']],
                    name='Presión (kPa)',
                    marker_color=['green', 'red']
                ))
                fig2.update_layout(
                    title='Comparación de Presión: Sensor vs Estación',
                    yaxis_title='Presión (kPa)',
                    showlegend=True
                )
                plot_pressure = plot(fig2, output_type='div')

                return {
                    'error': False,
                    'external_data': external_data,
                    'sensor_data': sensor_avg,
                    'comparisons': comparisons,
                    'plot_temperature': plot_temp,
                    'plot_pressure': plot_pressure,
                    'interpretation': self._interpret_weather_comparison(comparisons),
                    'query_date': flight_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_historical': is_historical,
                    'warning': (
                        'Usando datos meteorológicos actuales (la API histórica real requiere suscripción).'
                        if is_historical else None
                    )
                }

            else:
                return {
                    'error': True,
                    'message': f'Error al obtener datos meteorológicos: {response.status_code}',
                    'details': response.text
                }

        except requests.exceptions.Timeout:
            return {
                'error': True,
                'message': 'Timeout al conectar con OpenWeatherMap. Verifica tu conexión a internet.'
            }
        except Exception as e:
            return {
                'error': True,
                'message': f'Error inesperado: {str(e)}'
            }

    def _interpret_weather_comparison(self, comparisons):
        """Interpretar las diferencias entre sensor y datos meteorológicos (para la exposición)."""
        interpretations = []

        # Temperatura
        if abs(comparisons['diff_temperatura']) < 2:
            interpretations.append("✅ Temperatura del sensor muy precisa (diferencia < 2 °C).")
        elif abs(comparisons['diff_temperatura']) < 5:
            interpretations.append("⚠️ Temperatura del sensor aceptable (diferencia < 5 °C).")
        else:
            interpretations.append("❌ Temperatura del sensor con desviación significativa (diferencia > 5 °C).")

        # Presión
        if abs(comparisons['diff_presion']) < 1:
            interpretations.append("✅ Presión del sensor muy precisa (diferencia < 1 kPa).")
        elif abs(comparisons['diff_presion']) < 2:
            interpretations.append("⚠️ Presión del sensor aceptable (diferencia < 2 kPa).")
        else:
            interpretations.append("❌ Presión del sensor con desviación significativa (diferencia > 2 kPa).")

        return interpretations

    # =========================================
    # REQUERIMIENTO 2: DIAGNÓSTICO DE EVENTOS
    # =========================================

    def identify_flight_phases(self):
        """
        Req 2.1 – Identificar y graficar fases del vuelo: ascenso, apogeo, descenso.
        DETECTA AUTOMÁTICAMENTE SI HUBO VUELO REAL O SI SON DATOS EN REPOSO.
        """
        # PASO 1: Determinar si hubo vuelo real
        altura_min = self.df['altura'].min()
        altura_max = self.df['altura'].max()
        variacion_altura = altura_max - altura_min
        
        # Si la variación es menor a 2 metros, probablemente es ruido del sensor en reposo
        MIN_FLIGHT_VARIATION = getattr(settings, 'MIN_FLIGHT_ALTITUDE', 1.0)
        
        vuelo_detectado = variacion_altura > MIN_FLIGHT_VARIATION
        
        # Velocidad vertical (m/s)
        self.df['velocidad_vertical'] = (
            self.df['altura'].diff() / self.df['timestamp'].diff().dt.total_seconds()
        )

        # Suavizado
        window_size = min(20, len(self.df) // 5)  # Ajustado para datasets pequeños
        self.df['velocidad_suavizada'] = self.df['velocidad_vertical'].rolling(
            window=window_size, center=True
        ).mean()

        # Apogeo
        apogee_idx = self.df['altura'].idxmax()
        apogee_time = self.df.loc[apogee_idx, 'timestamp']
        apogee_height = self.df.loc[apogee_idx, 'altura']

        ascent = self.df[self.df['timestamp'] <= apogee_time]
        descent = self.df[self.df['timestamp'] > apogee_time]

        fig = go.Figure()

        if vuelo_detectado:
            # VUELO REAL DETECTADO
            fig.add_trace(go.Scatter(
                x=ascent['timestamp'],
                y=ascent['altura'],
                mode='lines',
                name='Ascenso',
                line=dict(color='green', width=2)
            ))

            fig.add_trace(go.Scatter(
                x=descent['timestamp'],
                y=descent['altura'],
                mode='lines',
                name='Descenso',
                line=dict(color='red', width=2)
            ))

            fig.add_trace(go.Scatter(
                x=[apogee_time],
                y=[apogee_height],
                mode='markers+text',
                name='Apogeo',
                marker=dict(size=15, color='orange', symbol='star'),
                text=[f'Apogeo: {apogee_height:.2f} m'],
                textposition='top center'
            ))

            titulo = '🚀 Perfil de Vuelo: Ascenso, Apogeo y Descenso'
        else:
            # SENSOR EN REPOSO (NO HAY VUELO REAL)
            fig.add_trace(go.Scatter(
                x=self.df['timestamp'],
                y=self.df['altura'],
                mode='lines',
                name='Altura (Sensor en Reposo)',
                line=dict(color='gray', width=2, dash='dot')
            ))
            
            # Marcar el punto más alto (aunque es ruido)
            fig.add_trace(go.Scatter(
                x=[apogee_time],
                y=[apogee_height],
                mode='markers+text',
                name='Pico Máximo (ruido)',
                marker=dict(size=10, color='orange', symbol='x'),
                text=[f'{apogee_height:.2f} m'],
                textposition='top center'
            ))

            titulo = '⚠️ Datos en Reposo - No se Detectó Vuelo Real'

        fig.update_layout(
            title=titulo,
            xaxis_title='Tiempo',
            yaxis_title='Altura (m)',
            hovermode='x unified',
            annotations=[
                dict(
                    x=0.5, y=0.95,
                    xref='paper', yref='paper',
                    text=(
                        f'Variación de altura: {variacion_altura:.2f} m<br>'
                        f'{"✅ VUELO DETECTADO" if vuelo_detectado else "⚠️ SENSOR EN REPOSO (ruido < 2m)"}'
                    ),
                    showarrow=False,
                    bgcolor='rgba(255,255,200,0.8)' if not vuelo_detectado else 'rgba(200,255,200,0.8)',
                    bordercolor='black',
                    borderwidth=1,
                    align='center',
                    font=dict(size=12)
                )
            ]
        )

        # Calcular velocidades solo si hay datos válidos
        vel_max_ascenso = ascent['velocidad_suavizada'].max() if len(ascent) > 0 and not ascent['velocidad_suavizada'].isna().all() else 0.0
        vel_max_descenso = abs(descent['velocidad_suavizada'].min()) if len(descent) > 0 and not descent['velocidad_suavizada'].isna().all() else 0.0

        phase_stats = {
            'vuelo_detectado': vuelo_detectado,
            'variacion_altura': float(variacion_altura),
            'apogeo_altura': float(apogee_height),
            'apogeo_tiempo': apogee_time.strftime('%Y-%m-%d %H:%M:%S'),
            'altura_minima': float(altura_min),
            'altura_maxima': float(altura_max),
            'duracion_ascenso': float(
                (apogee_time - self.df['timestamp'].min()).total_seconds()
            ),
            'duracion_descenso': float(
                (self.df['timestamp'].max() - apogee_time).total_seconds()
            ),
            'velocidad_max_ascenso': float(vel_max_ascenso),
            'velocidad_max_descenso': float(vel_max_descenso),
            'warning': (
                'ADVERTENCIA: La variación de altura es muy pequeña (< 2m). '
                'Estos datos parecen ser del sensor en reposo, no de un vuelo real. '
                'Para análisis significativo, necesitas datos de un lanzamiento real.'
            ) if not vuelo_detectado else None
        }

        return {
            'plot': plot(fig, output_type='div'),
            'stats': phase_stats
        }

    def analyze_parachute_deployment(self):
        """
        Req 2.2 – Analizar tasa de cambio de presión y velocidad en descenso
        para detectar altura probable de despliegue del paracaídas.
        INCLUYE DETECCIÓN DE SI HAY VUELO REAL.
        """
        # Verificar si hubo vuelo real
        variacion_altura = self.df['altura'].max() - self.df['altura'].min()
        MIN_FLIGHT_VARIATION = getattr(settings, 'MIN_FLIGHT_ALTITUDE', 1.0)
        vuelo_detectado = variacion_altura > MIN_FLIGHT_VARIATION
        
        apogee_idx = self.df['altura'].idxmax()
        descent_data = self.df.loc[apogee_idx:].copy()

        descent_data['tasa_presion'] = (
            descent_data['presion'].diff() / descent_data['timestamp'].diff().dt.total_seconds()
        )
        descent_data['velocidad_vertical'] = (
            descent_data['altura'].diff() / descent_data['timestamp'].diff().dt.total_seconds()
        )

        window = min(15, len(descent_data) // 3)
        descent_data['tasa_presion_suave'] = descent_data['tasa_presion'].rolling(
            window=window, center=True
        ).mean()
        descent_data['velocidad_suave'] = descent_data['velocidad_vertical'].rolling(
            window=window, center=True
        ).mean()

        parachute_detected = False
        parachute_time = None
        parachute_height = None
        parachute_idx = None
        
        if vuelo_detectado and len(descent_data) > 10:
            aceleracion = descent_data['velocidad_suave'].diff()

            if len(aceleracion.dropna()) > 0 and aceleracion.std() > 0.01:
                threshold = aceleracion.std() * 2
                parachute_candidates = descent_data[aceleracion > threshold]

                if len(parachute_candidates) > 0:
                    parachute_idx = parachute_candidates.index[0]
                    parachute_time = descent_data.loc[parachute_idx, 'timestamp']
                    parachute_height = descent_data.loc[parachute_idx, 'altura']
                    parachute_detected = True

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=descent_data['timestamp'],
            y=descent_data['tasa_presion_suave'],
            mode='lines',
            name='Tasa de Cambio de Presión' + (' (datos en reposo)' if not vuelo_detectado else ''),
            line=dict(color='blue' if vuelo_detectado else 'gray', width=2)
        ))

        if parachute_detected:
            fig.add_trace(go.Scatter(
                x=[parachute_time],
                y=[descent_data.loc[parachute_idx, 'tasa_presion_suave']],
                mode='markers+text',
                name='Posible Despliegue Paracaídas',
                marker=dict(size=15, color='red', symbol='diamond'),
                text=[f'Altura: {parachute_height:.2f} m'],
                textposition='top center'
            ))

        titulo = 'Análisis de Despliegue de Paracaídas (Tasa de Cambio de Presión)'
        if not vuelo_detectado:
            titulo += ' - ⚠️ Sin Vuelo Real Detectado'

        fig.update_layout(
            title=titulo,
            xaxis_title='Tiempo',
            yaxis_title='Tasa de Cambio de Presión (kPa/s)',
            hovermode='x unified'
        )

        return {
            'plot': plot(fig, output_type='div'),
            'vuelo_detectado': vuelo_detectado,
            'parachute_detected': parachute_detected,
            'parachute_time': parachute_time.strftime('%Y-%m-%d %H:%M:%S') if parachute_detected else 'No detectado',
            'parachute_height': float(parachute_height) if parachute_detected else None,
            'warning': (
                'No se puede analizar despliegue de paracaídas sin datos de vuelo real. '
                'La variación de altura es muy pequeña (< 2m).'
            ) if not vuelo_detectado else None
        }

    def calculate_air_density(self):
        """
        Req 2.3 – Calcular densidad del aire durante el vuelo.

        ρ = (P * M) / (R * T)

        - P en Pa (kPa * 1000)
        - T en K (°C + 273.15)
        - M ≈ 0.029 kg/mol
        - R ≈ 8.314 J/(mol·K)
        
        INCLUYE DETECCIÓN DE SI HAY VUELO REAL.
        """
        # Verificar si hubo vuelo real
        variacion_altura = self.df['altura'].max() - self.df['altura'].min()
        MIN_FLIGHT_VARIATION = getattr(settings, 'MIN_FLIGHT_ALTITUDE', 1.0)
        vuelo_detectado = variacion_altura > MIN_FLIGHT_VARIATION
        
        self.df['presion_pa'] = self.df['presion'] * 1000
        self.df['temperatura_k'] = self.df['temperatura'] + 273.15

        M = 0.029
        R = 8.314

        self.df['densidad_aire'] = (self.df['presion_pa'] * M) / (R * self.df['temperatura_k'])

        density_stats = {
            'densidad_promedio': float(self.df['densidad_aire'].mean()),
            'densidad_max': float(self.df['densidad_aire'].max()),
            'densidad_min': float(self.df['densidad_aire'].min()),
            'densidad_std': float(self.df['densidad_aire'].std())
        }

        fig = go.Figure()
        
        # Ajustar estilo según si es vuelo o reposo
        if vuelo_detectado:
            line_style = dict(color='purple', width=2)
            titulo = 'Densidad del Aire Durante el Vuelo'
        else:
            line_style = dict(color='gray', width=1, dash='dot')
            titulo = '⚠️ Densidad del Aire - Datos en Reposo (Sin Vuelo Real)'
        
        fig.add_trace(go.Scatter(
            x=self.df['timestamp'],
            y=self.df['densidad_aire'],
            mode='lines',
            name='Densidad del Aire',
            line=line_style
        ))
        fig.update_layout(
            title=titulo,
            xaxis_title='Tiempo',
            yaxis_title='Densidad (kg/m³)',
            hovermode='x unified'
        )

        return {
            'vuelo_detectado': vuelo_detectado,
            'variacion_altura': float(variacion_altura),
            'plot': plot(fig, output_type='div'),
            'stats': density_stats,
            'impact_analysis': self._analyze_density_impact(self.df, vuelo_detectado),
            'warning': (
                'ADVERTENCIA: Estos datos corresponden a un sensor en reposo (variación < 2m). '
                'La densidad calculada es representativa del aire en una ubicación fija, '
                'no durante un vuelo. Para análisis significativo, necesitas datos de un lanzamiento real.'
            ) if not vuelo_detectado else None
        }

    def _analyze_density_impact(self, df, vuelo_detectado=True):
        """Analizar cómo la densidad del aire pudo afectar el rendimiento."""
        apogee_idx = df['altura'].idxmax()

        avg_density_ascent = df.loc[:apogee_idx, 'densidad_aire'].mean()
        avg_density_descent = df.loc[apogee_idx:, 'densidad_aire'].mean()

        impact = {
            'densidad_promedio_ascenso': float(avg_density_ascent),
            'densidad_promedio_descenso': float(avg_density_descent),
            'diferencia_porcentual': float(
                (avg_density_descent - avg_density_ascent) / avg_density_ascent * 100
            ),
            'interpretacion': self._get_density_interpretation(avg_density_ascent, avg_density_descent, vuelo_detectado)
        }

        return impact

    def _get_density_interpretation(self, ascent_density, descent_density, vuelo_detectado=True):
        """Texto listo para explicar densidad en la presentación."""
        if not vuelo_detectado:
            return (
                "Los datos corresponden a un sensor en reposo. La densidad calculada refleja "
                "las condiciones atmosféricas en una ubicación fija, no durante un vuelo."
            )
        
        if descent_density > ascent_density:
            return (
                "La densidad fue ligeramente mayor en el descenso, lo que aumenta la resistencia del aire "
                "y ayuda al paracaídas a frenar el cohete de forma más efectiva."
            )
        else:
            return (
                "La densidad fue similar o menor en el descenso, lo que reduce la resistencia del aire y puede "
                "hacer que el paracaídas sea menos efectivo para frenar la caída."
            )

    def detect_anomalies(self):
        """
        Req 2.4 – Detección de anomalías:
        - Picos inusuales en temperatura y presión
        - Cambios bruscos entre muestras
        INCLUYE DETECCIÓN DE SI HAY VUELO REAL.
        """
        # Verificar si hubo vuelo real
        variacion_altura = self.df['altura'].max() - self.df['altura'].min()
        MIN_FLIGHT_VARIATION = getattr(settings, 'MIN_FLIGHT_ALTITUDE', 1.0)
        vuelo_detectado = variacion_altura > MIN_FLIGHT_VARIATION
        
        anomalies = []

        # ---- TEMPERATURA ----
        temp_mean = self.df['temperatura'].mean()
        temp_std = self.df['temperatura'].std()
        
        # Ajustar umbral según si es vuelo o reposo
        if vuelo_detectado:
            temp_threshold = 3 * temp_std  # Más estricto para vuelo real
        else:
            temp_threshold = 5 * temp_std  # Más tolerante para ruido en reposo

        temp_anomalies = self.df[abs(self.df['temperatura'] - temp_mean) > temp_threshold]

        if len(temp_anomalies) > 0:
            for _, row in temp_anomalies.iterrows():
                anomalies.append({
                    'tipo': 'Temperatura',
                    'timestamp': row['timestamp'],
                    'valor': float(row['temperatura']),
                    'altura': float(row['altura']),
                    'causa_probable': 'Exposición directa al sol, sombra repentina o calentamiento del sensor.' if vuelo_detectado else 'Variación térmica normal del sensor en reposo.'
                })

        # ---- PRESIÓN ----
        pressure_mean = self.df['presion'].mean()
        pressure_std = self.df['presion'].std()
        
        # Ajustar umbral según si es vuelo o reposo
        if vuelo_detectado:
            pressure_threshold = 3 * pressure_std
        else:
            pressure_threshold = 5 * pressure_std

        pressure_anomalies = self.df[abs(self.df['presion'] - pressure_mean) > pressure_threshold]

        if len(pressure_anomalies) > 0:
            for _, row in pressure_anomalies.iterrows():
                anomalies.append({
                    'tipo': 'Presión',
                    'timestamp': row['timestamp'],
                    'valor': float(row['presion']),
                    'altura': float(row['altura']),
                    'causa_probable': 'Golpe, vibración mecánica o turbulencia muy fuerte.' if vuelo_detectado else 'Variación barométrica normal del sensor en reposo.'
                })

        # ---- DERIVADAS (cambios bruscos) ----
        self.df['temp_change_rate'] = self.df['temperatura'].diff().abs()
        self.df['pressure_change_rate'] = self.df['presion'].diff().abs()

        sudden_temp_changes = self.df[
            self.df['temp_change_rate'] > self.df['temp_change_rate'].quantile(0.99)
        ]
        sudden_pressure_changes = self.df[
            self.df['pressure_change_rate'] > self.df['pressure_change_rate'].quantile(0.99)
        ]

        for _, row in sudden_temp_changes.iterrows():
            anomalies.append({
                'tipo': 'Cambio brusco de temperatura',
                'timestamp': row['timestamp'],
                'valor': float(row['temperatura']),
                'altura': float(row['altura']),
                'causa_probable': 'Paso rápido de sombra a sol, ráfaga de viento o contacto con el cuerpo.'
            })

        for _, row in sudden_pressure_changes.iterrows():
            anomalies.append({
                'tipo': 'Cambio brusco de presión',
                'timestamp': row['timestamp'],
                'valor': float(row['presion']),
                'altura': float(row['altura']),
                'causa_probable': 'Sacudida del cohete, turbulencia o pequeña fuga momentánea.'
            })

        # ---- Gráfica de temperatura con anomalías ----
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=self.df['timestamp'],
            y=self.df['temperatura'],
            mode='lines',
            name='Temperatura',
            line=dict(color='red', width=1)
        ))
        if len(temp_anomalies) > 0:
            fig_temp.add_trace(go.Scatter(
                x=temp_anomalies['timestamp'],
                y=temp_anomalies['temperatura'],
                mode='markers',
                name='Anomalías Temperatura',
                marker=dict(size=10, color='darkred', symbol='x')
            ))
        fig_temp.update_layout(
            title='Detección de Anomalías en Temperatura',
            xaxis_title='Tiempo',
            yaxis_title='Temperatura (°C)',
            hovermode='x unified'
        )
        plot_temp = plot(fig_temp, output_type='div')

        # ---- Gráfica de presión con anomalías ----
        fig_press = go.Figure()
        fig_press.add_trace(go.Scatter(
            x=self.df['timestamp'],
            y=self.df['presion'],
            mode='lines',
            name='Presión',
            line=dict(color='blue', width=1)
        ))
        if len(pressure_anomalies) > 0:
            fig_press.add_trace(go.Scatter(
                x=pressure_anomalies['timestamp'],
                y=pressure_anomalies['presion'],
                mode='markers',
                name='Anomalías Presión',
                marker=dict(size=10, color='navy', symbol='x')
            ))
        fig_press.update_layout(
            title='Detección de Anomalías en Presión',
            xaxis_title='Tiempo',
            yaxis_title='Presión (kPa)',
            hovermode='x unified'
        )
        plot_pressure = plot(fig_press, output_type='div')

        return {
            'vuelo_detectado': vuelo_detectado,
            'variacion_altura': float(variacion_altura),
            'plot': plot_temp,               # compatibilidad hacia atrás
            'plot_temperature': plot_temp,   # explícito
            'plot_pressure': plot_pressure,  # nueva gráfica
            'anomalies': anomalies,
            'total_anomalies': len(anomalies),
            'warning': (
                'ADVERTENCIA: Estos datos corresponden a un sensor en reposo (variación < 2m). '
                'Las "anomalías" detectadas son principalmente ruido normal del sensor, no eventos reales de vuelo. '
                'Para análisis significativo, necesitas datos de un lanzamiento real.'
            ) if not vuelo_detectado else None
        }

    # ===================================================
    # REQUERIMIENTO 3: OPTIMIZACIÓN BASADA EN EVIDENCIA
    # ===================================================

    def analyze_success_formula(self):
        """
        Req 3.1 – “Fórmula del éxito”:
        Determinar qué condiciones (presión, temperatura ambiente, etc.)
        estaban presentes cuando se logró el mejor apogeo en ESTE vuelo.

        Nota: la combinación “presión y agua” se toma desde settings:
          - ROCKET_PRESSURE_PSI
          - ROCKET_WATER_VOLUME_ML
        para que puedas explicarlo en la exposición.
        """
        apogee_idx = self.df['altura'].idxmax()
        best_conditions = self.df.loc[apogee_idx]

        launch_conditions = self.df.iloc[:10].mean(numeric_only=True)

        apogee_conditions = {
            'altura_maxima': float(best_conditions['altura']),
            'tiempo_al_apogeo': float(
                (best_conditions['timestamp'] - self.df['timestamp'].min()).total_seconds()
            ),
            'temperatura_apogeo': float(best_conditions['temperatura']),
            'presion_apogeo': float(best_conditions['presion'])
        }

        launch_analysis = {
            'presion_inicial': float(launch_conditions['presion']),
            'temperatura_inicial': float(launch_conditions['temperatura']),
            'altura_inicial': float(launch_conditions['altura'])
        }

        # Parámetros de experimento (para que lo cuentes en voz)
        rocket_pressure_psi = getattr(settings, 'ROCKET_PRESSURE_PSI', 45)  # 40–50 psi → promedio 45
        rocket_water_ml = getattr(settings, 'ROCKET_WATER_VOLUME_ML', 500)  # mL
        rocket_bottle_ml = getattr(settings, 'ROCKET_BOTTLE_VOLUME_ML', 1500)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.df['timestamp'],
            y=self.df['altura'],
            mode='lines',
            name='Trayectoria',
            line=dict(color='blue', width=2)
        ))

        fig.add_trace(go.Scatter(
            x=[self.df['timestamp'].min()],
            y=[self.df['altura'].min()],
            mode='markers+text',
            name='Lanzamiento',
            marker=dict(size=15, color='green', symbol='triangle-up'),
            text=[f'Inicio<br>P≈ {launch_analysis["presion_inicial"]:.2f} kPa'],
            textposition='bottom center'
        ))

        fig.add_trace(go.Scatter(
            x=[best_conditions['timestamp']],
            y=[best_conditions['altura']],
            mode='markers+text',
            name='Mejor Apogeo',
            marker=dict(size=20, color='gold', symbol='star'),
            text=[f'Apogeo: {best_conditions["altura"]:.2f} m'],
            textposition='top center'
        ))

        fig.update_layout(
            title='Fórmula del Éxito: Condiciones Óptimas para Máximo Apogeo',
            xaxis_title='Tiempo',
            yaxis_title='Altura (m)',
            hovermode='x unified'
        )

        return {
            'plot': plot(fig, output_type='div'),
            'apogee_conditions': apogee_conditions,
            'launch_conditions': launch_analysis,
            'experiment_setup': {
                'presion_bomba_psi': rocket_pressure_psi,
                'volumen_agua_ml': rocket_water_ml,
                'volumen_botella_ml': rocket_bottle_ml
            },
            'recommendations': self._generate_recommendations(launch_analysis, apogee_conditions,
                                                              rocket_pressure_psi, rocket_water_ml)
        }

    def _generate_recommendations(self, launch, apogee, pressure_psi, water_ml):
        """Recomendaciones en texto para la presentación del Req 3.1."""
        recommendations = [
            (
                f"Con la configuración utilizada (≈{pressure_psi} psi y {water_ml} mL de agua), "
                f"se alcanzó una altura máxima de {apogee['altura_maxima']:.2f} m."
            ),
            (
                f"El tiempo desde el lanzamiento hasta el apogeo fue de "
                f"{apogee['tiempo_al_apogeo']:.2f} segundos, lo que indica un ascenso "
                f"rápido pero estable."
            ),
            (
                f"La presión de lanzamiento promedio medida por el sensor fue de "
                f"{launch['presion_inicial']:.2f} kPa y la temperatura ambiente de "
                f"{launch['temperatura_inicial']:.2f} °C, condiciones típicas de Popayán."
            ),
            (
                "Para siguientes vuelos, se puede probar pequeños ajustes en la presión "
                "(±5 psi) y en el volumen de agua (±50 mL) para verificar si se incrementa "
                "el apogeo sin sacrificar estabilidad."
            )
        ]
        return recommendations

    def propose_blueprint_v2(self):
        """
        Req 3.3 – “Blueprint del Cohete v2.0”:
        Proponer 3 mejoras específicas basadas en los análisis anteriores
        (aerodinámica, electrónica/sensor y paracaídas).
        """
        phases = self.identify_flight_phases()
        density = self.calculate_air_density()
        parachute_info = self.analyze_parachute_deployment()

        phase_stats = phases['stats']
        density_stats = density['stats']
        density_impact = density['impact_analysis']

        improvements = []

        # 1) Aerodinámica
        improvements.append({
            'area': 'Aerodinámica (fuselaje y aletas)',
            'descripcion': (
                "Diseñar un cono más alargado y suave y usar 3–4 aletas simétricas, "
                "delgadas y bien alineadas (≈15–20 % de la altura de la botella), "
                "para reducir la turbulencia y el arrastre."
            ),
            'justificacion': (
                "El cohete alcanza un apogeo de "
                f"{phase_stats['apogeo_altura']:.2f} m con una densidad promedio del aire de "
                f"{density_stats['densidad_promedio']:.3f} kg/m³. "
                "Mejorar la forma aerodinámica disminuye la fuerza de arrastre y permite "
                "aprovechar mejor la energía almacenada en la presión."
            )
        })

        # 2) Electrónica / Montaje del sensor
        improvements.append({
            'area': 'Electrónica y montaje del sensor',
            'descripcion': (
                "Montar el sensor dentro del fuselaje protegido con espuma o material "
                "amortiguador, y asegurar el cableado para reducir vibraciones. "
                "Además, aplicar filtrado digital simple (promedio móvil) para suavizar "
                "picos espurios en temperatura y presión."
            ),
            'justificacion': (
                "En la detección de anomalías se observan picos y cambios bruscos en las "
                "lecturas de temperatura y presión. Esto es típico de vibraciones y golpes, "
                "no de cambios reales en la atmósfera. Un mejor montaje del sensor mejora "
                "la calidad de los datos y la confiabilidad del análisis."
            )
        })

        # 3) Sistema de recuperación (paracaídas)
        if parachute_info['parachute_height'] is not None:
            altura_deploy = parachute_info['parachute_height']
            deploy_text = (
                f"El análisis sugiere un despliegue del paracaídas alrededor de "
                f"{altura_deploy:.1f} m de altura."
            )
        else:
            deploy_text = (
                "En este vuelo no se detectó con claridad la altura exacta de despliegue "
                "del paracaídas, probablemente por caída sin apertura o por ruido excesivo "
                "en las señales."
            )

        improvements.append({
            'area': 'Sistema de recuperación (paracaídas)',
            'descripcion': (
                "Optimizar el tamaño del paracaídas y el mecanismo de despliegue para que "
                "se abra en una altura intermedia (ni demasiado bajo ni demasiado alto), "
                "usando un diseño de paracaídas tipo domo o cruz, con líneas simétricas y "
                "un punto de anclaje fuerte."
            ),
            'justificacion': (
                deploy_text + " El análisis de densidad muestra que "
                f"{density_impact['interpretacion']} "
                "Ajustar la altura de despliegue y el área del paracaídas mejora la seguridad "
                "del impacto y protege la estructura del cohete para reutilizarlo."
            )
        })

        return {
            'improvements': improvements,
            'supporting_metrics': {
                'apogeo_altura_m': phase_stats['apogeo_altura'],
                'tiempo_al_apogeo_s': phase_stats['duracion_ascenso'],
                'densidad_promedio_kg_m3': density_stats['densidad_promedio'],
                'densidad_impacto': density_impact,
                'parachute_detected': parachute_info['parachute_detected'],
                'parachute_height': parachute_info['parachute_height']
            }
        }

    # ==========================================
    # ORQUESTADOR: TODO EL ANÁLISIS JUNTO
    # ==========================================

    def get_comprehensive_analysis(self, weather_date=None, tiempo_vuelo_manual=None):
        """
        Genera un análisis comprensivo con TODOS los requerimientos implementados:

        - Req 1.1: validación altura teórica vs real (y_max = 1.225 × t²)
        - Req 1.2: dashboard ambiental (sensor vs estación)
        - Req 1.3: curva altitud vs presión
        - Req 2.1: fases del vuelo
        - Req 2.2: despliegue de paracaídas
        - Req 2.3: densidad del aire + impacto
        - Req 2.4: anomalías en temperatura y presión
        - Req 3.1: “fórmula del éxito”
        - Req 3.3: blueprint del cohete v2.0
        """
        results = {
            'validation': self.validate_theoretical_altitude(tiempo_vuelo_manual=tiempo_vuelo_manual),
            'weather_comparison': self.environmental_dashboard(target_date=weather_date),
            'altitude_pressure': self.altitude_pressure_curve(),
            'flight_phases': self.identify_flight_phases(),
            'parachute': self.analyze_parachute_deployment(),
            'air_density': self.calculate_air_density(),
            'anomalies': self.detect_anomalies(),
            'success_formula': self.analyze_success_formula(),
            'blueprint_v2': self.propose_blueprint_v2()
        }

        return results
