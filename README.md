# InfoDemics - Misinformation Spread Visualization

An interactive Streamlit web application that visualizes and simulates misinformation spread using the **SIR (Susceptible-Infected-Recovered)** epidemiological model on Twitter network data.

![InfoDemics Banner](https://img.shields.io/badge/InfoDemics-Misinformation%20Simulator-red?style=for-the-badge)

## 🎯 Project Overview

This application analyzes the spread of 5G conspiracy theories on Twitter using network science and epidemiological modeling. It provides:

- **Interactive Network Visualization**: See how misinformation spreads through social networks
- **SIR Model Simulation**: Mathematical modeling of information spread dynamics
- **Intervention Analysis**: Test the impact of removing super-spreaders
- **Real-time Analytics**: Track Susceptible, Infected, and Recovered populations over time

## 🚀 Features

### 1. Interactive Network Graph
- Visualize Twitter user network with 161 nodes and 266 edges
- Color-coded nodes: Red (Conspiracy/Infected), Blue (Non-Conspiracy/Susceptible), Green (Recovered)
- Node size proportional to follower count
- Click nodes to see detailed statistics

### 2. SIR Simulation Engine
- **Beta (β)**: Infection rate - probability of misinformation spreading
- **Gamma (γ)**: Recovery rate - probability of fact-checking/recovery
- Discrete-time simulation over 50 time steps
- Realistic network-based contagion model

### 3. Super-Spreader Intervention
- Toggle to remove top 1% most connected users
- Compare simulation results with/without intervention
- Analyze the impact of targeted content moderation

### 4. Dynamic Visualization
- Real-time SIR curves using Plotly
- Animated infection spread on network graph
- Downloadable simulation results (CSV)

## 📋 Requirements

### CSV File Format

**nodes.csv**
```csv
id,label,followers,friends
3449030,Non_Conspiracy_Graphs,16,16
13969437,5G_Conspiracy_Graphs,12,13
...
```

**Columns:**
- `id` (string/int): Unique user identifier
- `label` (string): Category - must contain "Conspiracy", "Non_Conspiracy", or "Other"
- `followers` (int): Number of followers (determines node size)
- `friends` (int): Number of friends/connections

**edges.csv**
```csv
source,target
10285276,10930230
10930230,44757832
...
```

**Columns:**
- `source` (string/int): Source user ID
- `target` (string/int): Target user ID

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download this repository**
   ```bash
   cd misInfoProject
   ```

2. **Install dependencies**
   
   **For MSYS2/MinGW Python (if you see "externally-managed" errors):**
   ```bash
   pacman -S mingw-w64-x86_64-python-pip
   pacman -S mingw-w64-x86_64-python-pandas
   pacman -S mingw-w64-x86_64-python-numpy
   pip install streamlit networkx pyvis plotly
   ```
   
   **For standard Python installations:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Alternative (using Python module):**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Ensure CSV files are in the project directory**
   ```
   misInfoProject/
   ├── app.py
   ├── requirements.txt
   ├── nodes.csv
   └── edges.csv
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

## 📖 How to Use

### Running a Simulation

1. **Configure Parameters** (Left Sidebar):
   - Adjust **β (Infection Rate)**: 0.0 to 1.0 (default: 0.3)
     - Higher values = faster spread
   - Adjust **γ (Recovery Rate)**: 0.0 to 1.0 (default: 0.1)
     - Higher values = faster fact-checking/recovery
   - Set **Initial Infected %**: Percentage of nodes starting as infected

2. **Choose Intervention** (Optional):
   - Enable "Ban Top 1% Influencers" to remove super-spreaders
   - Compare results with baseline simulation

3. **Run Simulation**:
   - Click "▶️ Run Simulation" button
   - Watch the network update with infection states
   - View SIR curves in real-time

4. **Analyze Results**:
   - Check peak infection time and magnitude
   - Review final statistics (S/I/R counts)
   - Download simulation data for further analysis

### Understanding the Visualization

- **Network Graph** (Left Panel):
  - Red nodes: Currently infected with misinformation
  - Blue nodes: Susceptible to misinformation
  - Green nodes: Recovered (fact-checked)
  - Larger nodes: More followers (higher influence)

- **SIR Curves** (Right Panel):
  - Blue line: Susceptible population over time
  - Red line: Infected population over time
  - Green line: Recovered population over time

## 🧮 SIR Model Explanation

The **SIR Model** is an epidemiological model adapted for information spread:

### States
- **S (Susceptible)**: Users who haven't been exposed to misinformation
- **I (Infected)**: Users who believe/share misinformation
- **R (Recovered)**: Users who fact-checked and stopped spreading

### Transitions
1. **S → I**: Susceptible becomes Infected
   - Probability: `1 - (1 - β)^n` where n = number of infected neighbors
   
2. **I → R**: Infected becomes Recovered
   - Probability: `γ` per time step

### Conservation Law
`S(t) + I(t) + R(t) = N` (constant total population)

## 🔧 Troubleshooting

### Common Issues

**Error: "Could not find CSV files"**
- Ensure `nodes.csv` and `edges.csv` are in the same directory as `app.py`
- Check file names are exactly `nodes.csv` and `edges.csv` (case-sensitive on Linux/Mac)

**Network graph not displaying**
- Try refreshing the page
- Check browser console for JavaScript errors
- Ensure you have a stable internet connection (PyVis loads some resources)

**Simulation runs slowly**
- This is normal for large networks
- Consider reducing the number of time steps (modify `time_steps` parameter in code)

**Import errors**
- Run `pip install -r requirements.txt` again
- Ensure you're using Python 3.8+
- Try creating a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

## 📊 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **NetworkX**: Graph algorithms and network analysis
- **PyVis**: Interactive network visualization
- **Plotly**: Dynamic charting
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations

### Algorithm Complexity
- Graph construction: O(V + E) where V = nodes, E = edges
- SIR simulation: O(T × E) where T = time steps
- Visualization: O(V + E)

### Data Processing
1. Load CSV files with Pandas
2. Map column names to expected schema
3. Classify nodes into Conspiracy/Non-Conspiracy categories
4. Calculate actual network degree from edge list
5. Build NetworkX graph with node attributes
6. Run SIR simulation with discrete-time updates
7. Visualize with PyVis and Plotly

## 🎓 Educational Use

This tool is designed for:
- Understanding network-based contagion models
- Analyzing social media misinformation dynamics
- Testing intervention strategies
- Data science and network science education
- Research on information spread

## 📝 Citation

If you use this tool in your research, please cite:

```
InfoDemics: Interactive Misinformation Spread Visualization
Built with Streamlit, NetworkX, and PyVis
SIR Model Implementation for Social Network Analysis
```

## 🤝 Contributing

Suggestions and improvements are welcome! Areas for enhancement:
- Additional intervention strategies
- More sophisticated infection models (SEIR, SIRS)
- Network metrics dashboard
- Comparative analysis tools
- Export visualizations as images

## 📄 License

This project is for educational purposes. Feel free to use and modify.

## 🙏 Acknowledgments

- SIR Model: Kermack-McKendrick (1927)
- Network Science: NetworkX library
- Visualization: PyVis and Plotly teams
- Framework: Streamlit

---

**Built with ❤️ for understanding misinformation spread through network science**
