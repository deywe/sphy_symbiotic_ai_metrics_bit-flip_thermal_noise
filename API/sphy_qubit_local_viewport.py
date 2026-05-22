import py5
import numpy as np
import pandas as pd
import hashlib
import os
from tkinter import Tk, filedialog

df_telemetry = None
total_rows = 0
current_frame_idx = 0

# Variáveis de auditoria forense
chain_valid = True
prev_hash = "0" * 64
broken_frame = None

def buscar_arquivo():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    caminho = filedialog.askopenfilename(
        title="Selecione o Log Parquet SPHY",
        filetypes=[("Arquivos Parquet", "*.parquet")]
    )
    root.destroy()
    return caminho

def settings():
    py5.size(1920, 1080, py5.P3D)
    py5.smooth(8)

def setup():
    global df_telemetry, total_rows
    py5.background(0)
    py5.stroke_weight(3)
    
    caminho_arquivo = buscar_arquivo()
    if not caminho_arquivo or not os.path.exists(caminho_arquivo):
        print("❌ Operação abortada pelo operador.")
        py5.exit_sketch()
        return
        
    df_telemetry = pd.read_parquet(caminho_arquivo)
    total_rows = len(df_telemetry)
    print(f"🌌 SPHY Engine Viewport Ativo. Reconstruindo {total_rows} frames históricos.")

def draw():
    global current_frame_idx, prev_hash, chain_valid, broken_frame
    
    if df_telemetry is None:
        return
        
    py5.background(5, 5, 12)
    
    # Seleciona a linha atual da telemetria gravada
    row = df_telemetry.iloc[current_frame_idx]
    
    t = int(row["frame"])
    f_opt = row["f_opt"]
    veracity = row["veracity"]
    t_stdj = row["t_stdj"]
    total_attacks = int(row["total_attacks"])
    total_corrections = int(row["total_corrections"])
    recorded_hash = row["sha256_hash"]
    timestamp_frame = row["timestamp"]
    
    # Recupera os estados vetoriais brutos que salvamos no Parquet
    phases = np.array(row["qubit_phases"])
    flips = np.array(row["bit_flip_status"])
    num_qubits = len(phases)
    
    # --- VALIDADOR CRIPTOGRÁFICO DE RUNTIME ---
    if recorded_hash != "NOT_ENCRYPTED" and chain_valid:
        raw_data_string = f"{t}-{f_opt:.8f}-{veracity:.8f}-{t_stdj:.2e}-{total_corrections}-{timestamp_frame}-{prev_hash}"
        calculated_hash = hashlib.sha256(raw_data_string.encode()).hexdigest()
        
        if calculated_hash != recorded_hash:
            chain_valid = False
            broken_frame = t
        else:
            prev_hash = recorded_hash

    # --- 1. VISUALIZAÇÃO GRÁFICA DAS ONDAS ORIGINAIS ---
    py5.push_matrix()
    py5.translate(0, py5.height / 2, -100)
    py5.no_fill()
    
    largura_tela = py5.width
    passo_x = 10
    
    for q in range(num_qubits):
        fator_cor = q / max(1, (num_qubits - 1))
        
        # CHECAGEM DE BIT-FLIP EM TEMPO REAL SALVA NO PARQUET
        if flips[q] == 1:
            py5.stroke(255, 0, 0, 230)
            py5.stroke_weight(5) # Linha grossa e vermelha para quebras de integridade
        else:
            r = py5.lerp(0, 255, fator_cor)
            g = py5.lerp(255, 0, fator_cor)
            b = 255
            py5.stroke(r, g, b, 140)
            py5.stroke_weight(3)
            
        py5.begin_shape()
        for x in range(0, largura_tela, passo_x):
            fase_atual = phases[q]
            modulador_amplitude = -1.0 if flips[q] == 1 else 1.0
            
            # Equação matemática reconstrutiva exata do seu kernel original
            amplitude_onda = 80 * modulador_amplitude * py5.sin(x * 0.005 * (q + 1) + fase_atual + py5.frame_count * 0.02)
            amplitude_onda += 15 * py5.cos(x * 0.02 - fase_atual * f_opt)
            
            distancia_z = -q * (300 / max(1, num_qubits))
            py5.vertex(x, amplitude_onda, distancia_z)
        py5.end_shape()
        
    py5.pop_matrix()

    # --- 2. DESENHO DO HUD ORIGINAL ---
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.text_size(32)
    
    py5.fill(0, 255, 255)
    py5.text(f"🚀 SPHY KERNEL: PLAYBACK VIEWPORT ({num_qubits} QUBITS)", 50, 80)
    
    py5.fill(255)
    py5.text(f"FRAME SHA-256: {recorded_hash}", 50, 140)
    py5.text(f"📅 FRAME TIMESTAMP: {timestamp_frame}", 50, 190)
    py5.text(f"DETERMINISTIC TICK: {t:05d} / {total_rows}", 50, 250)
    py5.text(f"STDJ COHERENCE CONTROL (F_opt): {f_opt:.6f}", 50, 310)
    
    py5.fill(255, 50, 50)
    py5.text(f"🚨 HISTORIC BIT-FLIP ATTACKS: {total_attacks}", 50, 390)
    py5.fill(50, 255, 50)
    py5.text(f"🛡️  IA ACTIVE MITIGATIONS: {total_corrections}", 50, 440)
    
    # Veracidade da cadeia geral
    py5.text_size(32)
    if not chain_valid:
        py5.fill(255, 0, 0)
        py5.text(f"🚨 CRYPTO CHAIN BROKEN AT FRAME {broken_frame}!! LOG VIOLADO!", 50, 520)
    elif any(flips):
        py5.fill(255, 100, 0)
        py5.text(f"🚨 FAULT DETECTED: ISOLATING REVERSE CORRECTION NODE...", 50, 520)
    elif veracity > 0.999050:
        py5.fill(0, 255, 0)
        py5.text(f"🛡️  ANTIFRAGILE COHERENCE LOCKED [Veracity: {veracity:.6f}]", 50, 520)
    else:
        py5.fill(255, 215, 0)
        py5.text(f"⚠️  STDJ FEEDBACK WARPING ACTIVE [Veracity: {veracity:.6f}]", 50, 520)
        
    py5.hint(py5.ENABLE_DEPTH_TEST)
    
    # Avança na linha do tempo do arquivo Parquet de forma circular
    current_frame_idx = (current_frame_idx + 1) % total_rows

if __name__ == "__main__":
    py5.run_sketch()
