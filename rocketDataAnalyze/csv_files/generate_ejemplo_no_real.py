import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuración
sample_rate = 20  # 20 muestras por segundo
dt = 1.0 / sample_rate  # 0.05 segundos

# Condiciones iniciales (Popayán, Colombia)
P0 = 81.43  # Presión en Popayán (kPa) - altura ~1800m
T0 = 22.0   # Temperatura inicial °C
alt0 = 1738.0  # Altura inicial de Popayán (metros sobre nivel del mar)

data = []
current_time = datetime(2025, 11, 26, 14, 30, 0)
sample_id = 1

print("Generando datos de cohete simulado...")

# ===== FASE 1: PREPARACIÓN (2 segundos) =====
print("Fase 1: Preparación...")
for i in range(40):
    noise_alt = np.random.normal(0, 0.1)
    noise_temp = np.random.normal(0, 0.05)
    noise_press = np.random.normal(0, 0.005)
    
    data.append({
        'id': sample_id,
        'temperatura': T0 + noise_temp,
        'presion': P0 + noise_press,
        'altura': alt0 + noise_alt,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    })
    current_time += timedelta(seconds=dt)
    sample_id += 1

# ===== FASE 2: LANZAMIENTO Y ASCENSO ACELERADO (0.8 segundos) =====
print("Fase 2: Lanzamiento y ascenso acelerado...")
t_impulso = 0.8
samples_impulso = int(t_impulso * sample_rate)
v_max = 45  # velocidad máxima m/s

for i in range(samples_impulso):
    t = i * dt
    accel = 60 * np.exp(-t/0.3)
    v = v_max * (1 - np.exp(-t/0.2))
    
    alt = alt0 + v * t + 0.5 * accel * t**2
    temp = T0 - 1.5 * (alt - alt0) / 50 + np.random.normal(0, 0.15)
    press = P0 * np.exp(-0.00012 * (alt - alt0)) + np.random.normal(0, 0.01)
    
    data.append({
        'id': sample_id,
        'temperatura': temp,
        'presion': press,
        'altura': alt,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    })
    current_time += timedelta(seconds=dt)
    sample_id += 1

alt_post_impulso = data[-1]['altura']
v_inicial_balistica = v_max

# ===== FASE 3: ASCENSO BALÍSTICO (2.5 segundos) =====
print("Fase 3: Ascenso balístico...")
t_balistica = 2.5
samples_balistica = int(t_balistica * sample_rate)
g = 9.81
drag_coef = 0.15

for i in range(samples_balistica):
    t = i * dt
    v = v_inicial_balistica * np.exp(-drag_coef * t) - g * t
    
    if v < 0:
        break
    
    alt = alt_post_impulso + v_inicial_balistica * t * np.exp(-drag_coef * t / 2) - 0.5 * g * t**2
    temp = T0 - 1.8 * (alt - alt0) / 50 + np.random.normal(0, 0.1)
    press = P0 * np.exp(-0.00012 * (alt - alt0)) + np.random.normal(0, 0.008)
    
    data.append({
        'id': sample_id,
        'temperatura': temp,
        'presion': press,
        'altura': alt,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    })
    current_time += timedelta(seconds=dt)
    sample_id += 1

# ===== FASE 4: APOGEO (0.3 segundos) =====
print("Fase 4: Apogeo...")
alt_apogeo = data[-1]['altura']
samples_apogeo = int(0.3 * sample_rate)

for i in range(samples_apogeo):
    noise_alt = np.random.normal(0, 0.5)
    noise_temp = np.random.normal(0, 0.2)
    noise_press = np.random.normal(0, 0.01)
    
    temp = T0 - 1.8 * (alt_apogeo - alt0) / 50 + noise_temp
    press = P0 * np.exp(-0.00012 * (alt_apogeo - alt0)) + noise_press
    
    data.append({
        'id': sample_id,
        'temperatura': temp,
        'presion': press,
        'altura': alt_apogeo + noise_alt,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    })
    current_time += timedelta(seconds=dt)
    sample_id += 1

