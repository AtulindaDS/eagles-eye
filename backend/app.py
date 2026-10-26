"""
Eagles Eye — Backend API Server
Team: Ugandan Eagles (Pre-DevFest Hackathon Kampala 2026)
Backend Leads: Atulinda Derek Solomon (Derek) & Lyazi Patrick (Lyazi)

This is a starter skeleton providing CORS-enabled Flask routes and stub responses
matching docs/DATA_CONTRACT.md to unblock frontend and dashboard team members.
"""

import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for frontend & dashboard clients
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
PORT = int(os.environ.get("PORT", 8080))
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")


# ------------------------------------------------------------------------------
# 1. Health Check Endpoint
# ------------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def health_check():
    """
    Health check route for Cloud Run and connectivity testing.
    """
    return jsonify({
        "status": "healthy",
        "service": "Eagles Eye API",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200


# ------------------------------------------------------------------------------
# 2. Crop Diagnosis Endpoint (POST /diagnose)
# ------------------------------------------------------------------------------
@app.route("/diagnose", methods=["POST"])
def diagnose_crop():
    """
    Diagnoses an uploaded crop image and returns treatment advice.
    Currently returns a stub response conforming to docs/DATA_CONTRACT.md.

    TODO (Derek):
      - Validate incoming multipart/form-data request and 'image' file.
      - Reject invalid MIME types, empty payloads, or images exceeding 5MB.
      - Save successful diagnosis records into Google Cloud Firestore ('scans' collection).

    TODO (Lyazi):
      - Initialize Google GenAI client using GEMINI_API_KEY.
      - Pass uploaded image bytes into Gemini 2.5 Flash with structured prompt.
      - Enforce JSON response matching the data contract schema (crop, condition,
        confidence, severity, is_healthy, advice, advice_luganda, location, timestamp).
      - Gracefully handle low-confidence or non-crop images (status: 'inconclusive').
    """
    # Placeholder stub data for testing frontend connectivity
    stub_diagnosis = {
        "status": "success",
        "message": "Stub response: Backend connection successful. Implement full Gemini logic.",
        "data": {
          "crop": "Cassava",
          "condition": "Cassava Mosaic Disease (CMD)",
          "confidence": 0.94,
          "severity": "high",
          "is_healthy": False,
          "advice": "Uproot and destroy infected plants immediately to prevent spread via whiteflies. Use certified disease-free stem cuttings for next planting.",
          "advice_luganda": "Simbula era oyokye ebirime ebirwadde mangu ddala okuziyiza okusaasaana kw'olukonvuba lwa whiteflies. Kozesa ebiti ebiramu ebyakakasibwa mu kusimba okuddako.",
          "location": {
            "district": request.form.get("district", "Mukono"),
            "latitude": 0.3549,
            "longitude": 32.7523
          },
          "timestamp": datetime.now(timezone.utc).isoformat()
        }
    }

    return jsonify(stub_diagnosis), 200


# ------------------------------------------------------------------------------
# 3. Surveillance Scans Endpoint (GET /scans)
# ------------------------------------------------------------------------------
@app.route("/scans", methods=["GET"])
def get_scans():
    """
    Returns recent crop diagnosis records for the outbreak heat map dashboard.
    Currently returns sample stub records conforming to docs/DATA_CONTRACT.md.

    TODO (Derek):
      - Query Google Cloud Firestore 'scans' collection.
      - Add optional query parameter filtering (e.g. ?district=Masaka, ?limit=50).
      - Order results by timestamp descending.
    """
    stub_scans = [
        {
            "id": "scan_001",
            "crop": "Banana / Matooke",
            "condition": "Banana Bacterial Wilt (BXW)",
            "confidence": 0.95,
            "severity": "high",
            "is_healthy": False,
            "advice": "Cut down the infected pseudostem immediately at ground level. Disinfect machetes in fire.",
            "advice_luganda": "Temako ekitooke ekirwadde mangu ddala wansi ku ttaka. Yosa emyso mu muliro.",
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
            "is_healthy": False,
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
            "is_healthy": False,
            "advice": "Prune shade trees to increase airflow and apply approved copper fungicide before wet rains.",
            "advice_luganda": "Saalira emiti gy'emmwanyi okuyingiza empewo era osaaseeko eddagala lya kopa erikakasibwa.",
            "location": {
                "district": "Mbale",
                "latitude": 1.0784,
                "longitude": 34.1754
            },
            "timestamp": "2026-10-26T13:20:00Z"
        }
    ]

    return jsonify({
        "status": "success",
        "count": len(stub_scans),
        "scans": stub_scans
    }), 200


if __name__ == "__main__":
    print(f"🦅 Eagles Eye API starting on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT, debug=True)
