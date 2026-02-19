# 🚀 HRTech Platform - Quick Start Guide

## Running the Platform

### Simple One-Command Startup

Just run this command from **any location**:

```powershell
.\start-platform.ps1
```

**That's it!** The script will:
- ✅ Automatically find the backend folder
- ✅ Start the FastAPI server on port 8000
- ✅ Open the frontend in your browser
- ✅ Show you the status and URLs

---

## 📋 Available Commands

### Start the Platform
```powershell
.\start-platform.ps1
```

### Stop the Platform
```powershell
.\stop-platform.ps1
```

---

## 🔧 Manual Commands (If you prefer)

### Start Backend Only
```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Open Frontend
Just double-click `index.html` or run:
```powershell
start index.html
```

---

## 📍 Important URLs

| Service | URL |
|---------|-----|
| **Frontend** | Open `index.html` in browser |
| **Backend API** | http://localhost:8000 |
| **API Documentation** | http://localhost:8000/docs |
| **API Redoc** | http://localhost:8000/redoc |

---

## 💡 Usage Flow

1. **Upload Resume** → Upload candidate resumes (PDF, DOCX, TXT)
2. **Create Job** → Define job requirements and skills
3. **Rank Candidates** → Run the ranking algorithm
4. **View Results** → See detailed explanations and scores

---

## 🛠️ Troubleshooting

### "Port 8000 is already in use"
Run the stop script first:
```powershell
.\stop-platform.ps1
```

### "Python not found"
Install Python 3.8+ from https://www.python.org/

### Script execution disabled
Run this command once (as Administrator):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📦 Project Structure

```
hrtech-platform/
├── start-platform.ps1      # 🚀 One-click startup script
├── stop-platform.ps1       # 🛑 Stop all services
├── index.html              # 🌐 Frontend application
├── backend/                # ⚙️ FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── apis/
│   │   ├── services/
│   │   └── models/
│   └── hrtech_db.db       # 💾 SQLite database
└── README_STARTUP.md      # 📖 This file
```

---

## 🎯 Features

### Ranking Algorithm
- **Skills Match** (45% weight) - Compares candidate skills to job requirements
- **Experience Match** (35% weight) - Years of experience alignment
- **Seniority Alignment** (20% weight) - Seniority level fit

### Chat-Style Explanations
Each candidate gets 5 detailed insights:
- 🔧 Skills Match Analysis
- 📈 Experience Analysis
- 🎯 Seniority Alignment
- ⭐ Overall Assessment
- 💡 Key Insights

---

## 📧 Support

For issues, check:
1. Backend logs in the PowerShell window
2. Browser console (F12) for frontend errors
3. API documentation at http://localhost:8000/docs

---

**Enjoy using the HRTech Platform! 🎉**
