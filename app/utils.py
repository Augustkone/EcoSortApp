"""
Fonctions utilitaires : styles, couleurs, CSS global (design EcoSortApp).
"""

CATEGORY_COLORS = {
    "jaune":  {"bg": "#E8B923", "text": "#FFFFFF", "emoji": "♻️", "label": "Jaune", "desc": "Plastique · Métal · Carton"},
    "vert":   {"bg": "#4A7C3C", "text": "#FFFFFF", "emoji": "♻️", "label": "Verte", "desc": "Verre d'emballage"},
    "bleu":   {"bg": "#2F6FB8", "text": "#FFFFFF", "emoji": "♻️", "label": "Bleue", "desc": "Papier · Journaux"},
    "gris":   {"bg": "#5B6470", "text": "#FFFFFF", "emoji": "♻️", "label": "Grise", "desc": "Électronique · Piles"},
    "marron": {"bg": "#5C4632", "text": "#FFFFFF", "emoji": "♻️", "label": "Marron", "desc": "Non recyclable"},
}

CO2_IMPACT = {
    "jaune":  {"co2": 45, "texte": "évitez la production de nouveau plastique/métal"},
    "vert":   {"co2": 30, "texte": "économisez l'énergie de fusion du verre neuf"},
    "bleu":   {"co2": 20, "texte": "sauvez l'équivalent de ressources forestières"},
    "gris":   {"co2": 85, "texte": "évitez la pollution de métaux lourds au sol"},
    "marron": {"co2": 5,  "texte": "assurez un traitement adapté aux déchets résiduels"},
}


def get_category_style(code: str) -> dict:
    return CATEGORY_COLORS.get(code, CATEGORY_COLORS["marron"])


def render_result_card(couleur_hex, texte_hex, emoji, label, matiere, confiance) -> str:
    return (
        f'<div class="result-card" style="background-color:{couleur_hex}; color:{texte_hex};">'
        f'<div class="result-emoji">{emoji}</div>'
        f'<div class="result-label">{label}</div>'
        f'<div class="result-matiere">{matiere}</div>'
        f'<div class="result-confiance">Confiance : {confiance * 100:.0f}%</div>'
        f'</div>'
    )


def render_category_grid() -> str:
    cards = ""
    for code, info in CATEGORY_COLORS.items():
        cards += (
            f'<div class="cat-card">'
            f'<div class="cat-icon" style="background-color:{info["bg"]};">♻️</div>'
            f'<div class="cat-title">{info["label"]}</div>'
            f'<div class="cat-desc">{info["desc"]}</div>'
            f'</div>'
        )
    return f'<div class="cat-grid">{cards}</div>'


def render_navbar() -> str:
    return (
        '<div class="eco-navbar fade-in">'
        '<div class="eco-nav-links">'
        '<span>Analyser</span>'
        '<span>Catégories</span>'
        '<span>À propos</span>'
        '</div>'
        '<span class="eco-nav-cta">EcoSortApp</span>'
        '</div>'
    )


def render_impact_section() -> str:
    return (
        '<div class="impact-section fade-in">'
        '<div class="impact-title">Pourquoi trier compte vraiment</div>'
        '<div class="impact-subtitle">Chaque geste de tri a un impact concret, mesurable, immédiat.</div>'
        '<div class="impact-grid">'
        '<div class="impact-stat"><span class="impact-number">70%</span>'
        '<span class="impact-label">d\'énergie économisée en recyclant l\'aluminium plutôt qu\'en le produisant</span></div>'
        '<div class="impact-stat"><span class="impact-number">1000 ans</span>'
        '<span class="impact-label">le temps qu\'une bouteille plastique met à se dégrader dans la nature</span></div>'
        '<div class="impact-stat"><span class="impact-number">17</span>'
        '<span class="impact-label">arbres sauvés par tonne de papier recyclé au lieu d\'être jeté</span></div>'
        '</div>'
        '</div>'
    )
def render_co2_card(code: str) -> str:
    data = CO2_IMPACT.get(code, CO2_IMPACT["marron"])
    return (
        '<div class="co2-card">'
        f'<div class="co2-icon">🌍</div>'
        f'<div class="co2-number">-{data["co2"]}g CO2</div>'
        f'<div class="co2-text">En triant ce produit, vous {data["texte"]}.</div>'
        '</div>'
    )
def render_team_section(members: list) -> str:
    cards = ""
    for m in members:
        photo_tag = (
            f'<img src="data:image/jpeg;base64,{m["photo_b64"]}" class="team-photo" />'
            if m.get("photo_b64")
            else '<div class="team-photo-placeholder">👤</div>'
        )
        cards += (
            '<div class="team-card">'
            f'{photo_tag}'
            f'<div class="team-name">{m["nom"]}</div>'
            f'<div class="team-role">{m["role"]}</div>'
            '</div>'
        )
    return f'<div class="team-grid">{cards}</div>'


