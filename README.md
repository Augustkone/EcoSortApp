# ♻️ EcoSortApp

Application web d'aide au tri sélectif pour les citoyens ivoiriens. L'utilisateur recherche un produit, prend une photo ou importe une image, et l'application lui indique la poubelle exacte à utiliser grâce à un modèle de deep learning combiné à un scraping en direct de Jumia.

Projet réalisé dans le cadre du module de Deep Learning & Développement Web — ENSEA, ISE2A.

---

## 🎯 Fonctionnalités

- **Recherche de produit** : scraping en direct de Jumia à partir d'un mot-clé
- **Prise de photo** : analyse directe via la caméra de l'appareil
- **Import d'image** : analyse d'une image déjà présente sur l'appareil
- **Classification automatique** : modèle CNN (Transfer Learning MobileNetV2) entraîné sur le dataset Garbage Classification (Kaggle)
- **Filtres intelligents** : détection en amont des produits électroniques (D3E) et de la vaisselle, via mots-clés, avant même d'appeler le modèle d'image
- **Impact environnemental** : estimation illustrative du CO2 évité par geste de tri
- **Explication du raisonnement** : transparence sur la classe détectée et le niveau de confiance du modèle

---

## 🏷️ Catégories de tri

| Poubelle | Couleur | Contenu |
|---|---|---|
| Jaune | 🟡 | Plastique, métal, carton |
| Verte | 🟢 | Verre d'emballage |
| Bleue | 🔵 | Papier, journaux |
| Grise | ⚫ | Électronique (D3E), piles |
| Marron | 🟤 | Déchets résiduels non recyclables |

---

## 🏗️ Architecture du projet
