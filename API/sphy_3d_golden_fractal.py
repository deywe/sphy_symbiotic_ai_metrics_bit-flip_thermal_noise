import pandas as pd
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
from tkinter import filedialog
import sys

def selecionar_arquivo_parquet():
    """Abre uma janela nativa do sistema para escolher o log Parquet."""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title="🛸 SPHY Golden Fractal Viewport: Select Parquet Telemetry",
        filetypes=[("Parquet Files", "*.parquet")]
    )
    if not file_path:
        print("[-] No file selected. Exiting System.")
        sys.exit()
    return file_path

def main():
    print("[*] Launching Harpia Quantum DeepTech Fractal Engine...")
    parquet_path = selecionar_arquivo_parquet()
    print(f"[+] Loading Telemetry Ledger: {parquet_path}")
    
    df = pd.read_parquet(parquet_path)
    frames_phases = [np.array(p) for p in df['qubit_phases'].values]
    total_frames = len(frames_phases)
    num_qubits = len(frames_phases[0])
    
    print(f"[📊] Fractal Node Count: {num_qubits} Qubits | Time Horizons: {total_frames} Ticks.")

    # Inicialização do Ambiente Gráfico 3D
    pygame.init()
    display_width = 1200
    display_height = 900
    pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("🛸 SPHY KERNEL: 3D Golden Ratio Quantum Fractal")

    gluPerspective(45, (display_width / display_height), 0.1, 200.0)
    glTranslatef(0.0, 0.0, -50.0) # Recua a câmera para enquadrar a expansão fractal
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    # Constantes da Geometria Sagrada / Física SPHY
    GOLDEN_RATIO = (1.0 + 5.0**0.5) / 2.0
    GOLDEN_ANGLE = 2.0 * np.pi * (1.0 - 1.0 / GOLDEN_RATIO) # ~137.5 graus em radianos

    current_frame_idx = 0
    rot_x, rot_y = 0, 0
    paused = False
    clock = pygame.time.Clock()

    print("\n[🧬] FRACTAL VIEWPORT ACTIVE:")
    print(" -> Drag LEFT MOUSE BUTTON to pivot the fractal lattice")
    print(" -> Use MOUSE WHEEL to warp space-time zoom")
    print(" -> Press SPACEBAR to freeze/thaw time flow")
    print(" -> Press ESC to break execution loop\n")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    print(f"[!] Fractal Frame Stream: {'FROZEN' if paused else 'EVOLVING'}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: glTranslatef(0, 0, 2.0)
                elif event.button == 5: glTranslatef(0, 0, -2.0)

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]: 
            rel_x, rel_y = pygame.mouse.get_rel()
            rot_x += rel_y * 0.4
            rot_y += rel_x * 0.4
        else:
            pygame.mouse.get_rel()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        # --- RECONSTRUÇÃO DA MALHA FRACTAL ÁUREA ---
        phases = frames_phases[current_frame_idx]
        coords = np.zeros((num_qubits, 3))
        
        for idx in range(num_qubits):
            fase = phases[idx]
            
            # 1. Distribuição de Vogel Baseada no Ângulo Áureo
            # O raio expande com a raiz quadrada do índice para criar densidade uniforme
            raio = 0.6 * np.sqrt(idx + 1) 
            
            # O ângulo acumula o salto áureo clássico modificado pela oscilação da fase quântica
            theta = (idx * GOLDEN_ANGLE) + (fase * 0.1)
            
            # 2. Projeção Espacial 3D (Onda Fractal Convoluta)
            x = raio * np.cos(theta)
            y = raio * np.sin(theta)
            
            # Z se torna o eixo hiperbólico da assinatura harmônica
            # Cria profundidade em funil/vórtice baseada na proporção áurea multiplicada pela fase senoidal
            z = np.sin(fase + (raio * 0.2)) * (3.0 + (raio * 0.15))
            
            coords[idx] = [x, y, z]

        # RENDER 1: A Espiral Conectora (O filamento da realidade)
        glLineWidth(1.8)
        glBegin(GL_LINE_STRIP)
        for idx in range(num_qubits):
            fase = phases[idx]
            
            # Gradiente Fractal de Cores: Transição Neon Áurea
            r_color = np.abs(np.sin(fase))
            g_color = np.abs(np.cos(fase * GOLDEN_RATIO))
            b_color = np.abs(np.sin(fase + GOLDEN_RATIO))
            
            glColor4f(r_color, g_color, b_color, 0.75)
            glVertex3fv(coords[idx])
        glEnd()

        # RENDER 2: Teias de Acoplamento Quântico (Relações de Fibonacci)
        # Conecta nós vizinhos distantes por números da sequência (ex: 8, 13, 21...) para amarrar a malha fractal
        glLineWidth(0.5)
        glBegin(GL_LINES)
        fibonacci_leap = 13 # Número de acoplamento fractal estável
        for idx in range(num_qubits - fibonacci_leap):
            fase = phases[idx]
            # Linhas de energia escuras em background ligando a geometria secreta
            glColor4f(0.1, np.abs(np.sin(fase * 0.5)), 0.6, 0.25)
            glVertex3fv(coords[idx])
            glVertex3fv(coords[idx + fibonacci_leap])
        glEnd()

        # RENDER 3: Nós Centrais dos Qubits (Pontos Criptográficos)
        glPointSize(3.5)
        glBegin(GL_POINTS)
        for idx in range(num_qubits):
            # Qubits normais pulsam em branco/azul brilhante, simulando fótons no tecido fractal
            fase = phases[idx]
            glColor4f(0.8, 0.95, 1.0, 0.9)
            glVertex3fv(coords[idx])
        glEnd()

        glPopMatrix()
        pygame.display.flip()
        
        if not paused:
            current_frame_idx = (current_frame_idx + 1) % total_frames

        clock.tick(60)

    pygame.quit()
    print("[+] SPHY Golden Fractal Node terminated cleanly.")

if __name__ == '__main__':
    main()
