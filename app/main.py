"""
EcoSortApp - Interface principale (version intégrée)
"""

import sys
import tempfile
from pathlib import Path

import requests
import streamlit as st

# --- Imports des modules des autres dossiers ---
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "model"))
sys.path.append(str(BASE_DIR / "scraper"))

from src.predict import predict_image
from src.upstream_filters import classify_before_image_model
from code_scraper import scrap_jumia

from utils import get_category_style, render_result_card, inject_custom_css
# Convertit les codes du modèle IA (français, majuscules) vers les codes UI (utils.py)
BIN_CODE_MAPPING = {
    "JAUNE": "jaune",
    "VERTE": "vert",
    "BLEUE": "bleu",
    "MARRON": "marron",
    "D3E": "gris",
    "INCERTAIN": "marron",
}

# ------------------------------------------------------------------
# CONFIGURATION DE LA PAGE
# ------------------------------------------------------------------
st.set_page_config(
    page_title="EcoSortApp — Tri sélectif intelligent",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.markdown(inject_custom_css(), unsafe_allow_html=True)


# ------------------------------------------------------------------
# ÉTAT DE SESSION
# ------------------------------------------------------------------
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "prediction" not in st.session_state:
    st.session_state.prediction = None


# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ♻️ EcoSortApp")
    st.markdown("---")
    st.markdown("""
    **Comment ça marche ?**
    1. Recherchez un produit
    2. Sélectionnez-le dans les résultats Jumia
    3. L'IA analyse et indique la bonne poubelle
    """)
    st.markdown("---")
    st.caption("Projet ENSEA — ISE2 — 2025/2026")


# ------------------------------------------------------------------
# EN-TÊTE
# ------------------------------------------------------------------
st.markdown('<p class="app-title">♻️ EcoSortApp</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Recherchez un produit, l\'IA vous indique la bonne poubelle.</p>',
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# BARRE DE RECHERCHE
# ------------------------------------------------------------------
col1, col2 = st.columns([4, 1])
with col1:
    keyword = st.text_input(
        "Recherche", placeholder="Ex : shampooing, smartphone...",
        label_visibility="collapsed",
    )
with col2:
    search_clicked = st.button("🔍 Rechercher", use_container_width=True)

if search_clicked and keyword.strip():
    with st.spinner("Recherche des produits sur Jumia..."):
        st.session_state.search_results = scrap_jumia(keyword.strip(), max_results=5)
        st.session_state.selected_product = None
        st.session_state.prediction = None
    if not st.session_state.search_results:
        st.error("Aucun résultat trouvé, ou le site Jumia est momentanément inaccessible.")
elif search_clicked and not keyword.strip():
    st.warning("Merci de saisir un nom de produit avant de rechercher.")


# ------------------------------------------------------------------
# AFFICHAGE DES RÉSULTATS
# ------------------------------------------------------------------
if st.session_state.search_results:
    st.markdown("### 📦 Résultats trouvés")
    st.caption(f"{len(st.session_state.search_results)} produit(s) — sélectionnez celui à analyser")

    for idx, product in enumerate(st.session_state.search_results):
        with st.container():
            c1, c2, c3 = st.columns([1, 3, 1])
            with c1:
                if product.get("image"):
                    st.image(product["image"], width=80)
            with c2:
                st.markdown(f"**{product['nom']}**")
                st.caption(f"{product['prix']} — {product['note']}")
            with c3:
                if st.button("Choisir", key=f"select_{idx}"):
                    st.session_state.selected_product = product
                    st.session_state.prediction = None
        st.divider()


# ------------------------------------------------------------------
# ANALYSE DU PRODUIT SÉLECTIONNÉ
# ------------------------------------------------------------------
if st.session_state.selected_product:
    st.markdown("### 🔬 Produit sélectionné")
    prod = st.session_state.selected_product

    c1, c2 = st.columns([1, 3])
    with c1:
        if prod.get("image"):
            st.image(prod["image"], width=120)
    with c2:
        st.markdown(f"**{prod['nom']}**")
        st.caption(prod["prix"])

    if st.button("♻️ Analyser et trouver la poubelle", type="primary"):
        with st.spinner("Analyse en cours..."):
            filtre = classify_before_image_model(
                prod["nom"], prod.get("categorie", "")
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
                    img_data = requests.get(prod["image"], timeout=10).content
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                        tmp.write(img_data)
                        tmp_path = tmp.name

                    result = predict_image(tmp_path)
                    code_normalise = BIN_CODE_MAPPING.get(result["poubelle"], "marron")

                    if result["poubelle"] == "INCERTAIN":
                        st.session_state.prediction = {
                            "code": "marron",
                            "label": "Incertain",
                            "matiere": f"Confiance trop faible ({result['confiance']*100:.0f}%), classification manuelle recommandée",
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
                    st.error(f"Impossible d'analyser l'image de ce produit : {e}")
                    st.session_state.prediction = None
    if st.session_state.prediction:
        pred = st.session_state.prediction
        style = get_category_style(pred.get("code", pred.get("poubelle", "marron")))
        st.markdown(
            render_result_card(
                couleur_hex=style["bg"],
                texte_hex=style["text"],
                emoji=style["emoji"],
                label=pred.get("label", pred.get("poubelle", "Inconnu")),
                matiere=pred.get("matiere", ""),
                confiance=pred.get("confiance", pred.get("confidence", 0)),
            ),
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------------
# ÉTAT VIDE
# ------------------------------------------------------------------
if not st.session_state.search_results and not search_clicked:
    st.info("👆 Commencez par rechercher un produit ci-dessus.")