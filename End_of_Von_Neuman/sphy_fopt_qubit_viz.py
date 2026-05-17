import py5
import numpy as np
import pandas as pd
import hashlib
import os
import struct

df_parquet = None
total_frames_dataset = 0
num_qubits_detectados = 0
colunas_qubits = []

integridade_violada = False
frame_falha_detectada = -1
INTERVALO_FRAMES = 200

def settings():
    py5.size(1600, 900, py5.P3D)
    py5.smooth(8)

def setup():
    global df_parquet, total_frames_dataset, num_qubits_detectados, colunas_qubits
    global integridade_violada, frame_falha_detectada
    
    py5.background(5, 5, 12)
    py5.stroke_weight(3)
    
    filename = 'sphy_audit_data.parquet'
    if not os.path.exists(filename):
        print(f"❌ Erro Crítico: O arquivo '{filename}' não existe! Execute o Core gerador.")
        py5.exit_sketch()
        return

    df_parquet = pd.read_parquet(filename)
    total_frames_dataset = len(df_parquet)
    
    colunas_qubits = [col for col in df_parquet.columns if col.startswith('q_')]
    num_qubits_detectados = len(colunas_qubits)
    
    print("=" * 75)
    print("🛸 SPHY LEDGER VISUALIZER & DETECTOR ACTIVE")
    print(f"📂 Arquivo carregado: {filename}")
    print(f"📊 Linhas Auditadas: {total_frames_dataset} Ticks | Largura da Matriz: {num_qubits_detectados} Qubits")
    print("=" * 75)
    print("🔒 Executando Auditoria Matemática Estrita...")

    ultimo_hash_esperado = hashlib.sha256(b"SPHY_GENESIS_CORE_ANCHOR").hexdigest()
    
    for idx, row in df_parquet.iterrows():
        t_val = int(row['frame'])
        ts_val = float(row['timestamp'])
        f_opt_val = float(row['f_opt'])
        veracity_val = float(row['veracity_stress'])
        
        fases_lista = [float(row[col]) for col in colunas_qubits]
        
        # Reconstrói a estrutura exata em bytes
        header_bytes = struct.pack("!Iddd", t_val, ts_val, f_opt_val, veracity_val)
        prev_hash_bytes = bytes.fromhex(row['prev_hash'])
        fases_bytes = struct.pack(f"!{num_qubits_detectados}d", *fases_lista)
        
        payload_reconstruido = prev_hash_bytes + header_bytes + fases_bytes
        hash_recalculado = hashlib.sha256(payload_reconstruido).hexdigest()
        
        if row['prev_hash'] != ultimo_hash_esperado or hash_recalculado != row['current_hash']:
            integridade_violada = True
            frame_falha_detectada = t_val
            print(f"🚨 QUEBRA DE INTEGRIDADE DETECTADA NO FRAME REGISTRADO {frame_falha_detectada}!")
            break
            
        ultimo_hash_esperado = hash_recalculado

    if not integridade_violada:
        print("🔒 CRIPTO-AUDITORIA: SUCESSO! Assinaturas encadeadas batem perfeitamente.")
    print("=" * 75)

def draw():
    if df_parquet is None:
        return
        
    py5.background(6, 6, 18)
    
    # Mapeia o loop contínuo sobre a linha do tempo do dataset
    idx_frame = py5.frame_count % total_frames_dataset
    row_atual = df_parquet.iloc[idx_frame]
    
    t_tick = int(row_atual['frame'])
    timestamp_real = row_atual['timestamp']
    f_opt = row_atual['f_opt']
    veracity = row_atual['veracity_stress']
    feedback_ativo = int(row_atual['feedback_ativo']) == 1
    current_hash = row_atual['current_hash']
    prev_hash = row_atual['prev_hash']
    ruido_residual = row_atual['ruido_residual']
    
    # Calcula quantos frames restam na tela para a inversão do ciclo atual
    frames_restantes_ciclo = INTERVALO_FRAMES - (t_tick % INTERVALO_FRAMES)
    
    renderizar_ondas_dataset(row_atual, feedback_ativo)
    renderizar_hud_auditor(t_tick, timestamp_real, f_opt, veracity, current_hash, prev_hash, ruido_residual, feedback_ativo, frames_restantes_ciclo)

