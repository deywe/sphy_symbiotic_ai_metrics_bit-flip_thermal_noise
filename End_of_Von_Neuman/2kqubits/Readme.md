### `README.md`

```markdown
# 📂 SPHY: Multiscale Quantum Ledger Repository
**Directory: `/End_of_Von_Neuman`**

---

## 🚨 TECHNICAL SPECIFICATIONS & SCALE ARCHITECTURE

This sub-directory contains the multi-scale dataset deployment for the **SPHY Immunological Quantum Core** validation. Each designated folder represents a scaling benchmark of logical qubits emulated under ambient thermodynamic noise ($300\text{ K}$) and discrete Pauli-X (*Bit-Flip*) attacks.


```

📁 End_of_Von_Neuman
│
├── 📁 1200qubit/               # 1,200 Logical Qubits Matrix (1,200 Frames)
│   └── sphy_audit_data.parquet
│
├── 📁 2kqubits/                # 2,000 Logical Qubits Matrix (1,200 Frames)
│   └── sphy_audit_data.parquet
│
├── 📄 sphy_audit_data.parquet  # Default Scale Matrix (120 Qubits Baseline)
└── 📄 sphy_fopt_qubit_viz.py   # Universal Binary Forensic Visualizer

```

---

## ⏳ Frame Constraints & GitHub Storage Limits

Every dataset compiled in these directories is locked at exactly **1,200 Ticks (Frames)**. 

* **The Scale vs. Storage Dilemma:** The internal architecture of the SPHY engine is fully capable of streaming and recording infinite continuous frames. However, because each frame records the exact high-precision phase (`double` float format) for every single qubit alongside its strict cryptographic tracking metadata (`prev_hash`, `current_hash`, `timestamp`), the file size scales exponentially.
* **The 25MB Threshold:** In order to bypass GitHub's strict **25 MB file size limit** for non-enterprise/free-tier uploads, the temporal sequence was intentionally truncated at 1,200 frames per matrix size. This constraint ensures the `.parquet` ledger remains compact enough for public hosting while providing more than enough historical data for complete cryptographic auditing.

---

## 🔒 Multi-Scale Forensic Verification

The universal visualizer **`sphy_fopt_qubit_viz.py`** located in the root of this folder is fully dynamic. It is programmed to auto-detect the layout of the dataset it is eating.

### How to Audit Different Scales:
To test the resilience and the deterministic 200-frame cryptographic tug-of-war on a larger scale:

1. Copy the `sphy_audit_data.parquet` file from either the `1200qubit/` or `2kqubits/` folder.
2. Paste it into the root directory (replacing the default 120-qubit baseline file).
3. Execute the visualizer:
   ```bash
   python3 sphy_fopt_qubit_viz.py

```

The script will automatically parse the column schemas (`q_0` to `q_1199` or `q_1999`), verify the structured binary `struct` parity line-by-line, and initiate the 3D wave visualization. If a single bit of phase was dropped or altered during transmission, the SHA-256 chain will break instantly, triggering an **`INTEGRITY FAULT`**.

---

## ✍️ Ownership and Sovereignty Notice

The data stored within these partitions constitutes empirical proof that scale does not degrade the efficiency of the geometric immune response. The code works, the hashes match, and the ledger is permanent.

Validate the chains, audit the timestamps, and prepare for the Post-Quantum transition.

**Secured and Published by:**
🛡️ **Deywe Okabe** *Developer, Quantum Researcher & Guardian of the Core*

```

```
