# Product Requirement Document (PRD)

**Project:** FLOW-ALGO — Real-Time Context-Aware Music Intelligence & Autoplay Engine  
**Author:** Akshat Barthwal  
**Target Delivery:** Q3 2026  
**Status:** Live Production (Deployed on Streamlit)  
**Target Audience:** Technical Leadership, Staff ML Engineers, and Product Review Boards  

---

## 1. Problem Statement & Context Collapse

* **Definition:** Traditional music recommendation systems use collaborative filtering or k-nearest neighbor (k-NN) models that rely on static item-to-item similarity and broad metadata tags. These systems fail to evaluate the continuous, immediate auditory environment of the listener.
* **User Failure Mode:** A listener who seeds an initial queue for late-night focus frequently encounters high-tempo, aggressive tracks (e.g., 150 BPM rage-trap) simply because of a shared artist or producer credit.
* **Industry Benchmark:** Across major streaming services, autoplay skip rates sit between 35% and 45% before reaching the 30-second monetization threshold.

---

## 2. Goals & Measurable Success Metrics

* **North Star Metric:** Reduce early (first-30-second) autoplay skip rates from the ~42% industry baseline down to <24% in live test sessions.
* **30-Second Stream-Through Rate:** Achieve >70% completion for top-ranked recommended autoplay tracks (industry baseline: ~50%).
* **Parametric Guardrail Safety:** 0.00% leakage rate for tracks outside defined tempo tolerances ($|\Delta\text{BPM}| > 12$) or energy thresholds ($|\Delta\text{Energy}| > 0.15$).
* **Harmonic Adjacency:** >80% of sequential autoplay transitions must satisfy Camelot Wheel adjacency rules (exact key match, relative major/minor, or adjacent 5th interval).
* **Latency SLA:** Sub-85 ms $p95$ recommendation latency across a 100k in-memory track vector space using vectorized NumPy operations.

---

## 3. User Personas & Use Cases

* **The Deep Focus Worker:** Requires steady acoustic parameters; zero tolerance for abrupt dynamic shifts or BPM spikes during high-focus sessions.
* **The Contextual Explorer:** Seeks track discovery within strict environmental boundaries (e.g., late-night highway driving vs. morning high-focus routines).

---

## 4. Algorithmic Architecture & Functional Requirements

### Stage 1: Dynamic Queue Centroid Extraction
* **Real-Time Vector Extraction:** Calculate the session acoustic centroid $\vec{C}_{\text{session}}$ across active queue items in real time:
  $$\vec{C}_{\text{session}} = \left[ \overline{\text{BPM}}, \overline{\text{Energy}}, \overline{\text{Valence}} \right]$$
* **Context Classifier:** Dynamically maps $\vec{C}_{\text{session}}$ to discrete listener archetypes (e.g., *Contemporary Silk R&B*, *Late-Night Solo Highway Drive*, *Underground Warehouse Rave*).

### Stage 2: Zero-Leak Parametric Gating
* **Deterministic Filtering:** Discards any catalog candidate failing strict acoustic boundary limits:
  $$|\Delta\text{BPM}| \le 12 \quad \text{and} \quad |\Delta\text{Energy}| \le 0.15$$
* **Sub-Genre Blacklisting:** Enforces strict categorical exclusion of conflicting subgenres (e.g., hardstyle or rage-trap during downtempo sessions).

### Stage 3: Harmonic Mixing & Stochastic Exploration
* **Camelot Compatibility Scoring:** Applies discrete transition weights based on Camelot key distance:
  * Identical Key ($N\text{A} \rightarrow N\text{A}$): $1.0$
  * Relative Mode Switch ($N\text{A} \leftrightarrow N\text{B}$): $0.9$
  * Adjacent 5th Step ($N \pm 1$): $0.8$
  * Incompatible / Dissonant: $0.0$
* **Boltzmann Exploration Sampling:** Mitigates deterministic discovery loops by sampling candidates from a softmax distribution:
  $$P(i) = \frac{\exp(S_i / \tau)}{\sum_j \exp(S_j / \tau)}$$
  * Temperature parameter set to $\tau = 0.75$ to balance acoustic affinity with serendipity.

---

## 5. UI Telemetry & Explainability (XAI)

* **Session Readouts:** Live visual indicators for session Mean BPM, Energy envelopes, and active archetype badges.
* **Explainable Flow Scores:** Each recommendation displays an explainable match coefficient (e.g., `44/100 Flow Score`) describing acoustic fit.
* **Catalog Vector Projection:** Live 2D scatter visualization plotting the active session coordinate against the broader 100k vector catalog distribution.
* **Deep Linking:** Direct streaming resolution endpoints for Apple Music, Spotify, and YouTube.

---

## 6. Non-Functional Requirements & Edge Cases

* **Cold-Start Queue:** If a session is initiated with an empty queue, initialize state using curated archetype seeds to avoid cold-start stalls.
* **Candidate Pool Starvation:** If strict parametric gating yields fewer than 5 candidates, progressively widen the energy boundary by $+0.05$ increments while holding harmonic filters constant.
* **Compute Constraints:** Store track feature embeddings in indexed in-memory arrays to ensure sub-85 ms retrieval on standard CPU instances.
