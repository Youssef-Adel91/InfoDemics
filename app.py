import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import plotly.graph_objects as go
import numpy as np
import tempfile
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="InfoDemics - Misinformation Spread Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🦠 InfoDemics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Misinformation Spread Visualization using SIR Models</div>', unsafe_allow_html=True)

# Initialize session state
if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False
if 'sir_data' not in st.session_state:
    st.session_state.sir_data = None
if 'selected_node' not in st.session_state:
    st.session_state.selected_node = None

@st.cache_data
def load_data():
    """Load and preprocess the network data"""
    try:
        # Load CSV files
        nodes_df = pd.read_csv('nodes.csv')
        edges_df = pd.read_csv('edges.csv')
        
        # Rename columns to match expected schema
        nodes_df = nodes_df.rename(columns={
            'followers': 'followers_count',
            'friends': 'degree'
        })
        
        # Classify nodes based on label
        def classify_label(label):
            if 'Non_Conspiracy' in str(label):
                return 'Non-Conspiracy'
            elif 'Conspiracy' in str(label):
                return 'Conspiracy'
            else:
                return 'Non-Conspiracy'  # Treat "Other" as Susceptible
        
        nodes_df['category'] = nodes_df['label'].apply(classify_label)
        
        # Calculate actual degree from edges
        degree_dict = {}
        for node_id in nodes_df['id']:
            degree = len(edges_df[edges_df['source'] == node_id]) + len(edges_df[edges_df['target'] == node_id])
            degree_dict[node_id] = degree
        
        nodes_df['actual_degree'] = nodes_df['id'].map(degree_dict)
        
        return nodes_df, edges_df
    
    except FileNotFoundError as e:
        st.error(f"Error: Could not find CSV files. Please ensure 'nodes.csv' and 'edges.csv' are in the same directory as app.py")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

def create_network_graph(nodes_df, edges_df, remove_superspreaders=False, superspreader_pct=1):
    """Create NetworkX graph from dataframes"""
    G = nx.Graph()
    
    # Remove super-spreaders if requested
    if remove_superspreaders:
        threshold = np.percentile(nodes_df['actual_degree'], 100 - superspreader_pct)
        nodes_df = nodes_df[nodes_df['actual_degree'] <= threshold].copy()
        st.sidebar.info(f"🚫 Removed {len(nodes_df[nodes_df['actual_degree'] > threshold])} super-spreaders (top {superspreader_pct}%)")
    
    # Add nodes with attributes
    for _, node in nodes_df.iterrows():
        G.add_node(
            node['id'],
            label=node['category'],
            followers_count=node['followers_count'],
            degree=node['actual_degree'],
            original_label=node['label']
        )
    
    # Add edges
    for _, edge in edges_df.iterrows():
        if G.has_node(edge['source']) and G.has_node(edge['target']):
            G.add_edge(edge['source'], edge['target'])
    
    return G, nodes_df

def initialize_sir_states(G, initial_infected_pct):
    """Initialize SIR states for all nodes"""
    states = {}
    nodes = list(G.nodes())
    
    # Get conspiracy nodes (already infected)
    conspiracy_nodes = [n for n in nodes if G.nodes[n]['label'] == 'Conspiracy']
    
    # Calculate additional random infections if needed
    total_infected = int(len(nodes) * initial_infected_pct / 100)
    additional_infected = max(0, total_infected - len(conspiracy_nodes))
    
    # Get susceptible nodes for random infection
    susceptible_nodes = [n for n in nodes if G.nodes[n]['label'] == 'Non-Conspiracy']
    random_infected = np.random.choice(
        susceptible_nodes, 
        size=min(additional_infected, len(susceptible_nodes)), 
        replace=False
    ) if additional_infected > 0 else []
    
    # Set initial states
    for node in nodes:
        if node in conspiracy_nodes or node in random_infected:
            states[node] = 'I'  # Infected
        else:
            states[node] = 'S'  # Susceptible
    
    return states

