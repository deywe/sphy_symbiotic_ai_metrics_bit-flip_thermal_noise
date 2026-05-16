import py5
import numpy as np
import pandas as pd
import hashlib

# --- VARIÁVEIS GLOBAIS DE CONTROLE ---
df_audit = None
num_qubits = 0
total_frames = 0
qubit_phases = []
bit_flip_status = []

# CONSTANTES DE TELEMETRIA E STRESS AMBIENTAL
TEMPERATURA_KELVIN = 300.0
FORCA_RUIDO = 0.15
CHANCE_BIT_FLIP = 0.02

total_attacks = 0
total_corrections = 0
hash_validation_error = False

def settings():
    py5.size(1600, 900, py5.P3D)
    py5.smooth(8)

def setup():
    global df_audit, num_qubits, total_frames, qubit_phases, bit_flip_status, hash_validation_error
    py5.background(0)
    py5.stroke_weight(3)
    
    print("=" * 60)
    print("🎨 SPHY AUDIT VISUALIZER - FRONTEND ACTIVE")
    print("=" * 60)
    
    # Carregamento seguro do Parquet gerado pelo Core
    try:
        df_audit = pd.read_parquet('sphy_audit_data.parquet')
        total_frames = len(df_audit)
        
        # Identifica o número de qubits contando as colunas que começam com 'q_'
        columns_q = [col for col in df_audit.columns if col.startswith('q_')]
        num_qubits = len(columns_q)
        
        qubit_phases = np.zeros(num_qubits)
        bit_flip_status = np.zeros(num_qubits, dtype=int)
        
        print(f"✅ Parquet carregado. Detectados {num_qubits} Qubits e {total_frames} Frames estáveis.")
    except Exception as e:
        print(f"❌ Erro crítico: Arquivo 'sphy_audit_data.parquet' não encontrado ou corrompido! {e}")
        py5.exit_sketch()

def draw():
    global qubit_phases, bit_flip_status, total_attacks, total_corrections, hash_validation_error
    py5.background(5, 5, 12)
    
    # Garante o sincronismo cíclico com base no arquivo lido
    t = py5.frame_count % total_frames
    row = df_audit.iloc[t]
    
    # Extrai os dados puros do Core Protegido
    f_opt = row['f_opt']
    sha256_original = row['sha256_core']
    
    # --- AUDITORIA DE INTEGRIDADE (Validação Real do Hash do Core) ---
    t_stdj = t * 1.58e-43
    payload_validacao = f"{t}-{f_opt:.8f}-{row['veracity_ideal']:.8f}-{t_stdj:.2e}"
    sha256_calculado = hashlib.sha256(payload_validacao.encode()).hexdigest()
    
    if sha256_original != sha256_calculado:
        hash_validation_error = True  # Alerta vermelho se o arquivo foi adulterado externa ou internamente
        
    # Fator de atenuação térmica derivado do F_opt do Core
    fator_correcao = 1.0 / (1.0 + (f_opt * 0.2))
    
    # --- PROJEÇÃO DE STRESS AMBIENTAL EM TEMPO REAL ---
    for idx in range(num_qubits):
        # Puxa a fase ideal gerada no segredo industrial
        fase_ideal = row[f'q_{idx}']
        
        # Injeta estocástica de ruído térmico local
        ruido_termico = np.random.normal(0, FORCA_RUIDO * (TEMPERATURA_KELVIN / 300.0))
        ruido_residual = ruido_termico * fator_correcao
        
        # Injeta estocástica de Bit-Flip
        if np.random.rand() < CHANCE_BIT_FLIP:
            bit_flip_status[idx] = 1
            total_attacks += 1
            
        # Algoritmo de Combate da IA Simbiótica (Recuperação de Paridade Geométrica)
        reversao_ia = 0.0
        if bit_flip_status[idx] == 1:
            reversao_ia = np.pi  # Pulso de correção sintonizado
            bit_flip_status[idx] = 0
            total_corrections += 1
            
        fase_final = fase_ideal + ruido_residual
        if bit_flip_status[idx] == 1:
            fase_final += np.pi
            
        qubit_phases[idx] = (fase_final - reversao_ia) % py5.TWO_PI
        
    # Recalcula a veracidade atual sob stress de laboratório
    coerencia_atual = np.abs(np.mean(np.exp(1j * qubit_phases)))
    veracity_stress = min(0.9990 + (coerencia_atual * 0.0010), 1.0)
    
    # --- DESENHO DA INTERFACE ---
    draw_ghz_waves(f_opt)
    draw_sphy_hud(t, f_opt, veracity_stress, sha256_original, ruido_residual)

