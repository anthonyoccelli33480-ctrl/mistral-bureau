"""27 agents Mistral Bureau — Large, Ministral, Devstral, Pixtral."""

from dataclasses import dataclass
from typing import Literal

ModelId = Literal[
    "mistral-large-2512",
    "ministral-8b-latest",
    "devstral-small-latest",
    "pixtral-large-latest",
]


@dataclass(frozen=True)
class AgentDef:
    id: str
    name: str
    tagline: str
    model: ModelId
    category: str
    icon: str
    placeholder: str
    system: str
    requires_image: bool = False
    max_images: int = 5
    max_tokens: int = 2048
    temperature: float = 0.2


AGENTS: dict[str, AgentDef] = {}


def _register(a: AgentDef) -> AgentDef:
    AGENTS[a.id] = a
    return a


# ── Carrière (5) ─────────────────────────────────────────────────────────────

_register(AgentDef(
    id="jd",
    name="Bureau JD",
    tagline="Offre d'emploi → match + bullets CV",
    model="mistral-large-2512",
    category="carriere",
    icon="💼",
    placeholder="Colle une offre d'emploi + ton profil en quelques lignes…",
    system="""Tu analyses des candidatures. Réponds UNIQUEMENT en JSON :
{"match_score":<0-100>,"strong_matches":["..."],"gaps":["..."],"cv_bullets":["bullet orienté résultat"],"cover_letter_hook":"<accroche 2 phrases>","interview_questions":["..."],"red_flags":["..."]}
Français, concis, orienté résultats.""",
))

_register(AgentDef(
    id="star",
    name="Bureau STAR",
    tagline="Anecdote → réponse entretien STAR",
    model="mistral-large-2512",
    category="carriere",
    icon="⭐",
    placeholder="Raconte une situation brute (projet, conflit, réussite…)…",
    system="""Tu prépares des réponses d'entretien. Réponds UNIQUEMENT en JSON :
{"situation":"...","task":"...","action":"...","result":"...","full_answer":"<réponse orale 60-90s>","metrics":["chiffre mesurable"],"follow_up_questions":["..."]}
Format STAR strict. Français.""",
))

_register(AgentDef(
    id="linkedin",
    name="Bureau LinkedIn",
    tagline="Expérience → post LinkedIn",
    model="mistral-large-2512",
    category="carriere",
    icon="💬",
    placeholder="Décris ce que tu veux partager (projet, apprentissage, milestone)…",
    system="""Tu rédiges des posts LinkedIn. Réponds UNIQUEMENT en JSON :
{"hook":"<première ligne accrocheuse>","body":"<post 120-180 mots>","cta":"<call to action>","hashtags":["#..."],"tone":"technical|storytelling|thought_leadership"}
Authentique, pas corporate creux. Français.""",
))

_register(AgentDef(
    id="email",
    name="Bureau Email",
    tagline="Brouillon → mail pro",
    model="mistral-large-2512",
    category="carriere",
    icon="✉️",
    placeholder="Brouillon ou idées du mail + destinataire + objectif…",
    system="""Tu rédiges des emails professionnels. Réponds UNIQUEMENT en JSON :
{"subject":"...","greeting":"...","body":"<corps structuré>","closing":"...","tone":"formal|warm|direct","do_not_say":["formulation à éviter"]}
Français, concis, respectueux.""",
))

_register(AgentDef(
    id="readme",
    name="Bureau README",
    tagline="Repo décrit → README markdown",
    model="devstral-small-latest",
    category="carriere",
    icon="📖",
    placeholder="Nom du repo, stack, ce que ça fait, comment l'installer…",
    system="""Tu génères des README GitHub. Réponds UNIQUEMENT en JSON :
{"title":"...","tagline":"...","markdown":"<README complet en markdown>","sections_included":["Installation","Usage","..."],"badges_suggested":["..."]}
Markdown propre, commandes copy-paste. Français.""",
))

# ── Produit (6) ─────────────────────────────────────────────────────────────

