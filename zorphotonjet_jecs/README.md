# 📜 Scripts for JEC studies


## 💻 Running the code
### ❗Prerequisite
Use a new ```CMSSW``` version e.g. ```12_6_5``` only for the environment setup (ROOT etc).

### :bulb: Check the available options  
```bash 
python3 analysis.py --help
```

### 🔍 Run locally (1 input root file, eg Photon channel) 
```bash 
python3 analysis.py -o output.root -c Photon --max_events -1
```

### 🖱️ Submit to HTCondor cluster
Check the directory ```HTCondor```