def renderizar_ondas_dataset(row_atual, feedback_ativo):
    py5.push_matrix()
    py5.translate(0, py5.height / 2 + 120, -150)
    py5.no_fill()
    
    largura_tela = py5.width
    passo_x = 15  
    
    qubits_para_renderizar = colunas_qubits[::4] if num_qubits_detectados > 30 else colunas_qubits
    
    for q_idx, col_name in enumerate(qubits_para_renderizar):
        fator_cor = q_idx / max(1, len(qubits_para_renderizar) - 1)
        fase_salva = row_atual[col_name]
        
        if not feedback_ativo and row_atual['veracity_stress'] < 0.95:
            py5.stroke(255, 0, 0, 100)
            py5.stroke_weight(2)
        else:
            r = py5.lerp(0, 150, fator_cor)
            g = py5.lerp(255, 100, fator_cor)
            b = 255
            py5.stroke(r, g, b, 120)
            py5.stroke_weight(2)
            
        py5.begin_shape()
        for x in range(0, largura_tela, passo_x):
            amplitude_onda = 60 * py5.sin(x * 0.005 * (q_idx + 1) + fase_salva)
            distancia_z = -q_idx * 15
            py5.vertex(x, amplitude_onda, distancia_z)
        py5.end_shape()
        
    py5.pop_matrix()

def renderizar_hud_auditor(t, timestamp, f_opt, veracity, current_hash, prev_hash, ruido_residual, feedback_ativo, frames_restantes):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.text_size(24)
    
    if integridade_violada:
        py5.fill(255, 0, 0)
        py5.text(f"🚨 INTEGRITY FAULT: LEDGER ADULTERADO OU ASSINATURA INVÁLIDA", 50, 60)
    elif feedback_ativo:
        py5.fill(0, 255, 200)
        py5.text(f"🛸 SPHY IMMUNOLOGICAL CORE: ONLINE (FRAME INTERVAL REGULATED)", 50, 60)
        py5.fill(200)
        py5.text_size(15)
        py5.text(f"Inversão determinística para modo BYPASS em: {frames_restantes} frames", 50, 90)
    else:
        py5.fill(255, 50, 50)
        py5.text(f"🚨 SPHY BYPASS MODE: UNPROTECTED REGION CHANNELS", 50, 60)
        py5.fill(200)
        py5.text_size(15)
        py5.text(f"Retorno automático da IA Harpia em: {frames_restantes} frames", 50, 90)
        
    py5.text_size(15)
    py5.fill(180)
    py5.text(f"CURRENT FRAME INDEX: {t:06d}/{total_frames_dataset:06d}  |  QUANTUM METRIC CONTROL: {t*1.58e-43:.2e} s", 50, 125)
    py5.text(f"GEODESIC FIELD RESONANCE (F_opt): {f_opt:.8f}", 50, 150)
    
    py5.fill(0, 80, 180, 80)
    py5.rect(45, 175, 1510, 105, 5)
    
    py5.fill(255)
    py5.text_size(13)
    py5.text(f"🔗 RECORDED HARDWARE TIMESTAMP: {timestamp:.6f} (UNIX EPOCH)", 60, 200)
    py5.text(f"🔗 BLOCK PREVIOUS HASH: {prev_hash}", 60, 230)
    py5.text(f"🔒 BLOCK CURRENT HASH: {current_hash}", 60, 260)
    
    py5.text_size(15)
    py5.fill(255, 120, 120)
    py5.text(f"RECORDED THERMAL DISTORTION (300 K): {ruido_residual:+.6f} rad", 50, 325)
    
    if not integridade_violada:
        py5.fill(50, 255, 50)
        py5.text(f"🔒 LEDGER CHECK STATUS: VERIFIED BYTES", 50, 355)
    else:
        py5.fill(255, 0, 0)
        py5.text(f"🚨 LEDGER CHECK STATUS: CORRUPTED DATA", 50, 355)
        
    py5.text_size(26)
    if feedback_ativo and not integridade_violada:
        py5.fill(0, 255, 0)
        py5.text(f"AUDITED VERACITY RATIO: {veracity:.6f}", 50, 420)
    else:
        if veracity < 0.3 or integridade_violada:
            py5.fill(255, 0, 0)
        else:
            py5.fill(255, 150, 0)
        py5.text(f"AUDITED VERACITY RATIO: {veracity:.6f} (DECOHERENCE)", 50, 420)
        
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
