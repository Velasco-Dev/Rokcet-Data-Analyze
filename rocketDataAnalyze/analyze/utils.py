import pandas as pd
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
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.filename = file_path.split('/')[-1]
    
    def get_basic_stats(self):
        """Retorna estadísticas básicas del dataset"""
        stats = {
            'total_records': len(self.df),
            'time_range': {
                'start': self.df['timestamp'].min(),
                'end': self.df['timestamp'].max()
            },
            'duration_minutes': (
                self.df['timestamp'].max() - self.df['timestamp'].min()
            ).total_seconds() / 60,
            'temperature_stats': self.df['temperatura'].describe().to_dict(),
            'pressure_stats': self.df['presion'].describe().to_dict(),
            'altitude_stats': self.df['altura'].describe().to_dict()
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
        fig_temp = px.line(self.df, x='timestamp', y='temperatura',
                          title=f'Temperatura vs Tiempo - {self.filename}',
                          labels={'temperatura': 'Temperatura (°C)', 
                                 'timestamp': 'Tiempo'})
        fig_temp.update_traces(line=dict(color='red', width=2))
        plots['temperature'] = plot(fig_temp, output_type='div')
        
        # Gráfica de presión interactiva
        fig_pressure = px.line(self.df, x='timestamp', y='presion',
                              title=f'Presión vs Tiempo - {self.filename}',
                              labels={'presion': 'Presión (kPa)', 
                                     'timestamp': 'Tiempo'})
        fig_pressure.update_traces(line=dict(color='blue', width=2))
        plots['pressure'] = plot(fig_pressure, output_type='div')
        
        # Gráfica de altura interactiva
        fig_altitude = px.line(self.df, x='timestamp', y='altura',
                              title=f'Altura vs Tiempo - {self.filename}',
                              labels={'altura': 'Altura (m)', 
                                     'timestamp': 'Tiempo'})
        fig_altitude.update_traces(line=dict(color='green', width=2))
        plots['altitude'] = plot(fig_altitude, output_type='div')
        
        return plots
    
    def create_combined_plot(self):
        """Crea una gráfica combinada con las tres variables"""
        fig = go.Figure()
        
        # Agregar las tres series
        fig.add_trace(go.Scatter(x=self.df['timestamp'], y=self.df['temperatura'],
                               mode='lines', name='Temperatura', 
                               line=dict(color='red'), yaxis='y1'))
        
        fig.add_trace(go.Scatter(x=self.df['timestamp'], y=self.df['presion'],
                               mode='lines', name='Presión',
                               line=dict(color='blue'), yaxis='y2'))
        
        fig.add_trace(go.Scatter(x=self.df['timestamp'], y=self.df['altura'],
                               mode='lines', name='Altura',
                               line=dict(color='green'), yaxis='y3'))
        
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
    
    # ===== REQUERIMIENTO 1: ANÁLISIS COMPARATIVO Y VALIDACIÓN MULTI-SENSOR =====
    
    def validate_theoretical_altitude(self, initial_pressure=101.325, theoretical_height=None):
        """
        Requerimiento 1.1: Validar altura teórica vs. real usando fórmula de Littlewood
        
        Fórmula Barométrica Internacional (Littlewood):
        h = (T₀/L) * [1 - (P/P₀)^(R*L/g*M)]
        
        Donde:
        - T₀ = 288.15 K (temperatura estándar al nivel del mar)
        - L = 0.0065 K/m (gradiente térmico)
        - P₀ = presión inicial (kPa)
        - R = 8.314 J/(mol·K) (constante de gases)
        - g = 9.80665 m/s² (gravedad)
        - M = 0.029 kg/mol (masa molar del aire)
        """
        T0 = 288.15  # K
        L = 0.0065   # K/m
        R = 8.314    # J/(mol·K)
        g = 9.80665  # m/s²
        M = 0.029    # kg/mol
        
        # Calcular altura teórica basada en la presión
        P0 = initial_pressure  # Presión inicial en kPa
        exponent = (R * L) / (g * M)
        
        self.df['altura_teorica'] = (T0 / L) * (1 - (self.df['presion'] / P0) ** exponent)
        self.df['error_altura'] = self.df['altura'] - self.df['altura_teorica']
        self.df['error_porcentual'] = (self.df['error_altura'] / self.df['altura_teorica']) * 100
        
        # Estadísticas del error
        error_stats = {
            'error_promedio': self.df['error_altura'].mean(),
            'error_std': self.df['error_altura'].std(),
            'error_max': self.df['error_altura'].max(),
            'error_min': self.df['error_altura'].min(),
            'error_porcentual_promedio': self.df['error_porcentual'].mean(),
            'rmse': np.sqrt(np.mean(self.df['error_altura']**2))
        }
        
        # Crear gráfica comparativa
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df['timestamp'], 
            y=self.df['altura'],
            mode='lines',
            name='Altura Real (Sensor)',
            line=dict(color='green', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=self.df['timestamp'], 
            y=self.df['altura_teorica'],
            mode='lines',
            name='Altura Teórica (Littlewood)',
            line=dict(color='orange', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Validación: Altura Real vs Teórica (Fórmula de Littlewood)',
            xaxis_title='Tiempo',
            yaxis_title='Altura (m)',
            hovermode='x unified'
        )
        
        plot_html = plot(fig, output_type='div')
        
        return {
            'error_stats': error_stats,
            'plot': plot_html,
            'data': self.df[['timestamp', 'altura', 'altura_teorica', 'error_altura', 'error_porcentual']].to_dict('records')
        }
    
    def altitude_pressure_curve(self):
        """
        Requerimiento 1.3: Graficar curva de altitud vs presión y comparar con ecuación barométrica
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
        
        # Curva teórica barométrica
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
        Requerimiento 1.2: Dashboard Ambiental - Comparar datos del sensor con datos meteorológicos externos
        
        Usa OpenWeatherMap API para obtener datos meteorológicos del momento del vuelo
        
        Args:
            lat: Latitud (por defecto usa settings.DEFAULT_LATITUDE)
            lon: Longitud (por defecto usa settings.DEFAULT_LONGITUDE)
            target_date: Fecha específica en formato 'YYYY-MM-DD' para obtener datos históricos
                        Si es None, usa la fecha del primer registro del CSV
        """
        # Usar coordenadas por defecto si no se proporcionan
        if lat is None:
            lat = getattr(settings, 'DEFAULT_LATITUDE', 40.4168)
        if lon is None:
            lon = getattr(settings, 'DEFAULT_LONGITUDE', -3.7038)
        
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
        
        # Si no hay API key configurada, retornar mensaje informativo
        if not api_key or api_key == 'TU_API_KEY_AQUI':
            return {
                'error': True,
                'message': 'API key no configurada. Obtén una gratis en https://openweathermap.org/api',
                'instructions': [
                    '1. Regístrate en OpenWeatherMap',
                    '2. Obtén tu API key gratuita',
                    '3. Agrégala en settings.py: OPENWEATHER_API_KEY = "tu_key"',
                    '4. Recarga esta página'
                ]
            }
        
        try:
            # Obtener timestamp del vuelo
            if target_date:
                # Usar fecha proporcionada
                from datetime import datetime as dt
                flight_date = dt.strptime(target_date, '%Y-%m-%d')
            else:
                # Usar fecha del primer registro del CSV
                flight_date = self.df['timestamp'].iloc[0]
            
            # Convertir a timestamp Unix para API de datos históricos
            unix_timestamp = int(flight_date.timestamp())
            
            # Determinar si usar API actual o histórica
            from datetime import datetime as dt, timedelta
            days_ago = (dt.now() - flight_date).days
            
            if days_ago > 5:
                # Usar API de datos históricos (requiere plan de pago en OpenWeatherMap)
                # Para demo, usaremos la API actual con advertencia
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                is_historical = True
            else:
                # Usar API de datos actuales
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                is_historical = False
                
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                weather_data = response.json()
                
                # Extraer datos relevantes
                external_data = {
                    'temperatura_externa': weather_data['main']['temp'],
                    'presion_externa': weather_data['main']['pressure'] / 10,  # hPa a kPa
                    'humedad': weather_data['main']['humidity'],
                    'descripcion': weather_data['weather'][0]['description'],
                    'ubicacion': weather_data['name']
                }
                
                # Calcular promedios del sensor
                sensor_avg = {
                    'temperatura_sensor': self.df['temperatura'].mean(),
                    'presion_sensor': self.df['presion'].mean(),
                }
                
                # Calcular diferencias
                comparisons = {
                    'diff_temperatura': sensor_avg['temperatura_sensor'] - external_data['temperatura_externa'],
                    'diff_temperatura_pct': ((sensor_avg['temperatura_sensor'] - external_data['temperatura_externa']) / external_data['temperatura_externa']) * 100,
                    'diff_presion': sensor_avg['presion_sensor'] - external_data['presion_externa'],
                    'diff_presion_pct': ((sensor_avg['presion_sensor'] - external_data['presion_externa']) / external_data['presion_externa']) * 100,
                }
                
                # Crear gráficas comparativas
                fig = go.Figure()
                
                # Gráfica de comparación de temperatura
                fig.add_trace(go.Bar(
                    x=['Sensor', 'Meteorológico'],
                    y=[sensor_avg['temperatura_sensor'], external_data['temperatura_externa']],
                    name='Temperatura (°C)',
                    marker_color=['blue', 'orange']
                ))
                
                fig.update_layout(
                    title=f'Comparación: Sensor vs Datos Meteorológicos ({external_data["ubicacion"]})',
                    yaxis_title='Temperatura (°C)',
                    showlegend=True
                )
                
                plot_temp = plot(fig, output_type='div')
                
                # Gráfica de comparación de presión
                fig2 = go.Figure()
                
                fig2.add_trace(go.Bar(
                    x=['Sensor', 'Meteorológico'],
                    y=[sensor_avg['presion_sensor'], external_data['presion_externa']],
                    name='Presión (kPa)',
                    marker_color=['green', 'red']
                ))
                
                fig2.update_layout(
                    title=f'Comparación de Presión: Sensor vs Meteorológico',
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
                    'warning': 'Usando datos meteorológicos actuales (API histórica requiere suscripción)' if is_historical else None
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
        """Interpretar las diferencias entre sensor y datos meteorológicos"""
        interpretations = []
        
        # Temperatura
        if abs(comparisons['diff_temperatura']) < 2:
            interpretations.append("✅ Temperatura del sensor muy precisa (diferencia < 2°C)")
        elif abs(comparisons['diff_temperatura']) < 5:
            interpretations.append("⚠️ Temperatura del sensor aceptable (diferencia < 5°C)")
        else:
            interpretations.append("❌ Temperatura del sensor con desviación significativa (diferencia > 5°C)")
        
        # Presión
        if abs(comparisons['diff_presion']) < 1:
            interpretations.append("✅ Presión del sensor muy precisa (diferencia < 1 kPa)")
        elif abs(comparisons['diff_presion']) < 2:
            interpretations.append("⚠️ Presión del sensor aceptable (diferencia < 2 kPa)")
        else:
            interpretations.append("❌ Presión del sensor con desviación significativa (diferencia > 2 kPa)")
        
        return interpretations
    
    # ===== REQUERIMIENTO 2: DIAGNÓSTICO DE EVENTOS Y ATMÓSFERA =====
    
    def identify_flight_phases(self):
        """
        Requerimiento 2.1: Identificar y graficar las fases del vuelo (ascenso, apogeo, descenso)
        """
        # Calcular velocidad vertical (derivada de altura respecto al tiempo)
        self.df['velocidad_vertical'] = self.df['altura'].diff() / self.df['timestamp'].diff().dt.total_seconds()
        
        # Suavizar la velocidad para reducir ruido
        window_size = 20
        self.df['velocidad_suavizada'] = self.df['velocidad_vertical'].rolling(window=window_size, center=True).mean()
        
        # Identificar apogeo (altura máxima)
        apogee_idx = self.df['altura'].idxmax()
        apogee_time = self.df.loc[apogee_idx, 'timestamp']
        apogee_height = self.df.loc[apogee_idx, 'altura']
        
        # Dividir las fases
        ascent = self.df[self.df['timestamp'] <= apogee_time]
        descent = self.df[self.df['timestamp'] > apogee_time]
        
        # Crear gráfica de fases
        fig = go.Figure()
        
        # Fase de ascenso
        fig.add_trace(go.Scatter(
            x=ascent['timestamp'],
            y=ascent['altura'],
            mode='lines',
            name='Ascenso',
            line=dict(color='green', width=2)
        ))
        
        # Fase de descenso
        fig.add_trace(go.Scatter(
            x=descent['timestamp'],
            y=descent['altura'],
            mode='lines',
            name='Descenso',
            line=dict(color='red', width=2)
        ))
        
        # Marcar apogeo
        fig.add_trace(go.Scatter(
            x=[apogee_time],
            y=[apogee_height],
            mode='markers+text',
            name='Apogeo',
            marker=dict(size=15, color='orange', symbol='star'),
            text=[f'Apogeo: {apogee_height:.2f} m'],
            textposition='top center'
        ))
        
        fig.update_layout(
            title='Fases del Vuelo del Cohete',
            xaxis_title='Tiempo',
            yaxis_title='Altura (m)',
            hovermode='x unified'
        )
        
        phase_stats = {
            'apogeo_altura': apogee_height,
            'apogeo_tiempo': apogee_time.strftime('%Y-%m-%d %H:%M:%S'),
            'duracion_ascenso': (apogee_time - self.df['timestamp'].min()).total_seconds(),
            'duracion_descenso': (self.df['timestamp'].max() - apogee_time).total_seconds(),
            'velocidad_max_ascenso': ascent['velocidad_suavizada'].max(),
            'velocidad_max_descenso': abs(descent['velocidad_suavizada'].min())
        }
        
        return {
            'plot': plot(fig, output_type='div'),
            'stats': phase_stats
        }
    
    def analyze_parachute_deployment(self):
        """
        Requerimiento 2.2: Analizar tasa de cambio de presión durante el descenso 
        para confirmar despliegue del paracaídas
        """
        # Identificar apogeo
        apogee_idx = self.df['altura'].idxmax()
        descent_data = self.df.loc[apogee_idx:].copy()
        
        # Calcular tasa de cambio de presión
        descent_data['tasa_presion'] = descent_data['presion'].diff() / descent_data['timestamp'].diff().dt.total_seconds()
        descent_data['velocidad_vertical'] = descent_data['altura'].diff() / descent_data['timestamp'].diff().dt.total_seconds()
        
        # Suavizar datos
        window = 15
        descent_data['tasa_presion_suave'] = descent_data['tasa_presion'].rolling(window=window, center=True).mean()
        descent_data['velocidad_suave'] = descent_data['velocidad_vertical'].rolling(window=window, center=True).mean()
        
        # Detectar cambio brusco en velocidad de descenso (indicador de paracaídas)
        # Un paracaídas causa una desaceleración repentina (velocidad menos negativa)
        aceleracion = descent_data['velocidad_suave'].diff()
        
        # Buscar picos de aceleración positiva (desaceleración del descenso)
        if len(aceleracion.dropna()) > 0:
            threshold = aceleracion.std() * 2
            parachute_candidates = descent_data[aceleracion > threshold]
            
            if len(parachute_candidates) > 0:
                parachute_idx = parachute_candidates.index[0]
                parachute_time = descent_data.loc[parachute_idx, 'timestamp']
                parachute_height = descent_data.loc[parachute_idx, 'altura']
                parachute_detected = True
            else:
                parachute_time = None
                parachute_height = None
                parachute_detected = False
        else:
            parachute_time = None
            parachute_height = None
            parachute_detected = False
        
        # Crear gráfica
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=descent_data['timestamp'],
            y=descent_data['tasa_presion_suave'],
            mode='lines',
            name='Tasa de Cambio de Presión',
            line=dict(color='blue', width=2)
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
        
        fig.update_layout(
            title='Análisis de Despliegue de Paracaídas (Tasa de Cambio de Presión)',
            xaxis_title='Tiempo',
            yaxis_title='Tasa de Cambio de Presión (kPa/s)',
            hovermode='x unified'
        )
        
        return {
            'plot': plot(fig, output_type='div'),
            'parachute_detected': parachute_detected,
            'parachute_time': parachute_time.strftime('%Y-%m-%d %H:%M:%S') if parachute_detected else 'No detectado',
            'parachute_height': parachute_height if parachute_detected else None
        }
    
    def calculate_air_density(self):
        """
        Requerimiento 2.3: Calcular densidad del aire durante el vuelo
        
        Ecuación de densidad del aire:
        ρ = (P * M) / (R * T)
        
        Donde:
        - P = presión (Pa)
        - M = masa molar del aire = 0.029 kg/mol
        - R = constante de gases = 8.314 J/(mol·K)
        - T = temperatura (K)
        """
        # Convertir a unidades SI
        self.df['presion_pa'] = self.df['presion'] * 1000  # kPa a Pa
        self.df['temperatura_k'] = self.df['temperatura'] + 273.15  # °C a K
        
        # Constantes
        M = 0.029  # kg/mol
        R = 8.314  # J/(mol·K)
        
        # Calcular densidad
        self.df['densidad_aire'] = (self.df['presion_pa'] * M) / (R * self.df['temperatura_k'])
        
        # Estadísticas
        density_stats = {
            'densidad_promedio': self.df['densidad_aire'].mean(),
            'densidad_max': self.df['densidad_aire'].max(),
            'densidad_min': self.df['densidad_aire'].min(),
            'densidad_std': self.df['densidad_aire'].std()
        }
        
        # Gráfica
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.df['timestamp'],
            y=self.df['densidad_aire'],
            mode='lines',
            name='Densidad del Aire',
            line=dict(color='purple', width=2)
        ))
        
        fig.update_layout(
            title='Densidad del Aire Durante el Vuelo',
            xaxis_title='Tiempo',
            yaxis_title='Densidad (kg/m³)',
            hovermode='x unified'
        )
        
        return {
            'plot': plot(fig, output_type='div'),
            'stats': density_stats,
            'impact_analysis': self._analyze_density_impact(self.df)
        }
    
    def _analyze_density_impact(self, df):
        """Analizar cómo la densidad del aire pudo afectar el rendimiento"""
        # Calcular resistencia del aire aproximada (proporcional a densidad)
        apogee_idx = df['altura'].idxmax()
        
        avg_density_ascent = df.loc[:apogee_idx, 'densidad_aire'].mean()
        avg_density_descent = df.loc[apogee_idx:, 'densidad_aire'].mean()
        
        impact = {
            'densidad_promedio_ascenso': avg_density_ascent,
            'densidad_promedio_descenso': avg_density_descent,
            'diferencia_porcentual': ((avg_density_descent - avg_density_ascent) / avg_density_ascent) * 100,
            'interpretacion': self._get_density_interpretation(avg_density_ascent, avg_density_descent)
        }
        
        return impact
    
    def _get_density_interpretation(self, ascent_density, descent_density):
        """Interpretar el impacto de la densidad del aire"""
        if descent_density > ascent_density:
            return "Mayor densidad en descenso aumenta la resistencia del aire, mejorando la efectividad del paracaídas."
        else:
            return "Menor densidad en descenso reduce la resistencia del aire, posiblemente afectando la efectividad del paracaídas."
    
    def detect_anomalies(self):
        """
        Requerimiento 2.4: Investigar anomalías en los datos (picos, caídas inesperadas)
        """
        anomalies = []
        
        # Detectar picos anómalos en temperatura
        temp_mean = self.df['temperatura'].mean()
        temp_std = self.df['temperatura'].std()
        temp_threshold = 3 * temp_std
        
        temp_anomalies = self.df[abs(self.df['temperatura'] - temp_mean) > temp_threshold]
        
        if len(temp_anomalies) > 0:
            for idx, row in temp_anomalies.iterrows():
                anomalies.append({
                    'tipo': 'Temperatura',
                    'timestamp': row['timestamp'],
                    'valor': row['temperatura'],
                    'altura': row['altura'],
                    'causa_probable': 'Exposición directa al sol o sombra repentina'
                })
        
        # Detectar picos anómalos en presión
        pressure_mean = self.df['presion'].mean()
        pressure_std = self.df['presion'].std()
        pressure_threshold = 3 * pressure_std
        
        pressure_anomalies = self.df[abs(self.df['presion'] - pressure_mean) > pressure_threshold]
        
        if len(pressure_anomalies) > 0:
            for idx, row in pressure_anomalies.iterrows():
                anomalies.append({
                    'tipo': 'Presión',
                    'timestamp': row['timestamp'],
                    'valor': row['presion'],
                    'altura': row['altura'],
                    'causa_probable': 'Vibración mecánica o interferencia del sensor'
                })
        
        # Detectar cambios bruscos (derivadas grandes)
        self.df['temp_change_rate'] = self.df['temperatura'].diff().abs()
        self.df['pressure_change_rate'] = self.df['presion'].diff().abs()
        
        sudden_temp_changes = self.df[self.df['temp_change_rate'] > self.df['temp_change_rate'].quantile(0.99)]
        sudden_pressure_changes = self.df[self.df['pressure_change_rate'] > self.df['pressure_change_rate'].quantile(0.99)]
        
        # Crear gráfica de anomalías
        fig = go.Figure()
        
        # Temperatura normal
        fig.add_trace(go.Scatter(
            x=self.df['timestamp'],
            y=self.df['temperatura'],
            mode='lines',
            name='Temperatura',
            line=dict(color='red', width=1)
        ))
        
        # Marcar anomalías de temperatura
        if len(temp_anomalies) > 0:
            fig.add_trace(go.Scatter(
                x=temp_anomalies['timestamp'],
                y=temp_anomalies['temperatura'],
                mode='markers',
                name='Anomalías Temperatura',
                marker=dict(size=10, color='darkred', symbol='x')
            ))
        
        fig.update_layout(
            title='Detección de Anomalías en Temperatura',
            xaxis_title='Tiempo',
            yaxis_title='Temperatura (°C)',
            hovermode='x unified'
        )
        
        return {
            'plot': plot(fig, output_type='div'),
            'anomalies': anomalies,
            'total_anomalies': len(anomalies)
        }
    
    # ===== REQUERIMIENTO 3: OPTIMIZACIÓN BASADA EN EVIDENCIA =====
    
    def analyze_success_formula(self):
        """
        Requerimiento 3.1: Determinar qué combinación de presión y condiciones 
        generó el mejor apogeo
        """
        apogee_idx = self.df['altura'].idxmax()
        best_conditions = self.df.loc[apogee_idx]
        
        # Analizar condiciones en el momento del lanzamiento (primeros registros)
        launch_conditions = self.df.iloc[:10].mean()
        
        # Analizar condiciones en el apogeo
        apogee_conditions = {
            'altura_maxima': best_conditions['altura'],
            'tiempo_al_apogeo': (best_conditions['timestamp'] - self.df['timestamp'].min()).total_seconds(),
            'temperatura_apogeo': best_conditions['temperatura'],
            'presion_apogeo': best_conditions['presion']
        }
        
        launch_analysis = {
            'presion_inicial': launch_conditions['presion'],
            'temperatura_inicial': launch_conditions['temperatura'],
            'altura_inicial': launch_conditions['altura']
        }
        
        # Crear visualización
        fig = go.Figure()
        
        # Trayectoria completa
        fig.add_trace(go.Scatter(
            x=self.df['timestamp'],
            y=self.df['altura'],
            mode='lines',
            name='Trayectoria',
            line=dict(color='blue', width=2)
        ))
        
        # Marcar punto de lanzamiento
        fig.add_trace(go.Scatter(
            x=[self.df['timestamp'].min()],
            y=[self.df['altura'].min()],
            mode='markers+text',
            name='Lanzamiento',
            marker=dict(size=15, color='green', symbol='triangle-up'),
            text=[f'Inicio<br>P: {launch_analysis["presion_inicial"]:.2f} kPa'],
            textposition='bottom center'
        ))
        
        # Marcar apogeo
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
            'recommendations': self._generate_recommendations(launch_analysis, apogee_conditions)
        }
    
    def _generate_recommendations(self, launch, apogee):
        """Generar recomendaciones basadas en el análisis"""
        recommendations = [
            f"Presión de lanzamiento óptima: {launch['presion_inicial']:.2f} kPa",
            f"Temperatura ambiente ideal: {launch['temperatura_inicial']:.2f}°C",
            f"Altura máxima alcanzada: {apogee['altura_maxima']:.2f} m",
            f"Tiempo de vuelo hasta apogeo: {apogee['tiempo_al_apogeo']:.2f} segundos"
        ]
        return recommendations
    
    def get_comprehensive_analysis(self, weather_date=None):
        """
        Generar un análisis comprensivo con todos los requerimientos
        
        Args:
            weather_date: Fecha específica para consultar datos meteorológicos (formato 'YYYY-MM-DD')
        """
        results = {
            'validation': self.validate_theoretical_altitude(),
            'weather_comparison': self.environmental_dashboard(target_date=weather_date),  # Req 1.2 con fecha específica
            'altitude_pressure': self.altitude_pressure_curve(),
            'flight_phases': self.identify_flight_phases(),
            'parachute': self.analyze_parachute_deployment(),
            'air_density': self.calculate_air_density(),
            'anomalies': self.detect_anomalies(),
            'success_formula': self.analyze_success_formula()
        }
        
        return results