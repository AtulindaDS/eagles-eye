# Eagles Eye — AI Input/Output Contract

**Status:** Draft for team review  
**Owner:** Lyazi Patrick — AI and Security  
**Project:** Eagles Eye — Pre-DevFest Hackathon Kampala 2026  
**Core flow:** Crop photo → AI diagnosis → Treatment advice

## 1. Purpose

This document defines the proposed inputs, outputs, validation requirements, and security rules for the AI-powered crop diagnosis component of Eagles Eye.

The component uses Google's Gemini API to analyze crop images and generate structured diagnostic guidance for Ugandan smallholder farmers.

The goal is to provide useful preliminary guidance while clearly communicating uncertainty and encouraging expert assessment when necessary. AI-generated results must not be presented as guaranteed diagnoses.

## 2. Scope

The hackathon MVP will focus on:

- Accepting a crop photograph for analysis.
- Identifying the crop and a possible disease, pest, nutrient deficiency, or healthy condition.
- Providing preliminary treatment and prevention guidance.
- Returning structured results that the farmer app can display and read aloud.
- Supporting scan logging and the district heat map through the backend.

Credit and marketplace features are outside the MVP and will remain on the product roadmap.

## 3. Input requirements

The AI component is expected to receive the following information through the backend:

| Field | Requirement | Description |
|---|---|---|
| `image` | Required | Photograph of the crop or affected plant. |
| `crop_type` | Optional | Crop name supplied by the farmer, if known. |
| `symptoms` | Optional | Symptoms described by the farmer. |

The backend must validate the uploaded image before sending it to Gemini. Unsupported, corrupted, excessively large, or invalid files must be rejected safely.

The image should contain enough visible information to support a meaningful assessment. If it does not, the AI should return an inconclusive result.

## 4. Expected output schema

The AI component should return a structured JSON object with the following proposed fields:

| Field | Type | Description |
|---|---|---|
| `status` | String | `success` or `inconclusive`. |
| `crop` | String | Identified crop, or `unknown`. |
| `condition` | String | Suspected condition or `unknown`. |
| `condition_type` | String | `disease`, `pest`, `nutrient_deficiency`, `healthy`, or `unknown`. |
| `severity` | String | `low`, `moderate`, `high`, or `unknown`. |
| `confidence` | String | `low`, `moderate`, `high`, or `unknown`. |
| `symptoms` | Array of strings | Visible symptoms relevant to the assessment. |
| `treatment` | Array of strings | Practical, cautious recommended actions. |
| `prevention` | Array of strings | Relevant preventive measures. |
| `needs_expert_review` | Boolean | Whether local agricultural expert assessment is recommended. |

These fields and allowed values are proposed for agreement with the backend and frontend developers before implementation.

The `confidence` field is a qualitative model assessment, not a calibrated probability of correctness.

## 5. Example response

The following is an illustrative example of the proposed response format, not a verified crop diagnosis.

```json
{
  "status": "success",
  "crop": "tomato",
  "condition": "Possible early blight",
  "condition_type": "disease",
  "severity": "moderate",
  "confidence": "moderate",
  "symptoms": [
    "Brown spots on older leaves"
  ],
  "treatment": [
    "Remove severely affected leaves where appropriate",
    "Seek local agricultural advice on suitable treatment options"
  ],
  "prevention": [
    "Avoid prolonged leaf wetness",
    "Monitor nearby plants for similar symptoms"
  ],
  "needs_expert_review": true
}
```

The backend must validate the response against the agreed schema before returning or storing it.

## 6. Uncertain and inconclusive results

The AI must not invent a diagnosis when the image is unclear, the crop cannot be identified, or the evidence is insufficient.

When the result is inconclusive:

- Set `status` to `inconclusive`.
- Use `unknown` for fields that cannot be determined reliably.
- Explain the limitation in farmer-friendly language through the appropriate app response.
- Recommend a clearer photograph or local agricultural expert assessment where appropriate.
- Avoid presenting speculative treatment advice as a confirmed recommendation.

