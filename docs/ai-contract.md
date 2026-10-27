# Eagles Eye — AI Input/Output Contract

**Status:** Draft aligned with the team data contract
**Owner:** Lyazi Patrick — AI and Security  
**Project:** Eagles Eye — Pre-DevFest Hackathon Kampala 2026  
**Core flow:** Crop photo → AI diagnosis → Farmer advice

## 1. Purpose

This document defines the inputs, outputs, validation requirements, uncertainty handling, and security rules for the AI-powered crop diagnosis component of Eagles Eye.

The component uses Google's Gemini API to analyze crop images and generate structured preliminary guidance for Ugandan smallholder farmers.

The AI component must follow the agreed schema in `docs/DATA_CONTRACT.md`. AI-generated results must not be presented as guaranteed diagnoses.

## 2. Scope

The MVP will focus on:

- Analyzing uploaded crop photographs.
- Identifying the crop and a possible disease, pest, nutrient deficiency, or healthy condition.
- Generating preliminary farmer advice in English and Luganda.
- Returning structured diagnostic content for the existing backend API.
- Supporting scan logging and the district heat map through the backend.

Credit and marketplace features are outside the MVP.

## 3. Input requirements

The backend exposes `POST /diagnose` using `multipart/form-data`.

| Field | Requirement | Description |
|---|---|---|
| `image` | Required | Crop photograph, subject to backend validation. |
| `district` | Optional | Farmer-provided or otherwise reliably obtained district; defaults must be handled by the backend. |
| `crop_hint` | Optional | Farmer-provided crop name, if known. |

The agreed API contract permits JPEG, PNG, and WebP images up to 5 MB.

The backend must validate uploaded files before sending their contents to Gemini. Invalid, unsupported, corrupted, or oversized files must be rejected safely.

The initial contract does not include a separate `symptoms` input. Adding it requires agreement with the backend and frontend developers.

## 4. AI output and diagnosis record

The AI-generated diagnostic content must be mapped to the team's agreed diagnosis schema.

| Field | Type | Responsibility |
|---|---|---|
| `crop` | String | AI identifies the crop or returns `"Unknown"`. |
| `condition` | String | AI identifies a suspected condition, `"Healthy"`, or `"Unknown"`. |
| `confidence` | Number | AI-provided confidence estimate between `0.00` and `1.00`; not a calibrated probability. |
| `severity` | String | One of `"none"`, `"low"`, `"moderate"`, or `"high"`. |
| `is_healthy` | Boolean | Indicates whether the assessment identifies the crop as healthy. |
| `advice` | String | Preliminary farmer guidance in English. |
| `advice_luganda` | String | Corresponding farmer guidance in Luganda. |
| `location` | Object | Added or validated by the backend; includes `district`, `latitude`, and `longitude` according to the agreed contract. |
| `timestamp` | String | Added by the backend in ISO-8601 UTC format. |

The outer API response must follow `docs/DATA_CONTRACT.md`, including its `status` and `data` structure.

Gemini must not invent coordinates, timestamps, or other trusted metadata. The backend must validate the AI-generated fields before returning or persisting the diagnosis.

Additional fields such as `condition_type`, `symptoms`, `treatment`, `prevention`, or `needs_expert_review` must not be introduced into the public response without agreement from the team.

## 5. Illustrative output

This example illustrates the required diagnostic fields. It is not a verified crop diagnosis.

```json
{
  "crop": "Tomato",
  "condition": "Possible early blight",
  "confidence": 0.72,
  "severity": "moderate",
  "is_healthy": false,
  "advice": "The leaf symptoms may be consistent with early blight. Remove severely affected leaves where appropriate and consult a local agricultural extension officer about suitable treatment.",
  "advice_luganda": "Obubonero obuli ku bikoola buyinza okuba obw'obulwadde bwa early blight. Ggyawo ebikoola ebirwadde ennyo nga kisaanidde era weebuuze ku mukugu mu by'obulimi ku ddagala erisaanira."
}
```

The backend adds the `location` and `timestamp` fields and wraps the completed record in the agreed API response format.

The example confidence value is illustrative, not a validated probability.

