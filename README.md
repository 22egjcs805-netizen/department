# 🛒 Smart Departmental Store — Billing System

A simple Python **Tkinter** desktop application for a departmental store.
Browse products by category, add items to cart, and generate a printed bill.

---

## 📁 Project Structure

```
departmental-store/
├── app/
│   └── store_app.py          # Main application (all-in-one)
├── k8s/
│   └── deployment.yaml       # Kubernetes manifests
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions CI/CD
├── Dockerfile                # Docker container config
├── requirements.txt          # Python dependencies (none external)
└── README.md
```

---

## ✅ Features

- 5 product categories: Groceries, Beverages, Snacks, Dairy, Personal Care
- Add items with custom quantity via a Spinbox
- Live cart with subtotal, 5% GST, and total
- Generate and save bill as a `.txt` file
- Customer name & phone capture

---

## 🚀 Part 1 — Run Locally (VS Code)

### Prerequisites
- Python 3.8+ installed
- Tkinter comes **built-in** with Python on Windows/macOS

> **Linux users:** run `sudo apt install python3-tk` if Tkinter is missing

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/departmental-store.git
cd departmental-store

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Run the app — no pip install needed!
python app/store_app.py
```

### VS Code Tips
- Install the **Python** extension (ms-python.python)
- Open the project folder: `File → Open Folder`
- Press **F5** or use the Run button to launch `store_app.py`
- Set breakpoints in the gutter to debug

---

## 🐙 Part 2 — GitHub Setup

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit: departmental store app"

# Create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/departmental-store.git
git branch -M main
git push -u origin main
```

### Add Docker Hub Secrets (for CI/CD)
1. Go to your GitHub repo → **Settings → Secrets and variables → Actions**
2. Click **New repository secret** and add:
   | Secret Name       | Value                    |
   |-------------------|--------------------------|
   | `DOCKER_USERNAME` | Your Docker Hub username |
   | `DOCKER_PASSWORD` | Your Docker Hub password |

---

## 🐳 Part 3 — Docker

### Build & Run Locally

```bash
# Build the image
docker build -t departmental-store .

# Run on Windows (requires VcXsrv or X410 for GUI)
docker run -e DISPLAY=host.docker.internal:0 departmental-store

# Run on Linux (X11 socket sharing)
docker run -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           departmental-store
```

### Push to Docker Hub

```bash
# Tag and push
docker tag departmental-store YOUR_USERNAME/departmental-store:latest
docker push YOUR_USERNAME/departmental-store:latest
```

### X11 on Windows (one-time setup)
1. Download & install **VcXsrv**: https://sourceforge.net/projects/vcxsrv/
2. Launch **XLaunch** → choose "Multiple windows" → tick "Disable access control"
3. Now Docker can forward the GUI to your desktop

---

## ☸️ Part 4 — Kubernetes

> **Note:** Kubernetes is designed for web services. Running a Tkinter GUI in K8s
> requires X11 forwarding or a VNC server. This is best used for staging/testing.

### Prerequisites
- Minikube or a real cluster
- `kubectl` configured

### Steps

```bash
# 1. Update the image name in k8s/deployment.yaml
#    Replace: your-dockerhub-username/departmental-store:latest

# 2. Apply manifests
kubectl apply -f k8s/deployment.yaml

# 3. Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# 4. View logs
kubectl logs <pod-name>

# 5. Delete deployment
kubectl delete -f k8s/deployment.yaml
```

---

## 🔄 Full DevOps Flow

```
Write code in VS Code
       ↓
git commit & push to GitHub
       ↓
GitHub Actions triggers automatically
       ↓
Docker image built & pushed to Docker Hub
       ↓
(Optional) kubectl apply deploys to Kubernetes
```

---

## 🛠 Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: tkinter` | `sudo apt install python3-tk` (Linux) |
| Docker GUI not showing | Start VcXsrv (Windows) or allow X11 (`xhost +local:docker`) |
| K8s pod CrashLoopBackOff | Check `kubectl logs <pod>` — likely no display server |
| GitHub Actions failing | Check DOCKER_USERNAME/PASSWORD secrets are set correctly |

---

## 📄 License
MIT — free to use and modify.