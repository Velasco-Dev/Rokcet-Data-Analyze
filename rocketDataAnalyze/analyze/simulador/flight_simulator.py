#!/usr/bin/env python3
"""
Generador de Simulaciones de Vuelo de Cohete

Este script genera simulaciones realistas y exitosas de vuelo de cohetes de agua
basándose en parámetros de presión (PSI) y volumen de agua (mL).
Todas las simulaciones son exitosas y generan archivos CSV.
"""

import csv
import numpy as np
import random
import sys
from typing import Dict, List, Any
from datetime import datetime, timedelta


class RocketFlightSimulationGenerator:
    """
    Generador de simulaciones de vuelo de cohete.
    
    Funcionalidades:
    - Genera simulaciones basadas en parámetros PSI y mL de agua
    - Añade variaciones aleatorias en ruido y timing
    - Simula eventos de vuelo con duración variable (6-8 segundos)
    - Produce CSVs con ~1,200-1,500 registros a 100 Hz (60-65% durante el vuelo)
    """
    
    def __init__(self):
        """Inicializa el generador con datos base del CSV real."""
        # Datos base del sensor_data_3.csv (lanzamiento real con ~500mL y ~45-50 PSI)
        self.base_stats = {
            'temperatura': {
                'min': 25.0,
                'max': 25.4,
                'mean': 25.2,
                'std': 0.1
            },
            'presion': {
                'min': 3200.0,
                'max': 3300.0,
                'mean': 3250.0,
                'std': 25.0
            },
            'altura': {
                'min': 160.0,
                'max': 163.0,
                'mean': 161.5,
                'std': 0.3
            }
        }
    
    def calculate_flight_parameters(self, psi: float, water_ml: float) -> Dict[str, Any]:
        """
        Calcula parámetros de vuelo basados en PSI y mL de agua.
        
        Args:
            psi: Presión de lanzamiento en PSI
            water_ml: Volumen de agua en mL
            
        Returns:
            Diccionario con parámetros ajustados para la simulación
        """
        # Factor de presión (45-50 PSI es óptimo)
        pressure_factor = psi / 47.5  # Normalizar a presión óptima
        
        # Factor de agua (500mL es óptimo)
        water_factor = water_ml / 500.0  # Normalizar a volumen óptimo
        
        # Ajustar estadísticas base según parámetros
        adjusted_stats = {
            'temperatura': {
                'mean': self.base_stats['temperatura']['mean'],
                'std': self.base_stats['temperatura']['std']
            },
            'presion': {
                'mean': self.base_stats['presion']['mean'] * pressure_factor,
                'std': self.base_stats['presion']['std'] * pressure_factor
            },
            'altura': {
                'mean': self.base_stats['altura']['mean'],
                'std': self.base_stats['altura']['std']
            },
            'flight_intensity': min(pressure_factor * water_factor, 1.5),  # Factor de intensidad del vuelo
            'max_altitude_gain': 13.5 * pressure_factor * water_factor  # Ganancia máxima de altura (12-15m)
        }
        
        return adjusted_stats
    
    def add_noise(self, value: float, noise_factor: float = 0.01) -> float:
        """
        Añade ruido aleatorio mucho más intenso para simular sensores reales.
        
        Args:
            value: Valor original
            noise_factor: Factor de ruido (0.02 = 2%)
            
        Returns:
            Valor con ruido añadido
        """
        # Ruido gaussiano base (más suave)
        gaussian_noise = np.random.normal(0, value * noise_factor * 0.3)
        
        # Añadir componentes adicionales para más variabilidad (reducidos)
        # Ruido de alta frecuencia (variaciones rápidas más sutiles)
        high_freq_noise = np.random.uniform(-value * noise_factor * 0.15, value * noise_factor * 0.15)
        
        # Ruido impulsivo ocasional muy reducido (picos aleatorios más pequeños)
        impulse_noise = 0
        if random.random() < 0.02:  # 2% de probabilidad de pico aún más reducido
            impulse_noise = np.random.uniform(-value * noise_factor * 0.25, value * noise_factor * 0.25)
        
        return value + gaussian_noise + high_freq_noise + impulse_noise
    
    def add_absolute_noise(self, value: float, noise_amplitude: float = 0.05) -> float:
        """
        Añade ruido absoluto (no porcentual) para valores pequeños como temperatura.
        
        Args:
            value: Valor original
            noise_amplitude: Amplitud del ruido en unidades absolutas
            
        Returns:
            Valor con ruido añadido
        """
        # Ruido gaussiano base
        gaussian_noise = np.random.normal(0, noise_amplitude * 0.3)
        
        # Ruido de alta frecuencia
        high_freq_noise = np.random.uniform(-noise_amplitude * 0.15, noise_amplitude * 0.15)
        
        # Ruido impulsivo ocasional
        impulse_noise = 0
        if random.random() < 0.02:
            impulse_noise = np.random.uniform(-noise_amplitude * 0.25, noise_amplitude * 0.25)
        
        return value + gaussian_noise + high_freq_noise + impulse_noise
    
    def generate_flight_event(self, start_index: int, duration: int, 
                            flight_params: Dict[str, Any], parachute_opened: bool = True) -> List[Dict[str, float]]:
        """
        Genera un evento de vuelo con cambios físicamente realistas.
        
        Args:
            start_index: Índice donde comienza el vuelo
            duration: Duración del vuelo en registros
            flight_params: Parámetros calculados del vuelo
            parachute_opened: Si el paracaídas se abrió (True) o no (False)
            
        Returns:
            Lista de modificaciones para el evento de vuelo
        """
        flight_mods = []
        max_height_gain = flight_params['max_altitude_gain']
        
        for i in range(duration):
            progress = i / duration
            
            # Calcular altura relativa para efectos físicos
            if parachute_opened:
                # CON PARACAÍDAS: Subida MÁS vertical (30%), descenso lento y suave (70%)
                if progress < 0.3:  # Subida MÁS vertical
                    relative_height = (progress / 0.3) ** 0.5 * max_height_gain
                else:  # Descenso lento con paracaídas - muy curvo y suave
                    descent_progress = (progress - 0.3) / 0.7
                    relative_height = max_height_gain * (1 - descent_progress ** 1.5)
            else:
                # SIN PARACAÍDAS: Subida MÁS vertical (50%), caída SECA y MÁS vertical (50%)
                # "Seco" = misma velocidad de subida pero invertida (simétrica)
                if progress < 0.5:  # Subida MÁS vertical
                    relative_height = (progress / 0.5) ** 0.5 * max_height_gain
                else:  # Caída SECA y MÁS vertical - similar velocidad que subida pero invertida
                    descent_progress = (progress - 0.5) / 0.5
                    relative_height = max_height_gain * (1 - descent_progress ** 0.5)  # Caída simétrica MÁS vertical
            
            # PRESIÓN: Disminuye con altura según fórmula barométrica
            pressure_change = -relative_height * 15  # Ajustado para unidades del CSV
            
            # TEMPERATURA: Efectos físicos realistas
            if i == 0:  # Lanzamiento: caída brusca por expansión Joule-Thomson
                temp_delta = -0.3
            elif progress < 0.3:  # Recuperación gradual
                temp_delta = -0.3 + (progress / 0.3) * 0.4
            elif progress < 0.7:  # Gradiente adiabático: -0.65°C/100m
                temp_delta = 0.1 - (relative_height * 0.003)
            else:  # Regreso a temperatura inicial
                temp_delta = 0.1 - (relative_height * 0.003) + (progress - 0.7) / 0.3 * 0.1
            
            # Altura: comportamiento según paracaídas
            if parachute_opened:
                # CON PARACAÍDAS: subida MÁS vertical, descenso suave
                if progress < 0.3:
                    height_delta = (progress / 0.3) ** 0.5 * max_height_gain
                else:
                    descent_progress = (progress - 0.3) / 0.7
                    height_delta = max_height_gain * (1 - descent_progress ** 1.5)
            else:
                # SIN PARACAÍDAS: subida MÁS vertical, caída SECA y MÁS vertical (simétrica)
                if progress < 0.5:
                    height_delta = (progress / 0.5) ** 0.5 * max_height_gain
                else:
                    descent_progress = (progress - 0.5) / 0.5
                    height_delta = max_height_gain * (1 - descent_progress ** 0.5)  # Caída simétrica MÁS vertical
            
            flight_mods.append({
                'index': start_index + i,
                'temp_delta': temp_delta,
                'pressure_delta': pressure_change,
                'height_delta': height_delta
            })
        
        return flight_mods
    
    def generate_simulation(self, psi: float, water_ml: float, target_records: int = None, 
                          flight_duration: int = None, flight_start: int = None,
                          noise_level: float = 0.02, parachute_opened: bool = True) -> List[Dict[str, Any]]:
        """
        Genera una simulación completa de vuelo.
        
        Args:
            psi: Presión de lanzamiento en PSI
            water_ml: Volumen de agua en mL
            target_records: Número objetivo de registros (ajustado según paracaídas)
            flight_duration: Duración del vuelo en registros (según paracaídas si None)
            flight_start: Posición de inicio del vuelo (80-120 registros = 2-3 segundos a 40 Hz si None)
            noise_level: Nivel de ruido (0.02 por defecto)
            parachute_opened: Si el paracaídas se abrió (True) o no (False)
            
        Returns:
            Lista de objetos con la simulación generada
        """
        # Parámetros aleatorios si no se especifican
        if target_records is None:
            if parachute_opened:
                # CON PARACAÍDAS: ~8-10 segundos totales a 40 Hz
                target_records = random.randint(320, 400)
            else:
                # SIN PARACAÍDAS: ~6-8 segundos totales a 40 Hz (vuelo más corto)
                target_records = random.randint(240, 320)
        
        if flight_duration is None:
            if parachute_opened:
                # CON PARACAÍDAS: 6-8 segundos de vuelo = 240-320 registros a 40 Hz
                flight_duration = random.randint(240, 320)
            else:
                # SIN PARACAÍDAS: ~5 segundos de vuelo = 200 registros a 40 Hz
                flight_duration = 200
        
        if flight_start is None:
            # Pre-vuelo: 2-3 segundos = 80-120 registros a 40 Hz
            min_start = 80
            max_start = 120
            flight_start = random.randint(min_start, max_start)
        
        # Calcular parámetros de vuelo basados en PSI y mL
        flight_params = self.calculate_flight_parameters(psi, water_ml)
        
        # Generar evento de vuelo con física realista
        flight_mods = self.generate_flight_event(flight_start, flight_duration, flight_params, parachute_opened)
        
        # Crear simulación
        simulation = []
        
        # Generar hora de inicio aleatoria (entre 08:00:00 y 20:00:00)
        start_hour = random.randint(8, 19)
        start_minute = random.randint(0, 59)
        start_second = random.randint(0, 59)
        base_time = datetime(2025, 11, random.randint(1, 28), start_hour, start_minute, start_second)
        
        for i in range(target_records):
            # Valores base con variación muy ligera
            base_temp = flight_params['temperatura']['mean'] + random.uniform(-0.02, 0.02)
            base_pressure = flight_params['presion']['mean'] + random.uniform(-20, 20)
            base_height = self.base_stats['altura']['mean'] + random.uniform(-0.2, 0.2)
            
            # Añadir ruido realista con niveles ajustados
            # Temperatura: ruido ABSOLUTO (no porcentual) aún más bajo
            temperature = round(self.add_absolute_noise(base_temp, 0.02), 4)  # Ruido absoluto ±0.02°C
            # Presión y Altura: ruido porcentual más bajo
            pressure = round(self.add_noise(base_pressure, noise_level * 0.08), 4)  # Ruido más bajo
            height = round(self.add_noise(base_height, noise_level * 0.15), 4)  # Ruido más bajo
            
            # Aplicar modificaciones de vuelo si corresponde
            for mod in flight_mods:
                if mod['index'] == i:
                    temperature = round(temperature + mod['temp_delta'], 2)
                    pressure = round(pressure + mod['pressure_delta'], 2)
                    height = round(height + mod['height_delta'], 2)
                    break
            
            # Generar timestamp progresivo (40 Hz = 25ms por registro)
            # Para ~320-400 registros a 40Hz = ~8-10 segundos totales con paracaídas
            current_time = base_time + timedelta(milliseconds=i * 25)
            # Formato con milisegundos para evitar líneas verticales en gráficas
            timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Cortar a 3 dígitos (ms)
            
            # Crear registro
            record = {
                "id": i + 1,
                "temperatura": temperature,
                "presion": pressure,
                "altura": height,
                "timestamp": timestamp_str
            }
            
            simulation.append(record)
        
        return simulation
    
    def save_simulation(self, simulation_data: List[Dict[str, Any]], 
                      psi: float, water_ml: float, 
                      filename_base: str = None) -> str:
        """
        Guarda los datos de simulación en archivo CSV con formato estándar.
        
        Args:
            simulation_data: Datos de simulación generados
            psi: Presión de lanzamiento en PSI (para nombre del archivo)
            water_ml: Volumen de agua en mL (para nombre del archivo)
            filename_base: Base para el nombre del archivo (por defecto 'simulacion')
            
        Returns:
            Ruta del archivo guardado
        """
        if filename_base is None:
            filename_base = "simulacion"
        
        # Crear nombre de archivo con parámetros
        filename = f"{filename_base}_{psi}PSI_{water_ml}mL.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['id', 'temperatura', 'presion', 'altura', 'timestamp'])
            writer.writeheader()
            writer.writerows(simulation_data)
        
        return filename
    

