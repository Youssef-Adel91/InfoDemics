# 🚀 How to Run InfoDemics After Restructuring

## Quick Fix for the Error

The error happens because the server needs to run from the **project root**, not from the `apps/` folder.

### ✅ Solution: Restart the Server

1. **Stop the current server:**
   - Go to the PowerShell window running the server
   - Press `Ctrl + C`

2. **Start the server from the correct location:**
   ```bash
   cd "d:\me\semester 5\BigData\project\misInfoProject"
   python3 apps/start_server.py
   ```

3. **Access the app:**
   - Browser will open to: `http://localhost:8000/apps/InfoDemics.html`
   - Or manually navigate to that URL

---

## Alternative: Use the Updated Paths

The `start_server.py` has been updated to serve from the project root, so it will automatically find the data files in `data/` folder.

---

## File Structure Reference

```
InfoDemics/  (← Run server from HERE)
├── apps/
│   └── InfoDemics.html (accesses ../data/nodes.csv)
├── data/
│   ├── nodes.csv
│   └── edges.csv
└── apps/start_server.py (serves from parent directory)
```

---

## Commands Summary

**Stop server:** `Ctrl + C` in the PowerShell window

**Start server (from project root):**
```bash
cd "d:\me\semester 5\BigData\project\misInfoProject"
python3 apps/start_server.py
```

**Access app:**
```
http://localhost:8000/apps/InfoDemics.html
```

---

The server is configured to serve from the project root, so all relative paths (`../data/nodes.csv`) will work correctly!
