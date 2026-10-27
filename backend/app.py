"""
Eagles Eye — Backend API Server
Team: Ugandan Eagles (Pre-DevFest Hackathon Kampala 2026)
Backend Leads: Atulinda Derek Solomon (Derek) & Lyazi Patrick (Lyazi)

This is a starter skeleton providing CORS-enabled Flask routes and stub responses
matching docs/DATA_CONTRACT.md to unblock frontend and dashboard team members.
"""

import os
from pathlib import Path
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import json
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv(Path(__file__).resolve().parent / ".env")

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for frontend & dashboard clients
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
PORT = int(os.environ.get("PORT", 8080))
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

GEMINI_MODEL = "gemini-3.5-flash-lite"

gemini_client = (
    genai.Client(api_key=GEMINI_API_KEY)
    if GEMINI_API_KEY
    else None
)

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
    """Analyze an uploaded crop image using Gemini."""

    # Basic upload checks; Derek can extend these validation rules.
    image_file = request.files.get("image")

    if image_file is None or not image_file.filename:
        return jsonify({
            "status": "error",
            "message": "Please upload a crop image using the 'image' field."
        }), 400

    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    mime_type = (image_file.mimetype or "").lower()

    if mime_type not in allowed_types:
        return jsonify({
            "status": "error",
            "message": "Supported image formats are JPEG, PNG, and WebP."
        }), 400

    image_bytes = image_file.read()

    if not image_bytes:
        return jsonify({
            "status": "error",
            "message": "The uploaded image is empty."
        }), 400

    if len(image_bytes) > 5 * 1024 * 1024:
        return jsonify({
            "status": "error",
            "message": "The image must not exceed 5 MB."
        }), 400

    if gemini_client is None:
        return jsonify({
            "status": "error",
            "message": "The AI service is not configured."
        }), 503

    district = (request.form.get("district") or "Unknown").strip()
    crop_hint = (request.form.get("crop_hint") or "").strip()

    # Temporary coordinate fallback. Replace with verified district
    # centroid coordinates before using scans for real outbreak mapping.
    location = {
        "district": district or "Unknown",
        "latitude": 0.3476,
        "longitude": 32.5825
    }

    prompt = f"""
You are the preliminary crop-health assessment assistant for Eagles Eye,
an application supporting smallholder farmers in Uganda.

Examine the attached image carefully. Identify visible crop symptoms,
possible diseases, pests, or nutrient deficiencies. Do not claim certainty
that the image does not support.

Farmer-provided crop hint: {crop_hint or "Not provided"}
Reported district: {district or "Unknown"}

Return ONLY a valid JSON object with exactly these keys:
- crop: string; use one of "Banana / Matooke", "Cassava", "Coffee",
  "Maize", "Beans", "Tomato", or "Unknown".
- condition: string; name the suspected condition or use "Healthy"
  when there is sufficient visual evidence of no visible damage.
  Use "Unknown" when it cannot be identified.
- confidence: number between 0.0 and 1.0 representing your estimated
  certainty, not a scientifically calibrated probability.
- severity: one of "none", "low", "moderate", "high".
- is_healthy: boolean; true only when there is sufficient evidence
  that the crop appears healthy.
- advice: practical, cautious advice in plain English for a Ugandan
  smallholder farmer.
- advice_luganda: a natural Luganda translation of the advice.
- is_inconclusive: boolean; true if the image is blurry, too distant,
  does not show a crop clearly, or does not support a useful assessment.

For an inconclusive image, use crop "Unknown", condition "Unknown",
confidence at or below 0.40, severity "none", and is_healthy false.
Explain in both advice fields that a clearer crop photo is needed.

Do not invent symptoms that are not visible. If a disease is only suspected,
say so in the advice. Do not recommend unsafe chemical use.
"""

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        result = json.loads(response.text)

        required_keys = {
            "crop",
            "condition",
            "confidence",
            "severity",
            "is_healthy",
            "advice",
            "advice_luganda",
            "is_inconclusive"
        }

        if not isinstance(result, dict) or not required_keys.issubset(result):
            raise ValueError("Gemini response is missing required fields.")

        if result["crop"] not in {
            "Banana / Matooke", "Cassava", "Coffee",
            "Maize", "Beans", "Tomato", "Unknown"
        }:
            result["crop"] = "Unknown"

        if result["severity"] not in {"none", "low", "moderate", "high"}:
            result["severity"] = "none"

        confidence = float(result["confidence"])

        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Gemini returned an invalid confidence value.")

        if not isinstance(result["is_healthy"], bool):
            raise ValueError("Gemini returned an invalid health flag.")

        if not isinstance(result["is_inconclusive"], bool):
            raise ValueError("Gemini returned an invalid inconclusive flag.")

        for key in ("condition", "advice", "advice_luganda"):
            if not isinstance(result[key], str) or not result[key].strip():
                raise ValueError(f"Gemini returned an invalid {key} field.")

        is_inconclusive = (
            result["is_inconclusive"] or confidence <= 0.40
        )

        diagnosis = {
            "crop": result["crop"],
            "condition": result["condition"],
            "confidence": confidence,
            "severity": result["severity"],
            "is_healthy": result["is_healthy"],
            "advice": result["advice"],
            "advice_luganda": result["advice_luganda"],
            "location": location,
            "timestamp": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        }

        return jsonify({
            "status": "inconclusive" if is_inconclusive else "success",
            "data": diagnosis
        }), 200

    except (ValueError, TypeError, json.JSONDecodeError) as error:
        app.logger.warning("Invalid Gemini diagnosis response: %s", error)
        return jsonify({
            "status": "error",
            "message": "The AI service returned an invalid diagnosis. Please try again."
        }), 502

    except Exception:
        app.logger.exception("Gemini crop diagnosis failed")
        return jsonify({
            "status": "error",
            "message": "Crop analysis failed. Please try again later."
        }), 502


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
