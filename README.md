# ⚽ Football AI Betting System 
### *Probabilistic Match Prediction Engine powered by TrueSkill & Monte Carlo Simulations*

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)

---

## 📖 Introduction

This project is an advanced **Football Match Prediction System** that goes beyond simple win/loss statistics. It combines **Microsoft's TrueSkill™** ranking algorithm with a **Bayesian Monte Carlo Simulation** to calculate the exact probability distributions of match outcomes.

Unlike traditional betting models that output a single predicted score, this AI "plays" the upcoming match **10,000 times** in a virtual environment to determine the most likely outcomes, factoring in:
- Team Skill ($\mu$) & Uncertainty ($\sigma$)
- Attack vs. Defense Strength
- Head-to-Head History
- Expected Goals (xG) & Form Decay

---

## 🧠 The AI Engine: How It Works

### 1. The Ranking System (TrueSkill)
We track every team's skill as a Gaussian distribution, not a single number (like Elo).
- **$\mu$ (Mu)**: The team's perceived skill level.
- **$\sigma$ (Sigma)**: The mathematical uncertainty (e.g., standard deviation) of that skill.
*When a new team plays, $\sigma$ is high. As they play more matches, $\sigma$ drops, giving us higher confidence.*

### 2. The "Multiverse" Simulation
To predict a match (e.g., Real Madrid vs. Barcelona):
1.  **Calculate Parameters**: The model computes expected goal rates ($\lambda$) based on skill differences and venue advantage.
2.  **Simulate**: It runs **10,000 simulations** using Poisson distributions.
3.  **Analyze**: It aggregates the results to find:
    - **Home Win %**
    - **Draw %**
    - **Away Win %**
    - **Confidence Score** (based on data consistency)

---

## 🏗️ Technical Architecture

The system is built as a set of Dockerized microservices:

| Service | Tech Stack | Role |
|:---|:---|:---|
| **Frontend** | React, Vite, TailwindCSS | Interactive Dashboard for users to select matches & view predictions. |
| **Backend** | Python, FastAPI, NumPy | The API handling math logic, database queries, and simulations. |
| **Database** | PostgreSQL, SQLModel | Stores teams, matches, bets, and historical stats. |
| **Cache** | Redis | Caches prediction results for high-speed access. |
| **AI Core** | SciPy, TrueSkill | The mathematical libraries powering the logic. |

---

## 🚀 Getting Started

### Prerequisites
- **Docker** and **Docker Compose** installed on your machine.

### Installation & Run
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/projetIA2dialzeb.git
    cd projetIA2dialzeb
    ```

2.  **Launch with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    *This will build the Python backend and React frontend images and start the database.*

3.  **Access the Application**:
    - **Frontend (UI)**: [http://localhost:5173](http://localhost:5173)
    - **Backend (API Docs)**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Initial Data
On first launch, the database is empty. The system includes a seeding script to populate it with:
- Top 5 European Leagues
- Synthetic Match History (to train the TrueSkill model)
- Fictional "Player Attributes" for deeper analysis.

---

## 📂 Project Structure

```bash
├── backend/
│   ├── app/
│   │   ├── bayesian_model.py    # The core AI simulation logic
│   │   ├── trueskill_ai_engine.py  # Wrapper for Microsoft TrueSkill
│   │   ├── opta_engine.py       # Advanced metrics (xG, Betting margins)
│   │   ├── routes/              # API Endpoints (FastAPI)
│   │   └── models.py            # Database Schemas (SQLModel)
│   ├── Dockerfile               # Backend container config
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PredictionDashboard.jsx  # Main UI
│   │   │   └── CustomComponents.jsx     # Layout stability library
│   │   └── services/            # API connectors
│   └── Dockerfile               # Frontend container config
├── docker-compose.yml           # Service orchestration
└── READY_TO_RUN.md              # Quick start guide
```

---

## 📊 Key Features

-   **Real-time Odds Calculation**: Converts probabilities into Decimal Odds.
-   **Confidence Metrics**: Warns the user if the prediction is based on insufficient data ("High Volatility Warning").
-   **Visual Analytics**: Displays match outcome probabilities as bar charts.
-   **Layout Stability**: Custom UI components to prevent layout shift during data loading.

---

## 📝 License
This project is for educational purposes as part of a Computer Science Masters project.