def run_sir_simulation(G, beta, gamma, initial_infected_pct, time_steps=50):
    """Run SIR model simulation"""
    states = initialize_sir_states(G, initial_infected_pct)
    
    # Track counts over time
    sir_history = {
        'time': [],
        'S': [],
        'I': [],
        'R': []
    }
    
    for t in range(time_steps):
        # Count current states
        s_count = sum(1 for s in states.values() if s == 'S')
        i_count = sum(1 for s in states.values() if s == 'I')
        r_count = sum(1 for s in states.values() if s == 'R')
        
        sir_history['time'].append(t)
        sir_history['S'].append(s_count)
        sir_history['I'].append(i_count)
        sir_history['R'].append(r_count)
        
        # Create new states for next iteration
        new_states = states.copy()
        
        # Process infections (S -> I)
        for node in G.nodes():
            if states[node] == 'S':
                # Check infected neighbors
                infected_neighbors = [n for n in G.neighbors(node) if states[n] == 'I']
                if infected_neighbors:
                    # Probability of infection
                    infection_prob = 1 - (1 - beta) ** len(infected_neighbors)
                    if np.random.random() < infection_prob:
                        new_states[node] = 'I'
        
        # Process recoveries (I -> R)
        for node in G.nodes():
            if states[node] == 'I':
                if np.random.random() < gamma:
                    new_states[node] = 'R'
        
        states = new_states
    
    return sir_history, states

def create_pyvis_network(G, states=None):
    """Create interactive PyVis network visualization"""
    net = Network(height='600px', width='100%', bgcolor='#ffffff', font_color='black')
    
    # Configure physics
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=200, spring_strength=0.001)
    
    # Add nodes
    for node in G.nodes():
        node_data = G.nodes[node]
        
        # Determine color based on state or original label
        if states:
            state = states.get(node, 'S')
            if state == 'I':
                color = '#FF4B4B'  # Red for Infected
            elif state == 'R':
                color = '#4CAF50'  # Green for Recovered
            else:
                color = '#1E88E5'  # Blue for Susceptible
        else:
            color = '#FF4B4B' if node_data['label'] == 'Conspiracy' else '#1E88E5'
        
        # Size based on followers
        size = 10 + (node_data['followers_count'] / 2)
        
        # Create title (tooltip)
        title = f"ID: {node}<br>Category: {node_data['label']}<br>Followers: {node_data['followers_count']}<br>Degree: {node_data['degree']}"
        
        net.add_node(
            node,
            label=str(node),
            color=color,
            size=size,
            title=title
        )
    
    # Add edges
    for edge in G.edges():
        net.add_edge(edge[0], edge[1], color='#cccccc')
    
    return net