# ===== FASE 5: DESCENSO SIN PARACAÍDAS (1 segundo) =====
print("Fase 5: Caída libre...")
t_caida_libre = 1.0
samples_caida = int(t_caida_libre * sample_rate)
v_descenso = 0

for i in range(samples_caida):
    t = i * dt
    v_descenso = g * t * 0.7
    alt = alt_apogeo - 0.5 * g * 0.7 * t**2
    
    if alt <= alt0:
        alt = alt0
        break
    
    temp = T0 - 1.5 * (alt - alt0) / 50 + np.random.normal(0, 0.15)
    press = P0 * np.exp(-0.00012 * (alt - alt0)) + np.random.normal(0, 0.01)
    
    data.append({
        'id': sample_id,
        'temperatura': temp,
        'presion': press,
        'altura': alt,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    })
    current_time += timedelta(seconds=dt)
    sample_id += 1

alt_antes_paracaidas = data[-1]['altura']

# ===== FASE 6: DESPLIEGUE Y DESCENSO CON PARACAÍDAS (3.5 segundos) =====
print("Fase 6: Descenso con paracaídas...")
t_paracaidas = 3.5
samples_paracaidas = int(t_paracaidas * sample_rate)
v_terminal = 6

for i in range(samples_paracaidas):
    t = i * dt
    v = v_terminal * (1 - np.exp(-2*t)) + v_descenso * np.exp(-2*t)
    alt = alt_antes_paracaidas - v_terminal * t + (v_descenso - v_terminal) * 0.5 * (1 - np.exp(-2*t))
    
    if alt <= alt0:
        alt = alt0 + np.random.normal(0, 0.05)
        break
    
    temp = T0 - 1.2 * (alt - alt0) / 50 + np.random.normal(0, 0.1)
    press = P0 * np.exp(-0.00012 * (alt - alt0)) + np.random.normal(0, 0.008)
    
    data.append({
        'id': sample_id,
        'temperatura': temp,
        'presion': press,
        'altura': alt,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    })
    current_time += timedelta(seconds=dt)
    sample_id += 1

# ===== FASE 7: ATERRIZAJE (0.5 segundos) =====
print("Fase 7: Aterrizaje...")
samples_aterrizaje = int(0.5 * sample_rate)

for i in range(samples_aterrizaje):
    noise_alt = np.random.normal(0, 0.1)
    noise_temp = np.random.normal(0, 0.05)
    noise_press = np.random.normal(0, 0.005)
    
    data.append({
        'id': sample_id,
        'temperatura': T0 + noise_temp + 0.3,
        'presion': P0 + noise_press,
        'altura': alt0 + noise_alt,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    })
    current_time += timedelta(seconds=dt)
    sample_id += 1

# Crear DataFrame y guardar
df = pd.DataFrame(data)
df.to_csv('ejemplo_no_real.csv', index=False)

print("\n" + "="*60)
print("✅ Archivo creado: ejemplo_no_real.csv")
print("="*60)
print(f"📊 Total de muestras: {len(df)}")
print(f"⏱️  Frecuencia de muestreo: {sample_rate} Hz (20 datos/segundo)")
print(f"⏱️  Duración total: {len(df)/sample_rate:.2f} segundos")
print(f"🚀 Altura máxima sobre lanzamiento: {df['altura'].max() - alt0:.2f} metros")
print(f"📍 Altura absoluta máxima: {df['altura'].max():.2f} metros snm")
print(f"🌡️  Temperatura promedio: {df['temperatura'].mean():.2f} °C")
print(f"💨 Presión promedio: {df['presion'].mean():.2f} kPa")
print("="*60)
print("\n📋 Fases del vuelo simuladas:")
print("  1. Preparación (2s)")
print("  2. Lanzamiento acelerado (0.8s)")
print("  3. Ascenso balístico (2.5s)")
print("  4. Apogeo (0.3s)")
print("  5. Caída libre (1s)")
print("  6. Descenso con paracaídas (3.5s)")
print("  7. Aterrizaje (0.5s)")
print("="*60)
