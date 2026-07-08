"""
EcoSortApp - Interface principale
Application Streamlit permettant à un utilisateur de rechercher un produit
sur Jumia, puis d'obtenir sa consigne de tri sélectif via un modèle CNN.
"""

import streamlit as st
from mocks import search_jumia, predict_category
from utils import get_category_style, render_result_card, inject_custom_css


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
# ÉTAT DE SESSION (pour garder les résultats entre les interactions)
# ------------------------------------------------------------------
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "prediction" not in st.session_state:
    st.session_state.prediction = None


# ------------------------------------------------------------------
# SIDEBAR — infos projet
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
    st.markdown("#### 🗂️ Légende des catégories")
    for code, info in {
        "jaune": "Plastique / Métal / Carton",
        "vert": "Verre",
        "bleu": "Papier",
        "gris": "Électronique (D3E)",
        "marron": "Déchet résiduel",
    }.items():
        style = get_category_style(code)
        st.markdown(
            f"<span style='background-color:{style['bg']}; color:{style['text']}; "
            f"padding:4px 10px; border-radius:6px; font-size:13px;'>"
            f"{style['emoji']} {info}</span>",
            unsafe_allow_html=True,
        )
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
        "Recherche",
        placeholder="Ex : shampooing, bouteille, smartphone...",
        label_visibility="collapsed",
    )
with col2:
    search_clicked = st.button("🔍 Rechercher", use_container_width=True)

if search_clicked and keyword.strip():
    with st.spinner("Recherche des produits sur Jumia..."):
        st.session_state.search_results = search_jumia(keyword.strip())
        st.session_state.selected_product = None
        st.session_state.prediction = None
elif search_clicked and not keyword.strip():
    st.warning("Merci de saisir un nom de produit avant de rechercher.")


# ------------------------------------------------------------------
# AFFICHAGE DES RÉSULTATS DE RECHERCHE
# ------------------------------------------------------------------
if st.session_state.search_results:
    st.markdown("### 📦 Résultats trouvés")
    st.caption(f"{len(st.session_state.search_results)} produit(s) — sélectionnez celui à analyser")

    for idx, product in enumerate(st.session_state.search_results):
        with st.container():
            c1, c2, c3 = st.columns([1, 3, 1])
            with c1:
                st.image(product["image_url"], width=80)
            with c2:
                st.markdown(f"**{product['titre']}**")
                st.caption(product["prix"])
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
        st.image(prod["image_url"], width=120)
    with c2:
        st.markdown(f"**{prod['titre']}**")
        st.caption(prod["prix"])

    if st.button("♻️ Analyser et trouver la poubelle", type="primary"):
        with st.spinner("Analyse de l'emballage par le modèle IA..."):
            st.session_state.prediction = predict_category(prod["image_url"])

    if st.session_state.prediction:
        pred = st.session_state.prediction
        style = get_category_style(pred["code"])
        st.markdown(
            render_result_card(
                couleur_hex=style["bg"],
                texte_hex=style["text"],
                emoji=style["emoji"],
                label=pred["label"],
                matiere=pred["matiere"],
                confiance=pred["confiance"],
            ),
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------------
# ÉTAT VIDE (aucune recherche encore effectuée)
# ------------------------------------------------------------------
if not st.session_state.search_results and not search_clicked:
    st.info("👆 Commencez par rechercher un produit ci-dessus.")