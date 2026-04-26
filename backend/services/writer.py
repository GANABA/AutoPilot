import json
from openai import OpenAI
from config import get_settings

settings = get_settings()

_PLATFORM_CONFIGS = {
    "seloger": {
        "label": "SeLoger",
        "instructions": (
            "Rédige une annonce immobilière professionnelle pour SeLoger (agences). "
            "Titre : 60-80 caractères, accrocheur et descriptif (ex: 'T3 lumineux 68m² balcon – Lyon 6e'). "
            "Corps : 400-500 caractères, ton professionnel, décris les points forts dans l'ordre : "
            "localisation, surface/pièces, prestations, atouts (balcon, parking, ascenseur), DPE, charges. "
            "Pas de prix dans le texte (géré par la plateforme)."
        ),
    },
    "leboncoin": {
        "label": "Leboncoin",
        "instructions": (
            "Rédige une annonce pour Leboncoin (grand public). "
            "Titre : 50-60 caractères, direct et efficace. "
            "Corps : 200-280 caractères, ton accessible, mets en avant le prix, la surface et les points clés. "
            "Utilise des abréviations courantes (ch, sdb, park, asc). Style simple et lisible."
        ),
    },
    "pap": {
        "label": "PAP (de particulier à particulier)",
        "instructions": (
            "Rédige une annonce pour PAP.fr (vente entre particuliers). "
            "Titre : 50-70 caractères, sobre. "
            "Corps : 250-350 caractères, comme si c'était le propriétaire qui parle directement. "
            "Pas de jargon d'agence, ton personnel et honnête. Mentionne le quartier, "
            "les transports ou commodités proches si possible."
        ),
    },
    "website": {
        "label": "Site web agence",
        "instructions": (
            "Rédige une description premium pour le site web de l'agence. "
            "Titre : 60-80 caractères, marketing et valorisant. "
            "Corps : 500-650 caractères, ton haut de gamme, raconte le bien comme une histoire, "
            "évoque l'environnement et le style de vie, mentionne les atouts cachés. "
            "Termine par un call to action discret ('Contactez-nous pour une visite')."
        ),
    },
}


def _build_property_summary(prop: dict) -> str:
    lines = []
    if prop.get("type"):
        lines.append(f"Type : {prop['type']}")
    if prop.get("surface"):
        lines.append(f"Surface : {prop['surface']} m²")
    if prop.get("nb_rooms"):
        lines.append(f"Pièces : {prop['nb_rooms']} (dont {prop.get('nb_bedrooms', '?')} chambre(s))")
    if prop.get("price"):
        lines.append(f"Prix : {int(prop['price']):,} €".replace(",", " "))
    if prop.get("address") or prop.get("city"):
        lines.append(f"Adresse : {prop.get('address', '')} {prop.get('city', '')} {prop.get('zipcode', '')}".strip())
    if prop.get("floor") is not None:
        lines.append(f"Étage : {prop['floor']}")
    features = []
    if prop.get("has_balcony"):
        features.append("balcon")
    if prop.get("has_parking"):
        features.append("parking")
    if prop.get("has_elevator"):
        features.append("ascenseur")
    if features:
        lines.append(f"Prestations : {', '.join(features)}")
    if prop.get("energy_class"):
        lines.append(f"DPE : classe {prop['energy_class']}")
    if prop.get("charges_monthly"):
        lines.append(f"Charges : {int(prop['charges_monthly'])} €/mois")
    if prop.get("description"):
        lines.append(f"Description libre : {prop['description']}")
    return "\n".join(lines)


def generate_listing(property_data: dict, platform: str) -> dict:
    config = _PLATFORM_CONFIGS.get(platform, _PLATFORM_CONFIGS["website"])
    client = OpenAI(api_key=settings.openai_api_key)

    system_prompt = (
        "Tu es un expert en rédaction d'annonces immobilières françaises. "
        f"{config['instructions']} "
        "Retourne uniquement un JSON : {\"title\": string, \"content\": string}"
    )

    response = client.chat.completions.create(
        model=settings.llm_complex_model,
        response_format={"type": "json_object"},
        temperature=0.7,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Bien immobilier :\n{_build_property_summary(property_data)}"},
        ],
    )

    result = json.loads(response.choices[0].message.content)
    return {
        "title": result.get("title", ""),
        "content": result.get("content", ""),
    }