def predict_max_altitude(psi: float, water_ml: float) -> float:
    """
    Modelo predictivo de altura máxima basado en principios físicos.
    No usa el generador - algoritmo independiente con variación realista.
    
    Args:
        psi: Presión de lanzamiento en PSI
        water_ml: Volumen de agua en mL
        
    Returns:
        Altura máxima predicha en metros
    """
    # Conversiones y constantes físicas
    psi_to_pa = 6894.76  # 1 PSI = 6894.76 Pa
    pressure_pa = psi * psi_to_pa
    water_kg = water_ml / 1000.0  # mL a litros, densidad agua ~1 kg/L
    
    # Volumen aproximado de la botella (típicamente 2L)
    bottle_volume = 0.002  # m³ (2 litros)
    air_volume = bottle_volume - (water_ml / 1000000.0)  # m³
    
    # Energía almacenada en el aire comprimido (aproximación)
    # E = P * V * ln(P/P_atm) para proceso politrópico
    p_atm = 101325  # Pa (presión atmosférica)
    stored_energy = pressure_pa * air_volume * np.log(pressure_pa / p_atm)
    
    # Eficiencia del sistema (pérdidas por fricción, resistencia del aire, etc.)
    efficiency = 0.35 + np.random.uniform(-0.05, 0.05)  # 30-40% eficiencia típica
    
    # Masa total (botella + agua + aire)
    bottle_mass = 0.045  # kg (botella PET típica)
    total_mass = bottle_mass + water_kg
    
    # Energía cinética convertida en altura
    # E_kinetic = efficiency * stored_energy
    # E_potential = m * g * h
    # h = (efficiency * stored_energy) / (m * g)
    g = 9.81  # m/s²
    
    # Altura máxima teórica
    max_height_theory = (efficiency * stored_energy) / (total_mass * g)
    
    # Ajustes empíricos basados en comportamiento real de cohetes de agua
    # Óptimo: ~500mL y ~47.5 PSI -> ~12-15m
    optimal_water = 500.0
    optimal_psi = 47.5
    
    # Factor de óptimo de agua (curva parabólica - muy poca o mucha agua reduce altura)
    water_efficiency = 1.0 - 0.3 * ((water_ml - optimal_water) / optimal_water) ** 2
    water_efficiency = max(0.4, min(1.0, water_efficiency))
    
    # Factor de presión (lineal hasta cierto punto, luego se satura)
    pressure_efficiency = min(1.0, psi / optimal_psi)
    
    # Aplicar factores empíricos
    predicted_height = max_height_theory * water_efficiency * pressure_efficiency
    
    # Escalar a rangos realistas (12-15m para condiciones óptimas)
    # Ajuste empírico basado en datos experimentales de cohetes de agua
    calibration_factor = 0.42  # Factor de calibración ajustado para 12-15m reales
    predicted_height *= calibration_factor
    
    # Añadir variación estocástica para simular incertidumbre del modelo
    prediction_noise = np.random.normal(0, 1.2)  # ±1.2m de incertidumbre
    predicted_height += prediction_noise
    
    # Limitar a rangos físicamente posibles
    predicted_height = max(5.0, min(25.0, predicted_height))
    
    return round(predicted_height, 2)