## 6. Uncertain and inconclusive results

The AI must not invent a diagnosis when the image is unclear, the crop cannot be identified, or the visual evidence is insufficient.

When the assessment is inconclusive:

- The API response must use the agreed `"inconclusive"` status.
- Unknown crop or condition values must use `"Unknown"` where appropriate.
- The advice must explain the limitation in farmer-friendly language.
- The farmer should be encouraged to submit a clearer photograph or consult an agricultural extension officer.
- Speculative treatment advice must not be presented as confirmed guidance.

The team must agree on the exact field values used for an inconclusive record, including the confidence and severity values, before implementation is finalized.

A model confidence estimate does not guarantee correctness.

## 7. Error handling

The integration must account for:

- Invalid, corrupted, unsupported, or oversized images.
- Images unrelated to crops.
- Images too unclear for assessment.
- Gemini timeouts, service failures, and rate limits.
- Empty, malformed, or schema-invalid model responses.

Technical failures must be distinguished from valid but inconclusive diagnoses. The backend and frontend must follow the agreed API error format.

Errors must not expose API keys, internal stack traces, or sensitive implementation details.

## 8. Security and privacy

- Keep Gemini credentials on the server, outside the farmer application.
- Load credentials from environment configuration or an appropriate managed secret store.
- Never commit credentials or other secrets to Git.
- Validate file size, content, and type before processing.
- Apply suitable request limits and timeouts.
- Treat uploaded images and model responses as untrusted input.
- Validate model output before returning it to the frontend or saving it to Firestore.
- Do not allow model-generated text to determine trusted location metadata.
- Collect only the location information needed for the agreed monitoring purpose.
- Avoid exposing individual farmers or exact household locations through the public heat map.

## 9. Responsibilities

**Lyazi — AI and Security**

- Develop and refine the Gemini prompt.
- Produce structured diagnostic content consistent with the agreed schema.
- Handle uncertainty and malformed model responses.
- Test 10–20 representative crop photographs.
- Document observed limitations and protect API credentials.

**Derek — Backend**

- Maintain the Flask `/diagnose` API and request validation.
- Integrate the diagnosis flow with Firestore.
- Add trusted metadata and validate the final API response.
- Coordinate error handling and response formats.

**Deborah — Farmer App and Testing**

- Capture or upload crop photographs.
- Display the agreed diagnosis and advice fields.
- Integrate the agreed voice-advice experience.
- Test the farmer-facing flow and report usability problems.

**Odriann — Dashboard**

- Develop the district heat-map dashboard.
- Coordinate with Derek on scan records and aggregation.
- Use sample data where real scan data is insufficient.

**Stephen — Product and UX**

- Coordinate product scope, user experience, pitch, slides, and submission.

## 10. Testing and evaluation

Test the AI component on 10–20 representative images, including:

- Crops with visible disease symptoms.
- Possible pest damage.
- Possible nutrient deficiencies.
- Healthy crops.
- Unclear or low-quality photographs.
- Images unrelated to crops.

For each test, record the image identifier, expected result where known, model output, schema validity, uncertainty handling, and observed issues.

Evaluate whether:

- The crop and suspected condition are plausible.
- Uncertainty is communicated appropriately.
- Advice is relevant, understandable, and cautious.
- The output conforms to the agreed schema.
- Inconclusive results and technical errors are handled correctly.

This initial test set is for functional evaluation and does not establish real-world diagnostic accuracy.

## 11. Decisions requiring team agreement

- Exact field values for inconclusive results.
- The minimum confidence threshold, if one is used.
- The agreed API error format.
- Whether additional fields such as symptoms or expert-review flags are needed.
- How district coordinates are obtained, validated, and protected.
- Which fields are stored in Firestore and exposed to the dashboard.
- How voice advice is generated and which fields are read aloud.

## 12. Limitations

Gemini may misidentify crops, diseases, pests, or nutrient deficiencies. Image-based assessment may miss symptoms requiring physical inspection or local context.

Eagles Eye must present results as preliminary guidance, communicate uncertainty, and encourage agricultural expert consultation when appropriate.