The AI should distinguish between a suspected condition and a confirmed diagnosis. A high model confidence label does not guarantee that the diagnosis is correct.

## 7. Error handling

The integration must account for:

- Invalid, corrupted, or unsupported images.
- Images unrelated to crops.
- Images that are too unclear for assessment.
- Gemini API timeouts or service failures.
- Rate limits and unavailable services.
- Empty, malformed, or schema-invalid model responses.

Technical failures must be distinguishable from valid but inconclusive diagnoses. The backend and frontend developers should agree on a consistent error response format.

Errors must not expose API keys, internal stack traces, or other sensitive implementation details to the farmer.

## 8. Security and privacy

- Keep Gemini API credentials on the server and out of the farmer app.
- Store credentials in appropriate environment configuration or a managed secret store.
- Never commit API keys, credentials, or other secrets to Git.
- Validate image content, file type, and file size before processing.
- Apply suitable request limits and timeouts.
- Treat uploaded images and AI-generated output as untrusted data.
- Validate model responses before returning them to the frontend or saving them to Firestore.
- Avoid collecting unnecessary personal information or precise location data.
- Use only the location detail needed for the agreed outbreak-monitoring purpose.
- Ensure that public heat-map data does not expose individual farmers or their exact locations.

## 9. Integration responsibilities

**Lyazi — AI and Security**
- Develop the Gemini prompt and structured response approach.
- Test the AI component on 10–20 representative crop photos.
- Record incorrect, uncertain, and malformed outputs.
- Protect Gemini credentials and document relevant limitations.

**Derek — Backend**
- Implement the Python `/diagnose` endpoint on Cloud Run.
- Validate incoming requests and AI responses.
- Integrate the diagnosis flow with Firestore scan logging.
- Coordinate the API request, success response, and error formats.

**Deborah — Farmer App and Testing**
- Capture or upload a crop photograph.
- Display diagnosis, severity, symptoms, treatment, and prevention advice.
- Integrate the agreed voice-advice experience.
- Test the farmer-facing flow and report usability problems.

**Odriann — Dashboard**
- Develop the district heat-map dashboard.
- Coordinate with Derek on the aggregated scan data available for display.
- Use demo data where real scan data is insufficient.

**Stephen — Product and UX**
- Coordinate product scope, user experience, pitch, slides, and submission.

## 10. Testing and evaluation

Test the AI component on 10–20 representative images, including:

- Crops showing visible disease symptoms.
- Crops with possible pest damage.
- Crops showing possible nutrient deficiencies.
- Healthy crops.
- Unclear or low-quality crop images.
- Images unrelated to crops.

For each test, record the image identifier, expected result where known, model result, whether the output follows the schema, observed issues, and any recommended improvement.

Evaluate:

- Whether the crop and suspected condition are plausible.
- Whether uncertainty is communicated appropriately.
- Whether treatment and prevention guidance is relevant and cautious.
- Whether the output is valid JSON matching the agreed schema.
- Whether errors and inconclusive results are handled correctly.

The test set is an initial functional evaluation, not enough on its own to establish real-world diagnostic accuracy.

## 11. Decisions requiring team agreement

Before implementation is finalized, the team should agree on:

- The exact input fields and supported image formats.
- The final output schema and allowed values.
- How inconclusive results and technical errors are represented.
- The API success and error response formats.
- Which diagnosis fields are saved in Firestore.
- How scan locations are collected, protected, and aggregated for the heat map.
- How voice advice is generated and which fields are read aloud.

## 12. Limitations

Gemini may misidentify crops, diseases, pests, or nutrient deficiencies. Image-based assessment may also miss symptoms that require physical inspection or local context.

Eagles Eye should therefore present its output as preliminary guidance, avoid unsupported certainty, and encourage consultation with an agricultural extension officer when appropriate.

**Next step:** Review this draft with the backend and frontend developers, agree on the API contract, and then implement and test the AI component against that agreement.