<div align="center">

# 🇫🇷 Mistral Bureau

**27 agents one-shot sur [La Plateforme Mistral](https://docs.mistral.ai) — FR, multi-modèles, Pixtral vision, zero-429.**

[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agents](https://img.shields.io/badge/agents-27-orange.svg)](#agents)
[![Mistral](https://img.shields.io/badge/Mistral-La_Plateforme-ff7000)](https://console.mistral.ai)

*Phase 2 du stack Mistral · Phase 1 = [Devstral Lab](https://github.com/anthonyoccelli33480-ctrl/devstral-lab)*

</div>

## Modèles

| Modèle | Agents | Gate |
|--------|--------|------|
| **Mistral Large** | Produit, carrière, sécurité, éval | 30s |
| **Ministral 8B** | TL;DR, router intent | 15s |
| **Devstral Small 2** | Dev, README, secrets | 30s |
| **Pixtral Large** | Vision (6 agents + upload) | 25s |

## Agents

- **Carrière** — JD, STAR, LinkedIn, Email, README
- **Produit** — MVP, Decision, Pitch, Competitor, Pricing, Onboarding
- **Contenu** — TL;DR, Compare, Outline
- **Sécurité** — Threat, RGPD, Secret
- **Vision** — UI Review, Diagram, OCR, A11y, Mockup, Wireframe
- **IA** — Router, Eval
- **Dev** — Review, Fix (pont vers Devstral Lab)

## Lancer

```bash
cp .env.example .env   # MISTRAL_API_KEY
make install
make backend   # :8789
make frontend  # :5177
```

## Stack Mistral

| Repo | Focus | Ports |
|------|-------|-------|
| [devstral-lab](https://github.com/anthonyoccelli33480-ctrl/devstral-lab) | Code agentique | 8788 / 5175 |
| **mistral-bureau** | FR multi-modèles + vision | **8789 / 5177** |

MIT