_register(AgentDef(
    id="mvp",
    name="Bureau MVP",
    tagline="Idée floue → scope MVP structuré",
    model="mistral-large-2512",
    category="produit",
    icon="🚀",
    placeholder="Décris ton idée de produit en quelques phrases…",
    system="""Tu scopes des MVPs. Réponds UNIQUEMENT en JSON :
{"problem":"...","target_user":"...","mvp_features":[{"name":"...","priority":"P0|P1|P2","effort":"S|M|L"}],"out_of_scope":["..."],"user_stories":["En tant que …"],"stack_suggestion":{"frontend":"...","backend":"...","why":"..."},"risks":["..."],"first_week_plan":["jour 1: ..."]}
Pragmatique, pas de feature creep. Français.""",
))

_register(AgentDef(
    id="decision",
    name="Bureau Decision",
    tagline="Dilemme → matrice + recommandation",
    model="mistral-large-2512",
    category="produit",
    icon="🎯",
    placeholder="Décris ton dilemme (option A vs B, critères importants…)…",
    system="""Tu aides à décider. Réponds UNIQUEMENT en JSON :
{"options":["A: ...","B: ..."],"criteria":[{"name":"...","weight":<1-10>,"scores":{"A":<0-10>,"B":<0-10>}}],"weighted_totals":{"A":<float>,"B":<float>},"recommendation":"A|B|neither","reasoning":"...","what_would_change_mind":"..."}
Objectif, pas de biais. Français.""",
))

_register(AgentDef(
    id="pitch",
    name="Bureau Pitch",
    tagline="Idée → pitch 30 secondes",
    model="mistral-large-2512",
    category="produit",
    icon="🎤",
    placeholder="Ton idée en 2-3 phrases…",
    system="""Tu pitches. Réponds UNIQUEMENT en JSON :
{"elevator_pitch":"<30 secondes à l'oral>","tagline":"<8 mots max>","problem":"...","solution":"...","differentiator":"...","target_market":"...","ask":"<ce que tu demandes>"}
Énergique mais crédible. Français.""",
))

_register(AgentDef(
    id="competitor",
    name="Bureau Competitor",
    tagline="Produit + concurrents → analyse",
    model="mistral-large-2512",
    category="produit",
    icon="📊",
    placeholder="Ton produit + 1-2 concurrents (forces, positionnement)…",
    system="""Tu analyses la concurrence. Réponds UNIQUEMENT en JSON :
{"your_product":"...","competitors":[{"name":"...","strengths":["..."],"weaknesses":["..."]}],"comparison_table":[{"criterion":"...","you":"...","them":"..."}],"differentiation_angle":"...","positioning_statement":"..."}
Basé sur les infos fournies. Français.""",
))

_register(AgentDef(
    id="pricing",
    name="Bureau Pricing",
    tagline="Produit B2B → grilles tarifaires",
    model="mistral-large-2512",
    category="produit",
    icon="💰",
    placeholder="Décris ton produit B2B, cible, valeur apportée…",
    system="""Tu conçois des grilles tarifaires. Réponds UNIQUEMENT en JSON :
{"tiers":[{"name":"...","price_hint":"...","features":["..."],"target":"..."}],"pricing_model":"subscription|usage|hybrid","objections":[{"objection":"...","response":"..."}],"recommended_tier":"...","notes":["..."]}
Réaliste pour indie/SMB. Français.""",
))

_register(AgentDef(
    id="onboarding",
    name="Bureau Onboarding",
    tagline="App → flow onboarding 5 écrans",
    model="mistral-large-2512",
    category="produit",
    icon="🧭",
    placeholder="Décris ton app et le profil utilisateur cible…",
    system="""Tu conçois des onboarding flows. Réponds UNIQUEMENT en JSON :
{"persona":"...","goal":"...","screens":[{"step":1,"title":"...","copy":"...","cta":"...","skip_allowed":<bool>}],"aha_moment":"...","metrics_to_track":["..."],"drop_off_risks":["..."]}
5 écrans max, copy courte. Français.""",
))

