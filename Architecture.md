# Systems Architecture & Algorithmic Specification: FLOW-ALGO

**System:** FLOW-ALGO (Two-Stage Context-Aware Music Recommendation Engine)  
**Author:** Akshat Barthwal  
**Status:** Deployed & Benchmarked  
**Engine Stack:** Python 3.11+, Streamlit, NumPy, Vectorized In-Memory Matrix  

---

## 1. End-to-End System Flow

The following data pipeline illustrates how user queue updates are converted into deterministic parametric gates and harmonic recommendations in real time:

```mermaid
flowchart TD
    subgraph Client ["Client Layer (Screen 1)"]
        A[User Queue Mutation] -->|Track IDs| B(Queue Builder State)
        B --> C[Real-Time Centroid Calculator]
    end

    subgraph Centroid_Inference ["Centroid & Context Inference"]
        C --> D["$$\vec{C}_{session} = [\overline{BPM}, \overline{Energy}, \overline{Valence}]$$"]
        D --> E{Archetype Classifier}
        E -->|Infer Context| F[Active State: e.g., 'Late-Night Solo Highway Drive']
    end

    subgraph Stage1_Gate ["Stage 1: Zero-Leak Parametric Gating"]
        F --> G[(100k In-Memory Track Catalog)]
        G --> H["Deterministic Bound Filter:<br/>|ΔBPM| ≤ 12<br/>|ΔEnergy| ≤ 0.15<br/>Sub-genre Blacklist"]
        H -->|Prune Incompatible Candidates| I[Filtered Candidate Pool: ~500 Tracks]
    end

    subgraph Stage2_Rank ["Stage 2: Harmonic & Stochastic Ranking (Screen 2)"]
        I --> J[Camelot Wheel Matrix Filter]
        J -->|Step Adjacency: ±1 / Relative Mode| K[Harmonic Candidate Subset: ~50 Tracks]
        K --> L["Composite Scoring Function:<br/>S_i = w_1·AcousticSim + w_2·Harmonic + w_3·CF"]
        L --> M["Boltzmann Softmax Exploration:<br/>P(i) = exp(S_i / τ) / Σ exp(S_j / τ)"]
    end

    subgraph Output ["Execution & Telemetry"]
        M --> N[Top-10 Ranked Recommendation Queue]
        N --> O[Hero Autoplay Stream Target]
        N --> P[Explainable AI Telemetry Logs]
        N --> Q[2D Vector Catalog Projection]
    end

    style Client fill:#1e1e24,stroke:#7c3aed,stroke-width:2px,color:#fff
    style Centroid_Inference fill:#1e1e24,stroke:#06b6d4,stroke-width:2px,color:#fff
    style Stage1_Gate fill:#1e1e24,stroke:#ef4444,stroke-width:2px,color:#fff
    style Stage2_Rank fill:#1e1e24,stroke:#10b981,stroke-width:2px,color:#fff
    style Output fill:#1e1e24,stroke:#f59e0b,stroke-width:2px,color:#fff
