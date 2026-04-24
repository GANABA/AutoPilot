# Guide de configuration — Variables d'environnement

Suivez ce guide dans l'ordre. Chaque section indique exactement où cliquer pour obtenir la valeur.

---

## Étape 1 — Copier le fichier .env

```bash
cp backend/.env.example backend/.env
```

---

## Étape 2 — Variables que vous définissez vous-même

Pas besoin de compte externe, vous choisissez ces valeurs librement.

```env
AGENCY_NAME="Agence ImmoPlus"          # Nom de votre agence
AGENCY_GREETING="Bonjour, bienvenue !" # Message d'accueil du chatbot
AGENCY_BRAND_VOICE="professionnel et chaleureux"
AGENCY_ESCALATION_EMAIL="vous@agence.fr"
AGENCY_WORKING_HOURS_START="09:00"
AGENCY_WORKING_HOURS_END="19:00"

ADMIN_EMAIL=votre@email.fr             # Email de connexion au dashboard
ADMIN_PASSWORD=MotDePasseSecurise123!  # Mot de passe (min. 12 caractères)

ALLOWED_ORIGINS=http://localhost:3000  # En prod : URL de votre frontend Vercel
DEBUG=true                             # Mettre false en production
```

---

## Étape 3 — SECRET_KEY et WIDGET_TOKEN (à générer)

Ces valeurs sont des chaînes aléatoires à générer une seule fois.

**Option A — avec Python (si installé) :**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
# → copiez le résultat dans SECRET_KEY

python -c "import secrets; print('tok_' + secrets.token_hex(16))"
# → copiez le résultat dans WIDGET_TOKEN
```

**Option B — avec OpenSSL :**
```bash
openssl rand -hex 32    # → SECRET_KEY
openssl rand -hex 16    # → préfixez avec "tok_" pour WIDGET_TOKEN
```

---

## Étape 4 — OpenAI (OPENAI_API_KEY)

1. Allez sur **[platform.openai.com](https://platform.openai.com)**
2. Menu gauche → **API keys**
3. Cliquez **Create new secret key**
4. Donnez-lui un nom (ex: "autopilot-immo-poc")
5. Copiez la clé `sk-...` → collez dans `OPENAI_API_KEY`

> La clé ne s'affiche qu'une seule fois. Si vous la perdez, il faudra en créer une nouvelle.

Les 3 valeurs suivantes ne changent pas :
```env
LLM_COMPLEX_MODEL=gpt-4o
LLM_SIMPLE_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
```

---

## Étape 5 — Neon PostgreSQL (DATABASE_URL)

1. Allez sur **[console.neon.tech](https://console.neon.tech)**
2. Cliquez **New Project**
   - Name : `autopilot-immo`
   - Region : **AWS eu-west-3 (Paris)** ← important pour la latence
   - PostgreSQL version : 16
3. Une fois créé, allez dans **Dashboard** de votre projet
4. Section **Connection Details** → sélectionnez **Connection string**
5. Cochez **Pooled connection** (recommandé pour production)
6. Copiez la chaîne qui ressemble à :
   ```
   postgresql://user:pass@ep-xxx-xxx.eu-west-3.aws.neon.tech/neondb?sslmode=require
   ```
7. Collez dans `DATABASE_URL`

> Pour le dev local avec Docker Compose, gardez `postgresql://autopilot:autopilot@localhost:5432/autopilot` et utilisez la valeur Neon uniquement pour Railway.

**Activer pgvector sur Neon :**
Dans Neon Console → **SQL Editor**, exécutez :
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

## Étape 6 — Upstash Redis (REDIS_URL)

