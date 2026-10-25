# 🦅 Eagles Eye

**An AI crop doctor for Ugandan smallholder farmers.**
Snap a photo of a sick crop, get a diagnosis and treatment advice by voice, and feed an early-warning outbreak map for extension officers and NGOs.

Built by **Team Ugandan Eagles** for the **Pre-DevFest Hackathon Kampala 2026** (SDG theme).

---

## 🌍 The Problem

Ugandan smallholder farmers lose an estimated **35-40% of their crops** to pests and diseases such as banana bacterial wilt, coffee wilt, cassava mosaic and fall armyworm. Extension officers are too few and too far away, so farmers often act too late or guess the treatment.

*Source: Watetezi report on challenges faced by smallholder farmers in Uganda.*

## 💡 Our Solution

Eagles Eye works in three layers:

1. **Farmer layer:** upload a photo, get a Gemini diagnosis with treatment steps, severity and voice advice.
2. **Community layer:** every scan is saved anonymously, so nearby farmers can be warned of outbreaks.
3. **Decision-maker layer:** a district heat map helps extension officers, NGOs and the Ministry spot outbreaks early.

## 🎯 Sustainable Development Goals

- **SDG 2:** Zero Hunger (primary)
- **SDG 13:** Climate Action
- **SDG 1:** No Poverty
- **SDG 9:** Industry, Innovation and Infrastructure

## 🛠 Google Tools and What Each One Does

| Tool | Role in the product |
|---|---|
| **Gemini** | Reads the crop photo and returns the diagnosis as structured JSON |
| **Firestore** | Stores anonymised scans that power alerts and the heat map |
| **Firebase Hosting and Auth** | Deploys the app and handles anonymous sign-in |
| **Google Maps** | Draws the outbreak heat map |
| **Cloud Text-to-Speech** | Reads the advice aloud for low-literacy users |
| **Cloud Run** | Hosts the Python API |

## 🏗 Architecture

Farmer app (PWA) → FastAPI on Cloud Run → Gemini API → Firestore → Dashboard (Google Maps heat map)

## 📁 Repository Structure

```
eagles-eye/
├── frontend/    # Farmer app (PWA)
├── dashboard/   # Extension officer heat map
├── backend/     # FastAPI + Gemini integration
├── data/        # Seed script and sample photos
└── docs/        # Brief, data contract, designs, pitch
```

## 🚀 Run Locally

1. Clone the repo:
   ```
   git clone https://github.com/<your-username>/eagles-eye.git
   cd eagles-eye
   ```
2. Copy `.env.example` to `.env` and add your own keys. **Never commit `.env`.**
3. Backend:
   ```
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
4. Frontend and dashboard: see the README inside each folder.

## 🔗 Live Demo

- Farmer app: _link_
- Dashboard: _link_
- Demo video: _link_
- Pitch slides: _link_

## 🗺 Roadmap

- Luganda and other local languages
- SMS/USSD for farmers with feature phones
- Partnerships with extension services and agro-dealers
- Access to credit and fair markets

## ⚠️ Limitations

Eagles Eye is an **advisory tool** and does not replace an extension officer. The demo heat map uses **seeded sample data**; real scans would replace it in production.

## 👥 Team Ugandan Eagles

| Member | Role |
|---|---|
| Stephen Wasswa | Coordinator, product, UX |
| Lyazi Patrick | AI and security |
| Atulinda Derek Solomon | Backend |
| Deborah Nzopi | Farmer app and testing |
| Twahirwa Odriann | Dashboard |
