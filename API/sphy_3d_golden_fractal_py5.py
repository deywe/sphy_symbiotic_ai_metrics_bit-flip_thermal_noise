import py5
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import sys

# --- VARIÁVEIS GLOBAIS DE CONTROLE ---
frames_phases = []
total_frames = 0
num_qubits = 0
current_frame_idx = 0
paused = False

# Constantes da Proporção Áurea
GOLDEN_RATIO = (1.0 + 5.0**0.5) / 2.0
GOLDEN_ANGLE = 2.0 * np.pi * (1.0 - 1.0 / GOLDEN_RATIO)

def selecionar_arquivo_parquet():
    """Abre o seletor de arquivos nativo do sistema operacional."""
    root = tk.Tk()
    root.withdraw()  # Oculta a janela em branco do tkinter
    root.attributes('-topmost', True)  # Força o seletor a ficar na frente de todas as janelas
    
    print("[*] Opening File Selector UI... Please choose your Parquet file.")
    file_path = filedialog.askopenfilename(
        title="🛸 SPHY py5 Viewport: Select Parquet Telemetry Ledger",
        filetypes=[("Parquet Files", "*.parquet")]
    )
    
    if not file_path:
        print("[-] Operation cancelled by operator. Exiting System.")
        sys.exit()
    return file_path

def settings():
    """Configurações primárias do motor gráfico (Engine Constraints)."""
    py5.size(1200, 900, py5.P3D)
    py5.smooth(8)  # Movido para cá para corrigir o RuntimeError

def setup():
    """Inicialização dos estados físicos e carregamento de memória."""
    global frames_phases, total_frames, num_qubits
    
    py5.frame_rate(60)
    
    # 1. Carrega os dados coletados antes de renderizar a geometria fractal
    df = pd.read_parquet(parquet_path_escolhido)
    frames_phases = [np.array(p) for p in df['qubit_phases'].values]
    total_frames = len(frames_phases)
    num_qubits = len(frames_phases[0])
    
    print(f"[📊] Fractal Network Successfully Locked: {num_qubits} Qubits | {total_frames} Ticks.")
    print("\n[🕹️] ENGINE RUNNING:")
    print(" -> Drag MOUSE around viewport to pivot the Golden Fractal Lattice")
    print(" -> Press SPACEBAR to freeze/thaw quantum time development\n")

def draw():
    global current_frame_idx, paused
    
    # Fundo profundo do espaço-tempo quântico
    py5.background(5, 5, 10)
    
    # Posiciona e centraliza a viewport tridimensional
    py5.translate(py5.width / 2, py5.height / 2, -200)
    
    # Rotação paramétrica baseada nas coordenadas do ponteiro do mouse
    py5.rotate_x(py5.mouse_y * 0.01)
    py5.rotate_y(py5.mouse_x * 0.01)
    
    # Extração vetorial das fases do frame atual
    phases = frames_phases[current_frame_idx]
    coords = np.zeros((num_qubits, 3))
    
    for idx in range(num_qubits):
        fase = phases[idx]
        
        # Distribuição Espacial de Vogel acoplada à Sequência de Fibonacci
        raio = 12.0 * np.sqrt(idx + 1)
        theta = (idx * GOLDEN_ANGLE) + (fase * 0.05)
        
        # Conversão de coordenadas cilíndricas para tensores espaciais 3D
        x = raio * np.cos(theta)
        y = raio * np.sin(theta)
        # O eixo Z mapeia as deformações ondulatórias causadas pelos operadores físicos
        z = np.sin(fase + (raio * 0.02)) * (60.0 + (raio * 0.1))
        
        coords[idx] = [x, y, z]

    # --- RENDERIZAÇÃO DA MALHA FRACTAL ---
    
    # Camada 1: Filamentos Logarítmicos (Espiral Principal)
    py5.no_fill()
    py5.stroke_weight(2.0)
    py5.begin_shape()
    for idx in range(num_qubits):
        fase = phases[idx]
        
        # Geração harmônica de cores baseada na proporção áurea
        r_color = int(np.abs(np.sin(fase)) * 255)
        g_color = int(np.abs(np.cos(fase * GOLDEN_RATIO)) * 255)
        b_color = int(np.abs(np.sin(fase + GOLDEN_RATIO)) * 255)
        
        py5.stroke(r_color, g_color, b_color, 180)
        py5.vertex(coords[idx][0], coords[idx][1], coords[idx][2])
    py5.end_shape()

    # Camada 2: Entrelaçamento Estrutural Secundário
    py5.stroke_weight(0.5)
    fibonacci_leap = 13  # Número de acoplamento da teia fractal
    for idx in range(num_qubits - fibonacci_leap):
        fase = phases[idx]
        py5.stroke(0, int(np.abs(np.sin(fase)) * 150), 200, 45)
        py5.line(
            coords[idx][0], coords[idx][1], coords[idx][2],
            coords[idx + fibonacci_leap][0], coords[idx + fibonacci_leap][1], coords[idx + fibonacci_leap][2]
        )

    # Camada 3: Emissores Quânticos (Nós dos Qubits)
    py5.stroke_weight(4.0)
    for idx in range(num_qubits):
        py5.stroke(240, 245, 255, 220)
        py5.point(coords[idx][0], coords[idx][1], coords[idx][2])

    # Controle temporal linear da simulação
    if not paused:
        current_frame_idx = (current_frame_idx + 1) % total_frames

def key_pressed():
    global paused
    if py5.key == ' ':
        paused = not paused
        print(f"[!] Engine Playback Stream: {'PAUSED' if paused else 'RUNNING'}")

if __name__ == '__main__':
    print("[*] Launching Harpia Quantum DeepTech File Interceptor...")
    # Executa a janela do seletor ANTES de iniciar a thread gráfica do py5
    parquet_path_escolhido = selecionar_arquivo_parquet()
    
    # Inicia a aplicação py5
    py5.run_sketch()
