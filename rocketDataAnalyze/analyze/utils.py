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