# 🦅 Eagles Eye

> **AI-Powered Crop Doctor & Outbreak Early-Warning System for Ugandan Smallholder Farmers**  
> Built by **Team Ugandan Eagles** for the **Pre-DevFest Hackathon Kampala 2026** (SDG Theme: Zero Hunger & Climate Action).

---

## 🌍 Overview

Smallholder farmers across Uganda lose an estimated **35–40% of their crop yields** to devastating diseases and pests (such as Banana Bacterial Wilt, Cassava Mosaic Disease, Coffee Leaf Rust, and Fall Armyworm). With agricultural extension officers spread thin across districts, farmers frequently diagnose issues too late or apply incorrect treatments.

**Eagles Eye** solves this through a three-tier intervention:
1. **Farmer Advisory Layer (Mobile Web / PWA):** Farmers snap a photo of an ailing crop and receive instant AI diagnosis with actionable treatment recommendations in English and voice-ready Luganda.
2. **Community Outbreak Layer:** Diagnoses are geotagged (district-level) and logged anonymously to track disease prevalence.
3. **Decision-Maker Surveillance Layer (Web Dashboard):** Agricultural extension officers, NGOs, and local cooperatives visualize live outbreaks on an interactive Google Maps heat map to deploy early interventions.

---

## 📁 Repository Structure & Team Ownership

```
eagles-eye/
├── docs/                      # Architectural specs, API schemas & guidelines
│   ├── DATA_CONTRACT.md       # Agreed JSON data contract between services
│   └── ai-contract.md         # AI prompt engineering & Gemini guidelines
├── backend/                   # Python Flask API + Gemini + Firestore (Derek & Lyazi)
│   ├── app.py                 # Barebones Flask server with CORS & stub routes
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment variable template
├── frontend/                  # Farmer-facing mobile web interface (Deborah)
│   ├── index.html             # HTML5 starter interface referencing Figma wireframes
│   └── mock_data.json         # Static mock diagnosis data matching the contract
├── dashboard/                 # Outbreak surveillance & heat map dashboard (Odriann)
│   ├── index.html             # Dashboard starter interface with Google Maps placeholder
│   └── seed_data.json         # 3 mock outbreak records (Masaka, Mukono, Mbale)
└── data/
    └── sample_crops/          # Test imagery for crops (Banana, Coffee, Cassava, Maize)
```

### Team Roles & Ownership

| Team Member | Role | Component Ownership |
|---|---|---|
| **Stephen Wasswa** | Project Coordinator & Product Lead | Architecture, repo governance, UX & pitch |
| **Atulinda Derek Solomon** | Backend Engineer | `backend/` (Flask API, endpoints, Firestore integration) |
| **Lyazi Patrick** | AI & Security Specialist | `backend/` (Gemini API prompt engineering, multimodal analysis) |
| **Deborah Nzopi** | Frontend Developer | `frontend/` (Farmer PWA, Figma implementation, camera upload, audio) |
| **Twahirwa Odriann** | Dashboard Developer | `dashboard/` (Surveillance dashboard, Google Maps heat map) |

---

## 🚀 Local Setup & Quickstart

### Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome, Firefox, Edge)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Wasswa-Phen/eagles-eye.git
cd eagles-eye
```

### 2. Backend Setup (`backend/`)
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

# Create your local environment configuration
copy .env.example .env     # Windows
# or: cp .env.example .env # macOS/Linux

# Run the Flask development server
python app.py
```
The backend API will start at: `http://localhost:8080`
- **Health check:** `http://localhost:8080/`
- **Diagnostics stub:** `http://localhost:8080/diagnose` (POST)
- **Scans query stub:** `http://localhost:8080/scans` (GET)

### 3. Frontend Development (`frontend/`)
- Open `frontend/index.html` in your browser, or serve it using a local static server:
  ```bash
  # Using Python http.server
  cd frontend
  python -m http.server 3000
  ```
- Access the farmer app at `http://localhost:3000`. It comes pre-linked with `mock_data.json` for unblocked UI development against Figma designs.

### 4. Surveillance Dashboard (`dashboard/`)
- Open `dashboard/index.html` in your browser, or serve it:
  ```bash
  cd dashboard
  python -m http.server 3001
  ```
- Access the extension officer heat map at `http://localhost:3001`. It reads sample outbreak records from `seed_data.json`.

---

## 📜 Data Contract & Schema

All components strictly adhere to the unified JSON schema documented in [docs/DATA_CONTRACT.md](docs/DATA_CONTRACT.md).

Example response payload:
```json
{
  "crop": "Cassava",
  "condition": "Cassava Mosaic Disease (CMD)",
  "confidence": 0.94,
  "severity": "high",
  "is_healthy": false,
  "advice": "Uproot and destroy infected plants immediately to prevent spread via whiteflies. Use certified disease-free stem cuttings for next planting.",
  "advice_luganda": "Simbula era oyokye ebirime ebirwadde mangu ddala okuziyiza okusaasaana kw'olukonvuba lwa whiteflies. Kozesa ebiti ebiramu ebyakakasibwa mu kusimba okuddako.",
  "location": {
    "district": "Mukono",
    "latitude": 0.3549,
    "longitude": 32.7523
  },
  "timestamp": "2026-10-26T14:30:00Z"
}
```

---

## 🛠 Google Technologies Used

- **Google GenAI / Gemini 2.5/Flash:** Multimodal computer vision analysis of crop leaves and diagnostic synthesis.
- **Google Cloud Firestore:** Scalable NoSQL persistence for anonymous scan metadata and geographic outbreak points.
- **Google Maps JavaScript API:** Visualizing outbreak intensity layers and district clusters.
- **Cloud Run:** Containerized deployment for the Python Flask backend.

---

## ⚠️ Advisory Disclaimer
Eagles Eye is an assistive diagnostic advisory system designed to augment agricultural practices. It does not replace field visits by certified agricultural extension specialists.