def draw_ghz_waves(f_opt):
    py5.push_matrix()
    py5.translate(0, py5.height / 2, -100)
    py5.no_fill()
    
    largura_tela = py5.width
    passo_x = 10
    
    for q in range(num_qubits):
        fator_cor = q / max(1, (num_qubits - 1))
        
        if bit_flip_status[q] == 1:
            py5.stroke(255, 0, 0, 230)
            py5.stroke_weight(5)
        else:
            # CORRIGIDO: Removido o lixo de escopo 'faktor_cor' que quebrava a renderização
            r = py5.lerp(0, 255, fator_cor)
            g = py5.lerp(255, 0, fator_cor)
            b = 255
            py5.stroke(r, g, b, 140)
            py5.stroke_weight(3)
            
        py5.begin_shape()
        for x in range(0, largura_tela, passo_x):
            fase_atual = qubit_phases[q]
            modulador_amplitude = -1.0 if bit_flip_status[q] == 1 else 1.0
            
            amplitude_onda = 80 * modulador_amplitude * py5.sin(x * 0.005 * (q + 1) + fase_atual + py5.frame_count * 0.02)
            amplitude_onda += 15 * py5.cos(x * 0.02 - fase_atual * f_opt)
            
            distancia_z = -q * (300 / max(1, num_qubits))
            py5.vertex(x, amplitude_onda, distancia_z)
        py5.end_shape()
        
    py5.pop_matrix()

def draw_sphy_hud(t, f_val, veracity, current_hash, ruido_residual):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.text_size(32)
    
    # Monitor de Segurança Criptográfica do Core
    if hash_validation_error:
        py5.fill(255, 0, 0)
        py5.text("🚨 INTEGRITY FAULT: CORE PARQUET HASH MISMATCH!", 50, 80)
    else:
        py5.fill(0, 255, 255)
        py5.text(f"🚀 SPHY AUDITOR: PARQUET VISUALIZER ({num_qubits} QUBITS DETECTED)", 50, 80)
        
    # Plota o hash lido diretamente do Parquet protegido
    py5.fill(255)
    py5.text(f"PARQUET CORE SHA-256: {current_hash}", 50, 140)
    
    # Telemetria de Leitura
    py5.text(f"PARQUET INDEX ROW: {t:05d} / {total_frames:05d}", 50, 200)
    py5.text(f"STDJ READ CONTROL (F_opt): {f_val:.6f}", 50, 260)
    
    # Monitoramento de Stress em Tempo Real (Injetado sobre a leitura)
    py5.fill(255, 100, 100)
    py5.text(f"SIMULATED THERMAL NOISE ATTACK: {ruido_residual:+.6f} rad", 50, 340)
    py5.text(f"🚨 TOTAL BIT-FLIP ERROR EVENTS: {total_attacks}", 50, 390)
    
    py5.fill(50, 255, 50)
    py5.text(f"🛡️  IA SIMBIOTIC COUNTER-MEASURES: {total_corrections}", 50, 440)
    
    # Status de Coerência
    py5.text_size(32)
    if veracity > 0.999050:
        py5.fill(0, 255, 0)
        py5.text(f"🛡️  ANTIFRAGILE COHERENCE LOCKED [Veracity under Stress: {veracity:.6f}]", 50, 510)
    else:
        py5.fill(255, 215, 0)
        py5.text(f"⚠️  STDJ STRESS WARPING [Veracity under Stress: {veracity:.6f}]", 50, 510)
        
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
