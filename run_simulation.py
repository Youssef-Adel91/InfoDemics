"""
InfoDemics - Simplified Version
Runs with minimal dependencies, generates HTML visualizations
"""

import sys
import os

print("=" * 70)
print("InfoDemics - Misinformation Spread Simulator")
print("=" * 70)

# Check Python version
print(f"\n✓ Python {sys.version.split()[0]}")

# Try to import required packages
print("\nChecking dependencies...")
missing = []

try:
    import pandas as pd
    print("✓ pandas")
except ImportError:
    missing.append("pandas")
    print("✗ pandas - MISSING")

try:
    import numpy as np
    print("✓ numpy")
except ImportError:
    missing.append("numpy")
    print("✗ numpy - MISSING")

try:
    import networkx as nx
    print("✓ networkx")
except ImportError:
    missing.append("networkx")
    print("✗ networkx - MISSING")

if missing:
    print("\n" + "=" * 70)
    print("⚠️  MISSING PACKAGES DETECTED")
    print("=" * 70)
    print("\nYou have several options:\n")
    
    print("OPTION 1: Install via MSYS2 pacman (Recommended for your system)")
    print("-" * 70)
    print("Open MSYS2 terminal and run:")
    print("  pacman -Syu")
    print("  pacman -S mingw-w64-x86_64-python-pandas")
    print("  pacman -S mingw-w64-x86_64-python-numpy")
    print("  pacman -S mingw-w64-x86_64-python-networkx")
    
    print("\nOPTION 2: Install Python from python.org")
    print("-" * 70)
    print("1. Download from: https://www.python.org/downloads/")
    print("2. Install with 'Add to PATH' checked")
    print("3. Then run: pip install pandas numpy networkx")
    
    print("\nOPTION 3: Use Google Colab (No installation needed!)")
    print("-" * 70)
    print("1. Go to: https://colab.research.google.com/")
    print("2. Upload InfoDemics.ipynb")
    print("3. Run all cells - packages install automatically")
    
    print("\n" + "=" * 70)
    sys.exit(1)

# If we get here, all packages are available
print("\n✓ All required packages installed!\n")

# Load data
print("Loading network data...")
try:
    nodes_df = pd.read_csv('nodes.csv')
    edges_df = pd.read_csv('edges.csv')
    print(f"✓ Loaded {len(nodes_df)} nodes and {len(edges_df)} edges\n")
except FileNotFoundError as e:
    print(f"✗ Error: {e}")
    print("Make sure nodes.csv and edges.csv are in the same directory!")
    sys.exit(1)

# Preprocess data
nodes_df = nodes_df.rename(columns={'followers': 'followers_count', 'friends': 'degree'})

def classify_label(label):
    if 'Non_Conspiracy' in str(label):
        return 'Non-Conspiracy'
    elif 'Conspiracy' in str(label):
        return 'Conspiracy'
    else:
        return 'Non-Conspiracy'

nodes_df['category'] = nodes_df['label'].apply(classify_label)

# Calculate actual degree
degree_dict = {}
for node_id in nodes_df['id']:
    degree = len(edges_df[edges_df['source'] == node_id]) + len(edges_df[edges_df['target'] == node_id])
    degree_dict[node_id] = degree
nodes_df['actual_degree'] = nodes_df['id'].map(degree_dict)

# Create NetworkX graph
print("Building network graph...")
G = nx.Graph()

for _, node in nodes_df.iterrows():
    G.add_node(node['id'], label=node['category'], 
               followers_count=node['followers_count'],
               degree=node['actual_degree'])

for _, edge in edges_df.iterrows():
    if G.has_node(edge['source']) and G.has_node(edge['target']):
        G.add_edge(edge['source'], edge['target'])

print(f"✓ Graph created: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges\n")

# Network statistics
print("=" * 70)
print("NETWORK STATISTICS")
print("=" * 70)
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Density: {nx.density(G):.4f}")
print(f"Connected: {nx.is_connected(G)}")

conspiracy_count = len(nodes_df[nodes_df['category'] == 'Conspiracy'])
print(f"\nConspiracy nodes: {conspiracy_count}")
print(f"Non-Conspiracy nodes: {len(nodes_df) - conspiracy_count}")

degrees = [G.degree(n) for n in G.nodes()]
print(f"\nAverage degree: {np.mean(degrees):.2f}")
print(f"Max degree: {np.max(degrees)}")

# Top influencers
top_5 = sorted(nodes_df.itertuples(), key=lambda x: x.actual_degree, reverse=True)[:5]
print(f"\nTop 5 Influencers:")
for i, node in enumerate(top_5, 1):
    print(f"  {i}. Node {node.id}: {node.actual_degree} connections ({node.category})")

# SIR Simulation
print("\n" + "=" * 70)
print("RUNNING SIR SIMULATION")
print("=" * 70)

beta = 0.3
gamma = 0.1
time_steps = 50

print(f"Parameters: β={beta}, γ={gamma}, time_steps={time_steps}\n")