if __name__ == "__main__":
    print("="*60)
    print("  GENERADOR DE SIMULACIONES DE VUELO DE COHETE DE AGUA")
    print("="*60)
    print()
    
    # Solicitar parámetros por consola
    try:
        psi = float(input("Ingrese la presión de lanzamiento (PSI): "))
        water_ml = float(input("Ingrese el volumen de agua (mL): "))
        
        parachute_input = input("¿Se abrirá el paracaídas? (s/n) [s]: ").strip().lower()
        parachute_opened = parachute_input != 'n' and parachute_input != 'no'
        
        output_base = input("Nombre base del archivo [simulacion]: ").strip()
        if not output_base:
            output_base = "simulacion"
    except ValueError:
        print("Error: Debe ingresar valores numéricos válidos.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
        sys.exit(0)
    
    # Validaciones
    if psi < 20 or psi > 80:
        print(f"Advertencia: PSI {psi} está fuera del rango recomendado (20-80)")
    
    if water_ml < 200 or water_ml > 800:
        print(f"Advertencia: Volumen {water_ml}mL está fuera del rango recomendado (200-800mL)")
    
    print()
    print("="*60)
    print("  FÓRMULA DEL ÉXITO")
    print("="*60)
    print("\n🏆 COMBINACIÓN ÓPTIMA PARA MÁXIMA ALTURA:")
    print("   • Presión: 47-50 PSI")
    print("   • Agua: 480-520 mL")
    print("   • Altura esperada: 13-15 metros")
    print("\n💡 JUSTIFICACIÓN:")
    print("   Esta combinación maximiza la eficiencia energética del cohete. Con ~47.5 PSI, el aire")
    print("   almacena suficiente energía sin comprometer la estructura de la botella. El volumen de")
    print("   ~500mL logra el balance perfecto: suficiente masa de agua para generar impulso prolongado,")
    print("   pero no tanta que aumente excesivamente el peso. Menos agua (<400mL) produce impulso")
    print("   insuficiente y se agota rápido. Más agua (>600mL) aumenta demasiado la masa, reduciendo")
    print("   la aceleración. Este equilibrio hace que el cohete aproveche al máximo la energía del")
    print("   aire comprimido, alcanzando la altura máxima posible para cohetes de agua caseros.")
    
    print()
    print("="*60)
    print("  PREDICCIÓN DE ALTURA MÁXIMA")
    print("="*60)
    
    # Modelo predictivo (independiente del generador)
    predicted_altitude = predict_max_altitude(psi, water_ml)
    print(f"\n🚀 PREDICCIÓN: El cohete alcanzará aproximadamente {predicted_altitude}m de altura")
    print(f"   (Basado en modelo físico: {psi} PSI, {water_ml}mL de agua)")
    
    # Justificación de la predicción
    print("\n📊 JUSTIFICACIÓN DEL MODELO:")
    print("   El modelo calcula la energía almacenada en el aire comprimido usando:")
    print("   energía = presión × volumen_aire × ln(presión / presión_atmosférica)")
    print("   Luego la convierte en altura: altura = (eficiencia × energía) / (masa_total × gravedad)")
    print("   La eficiencia es ~35% (±5% aleatorio) por pérdidas: fricción en la base, resistencia")
    print("   aerodinámica, turbulencia y ángulo no ideal. Aplica factores empíricos: agua en curva")
    print("   parabólica (óptimo 500mL para balance masa/impulso) y presión lineal (óptimo 47.5 PSI).")
    print("   Finalmente calibra con datos reales y añade ruido (±1.2m) para simular incertidumbre.")
    print()
    
    parachute_status = "con paracaídas" if parachute_opened else "SIN paracaídas (caída libre)"
    print("="*60)
    print("  GENERANDO SIMULACIÓN")
    print("="*60)
    print(f"\nSimulación {parachute_status}: {psi} PSI y {water_ml}mL de agua...")
    
    try:
        # Crear generador
        generator = RocketFlightSimulationGenerator()
        
        # Generar simulación
        simulation = generator.generate_simulation(psi=psi, water_ml=water_ml, parachute_opened=parachute_opened)
        
        # Guardar archivo
        output_file = generator.save_simulation(simulation, psi, water_ml, output_base)
        
        print(f"Simulación generada exitosamente:")
        print(f"  - Archivo: {output_file}")
        print(f"  - Registros: {len(simulation)}")
        print(f"  - Parámetros: {psi} PSI, {water_ml}mL")
        print(f"  - Paracaídas: {'Abierto' if parachute_opened else 'No abierto (caída brusca)'}")
        print(f"  - Duración aproximada: {'6-8 segundos' if parachute_opened else '~5 segundos'}")
        
        # Mostrar estadísticas de la simulación
        temps = [r['temperatura'] for r in simulation]
        pressures = [r['presion'] for r in simulation]
        heights = [r['altura'] for r in simulation]
        
        print(f"  - Temperatura: {min(temps):.1f}-{max(temps):.1f}°C")
        print(f"  - Presión: {min(pressures):.1f}-{max(pressures):.1f}")
        print(f"  - Altura: {min(heights):.1f}-{max(heights):.1f}m")
        
        # Comparar predicción vs simulación
        actual_max_height = max(heights)
        height_base = 161.5  # Altura base del sensor
        actual_gain = actual_max_height - height_base
        prediction_error = abs(predicted_altitude - actual_gain)
        
        print()
        print("="*60)
        print("  COMPARACIÓN: PREDICCIÓN vs SIMULACIÓN")
        print("="*60)
        print(f"  Altura predicha por modelo: {predicted_altitude:.2f}m")
        print(f"  Ganancia real en simulación: {actual_gain:.2f}m")
        print(f"  Error de predicción: {prediction_error:.2f}m ({(prediction_error/actual_gain)*100:.1f}%)")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error al generar la simulación: {e}")
        sys.exit(1)