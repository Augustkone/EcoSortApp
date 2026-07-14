#  EcoSortApp

Application web d'aide au tri sélectif pour les citoyens ivoiriens. L'utilisateur recherche un produit, prend une photo ou importe une image, et l'application lui indique la poubelle exacte à utiliser grâce à un modèle de deep learning combiné à un scraping en direct de Jumia.

Projet réalisé dans le cadre du module de Deep Learning & Développement Web — ENSEA, ISE2A.

---

##  Fonctionnalités

- **Recherche de produit** : scraping en direct de Jumia à partir d'un mot-clé
- **Prise de photo** : analyse directe via la caméra de l'appareil
- **Import d'image** : analyse d'une image déjà présente sur l'appareil
- **Classification automatique** : modèle CNN (Transfer Learning MobileNetV2) entraîné sur le dataset Garbage Classification (Kaggle)
- **Filtres intelligents** : détection en amont des produits électroniques (D3E) et de la vaisselle, via mots-clés, avant même d'appeler le modèle d'image
- **Impact environnemental** : estimation illustrative du CO2 évité par geste de tri
- **Explication du raisonnement** : transparence sur la classe détectée et le niveau de confiance du modèle

---

##  Catégories de tri

| Poubelle | Couleur | Contenu |
|---|---|---|
| Jaune | 🟡 | Plastique, métal, carton |
| Verte | 🟢 | Verre d'emballage |
| Bleue | 🔵 | Papier, journaux |
| Grise | ⚫ | Électronique (D3E), piles |
| Marron | 🟤 | Déchets résiduels non recyclables |

---

##  Architecture du projet
EcoSortApp/
├── app/                    # Interface Streamlit
│   ├── main.py
│   ├── utils.py
│   ├── assets/              # Logo, images illustratives, photos equipe
│   └── requirements.txt
├── model/                  # Entrainement et inference du modele CNN
│   ├── src/
│   │   ├── predict.py
│   │   ├── config.py
│   │   └── upstream_filters.py
│   ├── models/
│   │   ├── modele_eco_sort.h5
│   │   └── class_names.json
│   └── requirements.txt
├── scraper/                 # Scraping Jumia
│   ├── code_scraper.py
│   └── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md

---

##  Lancement avec Docker (recommandé)

Aucune installation manuelle de Python, TensorFlow, ou autre dépendance n'est nécessaire — Docker s'occupe de tout.

```bash
docker build -t ecosortapp .
docker run -p 8501:8501 ecosortapp
```

Puis ouvrir dans le navigateur :
http://localhost:8501

---

## 🧪 Lancement en local (développement)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

pip install -r app/requirements.txt
pip install -r model/requirements.txt
pip install -r scraper/requirements.txt

streamlit run app/main.py
```

---

## 🧠 Modèle de reconnaissance d'image

- **Architecture** : Transfer Learning sur MobileNetV2
- **Dataset** : Garbage Classification (Kaggle) — 6 classes natives (cardboard, glass, metal, paper, plastic, trash)
- **Précision** : ~85% sur le jeu de test
- **Seuil de confiance** : 0.6 — en dessous, le résultat est marqué "incertain" plutôt que d'imposer une réponse potentiellement fausse
- **Limite connue** : le dataset ne couvre pas la catégorie D3E (électronique) ni la distinction verre d'emballage / vaisselle — ces cas sont détectés en amont via mots-clés (voir `model/src/upstream_filters.py`), avant même l'appel au modèle d'image

---

## 🕸️ Scraping

Le scraper interroge `jumia.ci` avec un mot-clé utilisateur et retourne les 5 premiers résultats (nom, prix, image, note, lien) via `requests` et `BeautifulSoup`.

⚠️ **Limite connue** : le scraping dépend de la structure HTML actuelle de Jumia, qui peut évoluer sans préavis.

---

## 👥 Équipe

| Membre | Rôle |
|---|---|
| Kone Kpelban Augustin | Interface Streamlit & containerisation Docker |
| Ranaivomanana Angelo | Scraping Jumia |
| Bouiti Banza Olivier | Modèle IA / Deep Learning |

---

## 📋 Méthodologie de travail

- Trois branches distinctes (`feature/webapp`, `feature/ia-training`, `feature/scraping`), une par membre
- Fusion vers `main` exclusivement via Pull Requests reviewées
- Branche `main` protégée (aucun push direct)
- Intégration finale réalisée sur `feature/integration`

---

## 📅 Informations projet

- **Module** : ENSEA — ISE2A
- **Date limite** : 25/07/2026, 23h59:59