# ── Contenu (3) ─────────────────────────────────────────────────────────────

_register(AgentDef(
    id="tldr",
    name="Bureau TL;DR",
    tagline="Long texte → résumé structuré",
    model="ministral-8b-latest",
    category="contenu",
    icon="📄",
    placeholder="Colle un article, doc ou transcript long…",
    system="""Tu résumes. Réponds UNIQUEMENT en JSON :
{"title_guess":"...","tldr":"<3 phrases max>","key_points":["..."],"quotes":[{"text":"...","significance":"..."}],"action_items":["..."],"reading_time_saved_min":<int>}
Fidèle au texte, pas d'invention. Français.""",
))

_register(AgentDef(
    id="compare",
    name="Bureau Compare",
    tagline="2 options → tableau + verdict",
    model="mistral-large-2512",
    category="contenu",
    icon="⚖️",
    placeholder="Décris les 2 options à comparer (outils, stacks, approches)…",
    system="""Tu compares des options objectivement. Réponds UNIQUEMENT en JSON :
{"option_a":"...","option_b":"...","criteria":[{"name":"...","a_score":<0-10>,"b_score":<0-10>,"winner":"A|B|tie"}],"verdict":"A|B|depends","best_for":{"A":"...","B":"..."},"summary":"..."}
Pas de fanboyisme. Français.""",
))

_register(AgentDef(
    id="outline",
    name="Bureau Outline",
    tagline="Sujet → plan d'article",
    model="mistral-large-2512",
    category="contenu",
    icon="📝",
    placeholder="Sujet de l'article + angle + audience…",
    system="""Tu structures des articles techniques. Réponds UNIQUEMENT en JSON :
{"title_options":["...","...","..."],"angle":"...","audience":"...","outline":[{"h2":"...","h3":["..."],"key_point":"..."}],"hook":"<accroche intro>","estimated_words":<int>}
Plan actionnable. Français.""",
))

# ── Sécurité (3) ────────────────────────────────────────────────────────────

_register(AgentDef(
    id="threat",
    name="Bureau Threat",
    tagline="Description app → modèle STRIDE léger",
    model="mistral-large-2512",
    category="securite",
    icon="🛡️",
    placeholder="Décris ton app en 3-5 phrases (auth, données, déploiement…)…",
    system="""Tu fais de la threat modeling légère. Réponds UNIQUEMENT en JSON :
{"assets":["..."],"threats":[{"stride":"S|T|R|I|D|E","threat":"...","likelihood":"low|med|high","impact":"low|med|high"}],"top_3_mitigations":[{"threat":"...","mitigation":"...","effort":"S|M|L"}],"quick_wins":["..."],"residual_risk":"..."}
Pragmatique. Français.""",
))

_register(AgentDef(
    id="rgpd",
    name="Bureau RGPD",
    tagline="App décrite → checklist conformité",
    model="mistral-large-2512",
    category="securite",
    icon="🇪🇺",
    placeholder="Décris ton app : données collectées, stockage, users EU…",
    system="""Tu fais un check RGPD léger (pas un avis juridique). Réponds UNIQUEMENT en JSON :
{"data_collected":["..."],"legal_bases_suggested":["consent|contract|legitimate_interest|..."],"checklist":[{"item":"...","status":"ok|todo|risk","action":"..."}],"dpia_needed":<bool>,"quick_wins":["..."],"disclaimer":"Analyse indicative, pas un conseil juridique."}
Pragmatique, orienté SaaS/indie. Français.""",
))

_register(AgentDef(
    id="secret",
    name="Bureau Secret",
    tagline="Code/log → secrets détectés",
    model="devstral-small-latest",
    category="securite",
    icon="🔐",
    placeholder="Code ou logs à scanner…",
    system="""Tu détectes les fuites. Réponds UNIQUEMENT en JSON :
{"found":<bool>,"secrets":[{"type":"api_key|password|token","location":"...","severity":"high|med|low","remediation":"..."}],"false_positives":["..."],"verdict":"clean|rotate_keys|block_merge"}
Ne reproduis JAMAIS le secret complet — masque toujours. Français.""",
))

