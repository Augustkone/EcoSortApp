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


def inject_custom_css() -> str:
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Playfair+Display:ital@1&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background: linear-gradient(180deg, #EAF3E3 0%, #F7F9F2 40%, #FDFDF8 100%);
        }

        /* --- HEADER --- */
        .eco-header {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 0 20px 0;
        }
        .eco-logo {
            width: 42px; height: 42px;
            background: linear-gradient(145deg, #1b5e20, #66bb6a);
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px;
            box-shadow: 0 4px 10px rgba(27,94,32,0.3);
        }
        .eco-title { font-size: 22px; font-weight: 800; color: #14301A; margin:0; }

        /* --- HERO --- */
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
            margin: 18px 0 26px 0; line-height: 1.5;
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

        /* --- CARDS (produits / catégories) --- */
        .cat-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 20px;
        }
        @media (max-width: 640px) {
            .cat-grid { grid-template-columns: 1fr; }
        }
        .cat-card {
            background: #ffffff; border-radius: 18px; padding: 22px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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

        /* --- Logo header plus soigné --- */
        .eco-logo-img {
            width: 42px; height: 42px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(27,94,32,0.3);
        }
        .eco-logo-img {
            width: 44px; height: 44px;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(27,94,32,0.35);
        }
        div[data-testid="stImage"] img {
            border-radius: 20px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        }
    </style>
    """