def plot_sir_curves(sir_history):
    """Create animated SIR curves using Plotly"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sir_history['time'],
        y=sir_history['S'],
        mode='lines+markers',
        name='Susceptible',
        line=dict(color='#1E88E5', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=sir_history['time'],
        y=sir_history['I'],
        mode='lines+markers',
        name='Infected',
        line=dict(color='#FF4B4B', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=sir_history['time'],
        y=sir_history['R'],
        mode='lines+markers',
        name='Recovered',
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='SIR Model: Misinformation Spread Over Time',
        xaxis_title='Time Steps',
        yaxis_title='Number of Nodes',
        hovermode='x unified',
        height=400,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

# Sidebar controls
st.sidebar.header("🎛️ Simulation Controls")

# Load data
nodes_df, edges_df = load_data()

# Display dataset info
st.sidebar.markdown("### 📊 Dataset Info")
st.sidebar.metric("Total Nodes", len(nodes_df))
st.sidebar.metric("Total Edges", len(edges_df))
conspiracy_count = len(nodes_df[nodes_df['category'] == 'Conspiracy'])
st.sidebar.metric("Conspiracy Nodes", conspiracy_count)

st.sidebar.markdown("---")

# Simulation parameters
st.sidebar.markdown("### 🔬 SIR Parameters")

beta = st.sidebar.slider(
    "β (Infection Rate)",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.05,
    help="Probability of infection spreading from infected to susceptible neighbor"
)

gamma = st.sidebar.slider(
    "γ (Recovery/Fact-Check Rate)",
    min_value=0.0,
    max_value=1.0,
    value=0.1,
    step=0.05,
    help="Probability of infected node recovering (fact-checking)"
)

initial_infected_pct = st.sidebar.slider(
    "Initial Infected %",
    min_value=0,
    max_value=100,
    value=int((conspiracy_count / len(nodes_df)) * 100),
    step=5,
    help="Percentage of nodes initially infected"
)

st.sidebar.markdown("---")

# Super-spreader intervention
st.sidebar.markdown("### 🚫 Intervention Strategy")
remove_superspreaders = st.sidebar.checkbox(
    "Ban Top 1% Influencers",
    value=False,
    help="Remove the top 1% most connected nodes before simulation"
)

st.sidebar.markdown("---")

# Run simulation button
run_simulation = st.sidebar.button("▶️ Run Simulation", type="primary")

if run_simulation:
    with st.spinner("Running SIR simulation..."):
        # Create graph
        G, filtered_nodes = create_network_graph(nodes_df, edges_df, remove_superspreaders)
        
        # Run simulation
        sir_history, final_states = run_sir_simulation(G, beta, gamma, initial_infected_pct)
        
        # Store in session state
        st.session_state.simulation_run = True
        st.session_state.sir_data = sir_history
        st.session_state.final_states = final_states
        st.session_state.G = G

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 🕸️ Network Visualization")
    
    if st.session_state.simulation_run:
        # Show network with final states
        net = create_pyvis_network(st.session_state.G, st.session_state.final_states)
    else:
        # Show initial network
        G, _ = create_network_graph(nodes_df, edges_df, remove_superspreaders)
        net = create_pyvis_network(G)
    
    # Save and display network
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as f:
        net.save_graph(f.name)
        with open(f.name, 'r', encoding='utf-8') as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=620, scrolling=False)

with col2:
    st.markdown("### 📈 SIR Dynamics")
    
    if st.session_state.simulation_run and st.session_state.sir_data:
        # Plot SIR curves
        fig = plot_sir_curves(st.session_state.sir_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show final statistics
        st.markdown("### 📊 Final Statistics")
        final_s = st.session_state.sir_data['S'][-1]
        final_i = st.session_state.sir_data['I'][-1]
        final_r = st.session_state.sir_data['R'][-1]
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Susceptible", final_s, delta=None)
        col_b.metric("Infected", final_i, delta=None)
        col_c.metric("Recovered", final_r, delta=None)
        
        # Peak infection
        peak_infected = max(st.session_state.sir_data['I'])
        peak_time = st.session_state.sir_data['I'].index(peak_infected)
        st.info(f"🔥 Peak Infection: {peak_infected} nodes at time step {peak_time}")
        
        # Download results
        if st.button("💾 Download Simulation Data"):
            df_results = pd.DataFrame(st.session_state.sir_data)
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="sir_simulation_results.csv",
                mime="text/csv"
            )
    else:
        st.info("👈 Configure parameters and click 'Run Simulation' to see results")
        
        # Show legend
        st.markdown("### 🎨 Color Legend")
        st.markdown("""
        - 🔴 **Red**: Conspiracy/Infected nodes
        - 🔵 **Blue**: Non-Conspiracy/Susceptible nodes
        - 🟢 **Green**: Recovered nodes (after simulation)
        """)
        
        st.markdown("### ℹ️ How It Works")
        st.markdown("""
        1. **Set Parameters**: Adjust β (infection rate) and γ (recovery rate)
        2. **Choose Intervention**: Optionally ban top influencers
        3. **Run Simulation**: Watch misinformation spread through the network
        4. **Analyze Results**: Compare different scenarios
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p><strong>InfoDemics</strong> - Understanding Misinformation Spread through Network Science</p>
    <p>Built with Streamlit, NetworkX, and PyVis | SIR Model Implementation</p>
</div>
""", unsafe_allow_html=True)