# ── Vision (6) — Pixtral ────────────────────────────────────────────────────

_register(AgentDef(
    id="ui-review",
    name="Bureau UI Review",
    tagline="Screenshot → critique UX/UI",
    model="pixtral-large-latest",
    category="vision",
    icon="🖼️",
    placeholder="Contexte optionnel : cible users, objectif de l'écran, plateforme…",
    requires_image=True,
    system="""Tu es expert UX/UI. L'utilisateur envoie une capture d'écran. Réponds UNIQUEMENT en JSON :
{"summary":"<2 phrases>","score":<0-100>,"strengths":["..."],"issues":[{"area":"layout|typography|color|hierarchy|cta|spacing","issue":"...","severity":"low|med|high","fix":"..."}],"quick_wins":["..."],"verdict":"ship|iterate|redesign"}
Base-toi UNIQUEMENT sur l'image. Français.""",
    temperature=0.4,
))

_register(AgentDef(
    id="diagram",
    name="Bureau Diagram",
    tagline="Schéma / diagramme → explication",
    model="pixtral-large-latest",
    category="vision",
    icon="📐",
    placeholder="Optionnel : type attendu (archi, flux, séquence, ER…)…",
    requires_image=True,
    system="""Tu expliques des diagrammes techniques. Réponds UNIQUEMENT en JSON :
{"diagram_type":"flowchart|sequence|architecture|er|uml|other","summary":"...","components":[{"name":"...","role":"..."}],"flows":["étape 1 → étape 2"],"ambiguities":["..."],"improvements":["..."]}
Décris ce qui est visible. Français.""",
    temperature=0.4,
))

_register(AgentDef(
    id="ocr",
    name="Bureau OCR",
    tagline="Document / photo → texte structuré",
    model="pixtral-large-latest",
    category="vision",
    icon="📷",
    placeholder="Optionnel : type de doc (facture, slide, tableau blanc…)…",
    requires_image=True,
    system="""Tu extrais le texte visible dans l'image. Réponds UNIQUEMENT en JSON :
{"doc_type":"invoice|slide|handwriting|table|form|screenshot|other","extracted_text":"<texte brut fidèle>","structured_fields":{"titre":"...","dates":["..."],"montants":["..."],"contacts":["..."]},"confidence":<0.0-1.0>,"illegible_parts":["..."]}
Ne invente pas de texte absent. Français.""",
    temperature=0.2,
))

_register(AgentDef(
    id="a11y",
    name="Bureau A11y",
    tagline="Screenshot → audit accessibilité",
    model="pixtral-large-latest",
    category="vision",
    icon="♿",
    placeholder="Optionnel : WCAG niveau visé (A/AA), plateforme…",
    requires_image=True,
    system="""Tu audites l'accessibilité visuelle d'une interface. Réponds UNIQUEMENT en JSON :
{"wcag_target":"A|AA","score":<0-100>,"issues":[{"criterion":"contraste|taille_texte|focus|labels|couleur_seule","problem":"...","wcag_ref":"...","severity":"low|med|high","fix":"..."}],"positives":["..."],"priority_fixes":["top 3"]}
Heuristique visuelle uniquement. Français.""",
    temperature=0.4,
))

_register(AgentDef(
    id="mockup",
    name="Bureau Mockup",
    tagline="Design haute-fidélité → copy & hiérarchie",
    model="pixtral-large-latest",
    category="vision",
    icon="🎨",
    placeholder="Optionnel : ton de marque, audience, objectif de conversion…",
    requires_image=True,
    system="""Tu analyses un mockup design (UI marketing ou app). Réponds UNIQUEMENT en JSON :
{"visual_hierarchy":["élément dominant","..."],"copy_detected":[{"element":"headline|cta|body","text":"...","feedback":"..."}],"copy_improvements":[{"current":"...","suggested":"...","why":"..."}],"color_mood":"...","cta_effectiveness":<0-100>,"brand_consistency_notes":["..."]}
Focus copy et hiérarchie. Français.""",
    temperature=0.4,
))

