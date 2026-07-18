"""
EcoSortApp - Interface principale (design vert/crème, style Lovable)
"""

import base64
import sys
import tempfile
from pathlib import Path
from PIL import Image
import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "model"))
sys.path.append(str(BASE_DIR / "scraper"))

from src.predict import predict_image
from src.upstream_filters import classify_before_image_model
from code_scraper import scrap_jumia

from utils import (
    get_category_style, render_result_card, render_category_grid,
    inject_custom_css, render_navbar, render_impact_section,
    render_co2_card, render_team_section
)

BIN_CODE_MAPPING = {
    "JAUNE": "jaune", "VERTE": "vert", "BLEUE": "bleu",
    "MARRON": "marron", "D3E": "gris", "INCERTAIN": "marron",
}


# ============================================================
# FONCTION UTILITAIRE (doit etre definie avant tout appel)
# ============================================================
def get_base64_image(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


# --- CONFIGURATION DE LA PAGE ---
logo_icon_path = BASE_DIR / "app" / "assets" / "logo.png"
try:
    page_icon_img = Image.open(logo_icon_path)
except FileNotFoundError:
    page_icon_img = "♻️"

st.set_page_config(
    page_title="EcoSortApp — Le bon geste, en un instant",
    page_icon=page_icon_img,
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(inject_custom_css(), unsafe_allow_html=True)


# --- ÉTAT DE SESSION ---
for key in ["search_results", "selected_product", "prediction"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "search_results" else None


# ============================================================
# DIALOG D'ANALYSE (popup modale, evite le scroll)
# ============================================================
@st.dialog("🔬 Analyser ce produit")
def show_analysis_dialog(prod):
    c1, c2 = st.columns([1, 2])
    with c1:
        if prod.get("image"):
            st.image(prod["image"], width=100)
        elif prod.get("image_bytes"):
            st.image(prod["image_bytes"], width=100)
    with c2:
        st.markdown(f"**{prod['nom']}**")
        if prod.get("prix"):
            st.caption(prod["prix"])

    if st.button("♻️ Analyser et trouver la poubelle", type="primary", use_container_width=True):
        with st.spinner("Analyse en cours..."):
            filtre = classify_before_image_model(
                 prod["nom"],
                 prod.get("categorie", ""),
                 st.session_state.get("kw_input", "")
            )
            if filtre is not None:
                code_normalise = BIN_CODE_MAPPING.get(filtre, "marron")
                st.session_state.prediction = {
                    "code": code_normalise,
                    "label": "Bac Électronique (D3E)" if filtre == "D3E" else "Poubelle Marron/Noire",
                    "matiere": "Détecté via mot-clé produit" if filtre == "D3E" else "Vaisselle / déchet résiduel",
                    "confiance": 1.0,
                }
            else:
                try:
                    if prod.get("image_bytes"):
                        img_bytes = prod["image_bytes"]
                    else:
                        img_bytes = requests.get(prod["image"], timeout=10).content

                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                        tmp.write(img_bytes)
                        tmp_path = tmp.name

                    result = predict_image(tmp_path)
                    code_normalise = BIN_CODE_MAPPING.get(result["poubelle"], "marron")

                    if result["poubelle"] == "INCERTAIN":
                        st.session_state.prediction = {
                            "code": "marron", "label": "Incertain",
                            "matiere": f"Confiance trop faible ({result['confiance']*100:.0f}%)",
                            "confiance": result["confiance"],
                        }
                    else:
                        st.session_state.prediction = {
                            "code": code_normalise,
                            "label": result["poubelle"].capitalize(),
                            "matiere": f"Classe détectée : {result['classe']}",
                            "confiance": result["confiance"],
                        }
                except Exception as e:
                    st.error(f"Impossible d'analyser l'image : {e}")
                    st.session_state.prediction = None

    if st.session_state.prediction:
        pred = st.session_state.prediction
        style = get_category_style(pred["code"])
        st.markdown(
            render_result_card(style["bg"], style["text"], style["emoji"],
                                pred["label"], pred["matiere"], pred["confiance"]),
            unsafe_allow_html=True,
        )

        st.markdown(render_co2_card(pred["code"]), unsafe_allow_html=True)

        with st.expander("🧠 Pourquoi cette poubelle ?"):
            st.write(f"**Poubelle recommandée :** {pred['label']}")
            st.write(f"**Détail :** {pred['matiere']}")
            st.write(f"**Confiance du modèle :** {pred['confiance'] * 100:.0f}%")
            st.caption(
                "Le modèle utilise un seuil de confiance de 60% : en dessous, "
                "le résultat est marqué comme incertain plutôt que d'imposer "
                "une réponse potentiellement fausse."
            )

        texte_partage = (
            f"♻️ EcoSortApp - Résultat d'analyse\n"
            f"Poubelle : {pred['label']}\n"
            f"Détail : {pred['matiere']}\n"
            f"Confiance : {pred['confiance'] * 100:.0f}%\n"
            f"Analysé via EcoSortApp"
        )
        st.text_area("📋 Copier le résultat", texte_partage, height=100, key="share_text")


# --- HEADER (logo) ---
logo_path = BASE_DIR / "app" / "assets" / "logo.png"
logo_b64 = get_base64_image(logo_path)

if logo_b64:
    st.markdown(f"""
    <div class="eco-header">
        <img src="data:image/png;base64,{logo_b64}" class="eco-logo-img" />
        <p class="eco-title">EcoSortApp</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="eco-header">
        <div class="eco-logo">♻️</div>
        <p class="eco-title">EcoSortApp</p>
    </div>
    """, unsafe_allow_html=True)

# --- SECTION MEMBRES DU GROUPE (bien visible, juste sous le logo) ---
st.markdown("""
<p class="section-eyebrow">PROJET RÉALISÉ PAR</p>
""", unsafe_allow_html=True)

team_members = [
    {"nom": "Kone Kpelban Augustin", "role": "Interface & Containerisation", "photo_file": "team1.jpg.jpeg"},
    {"nom": "Ranaivomanana Angelo", "role": "Scraping Jumia", "photo_file": "team2.jpg.jpeg"},
    {"nom": "Bouiti Banza Olivier", "role": "Modèle IA / Deep Learning", "photo_file": "team3.jpg.jpeg"},
]

for member in team_members:
    photo_path = BASE_DIR / "app" / "assets" / member["photo_file"]
    member["photo_b64"] = get_base64_image(photo_path)

st.markdown(render_team_section(team_members), unsafe_allow_html=True)

# --- NAVBAR ---
st.markdown(render_navbar(), unsafe_allow_html=True)

# --- HERO ---
st.markdown('<div class="hero-zone">', unsafe_allow_html=True)
st.markdown("""
<div class="hero-badge fade-in">🟢 Classification par intelligence artificielle</div>
<p class="hero-title fade-in fade-in-delay-1">Le bon geste,<span class="hero-title-italic">en un instant.</span></p>
<p class="hero-subtitle fade-in fade-in-delay-2">Recherchez un produit, prenez une photo ou importez une image. L'IA vous indique la poubelle exacte.</p>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- IMAGE HERO (bouteille, animee) ---
hero_img_path = BASE_DIR / "app" / "assets" / "hero-bouteille.jpg"
hero_b64 = get_base64_image(hero_img_path)
if hero_b64:
    st.markdown(f"""
    <div class="hero-image-wrapper">
        <img src="data:image/jpeg;base64,{hero_b64}" class="hero-image-float" />
    </div>
    """, unsafe_allow_html=True)

# --- SECTION ANALYSE ---
st.markdown("""
<p class="section-eyebrow">ANALYSE</p>
<p class="section-title">Choisissez votre <span class="section-title-italic">méthode</span></p>
""", unsafe_allow_html=True)

tab_recherche, tab_photo, tab_import = st.tabs(["🔍 Rechercher", "📷 Photo", "⬆️ Importer"])

# ============================================================
# TAB 1 — RECHERCHE PAR MOT-CLÉ (scraping Jumia)
# ============================================================
with tab_recherche:
    col1, col2 = st.columns([4, 1])
    with col1:
        keyword = st.text_input(
            "Recherche", placeholder="ex : bouteille d'eau, smartphone, journal...",
            label_visibility="collapsed", key="kw_input"
        )
    with col2:
        search_clicked = st.button("✨ Analyser", use_container_width=True, key="btn_search")

    if search_clicked and keyword.strip():
        with st.spinner("Recherche des produits sur Jumia..."):
            st.session_state.search_results = scrap_jumia(keyword.strip(), max_results=5)
            st.session_state.selected_product = None
            st.session_state.prediction = None
        if not st.session_state.search_results:
            st.error("Aucun résultat trouvé, ou Jumia est momentanément inaccessible.")
    elif search_clicked and not keyword.strip():
        st.warning("Merci de saisir un nom de produit.")

    if st.session_state.search_results:
        st.markdown("#### 📦 Résultats trouvés")
        for idx, product in enumerate(st.session_state.search_results):
            with st.container():
                st.markdown('<div class="product-row">', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1, 3, 1])
                with c1:
                    if product.get("image"):
                        st.image(product["image"], width=70)
                with c2:
                    st.markdown(f"**{product['nom']}**")
                    st.caption(f"{product['prix']} — {product.get('note', '')}")
                with c3:
                    if st.button("Choisir", key=f"select_{idx}"):
                        st.session_state.selected_product = product
                        st.session_state.prediction = None
                        show_analysis_dialog(product)
                st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 2 — PHOTO (webcam en direct)
# ============================================================
with tab_photo:
    st.markdown("Prenez une photo du produit avec votre caméra.")
    photo = st.camera_input("Prendre une photo", label_visibility="collapsed", key="cam_input")
    if photo is not None:
        prod = {
            "nom": "Produit photographié",
            "prix": "",
            "note": "",
            "image_bytes": photo.getvalue(),
            "image": None,
            "categorie": "",
        }
        st.session_state.selected_product = prod
        st.session_state.prediction = None
        show_analysis_dialog(prod)

# ============================================================
# TAB 3 — IMPORTER UNE IMAGE
# ============================================================
with tab_import:
    st.markdown("Importez une image depuis votre appareil.")
    uploaded = st.file_uploader("Importer une image", type=["jpg", "jpeg", "png"],
                                 label_visibility="collapsed", key="upload_input")
    if uploaded is not None:
        prod = {
            "nom": "Image importée",
            "prix": "",
            "note": "",
            "image_bytes": uploaded.getvalue(),
            "image": None,
            "categorie": "",
        }
        st.session_state.selected_product = prod
        st.session_state.prediction = None
        show_analysis_dialog(prod)

# --- SECTION IMPACT / UTILITE DU RECYCLAGE ---
st.markdown(render_impact_section(), unsafe_allow_html=True)

# --- SECTION RÉFÉRENTIEL (5 catégories) ---
st.markdown("""
<p class="section-eyebrow">RÉFÉRENTIEL</p>
<p class="section-title">Cinq poubelles.<span class="section-title-italic"> Une décision claire.</span></p>
""", unsafe_allow_html=True)

poubelles_img_path = BASE_DIR / "app" / "assets" / "poubelles.jpg"
poubelles_b64 = get_base64_image(poubelles_img_path)
if poubelles_b64:
    st.markdown(f"""
    <div class="hero-image-wrapper">
        <img src="data:image/jpeg;base64,{poubelles_b64}" style="width:100%; display:block;" />
    </div>
    """, unsafe_allow_html=True)

st.markdown(render_category_grid(), unsafe_allow_html=True)
