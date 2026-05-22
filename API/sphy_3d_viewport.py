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
    root.withdraw() # Oculta a janela principal do tkinter
    root.attributes('-topmost', True) # Força a janela a ficar na frente
    file_path = filedialog.askopenfilename(
        title="🛸 SPHY Mesh Viewport: Select Quantum Telemetry Parquet",
        filetypes=[("Parquet Files", "*.parquet")]
    )
    if not file_path:
        print("[-] No file selected. Exiting System.")
        sys.exit()
    return file_path

def main():
    # 1. Seleção do dataset gerado pelo seu Kernel em Streamlit
    print("[*] Launching Harpia Quantum DeepTech File Selector...")
    parquet_path = selecionar_arquivo_parquet()
    print(f"[+] Loading Telemetry Ledger: {parquet_path}")
    
    # Lendo os dados do Apache Parquet
    df = pd.read_parquet(parquet_path)
    
    # Extraindo as fases calculadas (convertendo listas do pandas de volta para arrays numpy)
    frames_phases = [np.array(p) for p in df['qubit_phases'].values]
    total_frames = len(frames_phases)
    num_qubits = len(frames_phases[0])
    
    print(f"[📊] Data Checked: {num_qubits} Qubits detected across {total_frames} Ticks.")

    # 2. Inicialização do Motor Gráfico 3D (Pygame + OpenGL)
    pygame.init()
    display_width = 1100
    display_height = 800
    pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("🛸 SPHY KERNEL: Quantum Mesh 3D Viewport")

    # Configuração de perspectiva da câmera quântica
    gluPerspective(45, (display_width / display_height), 0.1, 150.0)
    glTranslatef(0.0, 0.0, -45.0) # Distância da visualização inicial
    
    # Configurações de física e renderização para linhas suaves
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    # Variáveis de controle de visualização
    current_frame_idx = 0
    rot_x, rot_y = 25, 45  # Ângulo inicial inclinado para melhor percepção da malha
    paused = False
    clock = pygame.time.Clock()

    print("\n[🕹️] MESH CONTROLS:")
    print(" -> Hold LEFT MOUSE BUTTON and drag to rotate the Quantum Mesh")
    print(" -> Use MOUSE WHEEL to Zoom In/Out")
    print(" -> Press SPACEBAR to Pause/Resume simulation timeline")
    print(" -> Press ESC to exit viewport\n")

    # 3. Loop Principal de Renderização da Malha
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
                    print(f"[!] Simulation Timeline: {'PAUSED' if paused else 'RUNNING'}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # Zoom In
                    glTranslatef(0, 0, 1.5)
                elif event.button == 5: # Zoom Out
                    glTranslatef(0, 0, -1.5)

        # Captura arrasto do mouse para rotação livre do tecido quântico
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]: 
            rel_x, rel_y = pygame.mouse.get_rel()
            rot_x += rel_y * 0.4
            rot_y += rel_x * 0.4
        else:
            pygame.mouse.get_rel()

        # Limpando a tela com fundo preto profundo do espaço
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        # --- PROCESSAMENTO GEOMÉTRICO DA MALHA QUANTICA SPHY ---
        phases = frames_phases[current_frame_idx]
        
        # Array para armazenar as coordenadas 3D geradas no tick atual
        coords = np.zeros((num_qubits, 3))
        
        for idx in range(num_qubits):
            fase = phases[idx]
            
            # Mapeamento Topológico em Casca Cilíndrica/Toroidal
            theta = fase
            phi = (idx / num_qubits) * 2.0 * np.pi * 3.0 # Fator multiplicador cria o entrelaçamento helicoidal
            
            r_base = 12.0 + np.sin(theta) * 1.0
            
            # Coordenadas X, Y da rede de oscilação
            x = r_base * np.cos(phi)
            y = r_base * np.sin(phi)
            # Z é a amplitude pura da fase deformada pelo ruído/bit-flip
            z = (idx / num_qubits) * 15.0 - 7.5 + (np.sin(theta * 3.0) * 1.5)
            
            coords[idx] = [x, y, z]

        # 1. Renderização das Conexões Longitudinais (O Tecido da Malha)
        glLineWidth(1.5)
        glBegin(GL_LINE_STRIP)
        for idx in range(num_qubits):
            # As cores mudam dinamicamente com base na fase local da onda
            fase = phases[idx]
            r_color = np.abs(np.sin(fase))
            g_color = np.abs(np.cos(fase * 0.5))
            b_color = np.abs(np.cos(fase))
            
            glColor4f(r_color, g_color, b_color, 0.85) # Opacidade em 85% para efeito holográfico
            glVertex3fv(coords[idx])
        glEnd()

        # 2. Renderização de Ligações Cruzadas (Entrelaçamento de Vizinhança)
        # Conecta nós paralelos para dar o aspecto de "rede/gaiola quântica" tridimensional
        glLineWidth(0.5)
        glBegin(GL_LINES)
        passo_rede = 12 # Distância de acoplamento dos nós na malha
        for idx in range(num_qubits - passo_rede):
            fase = phases[idx]
            # Linhas de acoplamento mais discretas (efeito neon apagado)
            glColor4f(0.0, np.abs(np.sin(fase)), np.abs(np.cos(fase)), 0.3)
            glVertex3fv(coords[idx])
            glVertex3fv(coords[idx + passo_rede])
        glEnd()

        # 3. Renderização dos Qubits como Nós Brilhantes na Malha
        glPointSize(4.0)
        glBegin(GL_POINTS)
        for idx in range(num_qubits):
            glColor4f(1.0, 1.0, 1.0, 0.9) # Pontos brancos intensos marcando a junção das ondas
            glVertex3fv(coords[idx])
        glEnd()

        glPopMatrix()
        pygame.display.flip()
        
        if not paused:
            current_frame_idx = (current_frame_idx + 1) % total_frames

        clock.tick(60) # Execução travada a 60 FPS fluídos

    pygame.quit()
    print("[+] SPHY Quantum Mesh Viewport terminated clean.")

if __name__ == '__main__':
    main()
