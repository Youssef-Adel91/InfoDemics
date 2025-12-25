# InfoDemics - Quick Start Guide

## 🚀 Easiest Option: Google Colab (No Installation Required!)

**This is the FASTEST way to run the project:**

1. Go to: https://colab.research.google.com/
2. Click "File" → "Upload notebook"
3. Upload `InfoDemics.ipynb` from your project folder
4. Click "Runtime" → "Run all"
5. Packages install automatically and simulation runs!

---

## 💻 Local Installation Options

### Option 1: Install Packages via MSYS2 (For your current Python)

Open **MSYS2 terminal** (not PowerShell) and run:

```bash
# Update package database
pacman -Syu

# Install required packages
pacman -S mingw-w64-x86_64-python-pandas
pacman -S mingw-w64-x86_64-python-numpy  
pacman -S mingw-w64-x86_64-python-networkx
```

Then run the simulation:
```bash
cd "/d/me/semester 5/BigData/project/misInfoProject"
python3 run_simulation.py
```

---

### Option 2: Install Standard Python (Recommended for Windows)

1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Download Python 3.11 or 3.12
   
2. **Install with these settings:**
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"
   - Click "Install Now"

3. **After installation, open NEW PowerShell and run:**
   ```powershell
   cd "d:\me\semester 5\BigData\project\misInfoProject"
   pip install pandas numpy networkx
   python run_simulation.py
   ```

---

### Option 3: Use Anaconda (Best for Data Science)

1. **Download Anaconda:**
   - Go to: https://www.anaconda.com/download
   - Download and install

2. **Open Anaconda Prompt and run:**
   ```bash
   cd "d:\me\semester 5\BigData\project\misInfoProject"
   conda install pandas numpy networkx
   python run_simulation.py
   ```

---

## 📊 What Each Script Does

### `run_simulation.py` (Simplest)
- Checks if packages are installed
- Runs SIR simulation with default parameters
- Generates `sir_results.html` (open in browser)
- Saves `sir_results.csv` (raw data)

### `InfoDemics.ipynb` (Most Interactive)
- Jupyter notebook with widgets
- Interactive parameter controls
- Best for exploration and analysis
- Requires: Jupyter (`pip install jupyter`)

### `app.py` (Full Web App)
- Complete Streamlit application
- Professional UI with sidebar controls
- Requires: Streamlit (`pip install streamlit`)
- Run with: `streamlit run app.py`

---

## ⚡ Quick Test

To check if packages are installed:

```bash
python3 -c "import pandas, numpy, networkx; print('✅ All packages ready!')"
```

If you see "✅ All packages ready!" then run:
```bash
python3 run_simulation.py
```

---

## 🎯 Recommended Path

**For quickest results:**
1. Use Google Colab (no installation needed)
2. Upload `InfoDemics.ipynb`
3. Run all cells
4. Done in 2 minutes!

**For local development:**
1. Install standard Python from python.org
2. Install packages: `pip install pandas numpy networkx`
3. Run: `python run_simulation.py`
4. Open `sir_results.html` in browser

---

## 📞 Still Having Issues?

The `run_simulation.py` script will show you exactly which packages are missing and provide installation instructions.

Just run:
```bash
python3 run_simulation.py
```

It will guide you through the next steps!
