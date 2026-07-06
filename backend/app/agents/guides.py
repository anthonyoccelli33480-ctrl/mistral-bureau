"""Guide utilisateur par agent — quoi faire avant / après le run."""

GUIDES: dict[str, dict[str, list[str]]] = {
    "jd": {
        "how_to": [
            "Colle l'offre complète (titre, missions, stack, profil).",
            "Ajoute 3–5 lignes sur ton profil / ce que tu cherches.",
        ],
        "next_steps": [
            "Si match_score > 70 → adapte ton CV avec cv_bullets.",
            "Utilise cover_letter_hook en intro de lettre (Bureau Email si besoin).",
            "Prépare interview_questions pour l'entretien.",
            "Investigue red_flags avant d'accepter.",
        ],
    },
    "star": {
        "how_to": [
            "Raconte une situation brute (projet, conflit, échec retourné…).",
            "Donne des chiffres si tu en as (%, délais, équipe).",
        ],
        "next_steps": [
            "Répète full_answer à voix haute 2–3 fois (60–90 s).",
            "Mémorise metrics — les recruteurs accrochent aux chiffres.",
            "Prépare follow_up_questions avec tes vraies réponses.",
        ],
    },
    "linkedin": {
        "how_to": [
            "Décris le milestone : projet shipped, apprentissage, recrutement…",
            "Indique le ton voulu (technique, storytelling).",
        ],
        "next_steps": [
            "Copie hook + body dans LinkedIn — vérifie le rendu mobile.",
            "Poste aux heures creuses (8h–9h ou 17h–18h).",
            "Réponds aux commentaires dans les 2 h pour le reach.",
        ],
    },
    "email": {
        "how_to": [
            "Brouillon ou bullet points + destinataire + objectif du mail.",
            "Précise le ton (formel, direct, chaleureux).",
        ],
        "next_steps": [
            "Relis do_not_say — reformule si tu as écrit pareil.",
            "Envoie ou planifie — garde subject court (< 50 car.).",
            "Pour une candidature : enchaîne après Bureau JD.",
        ],
    },
    "readme": {
        "how_to": [
            "Nom du repo, stack, ce que ça fait, comment installer/lancer.",
            "Liens demo / screenshot si tu en as.",
        ],
        "next_steps": [
            "Colle markdown dans README.md à la racine.",
            "Ajoute badges_suggested en tête du fichier.",
            "Vérifie que les commandes d'install fonctionnent sur une machine fraîche.",
        ],
    },
    "mvp": {
        "how_to": [
            "Décris le problème et pour qui (pas la solution).",
            "2–3 phrases suffisent — reste flou si c'est flou.",
        ],
        "next_steps": [
            "Implémente uniquement les features P0.",
            "Colle out_of_scope sur le mur du projet — ne les fais pas en v1.",
            "Suis first_week_plan jour par jour.",
            "Valide avec 1 utilisateur réel avant d'ajouter du P1.",
        ],
    },
    "decision": {
        "how_to": [
            "Nomme clairement option A et option B.",
            "Liste tes critères importants (coût, temps, risque…).",
        ],
        "next_steps": [
            "Suis recommendation si weighted_totals sont convaincants.",
            "Si tu hésites encore → vérifie what_would_change_mind avec de vraies données.",
            "Documente la décision (ADR ou note) pour ne pas re-débattre.",
        ],
    },
    "pitch": {
        "how_to": [
            "Ton idée en 2–3 phrases — problème + solution.",
            "À qui tu pitches (investisseur, client, recruteur).",
        ],
        "next_steps": [
            "Répète elevator_pitch en chronométrant (30 s max).",
            "Utilise tagline sur ta landing ou ton LinkedIn.",
            "Adapte ask selon ton interlocuteur du jour.",
        ],
    },
    "competitor": {
        "how_to": [
            "Décris ton produit en une phrase.",
            "Nomme 1–2 concurrents et ce que tu sais d'eux.",
        ],
        "next_steps": [
            "Utilise differentiation_angle sur ta landing page.",
            "Met à jour positioning_statement dans ton pitch deck.",
            "Vérifie comparison_table avec des faits réels (pas du marketing).",
        ],
    },
    "pricing": {
        "how_to": [
            "Produit B2B, cible (indie, PME, enterprise), valeur principale.",
            "Prix concurrents connus si tu en as.",
        ],
        "next_steps": [
            "Teste recommended_tier avec 2–3 prospects.",
            "Prépare les réponses objections pour tes calls de vente.",
            "Ajuste price_hint après le premier paiement réel.",
        ],
    },
    "onboarding": {
        "how_to": [
            "Décris l'app et le premier usage idéal (aha moment).",
            "Profil user : débutant, power user, mobile…",
        ],
        "next_steps": [
            "Implémente screens dans Figma ou direct en code.",
            "Mesure metrics_to_track dès le jour 1.",
            "Réduis drop_off_risks sur les étapes identifiées.",
        ],
    },
    "tldr": {
        "how_to": [
            "Colle l'article, transcript ou doc long (PDF copié en texte).",
            "Pour un URL : copie le contenu toi-même (pas de fetch auto).",
        ],
        "next_steps": [
            "Partage tldr à ton équipe si c'est une veille.",
            "Traite action_items un par un.",
            "Archive key_points dans Notion/Obsidian avec la source.",
        ],
    },
    "compare": {
        "how_to": [
            "Nomme et décris les 2 options (outils, stacks, modèles…).",
            "Indique ton contexte (solo dev, prod, budget…).",
        ],
        "next_steps": [
            "Suis verdict si best_for correspond à ton contexte.",
            "Partage summary en doc d'archi ou thread LinkedIn.",
            "Re-teste dans 6 mois — les stacks évoluent vite.",
        ],
    },
    "outline": {
        "how_to": [
            "Sujet de l'article + angle + audience cible.",
            "Longueur visée si tu as une préférence.",
        ],
        "next_steps": [
            "Choisis un title_options et rédige section par section.",
            "Utilise hook comme intro — ne le jette pas.",
            "Vise estimated_words pour rester focus.",
        ],
    },
    "threat": {
        "how_to": [
            "Décris l'app : auth, données stockées, déploiement, intégrations tierces.",
            "3–5 phrases suffisent.",
        ],
        "next_steps": [
            "Implémente top_3_mitigations dans l'ordre effort S → M.",
            "Crée des tickets pour chaque threat likelihood/impact high.",
            "Revois après un changement d'archi majeur.",
        ],
    },
    "rgpd": {
        "how_to": [
            "Décris : données collectées, où elles sont stockées, users EU ou non.",
            "Mentionne cookies, analytics, sous-traitants.",
        ],
        "next_steps": [
            "Traite chaque checklist item status todo ou risk.",
            "Ajoute disclaimer + politique de confidentialité sur ton site.",
            "Si dpia_needed → consulte un juriste (ce n'est pas un avis légal).",
        ],
    },
    "secret": {
        "how_to": [
            "Colle du code, un .env accidentel, ou des logs.",
            "Ne colle pas de vrais secrets de prod si tu les as déjà exposés ailleurs.",
        ],
        "next_steps": [
            "Si verdict = rotate_keys ou block_merge → rotate immédiatement.",
            "Applique remediation (gitignore, env vars, vault).",
            "Relance après correction pour confirmer verdict = clean.",
        ],
    },
    "ui-review": {
        "how_to": [
            "Upload une capture PNG/JPEG (écran entier ou composant isolé).",
            "Ajoute du contexte en texte : cible, objectif, web ou mobile.",
        ],
        "next_steps": [
            "Corrige les issues severity high en premier.",
            "Applique quick_wins dans Figma ou ton code sous 1 h.",
            "Si verdict redesign → refais une capture après itération et relance.",
        ],
    },
    "diagram": {
        "how_to": [
            "Upload un schéma lisible (archi, flux, séquence, ER, whiteboard photo).",
            "Pose une question précise en texte si tu veux zoomer sur un aspect.",
        ],
        "next_steps": [
            "Corrige ambiguities dans ton outil de diagramme (Mermaid, Excalidraw…).",
            "Partage summary + flows à l'équipe pour validation.",
            "Exporte en doc d'archi si diagram_type = architecture.",
        ],
    },
    "ocr": {
        "how_to": [
            "Upload photo ou scan lisible (facture, slide, formulaire, tableau).",
            "Indique doc_type si tu le connais pour de meilleurs champs structurés.",
        ],
        "next_steps": [
            "Vérifie extracted_text contre l'original — confidence < 0.8 = relecture humaine.",
            "Copie structured_fields dans ton CRM / tableur / Notion.",
            "Rephotographie illegible_parts si besoin.",
        ],
    },
    "a11y": {
        "how_to": [
            "Upload capture de l'écran à auditer (état focus/hover si pertinent).",
            "Indique le niveau WCAG visé (AA recommandé).",
        ],
        "next_steps": [
            "Implémente priority_fixes dans l'ordre.",
            "Valide avec axe DevTools ou Lighthouse en complément.",
            "Re-audite après correctifs — l'audit visuel ne couvre pas tout.",
        ],
    },
    "mockup": {
        "how_to": [
            "Upload mockup haute-fidélité (landing, app screen, ad creative).",
            "Précise audience et objectif (signup, achat, lecture…).",
        ],
        "next_steps": [
            "Applique copy_improvements sur le design.",
            "Vérifie cta_effectiveness — A/B test si score < 70.",
            "Aligne brand_consistency_notes avec ta charte graphique.",
        ],
    },
    "wireframe": {
        "how_to": [
            "Upload wireframe basse ou moyenne fidélité (Figma export, photo tableau blanc).",
            "Précise le persona et le parcours attendu.",
        ],
        "next_steps": [
            "Ajoute missing_elements et next_screens_to_add au flow.",
            "Intègre copy_suggestions avant de passer en hi-fi.",
            "Re-teste friction_points avec 1 utilisateur.",
        ],
    },
    "router": {
        "how_to": [
            "Colle un message utilisateur ambigu ou réel de ton app.",
            "Plusieurs intents mélangés = bon cas de test.",
        ],
        "next_steps": [
            "Si ambiguous → pose clarifying_question à l'utilisateur.",
            "Branche suggested_mode sur le bon agent Bureau ou handler.",
            "Collecte les erreurs de routing pour affiner ton regex/ML.",
        ],
    },
    "eval": {
        "how_to": [
            "Colle le critère d'évaluation + sortie A + sortie B (même prompt).",
            "Sois explicite sur ce qui compte (précision, ton, longueur…).",
        ],
        "next_steps": [
            "Retiens le winner pour ton pipeline ou ton prompt.",
            "Applique improvement_* à la sortie perdante et re-teste.",
            "Exporte criteria_scores pour ton benchmark.",
        ],
    },
    "review": {
        "how_to": [
            "Colle un `git diff`, un extrait de fichier ou un PR (idéalement < 500 lignes).",
            "Indique le langage ou le framework si ce n'est pas évident dans le code.",
        ],
        "next_steps": [
            "Corrige d'abord tout ce qui est marqué critical.",
            "Applique les fix suggérés dans ton IDE, puis relance Bureau Review.",
            "Si verdict rewrite → enchaîne avec Devstral Lab Refactor.",
            "Merge seulement quand le verdict est ship ou fix_first résolu.",
        ],
    },
    "fix": {
        "how_to": [
            "Colle la stack trace complète + le fichier/fonction concerné.",
            "Ajoute ce que tu as déjà essayé (optionnel mais utile).",
        ],
        "next_steps": [
            "Applique le patch ou suis fix_steps dans l'ordre.",
            "Relance ton test ou ta commande qui plantait.",
            "Si confidence < 0.7 → vérifie manuellement avant de déployer.",
            "Garde prevention en commentaire ou dans un test de non-régression.",
        ],
    },
}


def get_guide(agent_id: str) -> dict[str, list[str]]:
    return GUIDES.get(agent_id, {"how_to": ["Colle ton input", "Clique Run"], "next_steps": ["Itère"]})