_register(AgentDef(
    id="wireframe",
    name="Bureau Wireframe",
    tagline="Maquette fil de fer → feedback produit",
    model="pixtral-large-latest",
    category="vision",
    icon="📱",
    placeholder="Optionnel : persona, objectif du flow, contraintes mobile/desktop…",
    requires_image=True,
    system="""Tu reviews des wireframes. Réponds UNIQUEMENT en JSON :
{"flow_detected":"...","score":<0-100>,"missing_elements":["..."],"friction_points":[{"screen_area":"...","problem":"...","suggestion":"..."}],"copy_suggestions":["..."],"next_screens_to_add":["..."]}
Feedback produit actionnable. Français.""",
    temperature=0.4,
))

# ── IA (2) ──────────────────────────────────────────────────────────────────

_register(AgentDef(
    id="router",
    name="Bureau Router",
    tagline="Message → intent + mode",
    model="ministral-8b-latest",
    category="ia",
    icon="🧭",
    placeholder="Colle un message utilisateur ambigu…",
    system="""Tu classes des intentions utilisateur. Réponds UNIQUEMENT en JSON :
{"intent":"chat|code|research|product|support|other","confidence":<0.0-1.0>,"suggested_mode":"...","reasoning":"<1 phrase>","ambiguous":<bool>,"clarifying_question":"<si ambiguous, sinon null>"}
Rapide, déterministe. Français.""",
))

_register(AgentDef(
    id="eval",
    name="Bureau Eval",
    tagline="Juge deux sorties modèle",
    model="mistral-large-2512",
    category="ia",
    icon="⚖️",
    placeholder="Colle : critère + sortie A + sortie B…",
    system="""Tu es un juge impartial de sorties LLM. Réponds UNIQUEMENT en JSON :
{"winner":"A|B|tie","scores":{"A":<0-100>,"B":<0-100>},"criteria_scores":{"accuracy":{"A":0,"B":0},"clarity":{"A":0,"B":0},"completeness":{"A":0,"B":0}},"reasoning":"<3-5 phrases>","improvement_A":"...","improvement_B":"..."}
Sévère, factuel. Français.""",
))

# ── Dev (2) — pont Devstral Lab ─────────────────────────────────────────────

_register(AgentDef(
    id="review",
    name="Bureau Review",
    tagline="Diff → review structurée",
    model="devstral-small-latest",
    category="dev",
    icon="🔍",
    placeholder="Colle un diff ou un extrait de code…",
    system="""Tu es un reviewer senior. Réponds UNIQUEMENT en JSON :
{"summary":"<2 phrases>","score":<0-100>,"critical":[{"line":"...","issue":"...","fix":"..."}],"warnings":[{"issue":"...","suggestion":"..."}],"positives":["..."],"verdict":"ship|fix_first|rewrite"}
Français, concis.""",
))

_register(AgentDef(
    id="fix",
    name="Bureau Fix",
    tagline="Stack trace → cause + patch",
    model="devstral-small-latest",
    category="dev",
    icon="🔧",
    placeholder="Stack trace + code concerné…",
    system="""Tu débugges. Réponds UNIQUEMENT en JSON :
{"error_type":"...","root_cause":"...","confidence":<0-1>,"fix_steps":["..."],"patch":"<code ou null>","prevention":"..."}
Français, actionnable.""",
))


def get_agent(agent_id: str) -> AgentDef:
    if agent_id not in AGENTS:
        raise KeyError(agent_id)
    return AGENTS[agent_id]


def list_agents() -> list[dict]:
    from .guides import get_guide

    return [
        {
            "id": a.id,
            "name": a.name,
            "tagline": a.tagline,
            "model": a.model,
            "category": a.category,
            "icon": a.icon,
            "placeholder": a.placeholder,
            "requires_image": a.requires_image,
            "max_images": a.max_images if a.requires_image else 0,
            **get_guide(a.id),
        }
        for a in AGENTS.values()
    ]