# PassMetric

**PassMetric** is a high-performance password security evaluator that bridges the gap between theoretical mathematical entropy and empirical, real-world data breach exposure. 

PassMetric helps users understand password strength using local entropy calculations and zero-knowledge data breach verification.

---

## Key Features

* **Mathematical Entropy Scoring:** Utilizes advanced pattern-matching heuristics (via `zxcvbn`) to evaluate structural complexity, common dictionary words, keyboard patterns, and estimated crack times locally.
* **Zero-Knowledge Privacy (K-Anonymity):** Checks passwords against public breach logs via the HaveIBeenPwned API using SHA-1 prefix hashing (`k-Anonymity`). Your plain-text password and full hash **never** leave your machine.
* **Empirical Research Script:** Includes a standalone benchmarking module (`benchmark.py`) that generates scatter plots analyzing the correlation between password entropy and breach frequency.

---

## Project Structure

```text
pass-metric/ (Root)
│
├── ⚙️ Backend & Entry Points
│   ├── app.py                ──> Flask Backend Application
│   └── benchmark.py          ──> Empirical Research & Plotting Module
│
├── 📦 Configuration & Metadata
│   ├── requirements.txt      ──> Dependencies & Environment Setup
│   ├── .gitignore            ──> Git Ignored Files & Rules
│   ├── LICENSE               ──> MIT License
│   └── README.md             ──> Project Documentation
│
└── 🎨 Interface & Presentation
    └── templates/
        └── index.html        ──> Web Dashboard UI
```

---

## Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3, JavaScript
* **Cryptographic & Analytical Libraries:** `zxcvbn`, `requests`, `matplotlib`, `hashlib`

---

## Getting Started Locally

### Prerequisites
Make sure you have Python installed on your system.

### 1. Install Dependencies
Open your terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

### 2. Run the Web Application
Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

### 3. Run the Research Benchmark
To generate the empirical research graph comparing entropy scores to breach logs:
```bash
python benchmark.py
```
This will produce a `research_benchmark_plot.png` file in your root folder.

---

## Architecture Overview (K-Anonymity Flow)

```text
               +----------------------------------+
               |       User Input (Password)      |
               +----------------------------------+
                                |
        +-----------------------+-----------------------+
        |                                               |
        v                                               v
+---------------+                               +---------------+
| Local zxcvbn  |                               | Local SHA-1   |
| Engine        |                               | Hash Engine   |
+---------------+                               +---------------+
        |                                               |
        v                                               v
+---------------+                               +---------------+
| Calculate     |                               | Complete      |
| Entropy Score |                               | Hash String   |
| & Crack Time  |                               +---------------+
+---------------+                                       |
        |                       +-----------------------+
        |                       |
        |                       v
        |               +-----------------------+
        |               | Extract First 5 Chars |
        |               | (Hash Prefix)         |
        |               +-----------------------+
        |                       |
        |                       v  (HTTPS GET Query)
        |               +-----------------------+
        |               | HaveIBeenPwned API    |
        |               +-----------------------+
        |                       |
        |                       v  (Returns List of Matching Suffixes)
        |               +-----------------------+
        |               | Local Client Matcher  |
        |               | (Compare Hash Suffix) |
        |               +-----------------------+
        |                       |
        +-----------------------+
                                |
                                v
               +----------------------------------+
               | Consolidated UI Response Display |
               +----------------------------------+
```

---

## License

Distributed under the MIT License. See the `LICENSE` file for more details.