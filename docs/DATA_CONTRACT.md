# 🦅 Eagles Eye — Unified Data Contract

> **Version:** 1.0.0 (Pre-DevFest Hackathon 2026)  
> **Author:** Stephen Wasswa (Project Coordinator)  
> **Stakeholders:** Derek & Lyazi (Backend), Deborah (Frontend), Odriann (Dashboard)  
> **Status:** Agreed Baseline Schema

---

## 1. Overview & Purpose

This document defines the formal data schema exchanged across all subsystems of **Eagles Eye**:
- **Backend API (`backend/`)**: Produces diagnostic predictions via Gemini and serves persisted scan history from Firestore.
- **Farmer Web App (`frontend/`)**: Consumes the diagnosis payload to display farmer advisory results and trigger Luganda voice readout.
- **Surveillance Dashboard (`dashboard/`)**: Consumes historical and aggregated scan records to plot regional outbreak heat maps.

All components MUST conform to this contract to allow parallel, unblocked development across team members.

---

## 2. Core Diagnosis Schema

Each diagnosis record represents a completed crop assessment.

### Field Definitions

| Field | Type | Required | Description / Constraints | Example |
|---|---|---|---|---|
| `crop` | `string` | **Yes** | Common name of the recognized crop. Allowed values include: `"Banana / Matooke"`, `"Cassava"`, `"Coffee"`, `"Maize"`, `"Beans"`, `"Tomato"`, `"Unknown"`. | `"Cassava"` |
| `condition` | `string` | **Yes** | Identified pest, pathogen, deficiency, or `"Healthy"`. If unrecognizable, use `"Unknown"`. | `"Cassava Mosaic Disease (CMD)"` |
| `confidence` | `number` | **Yes** | Qualitative model certainty normalized between `0.00` and `1.00`. | `0.94` |
| `severity` | `string` | **Yes** | Urgency and damage level. Enum: `"none"`, `"low"`, `"moderate"`, `"high"`. | `"high"` |
| `is_healthy` | `boolean` | **Yes** | `true` if crop exhibits no disease/pest damage; `false` if condition detected. | `false` |
| `advice` | `string` | **Yes** | Plain-language, actionable guidance for smallholder farmers in English. | `"Uproot and destroy infected plants immediately. Plant certified disease-free cuttings."` |
| `advice_luganda` | `string` | **Yes** | Contextually translated Luganda guidance suitable for text display and Text-to-Speech (TTS) audio playback. | `"Simbula era oyokye ebirime ebirwadde mangu ddala okuziyiza okusaasaana..."` |
| `location` | `object` | **Yes** | District-level geographic context for community surveillance. | See Location Object below |
| `timestamp` | `string` | **Yes** | ISO-8601 UTC timestamp format: `YYYY-MM-DDTHH:MM:SSZ`. | `"2026-10-26T14:30:00Z"` |

### Nested `location` Object

| Sub-field | Type | Required | Description | Example |
|---|---|---|---|---|
| `district` | `string` | **Yes** | Ugandan administrative district where scan was recorded. | `"Mukono"` |
| `latitude` | `number` | **Yes** | Decimal coordinate latitude (WGS 84). | `0.3549` |
| `longitude` | `number` | **Yes** | Decimal coordinate longitude (WGS 84). | `32.7523` |

---

## 3. API Endpoints

### 3.1 `POST /diagnose`
Analyzes an uploaded crop photo and returns the diagnostic assessment.

- **Request Type:** `multipart/form-data`
  - `image`: Binary file (JPEG/PNG/WebP, max 5MB).
  - `district`: *(Optional, string)* e.g., `"Masaka"` (defaults to `"Unknown"` if omitted).
  - `crop_hint`: *(Optional, string)* Farmer-provided crop hint if known.