def inject_custom_css() -> str:
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Playfair+Display:ital@1&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background: linear-gradient(160deg, #DCEBD1 0%, #E9F3DE 30%, #F3F8EA 60%, #FBFCF6 100%);
            background-attachment: fixed;
        }

        /* --- HEADER --- */
        .eco-header {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 0 6px 0;
        }
        .eco-logo {
            width: 44px; height: 44px;
            background: linear-gradient(145deg, #1b5e20, #4CAF50);
            border-radius: 14px;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px;
            box-shadow: 0 4px 14px rgba(27,94,32,0.35);
            border: 1px solid rgba(255,255,255,0.15);
        }
        .eco-logo-img {
            width: 44px; height: 44px;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(27,94,32,0.35);
        }
        .eco-title { font-size: 22px; font-weight: 800; color: #14301A; margin:0; }

        /* --- NAVBAR --- */
        .eco-navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 0;
            margin-bottom: 10px;
            border-bottom: 1px solid rgba(27,94,32,0.12);
        }
        .eco-nav-links {
            display: flex;
            gap: 28px;
        }
        .eco-nav-links span {
            color: #4b5b45;
            font-weight: 600;
            font-size: 15px;
            cursor: default;
        }
        .eco-nav-cta {
            background: linear-gradient(145deg, #1b5e20, #2E7D32);
            color: white !important;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 13px;
        }
        @media (max-width: 640px) {
            .eco-nav-links { display: none; }
        }

        /* --- HERO ZONE --- */
        .hero-zone {
            background: radial-gradient(ellipse at top left, #C8E6B8 0%, transparent 60%),
                        radial-gradient(ellipse at bottom right, #A8D89A 0%, transparent 55%);
            border-radius: 28px;
            padding: 24px;
            margin-bottom: 10px;
        }
        .hero-badge {
            display: inline-flex; align-items: center; gap: 6px;
            background: #ffffffcc; padding: 6px 14px; border-radius: 20px;
            font-size: 13px; color: #345c2c; margin-bottom: 18px;
            border: 1px solid #d8e8cd;
        }
        .hero-title {
            font-size: clamp(32px, 6vw, 52px);
            font-weight: 800;
            color: #142B18;
            line-height: 1.1;
            margin: 0;
        }
        .hero-title-italic {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            color: #2E7D32;
            display: block;
        }
        .hero-subtitle {
            color: #4b5b45; font-size: 16px; max-width: 480px;
            margin: 18px 0 10px 0; line-height: 1.5;
        }

        /* --- Image hero flottante --- */
        .hero-image-wrapper {
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 12px 32px rgba(20, 60, 20, 0.18);
            margin: 8px 0 28px 0;
            position: relative;
        }
        .hero-image-wrapper::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, transparent 60%, rgba(0,30,0,0.25) 100%);
            pointer-events: none;
        }
        .hero-image-float {
            width: 100%;
            display: block;
            animation: floatSideways 6s ease-in-out infinite;
        }
        @keyframes floatSideways {
            0%   { transform: translateX(0) scale(1.05); }
            25%  { transform: translateX(-2.5%) scale(1.07); }
            50%  { transform: translateX(0) scale(1.05); }
            75%  { transform: translateX(2.5%) scale(1.07); }
            100% { transform: translateX(0) scale(1.05); }
        }

        /* --- SECTION TITLES --- */
        .section-eyebrow {
            color: #2E7D32; font-weight: 700; font-size: 13px;
            letter-spacing: 1.5px; text-transform: uppercase;
        }
        .section-title {
            font-size: clamp(26px, 4vw, 36px); font-weight: 800; color: #14301A;
            margin: 6px 0 10px 0;
        }
        .section-title-italic {
            font-family: 'Playfair Display', serif; font-style: italic; color: #2E7D32;
        }

        /* --- Fade-in --- */
        .fade-in {
            animation: fadeInUp 0.8s ease both;
        }
        .fade-in-delay-1 { animation-delay: 0.1s; }
        .fade-in-delay-2 { animation-delay: 0.25s; }
        .fade-in-delay-3 { animation-delay: 0.4s; }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(16px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* --- CARDS catégories --- */
        .cat-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 20px;
        }
        @media (max-width: 640px) {
            .cat-grid { grid-template-columns: 1fr; }
        }
        .cat-card {
            background: #ffffff; border-radius: 18px; padding: 22px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        .cat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 24px rgba(0,0,0,0.10);
        }
        .cat-icon {
            width: 46px; height: 46px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            color: white; font-size: 20px; margin-bottom: 14px;
        }
        .cat-title { font-weight: 700; font-size: 18px; color: #142B18; }
        .cat-desc { color: #6b7566; font-size: 14px; margin-top: 4px; }

        /* --- Résultat produit --- */
        .result-card {
            border-radius: 20px; padding: 30px; text-align: center;
            margin-top: 18px; box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        .result-emoji { font-size: 46px; }
        .result-label { font-size: 24px; font-weight: 800; margin-top: 6px; }
        .result-matiere { font-size: 14px; opacity: 0.9; margin-top: 4px; }
        .result-confiance { font-size: 12px; opacity: 0.75; margin-top: 10px; }

        /* --- Section impact / utilite du recyclage --- */
        .impact-section {
            background: linear-gradient(135deg, #1b5e20, #2E7D32);
            border-radius: 24px;
            padding: 36px 28px;
            margin: 30px 0;
            color: white;
        }
        .impact-title {
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 6px;
        }
        .impact-subtitle {
            font-size: 14px;
            opacity: 0.85;
            margin-bottom: 22px;
        }
        .impact-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }
        @media (max-width: 640px) {
            .impact-grid { grid-template-columns: 1fr; }
        }
        .impact-stat {
            background: rgba(255,255,255,0.12);
            border-radius: 16px;
            padding: 18px;
            text-align: center;
            backdrop-filter: blur(4px);
        }
        .impact-number {
            font-size: 28px;
            font-weight: 800;
            display: block;
        }
        .impact-label {
            font-size: 12.5px;
            opacity: 0.85;
            margin-top: 4px;
        }

        /* --- Boutons Streamlit --- */
        div[data-testid="stButton"] button {
            border-radius: 24px !important;
            font-weight: 700 !important;
            background: linear-gradient(145deg, #1b5e20, #2E7D32) !important;
            color: white !important;
            border: none !important;
            padding: 10px 22px !important;
        }
        div[data-testid="stButton"] button:hover {
            background: linear-gradient(145deg, #164a1a, #256b2a) !important;
        }

        /* --- Tabs --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px; background: #ffffff; border-radius: 16px; padding: 6px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 12px; font-weight: 600; color: #4b5b45;
        }
        .stTabs [aria-selected="true"] {
            background: #E7F2E1 !important; color: #1b5e20 !important;
        }

        /* --- Champs texte --- */
        div[data-testid="stTextInput"] input {
            border-radius: 24px !important; padding: 12px 18px !important;
            border: 1px solid #d8e8cd !important;
        }

        /* --- Cartes produit résultats --- */
        .product-row {
            background: white; border-radius: 14px; padding: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 10px;
        }

        /* --- Habillage caméra --- */
        div[data-testid="stCameraInput"] {
            border-radius: 20px;
            overflow: hidden;
            border: 2px solid #d8e8cd;
            background: #ffffff;
        }
        div[data-testid="stCameraInput"] button {
            border-radius: 24px !important;
            background: linear-gradient(145deg, #1b5e20, #2E7D32) !important;
            color: white !important;
        }

        /* --- Habillage file uploader --- */
        div[data-testid="stFileUploaderDropzone"] {
            border-radius: 16px !important;
            border: 2px dashed #a8cf9a !important;
            background: #F4F9EF !important;
        }

        /* --- Images illustratives --- */
        div[data-testid="stImage"] img {
            border-radius: 20px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        }
        /* --- Carte impact CO2 --- */
        .co2-card {
            background: linear-gradient(135deg, #EAF6E4, #F7FBF3);
            border: 1px solid #cfe8c2;
            border-radius: 16px;
            padding: 18px 20px;
            margin-top: 12px;
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .co2-icon { font-size: 28px; }
        .co2-number {
            font-size: 18px;
            font-weight: 800;
            color: #1b5e20;
            white-space: nowrap;
        }
        .co2-text {
            font-size: 13.5px;
            color: #3d5a38;
            line-height: 1.4;
        }

        /* --- Section equipe --- */
        .team-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 16px;
        }
        @media (max-width: 640px) {
            .team-grid { grid-template-columns: 1fr; }
        }
        .team-card {
            background: white;
            border-radius: 18px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .team-photo {
            width: 80px; height: 80px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 12px;
            border: 3px solid #A8D89A;
        }
        .team-photo-placeholder {
            width: 80px; height: 80px;
            border-radius: 50%;
            background: #E7F2E1;
            display: flex; align-items: center; justify-content: center;
            font-size: 32px;
            margin: 0 auto 12px auto;
        }
        .team-name { font-weight: 700; font-size: 16px; color: #142B18; }
        .team-role { font-size: 13px; color: #6b7566; margin-top: 4px; }
    </style>
    """