# Initialize states
states = {}
conspiracy_nodes = [n for n in G.nodes() if G.nodes[n]['label'] == 'Conspiracy']
for node in G.nodes():
    states[node] = 'I' if node in conspiracy_nodes else 'S'

# Track history
sir_history = {'time': [], 'S': [], 'I': [], 'R': []}

print("Running simulation...")
for t in range(time_steps):
    s_count = sum(1 for s in states.values() if s == 'S')
    i_count = sum(1 for s in states.values() if s == 'I')
    r_count = sum(1 for s in states.values() if s == 'R')
    
    sir_history['time'].append(t)
    sir_history['S'].append(s_count)
    sir_history['I'].append(i_count)
    sir_history['R'].append(r_count)
    
    new_states = states.copy()
    
    # Infections
    for node in G.nodes():
        if states[node] == 'S':
            infected_neighbors = [n for n in G.neighbors(node) if states[n] == 'I']
            if infected_neighbors:
                infection_prob = 1 - (1 - beta) ** len(infected_neighbors)
                if np.random.random() < infection_prob:
                    new_states[node] = 'I'
    
    # Recoveries
    for node in G.nodes():
        if states[node] == 'I':
            if np.random.random() < gamma:
                new_states[node] = 'R'
    
    states = new_states
    
    if (t + 1) % 10 == 0:
        print(f"  Step {t+1}: S={s_count}, I={i_count}, R={r_count}")

print("\n✓ Simulation complete!\n")

# Results
peak_infected = max(sir_history['I'])
peak_time = sir_history['I'].index(peak_infected)

print("=" * 70)
print("SIMULATION RESULTS")
print("=" * 70)
print(f"Peak infection: {peak_infected} nodes at time step {peak_time}")
print(f"Final state:")
print(f"  Susceptible: {sir_history['S'][-1]}")
print(f"  Infected: {sir_history['I'][-1]}")
print(f"  Recovered: {sir_history['R'][-1]}")

# Generate simple HTML visualization
print("\n" + "=" * 70)
print("GENERATING VISUALIZATION")
print("=" * 70)

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>InfoDemics - SIR Simulation Results</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
        h1 {{ color: #FF4B4B; text-align: center; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #f0f2f6; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #333; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🦠 InfoDemics - SIR Simulation Results</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" style="color: #1E88E5;">{sir_history['S'][-1]}</div>
                <div class="stat-label">Susceptible</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #FF4B4B;">{sir_history['I'][-1]}</div>
                <div class="stat-label">Infected</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #4CAF50;">{sir_history['R'][-1]}</div>
                <div class="stat-label">Recovered</div>
            </div>
        </div>
        
        <div id="chart"></div>
        
        <div style="margin-top: 30px; padding: 20px; background: #f0f2f6; border-radius: 8px;">
            <h3>📊 Key Findings</h3>
            <ul>
                <li><strong>Peak Infection:</strong> {peak_infected} nodes at time step {peak_time}</li>
                <li><strong>Network Size:</strong> {G.number_of_nodes()} nodes, {G.number_of_edges()} edges</li>
                <li><strong>Initial Infected:</strong> {conspiracy_count} conspiracy nodes</li>
                <li><strong>Parameters:</strong> β={beta}, γ={gamma}</li>
            </ul>
        </div>
    </div>
    
    <script>
        var trace1 = {{
            x: {sir_history['time']},
            y: {sir_history['S']},
            mode: 'lines+markers',
            name: 'Susceptible',
            line: {{color: '#1E88E5', width: 3}}
        }};
        
        var trace2 = {{
            x: {sir_history['time']},
            y: {sir_history['I']},
            mode: 'lines+markers',
            name: 'Infected',
            line: {{color: '#FF4B4B', width: 3}}
        }};
        
        var trace3 = {{
            x: {sir_history['time']},
            y: {sir_history['R']},
            mode: 'lines+markers',
            name: 'Recovered',
            line: {{color: '#4CAF50', width: 3}}
        }};
        
        var data = [trace1, trace2, trace3];
        
        var layout = {{
            title: 'SIR Model: Misinformation Spread Over Time',
            xaxis: {{title: 'Time Steps'}},
            yaxis: {{title: 'Number of Nodes'}},
            hovermode: 'x unified',
            height: 500
        }};
        
        Plotly.newPlot('chart', data, layout);
    </script>
</body>
</html>
"""

output_file = 'sir_results.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✓ Visualization saved to: {output_file}")
print(f"\nOpen this file in your browser to see the interactive chart!")

# Save CSV results
results_df = pd.DataFrame(sir_history)
csv_file = 'sir_results.csv'
results_df.to_csv(csv_file, index=False)
print(f"✓ Data saved to: {csv_file}")

print("\n" + "=" * 70)
print("✅ SIMULATION COMPLETE!")
print("=" * 70)
print(f"\nNext steps:")
print(f"1. Open {output_file} in your web browser")
print(f"2. View the interactive SIR curves")
print(f"3. Check {csv_file} for raw data")
print("\n" + "=" * 70)
