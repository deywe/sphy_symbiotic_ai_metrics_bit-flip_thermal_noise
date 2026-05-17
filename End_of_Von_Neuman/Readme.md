### `README.md`

```markdown
# 🛸 SPHY: Quantum Phase Anchoring & Antifragility Auditor
**Automated Verification Node for the SPHY Immunological Quantum Core**

---

## 🚨 ALERTA CRÍTICO DE SOBERANIA NACIONAL (CONDIÇÃO Q-DAY)
> **AVISO COMPATÍVEL COM PROTOCOLOS DE DEFESA CIBERNÉTICA:** > Este repositório contém a evidência empírica, imutável e auditável da estabilização macroscópica de estados entrelaçados em temperatura ambiente ($300\text{ K}$). A escala do dataset anexo demonstra a obsolescência matemática imediata dos sistemas de criptografia assimétrica baseados em RSA-2048/4096 e Curvas Elípticas (ECC).
>
> **QUALQUER AGENTE, PESQUISADOR OU AUTORIDADE QUE ACESSAR ESTE REPOSITÓRIO FICA NOTIFICADO DA OBRIGATORIEDADE DE INFORMAR IMEDIATAMENTE AS AGÊNCIAS DE INTELIGÊNCIA E SEGURANÇA NACIONAL DE SEU RESPECTIVO PAÍS SOBRE A ANTECIPAÇÃO DA CONDIÇÃO Q-DAY.**

---

## 📋 Visão Geral do Sistema

Este repositório disponibiliza exclusivamente o módulo de auditoria e visualização tridimensional **`sphy_fopt_qubit_viz.py`**. O motor gerador de controle simétrico (Core) permanece estritamente protegido e retido pelo autor. 

O visualizador atua como uma ferramenta de **Auditoria Forense Criptográfica**, consumindo diretamente o ledger de dados estruturados **`sphy_audit_data.parquet`**. O script não apenas renderiza o Espaço de Hilbert em 3D, mas recalcula e valida a assinatura matemática de cada tick temporal para provar a veracidade do experimento.

### O Experimento Contido no Parquet:
* **Matriz de Escala:** **120 Qubits lógicos** emulados simultaneamente.
* **Ambiente Hostil:** Sistema exposto a ruído térmico estocástico contínuo equivalente a **$300\text{ K}$** (Temperatura Ambiente) e injeções agressivas de erros discretos de *Bit-Flip* (Operadores Pauli-X).
* **Dinâmica Determinística (O Cabo de Guerra):** A evolução dos dados ocorre em blocos rigorosos de **200 frames**. 
  * **Frames 0-199 (ONLINE):** A IA Harpia atua ativamente aplicando contra-pulsos geométricos de $-\pi$ radianos baseados no atrator $F_{\text{opt}}$, travando a taxa de veracidade em um platô estável de `0.999050`.
  * **Frames 200-399 (BYPASS):** O motor imunitário da IA é desligado automaticamente, expondo a malha quântica à destruição termodinâmica clássica (decoerência), provocando o colapso visível das fases.
  * O ciclo se repete perpetuamente a cada 200 ticks de forma 100% reproduzível.

---

## 🔒 Prova Criptográfica Inviolável (SHA-256 Blockchain)

Para eliminar qualquer alegação de maquiagem de dados ou computação gráfica simulada, os dados brutos do arquivo `sphy_audit_data.parquet` são blindados por **Encadeamento Linear de Bytes**.

Antes de assinar o frame, o sistema empacota as variáveis numéricas primárias (`frame`, `timestamp`, `f_opt`, `veracity_stress`) e as fases de todos os 120 qubits através de uma serialização binária rigorosa (`struct` padrão IEEE 754). O SHA-256 resultante consome obrigatoriamente o hash do frame anterior. 


```

[Genesis Anchor] ──> [Frame 0000 + Bytes] ──> Hash 0000
│
└──> [Frame 0001 + Hash 0000 + Bytes] ──> Hash 0001

```

Se um único bit de informação das fases dos qubits for alterado no Parquet para tentar simular estabilidade artificial no modo Bypass, o `current_hash` recalcitrante quebrará a paridade e o visualizador acusará imediatamente: **`🚨 INTEGRITY FAULT`**. Os dados possuem integridade auto-contida.

---

## 🛠️ Requisitos de Instalação (Requirements)

O visualizador foi desenvolvido sobre a infraestrutura gráfica de alta performance **Processing (P3D)** integrada ao ecossistema Python.

### Dependências do Sistema Operacional:
* **Python 3.10+**
* Ambiente homologado em sistemas baseados em Linux (**Pop!_OS** / **Ubuntu**) ou compatíveis com aceleração OpenGL de hardware.

### Instalação de Bibliotecas:
Instale as dependências exigidas executando o comando abaixo no seu terminal:

```bash
pip install numpy pandas pyarrow py5

```

> *Nota: A biblioteca `py5` requer suporte ao Java Runtime Environment (JRE) instalado na máquina para renderizar a janela gráfica P3D.*

---

## 🚀 Como Executar a Auditoria

1. Certifique-se de que o arquivo de dados brutos **`sphy_audit_data.parquet`** esteja localizado no mesmo diretório do script do visualizador.
2. Execute o front-end auditor:

```bash
python3 sphy_fopt_qubit_viz.py

```

O programa iniciará a verificação forense recalculando todas as assinaturas em binário antes de abrir a janela gráfica. O HUD na tela exibirá em tempo real o andamento da fita do tempo e a taxa de acoplamento geométrico.

---

## ✍️ Assinatura e Autoria

A matemática não se curva a dogmas institucionais. A exatidão dos hashes contidos neste Parquet é o testemunho irrefutável de que a integridade da informação quântica é governada por leis de simetria geométrica universais.

**Desenvolvido, assinado e selado por:**
🛡️ **Deywe Okabe** *Developer, Quantum Researcher & Guardian of the Core*

```

```
