# 🦠 InfoDemics - Misinformation Spread Visualization

An interactive web application that visualizes and simulates misinformation spread using the **SIR (Susceptible-Infected-Recovered)** epidemiological model on Twitter network data analyzing 5G conspiracy theories.

![InfoDemics Banner](https://img.shields.io/badge/InfoDemics-Misinformation%20Simulator-red?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Project Overview

This project analyzes the spread of 5G conspiracy theories on Twitter using network science and epidemiological modeling. It provides interactive visualizations and simulations to understand how misinformation propagates through social networks.

### Key Features

- 🕸️ **Interactive Network Visualization** - 161 nodes, 266 edges with physics-based layout
- 📊 **SIR Model Simulation** - Mathematical modeling of information spread dynamics
- 🚫 **Intervention Analysis** - Test the impact of removing super-spreaders
- 📈 **Real-time Analytics** - Track Susceptible, Infected, and Recovered populations
- 🎨 **Beautiful UI** - Modern, responsive web interface

## 📁 Project Structure

```
InfoDemics/
├── 📂 apps/                     # Web applications
│   ├── app.py                   # Streamlit web app
│   ├── InfoDemics.html          # Standalone HTML app
│   ├── InfoDemics.ipynb         # Jupyter notebook version
│   ├── start_server.py          # Local HTTP server
│   ├── run_simulation.py        # CLI simulation script
│   └── requirements.txt         # Python dependencies
│
├── 📂 notebooks/                # Analysis & Engineering
│   ├── 01_Data_Cleaning_Spark.ipynb        # Data preprocessing
│   ├── 02_EDA_and_Network_Analysis.ipynb   # Exploratory analysis
│   └── 03_SIR_Model_Testing.ipynb          # Model testing
│
├── 📂 data/                     # Processed datasets
│   ├── nodes.csv                # Network nodes (161 users)
│   └── edges.csv                # Network edges (266 connections)
│
├── 📂 docs/                     # Documentation
│   ├── Walkthrough_PDF.html     # Print-ready walkthrough
│   └── PDF_Instructions.md      # PDF generation guide
│
├── README.md                    # This file
├── QUICKSTART.md                # Quick start guide
└── .gitignore                   # Git ignore rules
```

## 🚀 Quick Start

### Option 1: Standalone HTML App (Easiest - No Installation!)

1. **Start the server:**
   ```bash
   cd apps
   python3 start_server.py
   ```

2. **Open in browser:**
   - Automatically opens at `http://localhost:8000/InfoDemics.html`
   - Use interactive controls to run simulations
   - No package installation required!

### Option 2: Jupyter Notebook (Best for Analysis)

1. **Navigate to notebooks:**
   ```bash
   cd notebooks
   jupyter notebook
   ```

2. **Open and run:**
   - `01_Data_Cleaning_Spark.ipynb` - Data preprocessing
   - `02_EDA_and_Network_Analysis.ipynb` - Network analysis
   - `03_SIR_Model_Testing.ipynb` - SIR model experiments

### Option 3: Streamlit Web App (Full Features)

1. **Install dependencies:**
   ```bash
   cd apps
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## 📊 Dataset Information

### Network Statistics
- **Nodes**: 161 Twitter users
- **Edges**: 266 interactions (retweets, mentions)
- **Conspiracy Nodes**: ~65% of network
- **Non-Conspiracy Nodes**: ~35% of network

### Node Attributes
- `id`: Unique user identifier
- `label`: Category (5G_Conspiracy_Graphs, Non_Conspiracy_Graphs, Other_Graphs)
- `followers`: Number of followers
- `friends`: Number of friends/connections

### Edge Attributes
- `source`: Source user ID
- `target`: Target user ID

## 🔬 SIR Model Explanation

The **SIR Model** is an epidemiological model adapted for information spread:

### States
- **S (Susceptible)**: Users who haven't been exposed to misinformation
- **I (Infected)**: Users who believe/share misinformation
- **R (Recovered)**: Users who fact-checked and stopped spreading

### Parameters
- **β (Beta)**: Infection rate (0.0 - 1.0) - Probability of misinformation spreading
- **γ (Gamma)**: Recovery rate (0.0 - 1.0) - Probability of fact-checking

### Simulation Process
1. Initialize node states based on conspiracy classification
2. For each time step (50 total):
   - Infected nodes may spread to susceptible neighbors (probability β)
   - Infected nodes may recover (probability γ)
3. Track S, I, R populations over time

## 🎨 Visualization Features

### Network Graph
- **Color Coding**:
  - 🔴 Red: Conspiracy/Infected nodes
  - 🔵 Blue: Non-Conspiracy/Susceptible nodes
  - 🟢 Green: Recovered nodes
- **Node Size**: Proportional to follower count
- **Interactive**: Hover for details, drag to rearrange

### SIR Curves
- Real-time Plotly charts
- Three lines: Susceptible, Infected, Recovered
- Interactive hover information
- Shows peak infection time and magnitude

## 🚫 Super-Spreader Intervention

Test the effectiveness of targeted content moderation:

1. **Enable "Ban Top 1% Influencers"**
2. **Run simulation**
3. **Compare results:**
   - Baseline: Full network
   - Intervention: Top 1% removed
   - Expected: 30-40% reduction in peak infection

## 📈 Sample Results

### Default Parameters (β=0.3, γ=0.1)

**Baseline Simulation:**
- Peak Infection: ~120-140 nodes (time step 15-20)
- Final Recovered: ~100-120 nodes
- Final Infected: ~10-20 nodes

**With Intervention (Ban Top 1%):**
- Peak Infection: ~80-100 nodes (reduced by 30-40%)
- Slower spread rate
- Lower final infection count

## 🛠️ Technical Stack

### Frontend
- HTML/CSS/JavaScript (Standalone app)
- Streamlit (Web framework)
- Vis.js (Network visualization)
- Plotly.js (Interactive charts)

### Backend
- Python 3.8+
- NetworkX (Graph algorithms)
- Pandas (Data manipulation)
- NumPy (Numerical computations)

### Notebooks
- Jupyter
- PySpark (Data cleaning)
- Matplotlib/Seaborn (Visualization)

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Installation and setup guide
- **[docs/PDF_Instructions.md](docs/PDF_Instructions.md)** - How to generate PDF walkthrough
- **[notebooks/](notebooks/)** - Detailed analysis notebooks

## 🎓 Educational Use

This tool is designed for:
- Understanding network-based contagion models
- Analyzing social media misinformation dynamics
- Testing intervention strategies
- Data science and network science education
- Research on information spread

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional intervention strategies
- More sophisticated infection models (SEIR, SIRS)
- Network metrics dashboard
- Comparative analysis tools

## 📄 License

This project is for educational purposes. Feel free to use and modify.

## 🙏 Acknowledgments

- SIR Model: Kermack-McKendrick (1927)
- Network Science: NetworkX library
- Visualization: Vis.js and Plotly teams
- Framework: Streamlit

## 📞 Contact

**Repository**: [github.com/Youssef-Adel91/InfoDemics](https://github.com/Youssef-Adel91/InfoDemics)

---

**Built with ❤️ for understanding misinformation spread through network science**