1. Allez sur **[console.upstash.com](https://console.upstash.com)**
2. Cliquez **Create Database**
   - Name : `autopilot-redis`
   - Type : **Regional**
   - Region : **EU-West-1 (Ireland)** ou **EU-Central-1 (Frankfurt)**
   - TLS : **activé** (coché par défaut)
3. Une fois créé, ouvrez votre base
4. Section **REST API** ou **Details** → copiez **Redis URL**
   - Elle commence par `rediss://default:xxx@apn-xxx.upstash.io:6380`
5. Collez dans `REDIS_URL`

> `rediss://` (avec deux s) = connexion chiffrée TLS. C'est la valeur correcte pour Upstash.

---

## Étape 7 — Cloudflare R2 (stockage de fichiers)

### 7a — Créer le bucket

1. Allez sur **[dash.cloudflare.com](https://dash.cloudflare.com)**
2. Menu gauche → **R2 Object Storage**
3. Cliquez **Create bucket**
   - Bucket name : `autopilot-docs`
   - Location : **Automatic** (ou Europe si disponible)
4. Notez votre **Account ID** visible dans la barre latérale droite (format `abc123def456...`)

### 7b — Créer les clés d'accès API

1. Dans R2 → cliquez **Manage R2 API Tokens**
2. Cliquez **Create API token**
   - Token name : `autopilot-immo`
   - Permissions : **Object Read & Write**
   - Bucket : **Specific bucket** → sélectionnez `autopilot-docs`
3. Cliquez **Create API Token**
4. Copiez les valeurs affichées (elles n'apparaissent qu'une fois) :

```env
CLOUDFLARE_R2_ENDPOINT=https://<votre_account_id>.r2.cloudflarestorage.com
CLOUDFLARE_R2_ACCESS_KEY=<Access Key ID affiché>
CLOUDFLARE_R2_SECRET_KEY=<Secret Access Key affiché>
CLOUDFLARE_R2_BUCKET=autopilot-docs
```

---

## Résultat final — votre .env complété

```env
# Agence
AGENCY_NAME="Agence ImmoPlus"
AGENCY_GREETING="Bonjour, bienvenue chez ImmoPlus !"
AGENCY_BRAND_VOICE="professionnel et chaleureux"
AGENCY_ESCALATION_EMAIL="contact@immoplus.fr"
AGENCY_WORKING_HOURS_START="09:00"
AGENCY_WORKING_HOURS_END="19:00"
WIDGET_TOKEN="tok_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# LLM
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_COMPLEX_MODEL=gpt-4o
LLM_SIMPLE_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Base de données
DATABASE_URL=postgresql://user:pass@ep-xxx.eu-west-3.aws.neon.tech/neondb?sslmode=require

# Redis
REDIS_URL=rediss://default:xxx@apn-xxx.upstash.io:6380

# Cloudflare R2
CLOUDFLARE_R2_ENDPOINT=https://abc123.r2.cloudflarestorage.com
CLOUDFLARE_R2_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CLOUDFLARE_R2_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CLOUDFLARE_R2_BUCKET=autopilot-docs

# Auth
SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ADMIN_EMAIL=admin@immoplus.fr
ADMIN_PASSWORD=MotDePasseSecurise123!

# App
ALLOWED_ORIGINS=http://localhost:3000
DEBUG=true
```

---

## Étape 8 — Variables Railway (déploiement cloud)

Une fois votre app connectée à Railway via GitHub :

1. Ouvrez votre projet Railway
2. Cliquez sur le service **api**
3. Onglet **Variables**
4. Cliquez **Raw Editor** et collez tout votre `.env`
5. **Modifiez ces 2 valeurs** pour la prod :
   - `DATABASE_URL` → la valeur Neon (pas localhost)
   - `REDIS_URL` → la valeur Upstash (pas localhost)
   - `ALLOWED_ORIGINS` → URL de votre frontend Vercel
   - `DEBUG` → `false`

Faites la même chose pour le service **worker**.

---

## Variables ajoutées plus tard (semaines suivantes)

Ces variables ne sont pas encore nécessaires — elles seront ajoutées quand on implémentera les agents correspondants :

| Variable | Semaine | Service |
|----------|---------|---------|
| `RESEND_API_KEY` | Semaine 6 (relances email) | [resend.com](https://resend.com) → API Keys |
| `VAPI_API_KEY` | Semaine 6 (agent vocal) | [vapi.ai](https://vapi.ai) → Dashboard → API Keys |
| `TWILIO_ACCOUNT_SID` | Semaine 6 (téléphonie) | [console.twilio.com](https://console.twilio.com) → Account Info |
| `TWILIO_AUTH_TOKEN` | Semaine 6 | Même page que SID |
| `TWILIO_PHONE_NUMBER` | Semaine 6 | Twilio → Phone Numbers → Manage |
| `GOOGLE_CALENDAR_CREDENTIALS` | Semaine 5 | Google Cloud Console → APIs → OAuth 2.0 |
