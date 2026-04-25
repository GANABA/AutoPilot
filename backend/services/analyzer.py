import json
import fitz  # PyMuPDF
from openai import OpenAI
from config import get_settings

settings = get_settings()

_CLASSIFY_SYSTEM = """Tu es un expert immobilier français. Analyse le début d'un document et retourne uniquement un JSON :
{"doc_type": "dpe"|"mandat"|"pv_copro"|"autre", "confidence": "high"|"medium"|"low"}

- "dpe" : Diagnostic de Performance Énergétique (classe énergie A-G, kWh/m²/an, GES, DPE)
- "mandat" : Mandat de vente ou location (mandat exclusif/simple, honoraires, prix de vente)
- "pv_copro" : Procès-verbal d'assemblée générale de copropriété (AG, résolutions, charges, syndic)
- "autre" : tout autre document"""

_EXTRACT_PROMPTS = {
    "dpe": """Extrais les données du DPE. Retourne un JSON avec ces champs (null si absent) :
{
  "energy_class": "A"|"B"|"C"|"D"|"E"|"F"|"G",
  "ges_class": "A"|"B"|"C"|"D"|"E"|"F"|"G",
  "energy_consumption_kwh": number,
  "ges_emission_kg": number,
  "address": string,
  "validity_date": "YYYY-MM-DD"
}""",

    "mandat": """Extrais les données du mandat. Retourne un JSON avec ces champs (null si absent) :
{
  "reference": string,
  "type": "exclusif"|"simple"|"semi-exclusif",
  "duration_months": number,
  "sale_price": number,
  "address": string,
  "owner_name": string,
  "agency_commission_pct": number,
  "start_date": "YYYY-MM-DD"
}""",

    "pv_copro": """Extrais les données du PV de copropriété. Retourne un JSON avec ces champs (null si absent) :
{
  "meeting_date": "YYYY-MM-DD",
  "resolutions": [string],
  "approved_works": [{"description": string, "amount": number}],
  "annual_charges": number
}""",

    "autre": """Résume ce document immobilier. Retourne un JSON :
{
  "summary": string,
  "key_points": [string]
}""",
}


def extract_text(pdf_bytes: bytes, max_chars: int = 6000) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
        if len(text) >= max_chars:
            break
    doc.close()
    return text[:max_chars]


def classify_document(text: str) -> tuple[str, str]:
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model=settings.llm_simple_model,
        response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {"role": "system", "content": _CLASSIFY_SYSTEM},
            {"role": "user", "content": f"Document à classifier :\n\n{text[:2000]}"},
        ],
    )
    result = json.loads(response.choices[0].message.content)
    return result.get("doc_type", "autre"), result.get("confidence", "low")


def extract_data(text: str, doc_type: str) -> dict:
    client = OpenAI(api_key=settings.openai_api_key)
    system_prompt = f"Tu es un expert immobilier français. {_EXTRACT_PROMPTS.get(doc_type, _EXTRACT_PROMPTS['autre'])}"
    response = client.chat.completions.create(
        model=settings.llm_simple_model,
        response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Texte du document :\n\n{text[:4000]}"},
        ],
    )
    return json.loads(response.choices[0].message.content)


def analyze(pdf_bytes: bytes) -> dict:
    text = extract_text(pdf_bytes)
    doc_type, confidence = classify_document(text)
    data = extract_data(text, doc_type)
    return {"doc_type": doc_type, "confidence": confidence, "data": data}
