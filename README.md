# 🛡️ IDS Attack Classifier XGBoost

![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![XGBoost](https://img.shields.io/badge/ML-XGBoost-F37626?style=flat&logo=xgboost&logoColor=white)

An End-to-End, Full-Stack MLOps project that leverages Supervised Machine Learning (**XGBoost & Random Forest**) to classify and profile network traffic into 15 distinct states (1 Benign + 14 Attack types). Trained on the massive **CICIDS2017** dataset (~2.8M flows), this system features a FastAPI backend, a modern React (Vite) SOC dashboard, and is fully containerized using **Docker** for seamless production deployment.

## 🌟 Key Features
- **Dual-Mode Scanning:** Users can manually inject the 6 most critical network flow parameters via an interactive cyber-themed dashboard or upload a full CSV file for batch processing and threat hunting.
- **Smart Background Imputation:** The trained ML models expect exactly 78 features. To drastically improve User Experience (UX), the API dynamically injects a zero-padded baseline for the missing 72 features in the background. This allows the user to manually input only the most important features (like `Bwd Packet Length Std` and `Init_Win_bytes_forward`) without crashing the strict scaler.
- **Dockerized Architecture:** The entire stack (React frontend and FastAPI backend) is containerized, eliminating version conflicts and ensuring a smooth "plug-and-play" experience across all operating systems.

## 🏗️ System Architecture
The machine learning pipeline is built with a modular, production-ready Object-Oriented design:
1. **DataLoader:** Ingests the raw CICIDS2017 CSV files, merges them, and cleans infinite/NaN values.
2. **Preprocessor:** Handles feature scaling (`StandardScaler`) and label encoding (`LabelEncoder`).
3. **Model Tuner:** Uses `RandomizedSearchCV` to dynamically find the optimal hyperparameters for the ensemble models.
4. **Predictive Engine:** Powered by an optimized `XGBoost` model that achieved **99.85% Accuracy** on testing data.
5. **API & Frontend:** A decoupled FastAPI backend serving predictions to a Framer Motion-animated React dashboard.

## 🧠 MLOps & Engineering Challenges Solved
- **Preventing "Shortcut Learning" (Data Leakage):** Initial models relied heavily on `Destination Port` to classify attacks. Realizing that attackers can easily spoof ports, I dropped this feature. This forced the algorithm to learn genuine, hard-to-spoof behavioral patterns (packet timings, variances), creating a robust, real-world IDS.
- **Handling Extreme Imbalance & XGBoost Strictness:** The dataset contains extreme class imbalances (e.g., 1 row for `Heartbleed`, millions for `BENIGN`). During Cross-Validation, XGBoost crashed because rare classes were missing in certain folds. I engineered a targeted sampling and filtering mechanism during the tuning phase, allowing XGBoost to find optimal parameters (`learning_rate: 0.2`, `subsample: 0.8`) and boosting its F1-Score to **99.84%**.
- **Network vs. Application Layer Insights:** The system achieved near-perfect recall for network/transport layer attacks (DDoS, PortScan). However, it highlighted a known cybersecurity limitation: Network-flow models struggle with payload-based attacks (XSS, SQL Injection). This transparent failure is a documented strength, proving the model relies on flow metadata rather than overfitting.

## 🛠️ Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Machine Learning** | Python, Scikit-Learn, Pandas, Numpy, Joblib, **XGBoost** |
| **Backend API** | FastAPI, Uvicorn, Python-Multipart |
| **Frontend Dashboard**| React.js (Vite), TailwindCSS, Framer Motion, Axios |
| **DevOps / Deployment** | Docker, Docker-Compose |

## 🚀 How to Run the Project

Because the entire application is containerized, you don't need to install Python, Node.js, or any ML libraries on your local machine.

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/) installed and running on your machine.

### Installation & Execution
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Djilali-77/attack_classification.git
   cd attack_classification
   ```

2. **Build and start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
- **Frontend SOC Dashboard:** Open your browser and navigate to 👉 `http://localhost:5173`
- **Backend API (Swagger UI):** Open your browser and navigate to 👉 `http://localhost:8000/docs`

> **Note for Mac users:** If Safari fails to connect to `localhost:5173`, simply use `http://127.0.0.1:5173` instead.

### 🛑 How to Stop the Application
To safely shut down the containers and free up the ports, press `Ctrl+C` in the terminal, then run:
```bash
docker-compose down
```