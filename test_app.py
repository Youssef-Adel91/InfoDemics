"""
Test script to verify the InfoDemics application logic without Streamlit
"""
import sys

print("Testing InfoDemics Application Components...")
print("=" * 60)

# Test 1: Check Python version
print(f"\n1. Python Version: {sys.version}")
if sys.version_info < (3, 8):
    print("   ❌ ERROR: Python 3.8+ required")
    sys.exit(1)
else:
    print("   ✓ Python version OK")

# Test 2: Check if CSV files exist
print("\n2. Checking CSV files...")
import os
if os.path.exists('nodes.csv'):
    print("   ✓ nodes.csv found")
else:
    print("   ❌ nodes.csv NOT found")

if os.path.exists('edges.csv'):
    print("   ✓ edges.csv found")
else:
    print("   ❌ edges.csv NOT found")

# Test 3: Try importing required modules
print("\n3. Checking required packages...")
required_packages = {
    'pandas': 'Data manipulation',
    'numpy': 'Numerical computations',
    'networkx': 'Graph algorithms',
    'streamlit': 'Web framework',
    'pyvis': 'Network visualization',
    'plotly': 'Interactive charts'
}

missing_packages = []
for package, description in required_packages.items():
    try:
        __import__(package)
        print(f"   ✓ {package:15} - {description}")
    except ImportError:
        print(f"   ❌ {package:15} - {description} (NOT INSTALLED)")
        missing_packages.append(package)

# Test 4: If pandas is available, test data loading
if 'pandas' not in missing_packages:
    print("\n4. Testing data loading...")
    try:
        import pandas as pd
        nodes_df = pd.read_csv('nodes.csv')
        edges_df = pd.read_csv('edges.csv')
        print(f"   ✓ Loaded {len(nodes_df)} nodes")
        print(f"   ✓ Loaded {len(edges_df)} edges")
        print(f"   ✓ Node columns: {list(nodes_df.columns)}")
        print(f"   ✓ Edge columns: {list(edges_df.columns)}")
    except Exception as e:
        print(f"   ❌ Error loading data: {e}")

# Test 5: If networkx is available, test graph creation
if 'networkx' not in missing_packages and 'pandas' not in missing_packages:
    print("\n5. Testing graph creation...")
    try:
        import networkx as nx
        G = nx.Graph()
        G.add_nodes_from(nodes_df['id'])
        for _, edge in edges_df.iterrows():
            if edge['source'] in nodes_df['id'].values and edge['target'] in nodes_df['id'].values:
                G.add_edge(edge['source'], edge['target'])
        print(f"   ✓ Created graph with {G.number_of_nodes()} nodes")
        print(f"   ✓ Graph has {G.number_of_edges()} edges")
        print(f"   ✓ Graph is connected: {nx.is_connected(G)}")
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            print(f"   ℹ Number of components: {len(components)}")
            print(f"   ℹ Largest component size: {len(max(components, key=len))}")
    except Exception as e:
        print(f"   ❌ Error creating graph: {e}")

# Summary
print("\n" + "=" * 60)
if missing_packages:
    print(f"\n❌ MISSING PACKAGES: {', '.join(missing_packages)}")
    print("\nTo install missing packages, run:")
    print(f"   python3 -m pip install {' '.join(missing_packages)}")
    print("\nOr install all at once:")
    print("   python3 -m pip install -r requirements.txt")
else:
    print("\n✅ All packages installed! Ready to run the app.")
    print("\nTo start the application, run:")
    print("   streamlit run app.py")

print("\n" + "=" * 60)
