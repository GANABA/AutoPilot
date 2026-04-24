# PRD — AutoPilot Immo
## Système Multi-Agents IA pour Agences Immobilières

> **Version :** 1.1  
> **Date :** Avril 2026  
> **Statut :** Brouillon de travail  
> **Modèle business :** SaaS multi-tenant  
> **Marché cible :** France (marché initial — expansion internationale décision ultérieure délibérée)

---

## Table des matières

1. [Executive Summary](#1-executive-summary)
2. [Analyse du marché et opportunité](#2-analyse-du-marché-et-opportunité)
3. [Pain Points validés des agences immobilières](#3-pain-points-validés-des-agences-immobilières)
4. [Use Cases prioritaires](#4-use-cases-prioritaires)
5. [Architecture technique](#5-architecture-technique)
6. [Stack technologique recommandée](#6-stack-technologique-recommandée)
7. [Modèle de données](#7-modèle-de-données)
8. [Roadmap et phases de développement](#8-roadmap-et-phases-de-développement)
9. [Modèle économique SaaS](#9-modèle-économique-saas)
10. [Risques et mitigations](#10-risques-et-mitigations)

---

## 1. Executive Summary

### Vision

AutoPilot Immo est une plateforme SaaS multi-agents IA destinée aux agences immobilières françaises. Elle automatise les tâches répétitives à faible valeur ajoutée (réponse aux leads, traitement de documents, rédaction d'annonces, relances prospects) pour permettre aux agents de se concentrer sur la négociation, le conseil, et la relation client à haute valeur.

Le marché initial est la France uniquement. Cette concentration volontaire permet de valider le product-market fit, de maîtriser les contraintes réglementaires (RGPD, loi ALUR, DPE obligatoire) et de construire des intégrations profondes avec les portails français (SeLoger, LeBonCoin, PAP, Bien'ici) avant toute expansion.

### Proposition de valeur

| Pour qui | Problème résolu | Valeur apportée |
|----------|----------------|-----------------|
| Agences indépendantes (1-10 agents) | Manque de ressources pour assurer un suivi 24/7 | Présence digitale permanente sans coût salarial supplémentaire |
| Réseaux immobiliers (10-100 agences) | Incohérence de la communication entre agences | Standardisation de la qualité de service sur tout le réseau |
| Agents individuels mandataires | Gestion administrative chronophage | 40% de temps récupéré, concentré sur la vente |

### Positionnement

AutoPilot Immo se positionne entre les CRM immobiliers classiques (Périclès, Hektor, Apimo) qui ne proposent pas d'IA conversationnelle, et les solutions IA généralistes (ChatGPT, Copilot) qui ne sont pas calibrées pour le secteur immobilier. Il n'existe pas aujourd'hui de solution multi-agents verticalisée immobilier en langue française avec un déploiement SaaS clé en main.

---

## 2. Analyse du marché et opportunité

### 2.1 Taille du marché

| Segment | Valeur | Horizon |
|---------|--------|---------|
| Marché mondial SaaS immobilier | USD 25,39 Mds | 2030 |
| Marché mondial IA dans l'immobilier | USD 140+ Mds | 2033 |
| Agences immobilières en France | ~12 000 agences indépendantes + réseaux nationaux | 2025 |
| Réseau mandataires (IAD, CapiFrance, etc.) | ~50 000 agents mandataires actifs | 2025 |
| Administrateurs de biens / gestionnaires locatifs | ~5 000 cabinets | 2025 |

### 2.2 Adoption de l'IA dans le secteur

- **68%** des agences françaises utilisent déjà des outils IA en 2025
- **90%** des investissements IA immobilier en 2025 concentrés sur 3 priorités : **efficacité, insights, personnalisation** (rapport Rechat, janvier 2026)
- **82%** des agents utilisent l'IA pour rédiger des descriptions de biens, mais **60%** comprennent mal le fonctionnement de la technologie → opportunité de solution clé en main
- Les outils bien implémentés génèrent un ROI positif en **3 à 6 mois**

### 2.3 Segmentation marché cible (France)

Trois segments accessibles sur le marché français, par ordre de priorité d'adressage :

#### Segment 1 — Agences indépendantes (priorité MVP)
- **ICP :** Agence de 2 à 15 agents, urbaine ou périurbaine, avec un site web existant et un volume de 20+ leads/mois
- **Douleur principale :** Pas de ressources pour assurer une présence digitale 24/7 ni pour traiter la charge administrative
- **Canaux d'acquisition :** FNAIM, SNPI, salons immobiliers (RENT), LinkedIn, démarchage direct
- **Facteurs de décision :** Simplicité d'onboarding, preuve de ROI rapide (<3 mois), conformité RGPD native, intégration avec leur site existant en 1 ligne de code

#### Segment 2 — Agents mandataires (priorité V2)
- **ICP :** Agents mandataires IAD, CapiFrance, SAFTI — travaillent seuls, très peu d'outils, fortement axés sur la prospection
- **Douleur principale :** Gestion totalement manuelle de leurs leads et de leur communication, aucun support administratif
- **Canal :** Via les réseaux eux-mêmes (partenariat réseau = accès à des milliers d'agents d'un coup)
- **Facteurs de décision :** Prix accessible (plan Starter), application mobile, autonomie totale

#### Segment 3 — Réseaux et grands groupes (priorité V3 / Enterprise)
- **ICP :** Réseaux de franchise (Century 21, ERA, Laforêt), groupes immobiliers régionaux 15+ agences
- **Douleur principale :** Incohérence de la communication entre agences, absence de reporting consolidé
- **Canal :** Approche commerciale directe (B2B), appels d'offres
- **Facteurs de décision :** SLA garanti, personnalisation avancée, instance dédiée possible, API ouverte

> **Note stratégique :** L'expansion vers d'autres marchés (Afrique francophone, Canada/Québec) est reconnue comme une opportunité réelle mais est volontairement hors scope jusqu'à validation du product-market fit en France.

### 2.4 Analyse concurrentielle

| Solution | Type | Forces | Faiblesses | Prix estimé |
|----------|------|--------|------------|-------------|
| **Lofty (USA)** | CRM + IA | Lead automation avancée | En anglais, non adapté France | $300-500/mois |
| **Rechat (USA)** | IA marketing immo | Personnalisation marketing | Anglais, pas multi-agents | $200-400/mois |
| **Keyzia (France)** | Outils IA immo | En français, spécialisé | Pas de multi-agents, pas vocal | ~€49-99/mois |
| **Ringover Immo** | Téléphonie IA | Appels entrants IA | Limité à la voix | €50-150/mois |
| **Périclès/Hektor** | CRM immo FR | Maturité, intégrations | Pas d'IA conversationnelle | €100-300/mois |
| **VAPI.ai** | Agent vocal | Infrastructure robuste | Non verticalisé immo | Usage-based |
| **AutoPilot Immo** | **Multi-agents IA** | **Full-stack, francophone, SaaS multi-tenant, verticalisé** | **Nouveau, notoriété à construire** | **€99-399/mois** |

### 2.5 Barrières à l'entrée (notre avantage défensif)

1. **Data propriétaire :** Chaque conversation, chaque bien traité enrichit les modèles de matching et les prompts sectoriels
2. **Intégrations métier :** Connexions aux portails français (SeLoger, LeBonCoin, PAP, Bien'ici) = travail de longue haleine
3. **Confiance et RGPD :** Certification RGPD et hébergement européen = barrière réglementaire
4. **Effet réseau :** Plus d'agences = plus de données de benchmark marché = meilleure qualité des estimations

---

## 3. Pain Points validés des agences immobilières

Basé sur des données de terrain consolidées de multiples études (PwC, Rechat, AgentZap, Salesmate) :

### 3.1 Réponse aux leads : la course au premier répondant

> **Chiffre clé :** Répondre en moins de 5 minutes multiplie par **21** la probabilité de qualifier un lead. La moyenne réelle du secteur est de **4 heures** en jours ouvrables.

- **78%** des acheteurs travaillent avec le premier agent qui répond
- **48%** des demandes entrantes ne reçoivent jamais de réponse
- Le week-end et les soirs représentent 30-40% du trafic web → heures creuses humaines = heures de pointe des leads

**Ce que l'IA résout :** Réponse automatique instantanée 24/7, qualification du lead, proposition de créneaux de visite, tout en notifiant l'agent humain en parallèle.

### 3.2 Suivi insuffisant : le gouffre des 5 relances

> **Chiffre clé :** **80%** des ventes nécessitent 5+ points de contact. **44%** des agents abandonnent après 1 seul essai.

- Le suivi manuel est chronophage et souvent oublié en période de forte activité
- Les relances génériques (email standard) ont un taux d'ouverture faible

**Ce que l'IA résout :** Séquences de relances automatiques et personnalisées (J+1, J+7, J+30) adaptées au statut du prospect et à ses critères de recherche.

### 3.3 Surcharge administrative documentaire

- Un agent immobilier passe en moyenne **2h30/jour** sur des tâches administratives (rédaction, documents, emails)
- Lecture et extraction manuelle des DPE, PV d'AG de copropriété, mandats = source d'erreurs et de pertes de temps
- Rédaction d'annonces sur 4-6 plateformes avec formats différents = tâche répétitive sans valeur

**Ce que l'IA résout :** Extraction automatique de données structurées depuis les PDFs, génération d'annonces multi-formats en quelques secondes.

### 3.4 Appels entrants hors horaires

- Les agences immobilières perdent en moyenne 25-35% de leurs appels entrants (messagerie, non-réponse)
- Les clients potentiels rappellent rarement → lead perdu définitivement

**Ce que l'IA résout :** Agent vocal IA actif 24/7, capable de qualifier le prospect, répondre aux questions sur les biens, et poser un rendez-vous dans le calendrier de l'agent.

### 3.5 Qualification non structurée des prospects

- La plupart des agences n'utilisent pas de CRM ou l'utilisent mal
- Les critères de recherche des prospects (budget, surface, localisation) ne sont pas systématiquement capturés
- Impossibilité de faire du matching automatique prospect ↔ nouveaux biens

**Ce que l'IA résout :** Extraction structurée des critères de chaque prospect, constitution automatique d'une fiche prospect dans le CRM, alertes automatiques quand un nouveau bien correspond.

### 3.6 Absence de suivi post-visite

- Après une visite, 60% des agents n'envoient pas de compte-rendu structuré
- Le feedback des visiteurs n'est pas systématiquement collecté
- Le propriétaire vendeur est rarement tenu informé en temps réel

**Ce que l'IA résout :** Email de suivi post-visite automatique, collecte de feedback structuré, rapport synthétique au propriétaire.

---

## 4. Use Cases prioritaires

### 4.1 Tier 1 — MVP (Valeur maximale, impact immédiat)

#### UC-01 : Agent Support Conversationnel 24/7
**Description :** Chatbot IA intégré sur le site de l'agence (widget JS embeddable) qui répond aux prospects, extrait leurs critères, présente les biens correspondants, et propose des créneaux de visite.

| Dimension | Détail |
|-----------|--------|
| Canal | Widget web, email entrant |
| Modèle IA | LLM (Claude Sonnet 4.6 ou GPT-4o-mini) + RAG pgvector |
| Intégrations | Google Calendar (créneaux), PostgreSQL (biens), SendGrid (emails) |
| Bénéfice mesuré | +21x taux de qualification lead, -90% temps de réponse initial |
| Escalade | Si confiance < 0.7 ou hors scope → notification email/Slack à l'agent humain |
| Complexité | Moyenne |

**Comportement détaillé :**
1. Accueil personnalisé avec le nom de l'agence et son ton de marque
2. Extraction des critères (type bien, budget, surface, localisation, critères spécifiques)
3. Recherche hybride : matching sémantique (pgvector) + filtres SQL stricts
4. Présentation de 2-3 biens avec photos, prix, points forts
5. Proposition de créneaux de visite via Calendar API
6. Capture des coordonnées pour le CRM (nom, email, téléphone)
7. Génération d'un résumé de conversation pour l'agent humain

---

#### UC-02 : Agent Analyste de Documents
**Description :** Analyse automatique des PDFs immobiliers (DPE, PV d'AG copropriété, mandats) pour en extraire les données structurées et créer ou enrichir la fiche du bien.

| Dimension | Détail |
|-----------|--------|
| Documents traités | DPE, PV d'AG copro, mandats de vente/location, diagnostics |
| Traitement | Asynchrone via Celery (l'utilisateur n'attend pas) |
| Sortie | JSON structuré stocké dans `Document.extracted_data`, fiche bien créée/enrichie |
| Bénéfice mesuré | -70% temps de traitement documentaire, 0 erreur de saisie manuelle |
| Complexité | Moyenne |

**Données extraites par type de document :**

*DPE :*
- Classe énergétique (A-G), consommation kWh/m²/an
- Émissions CO₂, recommandations travaux
- Validité du diagnostic

*PV d'AG copropriété :*
- Montant des charges mensuelles
- Travaux votés et budget associé
- Fonds de travaux disponibles
- Incidents ou litiges en cours

*Mandat de vente/location :*
- Prix demandé, commission agence
- Durée du mandat, exclusivité ou simple
- Coordonnées propriétaire

---

#### UC-03 : Agent Rédacteur d'Annonces
**Description :** Génération automatique d'annonces immobilières optimisées par plateforme cible (SeLoger, LeBonCoin, PAP, Bien'ici, site propre de l'agence).

| Dimension | Détail |
|-----------|--------|
| Entrée | property_id + plateforme cible |
| Sources | Données Property + Document.extracted_data |
| Contraintes | Template par plateforme (longueur, format, mots-clés SEO) |
| Workflow | Génère en "draft" → validation humaine dans dashboard → publication |
| Bénéfice mesuré | -85% temps de rédaction, cohérence multi-plateformes |
| Complexité | Faible-Moyenne |

**Spécificités par plateforme :**
- **SeLoger :** 1500 caractères max, accent sur DPE et charges, mots-clés SEO locaux
- **LeBonCoin :** Ton plus accessible, prix mis en avant, courte accroche
- **PAP.fr :** Format direct, sans superflu
- **Site agence :** Version longue, storytelling, photos mises en avant
- **Email prospect :** Format personnalisé avec le prénom du prospect

---

#### UC-04 : Dashboard de Gestion et Configuration
**Description :** Interface web pour les gérants d'agence permettant de configurer le système, valider les annonces, suivre les conversations, et consulter les métriques.

| Fonctionnalité | Détail |
|---------------|--------|
| Gestion des biens | CRUD complet, upload documents, statuts |
| Gestion des prospects | Liste, critères, statut du pipeline, historique conversations |
| Validation annonces | Review des drafts avant publication |
| Configuration tenant | Ton de marque, horaires, email d'escalade, plateformes actives |
| Métriques | Nb leads, taux de qualification, taux de conversion visite/offre |
| Agents | Comptes utilisateurs, rôles (admin agence / agent / directeur) |

---

### 4.2 Tier 2 — Version 2 (6-8 semaines après MVP)

#### UC-05 : Agent Vocal Entrant (téléphonie IA)
**Description :** Système de réponse téléphonique IA capable de gérer les appels entrants hors heures ouvrables. L'agent IA présente les biens, qualifie le prospect, et pose un rendez-vous.

| Dimension | Détail |
|-----------|--------|
| Infrastructure | VAPI.ai (recommandé) ou Twilio + Whisper STT + ElevenLabs TTS |
| Latence cible | < 1.5 secondes entre fin de parole et début de réponse IA |
| Intégration | Numéro Twilio fourni par l'agence → webhook → pipeline vocal → Google Calendar |
| Voix | Voix clonée de l'agence (option) ou voix neutre professionnelle pré-sélectionnée |
| Bénéfice mesuré | -35% leads perdus sur appels hors horaires |
| Complexité | Haute |

---

#### UC-06 : Relances Automatiques Intelligentes
**Description :** Séquences de relances automatiques post-contact initial, adaptées au comportement du prospect et à son stade dans le pipeline.

| Stade prospect | Déclencheur | Action automatique |
|---------------|-------------|-------------------|
| Nouveau lead | Conversation ouverte | Email de bienvenue + 3 biens correspondants (J+0) |
| Prospect qualifié | Critères extraits | Email "nouvelles opportunités" si nouveau bien correspond |
| Visite planifiée | RDV dans calendrier | Rappel SMS/email J-1 + J du rendez-vous |
| Post-visite | 24h après visite | Email de suivi + demande de feedback |
| Prospect froid | Inactivité > 7 jours | Email de relance avec nouveaux biens ou baisse de prix |
| Prospect froid > 30j | Inactivité > 30 jours | Email "Le marché a évolué" |

**Canaux MVP :** Email (SendGrid), SMS (Twilio)

---

#### UC-07 : Scoring et Qualification des Leads
**Description :** Score automatique attribué à chaque prospect sur 100 points, basé sur ses signaux d'intérêt et la correspondance avec le portefeuille de biens.

**Critères de scoring :**
- Budget défini et cohérent avec le marché local (+20 pts)
- Critères de recherche précis (surface, localisation) (+15 pts)
- Engagement dans la conversation (questions posées, photos vues) (+20 pts)
- Demande de visite (+25 pts)
- Coordonnées complètes fournies (+10 pts)
- Urgence exprimée ("cherche pour le mois prochain") (+10 pts)

---

#### UC-08 : Analytics et Rapports
**Description :** Tableau de bord analytique pour le gérant d'agence avec métriques de performance.

**Métriques disponibles :**
- Volume de leads par canal (web, email, téléphone)
- Taux de réponse IA vs humain
- Temps moyen de qualification
- Taux de conversion leads → visites → offres
- Performance par bien (vues, leads générés, demandes de visite)
- Rapports hebdomadaires automatiques par email

---

### 4.3 Tier 3 — Version 3 / Fonctionnalités avancées (Futur)

#### UC-09 : Estimation Automatique de Prix (AVM)
Modèle d'estimation de valeur vénale basé sur les données de transactions récentes dans le secteur, les caractéristiques du bien et les tendances du marché local.

#### UC-10 : Publication Automatique sur les Portails
Connexion API directe aux portails immobiliers (SeLoger Pro, LeBonCoin Pro) pour publier les annonces validées sans intervention manuelle.

#### UC-11 : Veille Marché et Alertes
Suivi des nouvelles annonces concurrentes dans le secteur, alertes si un bien similaire est mis en vente moins cher, rapports de positionnement prix.

#### UC-12 : Agent WhatsApp Business
Extension de l'Agent Support sur WhatsApp. En France, WhatsApp est peu utilisé en contexte professionnel immobilier — ce use case est conservé en Tier 3 car il devient pertinent pour une expansion future ou pour certains segments (mandataires qui communiquent déjà avec leurs clients via WhatsApp).

#### UC-13 : Suivi Transactionnel Complet
Workflow de suivi de la transaction de l'offre acceptée jusqu'à la signature finale : coordination notaire, banque, diagnostiqueur, déménageur.

---

## 5. Architecture technique

### 5.1 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTS (Tenants)                        │
│  Site agence (widget JS) | Dashboard React | App mobile (v3)   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS
┌──────────────────────────▼──────────────────────────────────────┐
│                    API GATEWAY (FastAPI)                         │
│   Auth JWT | Rate limiting | Tenant isolation | CORS            │
└───┬──────────┬────────────┬───────────────┬─────────────────────┘
    │          │            │               │
┌───▼──┐  ┌───▼──┐  ┌──────▼──┐  ┌────────▼────────┐
│Agent │  │Agent │  │  Agent  │  │  Agent Vocal    │
│Supp. │  │Anal. │  │Rédact.  │  │  (VAPI.ai)      │
└───┬──┘  └───┬──┘  └──────┬──┘  └────────┬────────┘
    │          │            │               │
┌───▼──────────▼────────────▼───────────────▼────────┐
│            ORCHESTRATEUR (LangGraph)                │
│   Workflows stateful | Graphes conditionnels        │
└───┬──────────┬────────────┬───────────────┬─────────┘
    │          │            │               │
┌───▼──┐  ┌───▼────┐  ┌────▼────┐  ┌──────▼──────┐
│Celery│  │  RAG   │  │External │  │  Monitoring  │
│+Redis│  │pgvector│  │  APIs   │  │  (Grafana)   │
└───┬──┘  └───┬────┘  └────┬────┘  └─────────────┘
    │          │            │
┌───▼──────────▼────────────▼────────────────────────┐
│              PostgreSQL (données structurées)       │
│   Isolation par tenant_id sur toutes les tables    │
└────────────────────────────────────────────────────┘
```

### 5.2 Architecture multi-tenant — approche progressive

L'isolation multi-tenant est implémentée de façon progressive pour ne pas sur-ingéniérer le MVP tout en posant les bonnes fondations dès le départ.

| Phase | Stratégie d'isolation | Effort | Clients cibles |
|-------|----------------------|--------|----------------|
| **MVP (0-10 clients)** | `tenant_id` sur toutes les tables + filtre applicatif systématique dans chaque repository | ~2 jours | Agences pilotes |
| **V2 (10-50 clients)** | Activation du RLS PostgreSQL pour sécurité renforcée, sans refonte du code | ~1 jour | Croissance |
| **Enterprise (sur demande)** | Instance dédiée (base + infra séparées) pour grands réseaux exigeant l'isolation totale | ~1 semaine | Grands groupes |

**MVP — Filtre applicatif (`tenant_id` partout) :**

```python
# Chaque repository filtre systématiquement par tenant
class PropertyRepository:
    def get_active(self, tenant_id: UUID) -> list[Property]:
        return db.query(Property).filter(
            Property.tenant_id == tenant_id,
            Property.status == "active"
        ).all()

# Middleware FastAPI injecte le tenant_id dans chaque requête
async def tenant_middleware(request: Request, call_next):
    token = request.headers.get("X-Widget-Token") or extract_jwt_tenant(request)
    request.state.tenant_id = resolve_tenant(token)
    return await call_next(request)
```

**V2 — Activation RLS PostgreSQL (non-breaking) :**

```sql
ALTER TABLE properties ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON properties
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

**Isolation des données vectorielles :** Filtrage par `tenant_id` à chaque requête pgvector dès le MVP — le RLS sur les vecteurs arrive avec la V2.

**Configuration par tenant :** Stockée dans `tenants.settings` (JSON) — ton de marque, horaires, plateformes actives, numéro Twilio, email d'escalade, templates personnalisés.

### 5.3 Flux d'un message entrant (Agent Support)

```
Prospect envoie message
        │
        ▼
WebSocket / REST endpoint (FastAPI)
        │
        ▼
Middleware : identifie tenant_id via widget_token
        │
        ▼
SupportAgent.process(message, conversation_id)
    ├── Extraire critères de recherche (LLM)
    ├── Recherche vectorielle pgvector (top 10 candidats)
    ├── Filtrage SQL (prix, surface, nb pièces, statut=active)
    ├── Si visite souhaitée → Google Calendar API (créneaux libres)
    ├── Formuler réponse naturelle (LLM)
    └── Sauvegarder message + critères extraits (PostgreSQL)
        │
        ▼
Réponse streamée au prospect
        │
        ▼
Si confiance < 0.7 → Notification email/Slack à l'agent humain
```

### 5.4 Flux d'un nouveau bien entrant (Orchestrateur)

```
POST /api/properties (fichiers PDF uploadés)
        │
        ▼
Celery task créée : analyze_documents
        │
        ▼
AnalystAgent :
    ├── Classifier le document (DPE ? Mandat ? PV copro ?)
    ├── Extraction structurée → JSON (extracted_data)
    └── Indexation texte dans pgvector
        │
        ▼
Celery task créée : generate_listings
        │
        ▼
WriterAgent :
    ├── Pour chaque plateforme configurée :
    │   ├── Charger template plateforme
    │   ├── Générer titre + description
    │   └── Créer Listing (status="draft")
    └── Notification dashboard : "X annonces à valider"
        │
        ▼
Celery task créée : notify_matching_prospects
        │
        ▼
Orchestrateur :
    ├── Recherche prospects avec critères correspondants
    └── Déclenche séquence email "Nouveau bien pour vous"
```

### 5.5 Sécurité

| Couche | Mécanisme |
|--------|-----------|
| Authentification | JWT (access token 15min + refresh token 7j), rotation automatique |
| Autorisation | RBAC : rôles `admin_tenant`, `agent`, `viewer`, `super_admin` |
| Isolation données | Row-Level Security PostgreSQL par tenant_id |
| Données en transit | TLS 1.3 obligatoire |
| Données au repos | Chiffrement AES-256 sur disques (option cloud provider) |
| Clés API | Stockées chiffrées dans la base (pas en clair dans settings JSON) |
| RGPD | Droit à l'oubli : endpoint `/api/gdpr/erase` par tenant, logs d'accès |
| Rate limiting | 100 req/min par tenant, 10 req/min par IP anonyme (chatbot) |
| Audit logs | Toutes les actions sur données sensibles tracées dans `audit_logs` |

---

## 6. Stack technologique recommandée

### 6.1 Tableau de décision

| Brique | Choix retenu | Alternatives considérées | Justification |
|--------|-------------|--------------------------|---------------|
| **Framework API** | FastAPI (Python 3.12) | Django REST, Node.js/Express | Async natif, performances, écosystème IA Python |
| **Orchestration agents** | LangGraph | CrewAI, AutoGen, Haystack | Contrôle fin des états, cycles conditionnels, production-ready, cas réel estate documenté |
| **LLM principal** | Claude Sonnet 4.6 (Anthropic) | GPT-4o, Mistral, Llama 3 | Meilleur rapport qualité/coût/contexte long, prompt caching Anthropic réduit les coûts |
| **LLM économique** | Claude Haiku 4.5 | GPT-4o-mini | Tâches simples (classification, extraction courte), très faible latence |
| **Base de données** | PostgreSQL 16 + pgvector | MongoDB, Chroma, Pinecone | Un seul système, RLS natif, ACID, pgvector mature en prod |
| **Cache / Queue** | Redis 7 | RabbitMQ, Kafka | Simplicité, Celery support natif, mémoire court terme agents |
| **Tâches async** | Celery 5 | ARQ, Dramatiq | Mature, bataille-testé, monitoring avec Flower |
| **Agent vocal** | VAPI.ai | Twilio + Whisper + ElevenLabs DIY | VAPI abstrait la complexité WebSocket+STT+TTS, latence optimisée <1s |
| **TTS (si DIY)** | ElevenLabs | Coqui TTS, Azure TTS | Qualité voix naturelle en français, clonage de voix |
| **STT** | Whisper API (OpenAI) | Deepgram, Azure Speech | Meilleure précision sur le français, accents régionaux inclus |
| **Email** | SendGrid | Mailgun, AWS SES | Deliverability, templates, analytics |
| **Téléphonie** | Twilio | Vonage, Sinch | Maturité, numéros français disponibles, WebSocket stable |
| **Calendrier** | Google Calendar API | CalDAV, Calendly API | Adoption massive en France, tokens OAuth2 par tenant |
| **Workflow no-code** | n8n (self-hosted) | Zapier, Make | Open source, self-hosted = RGPD, webhooks entrants |
| **Frontend** | React 18 + Tailwind CSS | Vue.js, Next.js | Next.js possible pour SEO, React pour SPA dashboard |
| **Widget chatbot** | JS Vanilla (iframe ou Web Component) | React micro-frontend | Légèreté, compatibilité max avec sites clients (Wix, WordPress, custom) |
| **Conteneurisation** | Docker + Docker Compose | — | Standard industrie |
| **Orchestration prod** | Kubernetes (K8s) | Docker Swarm | Scalabilité horizontale par tenant, rolling updates |
| **CI/CD** | GitHub Actions | GitLab CI, CircleCI | Intégration GitHub, gratuit pour repos publics |
| **Monitoring** | Grafana + Prometheus + Sentry | Datadog (coûteux) | Open source, alertes, traces d'erreur |
| **Tests** | pytest + httpx + Playwright | — | Coverage API + E2E frontend |

### 6.2 Note sur le choix LLM

**Recommandation : Claude Sonnet 4.6 comme LLM principal**

- **Prompt caching Anthropic :** Réduit les coûts de 60-90% sur les prompts système répétitifs (contexte du tenant, catalogue de biens). Critique pour un SaaS multi-tenant à volume élevé.
- **Fenêtre de contexte 200K tokens :** Permet de passer l'intégralité d'un catalogue de biens ou d'un dossier de transaction dans le contexte sans chunking complexe.
- **Qualité du français :** Supérieur à GPT-4o-mini sur le français formel attendu en immobilier.
- **Modèle économique prévisible :** Tarification per-token plutôt que per-request, meilleure pour un SaaS facturant à l'usage.

**Pour les tâches de classification et d'extraction simples :** Claude Haiku 4.5 (4-5x moins cher, latence <500ms).

### 6.3 Architecture de déploiement

```
Production :
├── Kubernetes cluster (3+ nœuds)
│   ├── Namespace par environnement (prod / staging / dev)
│   ├── HPA (Horizontal Pod Autoscaler) sur les pods agents
│   └── Secrets chiffrés (Kubernetes Secrets + Vault optionnel)
├── PostgreSQL managé (Supabase ou AWS RDS eu-west-3 Paris) avec backups automatiques
├── Redis managé (Upstash région Europe)
├── CDN (Cloudflare) pour le widget JS et les assets frontend
└── Hébergement : OVH Cloud ou AWS Paris (eu-west-3) — données hébergées en France, conformité RGPD

Développement :
└── Docker Compose (tous les services en local)

Note : L'hébergement en France (pas seulement en UE) est un argument commercial fort
auprès des agences françaises sensibles à la souveraineté des données.
```

---

## 7. Modèle de données

### 7.1 Entités principales

```python
# Enrichissement du modèle de données de base

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True)
    website_url = Column(String, nullable=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    country = Column(String, default="FR")          # "FR" — champ prévu pour expansion future
    timezone = Column(String, default="Europe/Paris")
    locale = Column(String, default="fr-FR")
    plan = Column(String, default="starter")        # "starter", "pro", "enterprise"
    plan_expires_at = Column(DateTime, nullable=True)
    settings = Column(JSON, default={})             # Config spécifique tenant
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Lead(Base):
    """Un prospect qualifié par l'agent IA"""
    __tablename__ = "leads"
    id = Column(UUID, primary_key=True, default=uuid4)
    tenant_id = Column(UUID, ForeignKey("tenants.id"), nullable=False)
    conversation_id = Column(UUID, ForeignKey("conversations.id"), nullable=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    whatsapp = Column(String, nullable=True)
    criteria = Column(JSON, nullable=True)          # {type, budget_min, budget_max, surface_min, city, ...}
    score = Column(Integer, default=0)              # 0-100
    status = Column(String, default="new")          # "new", "qualified", "visit_scheduled", "offer_made", "won", "lost"
    source = Column(String, nullable=True)          # "chatbot", "email", "phone", "referral"
    assigned_agent_id = Column(UUID, ForeignKey("users.id"), nullable=True)
    gdpr_consent = Column(Boolean, default=False)
    gdpr_consent_at = Column(DateTime, nullable=True)
    last_contact_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class User(Base):
    """Un utilisateur de l'agence (agent, directeur, admin)"""
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid4)
    tenant_id = Column(UUID, ForeignKey("tenants.id"), nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="agent")          # "super_admin", "admin_tenant", "agent", "viewer"
    is_active = Column(Boolean, default=True)
    calendar_token = Column(JSON, nullable=True)    # OAuth2 token Google Calendar
    notification_prefs = Column(JSON, default={})   # Canaux notifs : email, Slack, SMS
    created_at = Column(DateTime, server_default=func.now())

class Visit(Base):
    """Une visite planifiée"""
    __tablename__ = "visits"
    id = Column(UUID, primary_key=True, default=uuid4)
    tenant_id = Column(UUID, ForeignKey("tenants.id"), nullable=False)
    property_id = Column(UUID, ForeignKey("properties.id"), nullable=False)
    lead_id = Column(UUID, ForeignKey("leads.id"), nullable=False)
    agent_id = Column(UUID, ForeignKey("users.id"), nullable=True)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")    # "scheduled", "done", "cancelled", "no_show"
    feedback_prospect = Column(Text, nullable=True)
    feedback_agent = Column(Text, nullable=True)
    calendar_event_id = Column(String, nullable=True)  # ID événement Google Calendar
    created_at = Column(DateTime, server_default=func.now())

class Notification(Base):
    """Notifications système (escalades, alertes, rapports)"""
    __tablename__ = "notifications"
    id = Column(UUID, primary_key=True, default=uuid4)
    tenant_id = Column(UUID, ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=True)
    type = Column(String)                           # "escalation", "new_lead", "visit_reminder", "report"
    title = Column(String)
    body = Column(Text)
    channel = Column(String)                        # "email", "slack", "in_app", "sms"
    is_read = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class AuditLog(Base):
    """Logs d'audit RGPD et sécurité"""
    __tablename__ = "audit_logs"
    id = Column(UUID, primary_key=True, default=uuid4)
    tenant_id = Column(UUID, ForeignKey("tenants.id"), nullable=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=True)
    action = Column(String)                         # "lead.view", "lead.delete", "property.create", ...
    resource_type = Column(String)
    resource_id = Column(UUID, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
```

### 7.2 Configuration tenant (settings JSON enrichi)

```json
{
  "brand": {
    "name": "Agence ImmoPlus",
    "voice": "professionnel et chaleureux",
    "greeting": "Bonjour, bienvenue chez ImmoPlus !",
    "signature": "L'équipe ImmoPlus - Votre partenaire immobilier de confiance",
    "logo_url": "https://cdn.autopilot-immo.fr/tenants/immoplus/logo.png",
    "primary_color": "#2563EB"
  },
  "operations": {
    "working_hours": {"start": "09:00", "end": "19:00", "days": ["mon","tue","wed","thu","fri","sat"]},
    "timezone": "Europe/Paris",
    "auto_followup_days": [1, 7, 30],
    "escalation_threshold": 0.7,
    "escalation_channels": ["email", "slack"]
  },
  "contacts": {
    "escalation_email": "direction@immoplus.fr",
    "escalation_slack_webhook": "https://hooks.slack.com/...",
    "twilio_number": "+33123456789"
  },
  "features": {
    "voice_enabled": true,
    "sms_enabled": false,
    "whatsapp_enabled": false,
    "auto_publish_listings": false,
    "scoring_enabled": true
  },
  "platforms": {
    "active": ["seloger", "leboncoin", "website"],
    "seloger_api_key": "encrypted:...",
    "leboncoin_api_key": "encrypted:..."
  },
  "agents": {
    "support": {"model": "claude-haiku-4-5-20251001", "max_tokens": 1024},
    "analyst": {"model": "claude-sonnet-4-6", "max_tokens": 4096},
    "writer": {"model": "claude-sonnet-4-6", "max_tokens": 2048}
  }
}
```

---

## 8. Roadmap et phases de développement

### Phase 1 — MVP (Semaines 1-12)

**Objectif :** Déployer le produit chez les 3 premières agences pilotes.

| Semaine | Livrables |
|---------|-----------|
| 1-2 | Infrastructure : Docker Compose, PostgreSQL + pgvector, Redis, FastAPI skeleton, auth JWT |
| 3-4 | Modèles de données, CRUD biens, multi-tenant avec RLS |
| 5-6 | Agent Analyste : upload PDF, classification, extraction DPE + mandats, Celery async |
| 7-8 | Agent Rédacteur : génération annonces SeLoger/LeBonCoin, workflow draft → validation |
| 9-10 | Agent Support : chatbot web, matching RAG + SQL, Google Calendar |
| 11 | Dashboard React : gestion biens, prospects, conversations, validation annonces |
| 12 | Widget JS embeddable, tests E2E, déploiement OVH, onboarding 3 agences pilotes |

**KPIs de succès MVP :**
- 3 agences pilotes actives avec > 50 conversations/mois chacune
- Taux de qualification automatique > 60% (sans escalade humaine)
- Temps moyen de réponse initiale < 10 secondes
- Satisfaction agents (NPS) > 7/10

---

### Phase 2 — V2 (Semaines 13-22)

**Objectif :** Atteindre 20 agences, lancer la monétisation complète.

| Semaine | Livrables |
|---------|-----------|
| 13-15 | Agent Vocal (VAPI.ai), numéros Twilio, tests voix française |
| 16-17 | Scoring leads (0-100), pipeline CRM visuel dans dashboard |
| 18-19 | Séquences de relances automatiques (email J+1, J+7, J+30) |
| 20-21 | Analytics et rapports hebdomadaires automatiques |
| 22 | Module facturation (Stripe), plans Starter/Pro/Enterprise |

---

### Phase 3 — V3 (Semaines 23-36)

**Objectif :** Différenciation avancée sur le marché français, préparer l'expansion Enterprise.

| Semaine | Livrables |
|---------|-----------|
| 23-25 | Publication automatique portails (SeLoger Pro API, LeBonCoin Pro API) |
| 26-28 | Estimation automatique de prix (AVM) basée sur données DVF et transactions locales |
| 29-31 | Veille marché : alertes concurrentielles, rapport de positionnement prix automatique |
| 32-33 | Application mobile gérant d'agence (React Native), notifications push |
| 34-35 | API publique (pour intégrations CRM tiers : Périclès, Hektor, Apimo) |
| 36 | Bilan, décision go/no-go expansion internationale basée sur métriques réelles |

---

## 9. Modèle économique SaaS

### 9.1 Plans tarifaires

| Plan | Prix/mois | Cible | Inclus |
|------|-----------|-------|--------|
| **Starter** | 99 € | Agence 1-3 agents | Agent Support chatbot, Analyste docs, Rédacteur annonces, 1 000 conversations/mois, 50 biens actifs |
| **Pro** | 249 € | Agence 4-15 agents | Tout Starter + Agent Vocal, relances automatiques, scoring leads, analytics avancés, 5 000 conversations/mois, biens illimités |
| **Enterprise** | 399 €+ | Réseaux, grands groupes | Tout Pro + SLA garanti, onboarding dédié, personnalisation avancée, API accès, conversations illimitées, support prioritaire |

**Options add-on :**
- WhatsApp Business : +29 €/mois
- Numéro vocal dédié (Twilio) : +19 €/mois
- Rapport mensuel automatique propriétaires : +15 €/mois
- Dépassement de conversations : 0,02 € par conversation supplémentaire

### 9.2 Coûts opérationnels estimés (par tenant actif/mois)

| Coût | Estimation | Base de calcul |
|------|-----------|----------------|
| LLM (Claude Sonnet + Haiku) | 8-25 € | 1 000-5 000 conversations avec prompt caching activé |
| Infrastructure (RDS, Redis, K8s pod) | 5-15 € | Mutualisé entre tenants |
| Twilio (SMS + téléphonie) | 0-20 € | Selon usage vocal |
| ElevenLabs (TTS) | 2-8 € | Selon minutes d'appel |
| Total coûts directs | **15-68 €** | Selon plan |

**Marge brute cible :**
- Starter : 99 € - 35 € = 64 € (65% de marge)
- Pro : 249 € - 68 € = 181 € (73% de marge)

### 9.3 Métriques SaaS à suivre

| Métrique | Cible M6 | Cible M12 | Cible M24 |
|----------|----------|----------|----------|
| MRR | 3 000 € | 15 000 € | 60 000 € |
| Nombre de tenants actifs | 30 | 100 | 300 |
| Churn mensuel | < 5% | < 3% | < 2% |
| NPS | > 30 | > 40 | > 50 |
| ARPU | 120 € | 150 € | 200 € |
| CAC (coût acquisition client) | < 300 € | < 250 € | < 200 € |
| LTV/CAC ratio | > 3x | > 5x | > 8x |

---

## 10. Risques et mitigations

### 10.1 Risques RGPD et conformité

| Risque | Impact | Mitigation |
|--------|--------|-----------|
| Données prospects stockées sans consentement | Élevé | Bannière de consentement dans le widget, champ `gdpr_consent` obligatoire, endpoint d'effacement RGPD |
| Transfert de données hors UE (APIs OpenAI/Anthropic) | Moyen | DPA (Data Processing Agreement) signé avec Anthropic, option de ne pas logguer les prompts, hébergement données sensibles en UE |
| Violation de données multi-tenant | Élevé | RLS PostgreSQL, tests de pénétration réguliers, audit logs, isolation des embeddings pgvector |
| Durée de conservation excessive | Moyen | Politique de rétention automatique : conversations purgées après 24 mois, audit logs après 36 mois |

### 10.2 Risques techniques

| Risque | Impact | Mitigation |
|--------|--------|-----------|
| Hallucinations IA (informations fausses sur un bien) | Élevé | RAG strict : réponse uniquement basée sur les données indexées, pas de "génération libre" sur les prix ou caractéristiques |
| Latence agent vocal > 2s | Moyen | VAPI.ai gère l'optimisation, streaming TTS, pré-chargement contexte tenant |
| Dépendance API externe (Anthropic down) | Moyen | Fallback sur GPT-4o-mini (OpenAI) pour continuité de service, circuit breaker |
| Coûts LLM explosifs | Moyen | Prompt caching Anthropic (-60-90%), rate limiting par tenant, monitoring coûts en temps réel avec alertes |

### 10.3 Risques métier et adoption

| Risque | Impact | Mitigation |
|--------|--------|-----------|
| Résistance des agents immobiliers à l'IA | Moyen | Positionner l'IA comme "assistant" non comme "remplaçant", dashboard agent-friendly, formation onboarding incluse |
| Concurrence d'un grand acteur (SeLoger, Meilleurs Agents) | Élevé | Vitesse d'exécution, focus France exclusive, relations directes agences, multi-agents différenciant vs outils mono-fonction |
| Difficulté d'intégration sur sites clients hétérogènes | Faible | Widget JS universel (1 ligne de code), documentation WordPress/Wix/custom, support intégration inclus en onboarding |
| CRM tiers déjà en place chez les agences | Moyen | API ouverte en V3 pour s'intégrer comme couche IA au-dessus du CRM existant plutôt que de le remplacer |

---

## Annexes

### A. Glossaire

| Terme | Définition |
|-------|-----------|
| **Tenant** | Une agence immobilière cliente de la plateforme |
| **Lead** | Un prospect qualifié avec des critères de recherche identifiés |
| **RAG** | Retrieval-Augmented Generation — technique de recherche dans une base vectorielle pour enrichir les réponses IA |
| **pgvector** | Extension PostgreSQL pour le stockage et la recherche par similarité d'embeddings |
| **LangGraph** | Librairie d'orchestration multi-agents de LangChain basée sur des graphes d'états |
| **RLS** | Row-Level Security — mécanisme PostgreSQL d'isolation des données par tenant |
| **VAPI.ai** | Infrastructure spécialisée pour agents vocaux IA (STT + LLM + TTS optimisé) |
| **DPE** | Diagnostic de Performance Énergétique — document obligatoire en France pour les transactions immobilières |
| **PV d'AG** | Procès-verbal d'Assemblée Générale de copropriété |
| **AVM** | Automated Valuation Model — modèle d'estimation automatique de la valeur d'un bien |

### B. Sources et références

- PwC / ULI — *Emerging Trends in Real Estate 2025* : adoption IA secteur immobilier
- Rechat — *2025 AI Investment in Real Estate* (janvier 2026) : priorités IA immo
- AgentZap — *Real Estate Lead Response Statistics 2026* : données réponse leads
- Salesmate — *Problems of Being in Real Estate Industry 2025* : pain points agents
- Grand View Research — *Real Estate Software Market Size 2030*
- LangChain Blog — *Build.inc LangGraph CRE Automation* : cas réel immobilier commercial avec LangGraph
- Keyzia.fr — *IA agence immobilière usages 2026* : marché français
- Maformationimmo.fr — *IA agent immobilier, gain 10h/semaine* : ROI terrain France
- Biz4group — *Multi-Tenant Real Estate SaaS Application* : architecture SaaS immo

---

*Document vivant — à mettre à jour à chaque fin de phase de développement.*