- **Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "crop": "Banana / Matooke",
    "condition": "Banana Bacterial Wilt (BXW)",
    "confidence": 0.92,
    "severity": "high",
    "is_healthy": false,
    "advice": "Cut down the infected plant at ground level and bury plant residues. Disinfect all farming tools with fire or bleach before using them on other plants.",
    "advice_luganda": "Sazaako ekitooke ekirwadde wansi ku ttaka era oziike ebisigalira. Oziyize okusaasaana ng'ookya ebyuma oba okubizika mu ddagala lya klorini.",
    "location": {
      "district": "Masaka",
      "latitude": -0.3411,
      "longitude": 31.7361
    },
    "timestamp": "2026-10-26T15:10:00Z"
  }
}
```

- **Inconclusive / Low Quality Image Response (200 OK):**
```json
{
  "status": "inconclusive",
  "data": {
    "crop": "Unknown",
    "condition": "Inconclusive Image",
    "confidence": 0.25,
    "severity": "none",
    "is_healthy": false,
    "advice": "The photo is too blurry or distant to provide an accurate diagnosis. Please take a closer, well-lit photo of the affected leaves or stems.",
    "advice_luganda": "Ekifanyi kino tekirabika bulungi oba kiri wala nnyo. Nsaba okube ekifanyi ekirala ekiri okumpi era nga kiriko ekitangaala eky'amaanyi.",
    "location": {
      "district": "Unknown",
      "latitude": 0.3476,
      "longitude": 32.5825
    },
    "timestamp": "2026-10-26T15:12:00Z"
  }
}
```

---

### 3.2 `GET /scans`
Retrieves logged scans for surveillance mapping.

- **Query Parameters:**
  - `district` *(optional)*: Filter by district name (e.g. `?district=Masaka`).
  - `limit` *(optional)*: Number of records (default: 50).

- **Success Response (200 OK):**
```json
{
  "status": "success",
  "count": 3,
  "scans": [
    {
      "id": "scan_001",
      "crop": "Banana / Matooke",
      "condition": "Banana Bacterial Wilt (BXW)",
      "confidence": 0.95,
      "severity": "high",
      "is_healthy": false,
      "advice": "Cut down the infected pseudostem immediately and de-bud using a wooden fork.",
      "advice_luganda": "Temako ekitooke ekirwadde mangu ddala era okozese ekitayiriro okuggyako empumpu.",
      "location": {
        "district": "Masaka",
        "latitude": -0.3411,
        "longitude": 31.7361
      },
      "timestamp": "2026-10-26T10:15:00Z"
    },
    {
      "id": "scan_002",
      "crop": "Cassava",
      "condition": "Cassava Mosaic Disease (CMD)",
      "confidence": 0.88,
      "severity": "moderate",
      "is_healthy": false,
      "advice": "Rogue out stunted or curling cassava plants. Inspect for whitefly infestations.",
      "advice_luganda": "Simbula ebiwuka ebikyamye ebiraga obulwadde bwa mosaic. Kebera obuwuka obweru.",
      "location": {
        "district": "Mukono",
        "latitude": 0.3549,
        "longitude": 32.7523
      },
      "timestamp": "2026-10-26T11:45:00Z"
    },
    {
      "id": "scan_003",
      "crop": "Coffee",
      "condition": "Coffee Leaf Rust (CLR)",
      "confidence": 0.91,
      "severity": "high",
      "is_healthy": false,
      "advice": "Prune excess branches to improve aeration and apply approved copper-based fungicides before wet seasons.",
      "advice_luganda": "Saalira emiti gy'emmwanyi okuyingiza empewo era osaaseeko eddagala lya kopa erikakasibwa ng'enkuba tenatandika.",
      "location": {
        "district": "Mbale",
        "latitude": 1.0784,
        "longitude": 34.1754
      },
      "timestamp": "2026-10-26T13:20:00Z"
    }
  ]
}
```

---

### 3.3 `GET /`
Health check endpoint.
```json
{
  "status": "healthy",
  "service": "Eagles Eye API",
  "version": "1.0.0"
}
```

---

## 4. Implementation Guidelines by Team Member

- **Derek (Backend Lead):**
  - Implement request validation for incoming `multipart/form-data` uploads.
  - Persist valid diagnosis records to Google Cloud Firestore (`scans` collection).
  - Serve `GET /scans` with appropriate query filtering and pagination.

- **Lyazi (AI & Security):**
  - Write the Gemini structured prompt (JSON schema mode) enforcing these exact keys.
  - Formulate natural language advice and accurate Luganda translations in the prompt.
  - Safeguard the `GEMINI_API_KEY` on the server-side.

- **Deborah (Frontend Lead):**
  - Read `frontend/mock_data.json` during UI prototyping.
  - Build the diagnostic card reflecting `crop`, `condition`, `severity` badge, `advice`, and a TTS voice button for `advice_luganda`.

- **Odriann (Dashboard Lead):**
  - Use `dashboard/seed_data.json` for initial Google Maps heat map and marker testing.
  - Connect the dashboard to `GET /scans` for live district outbreak visualization.
