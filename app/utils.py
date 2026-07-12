"""
Fonctions utilitaires pour l'affichage : couleurs, styles, mise en page.
"""

CATEGORY_COLORS = {
    "jaune":  {"bg": "#FFD93D", "text": "#4A3B00", "emoji": "🟡"},
    "vert":   {"bg": "#4CAF50", "text": "#FFFFFF", "emoji": "🟢"},
    "bleu":   {"bg": "#2196F3", "text": "#FFFFFF", "emoji": "🔵"},
    "gris":   {"bg": "#9E9E9E", "text": "#FFFFFF", "emoji": "🎛️"},
    "marron": {"bg": "#6D4C33", "text": "#FFFFFF", "emoji": "⚫"},
}


def get_category_style(code: str) -> dict:
    """Retourne le style (couleurs, emoji) associé à un code de catégorie."""
    return CATEGORY_COLORS.get(code, CATEGORY_COLORS["marron"])


def render_result_card(couleur_hex: str, texte_hex: str, emoji: str,
                        label: str, matiere: str, confiance: float) -> str:
    """Génère le HTML de la carte de résultat final (couleur de poubelle)."""
    return f"""
    <div style="
        background-color: {couleur_hex};
        color: {texte_hex};
        padding: 32px;
        border-radius: 16px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    ">
        <div style="font-size: 48px;">{emoji}</div>
        <div style="font-size: 24px; font-weight: 700; margin-top: 8px;">{label}</div>
        <div style="font-size: 15px; margin-top: 6px; opacity: 0.9;">{matiere}</div>
        <div style="font-size: 13px; margin-top: 12px; opacity: 0.75;">
            Confiance du modèle : {confiance * 100:.0f}%
        </div>
    </div>
    """


def inject_custom_css():
    """CSS global pour styliser l'application au-delà des composants Streamlit natifs."""
    return """
    <style>
        .main {
            background-color: #F8F9FA;
        }
        .product-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s ease;
            margin-bottom: 12px;
        }
        .product-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        }
        .app-title {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(90deg, #4CAF50, #2196F3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
        }
        .app-subtitle {
            color: #6B7280;
            font-size: 16px;
            margin-top: 0px;
            margin-bottom: 24px;
        }
        div[data-testid="stButton"] button {
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
    """