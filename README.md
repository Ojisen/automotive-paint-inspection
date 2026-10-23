# Qualification des pièces repeintes par vision artificielle

Application expérimentale qui estime, à partir d’une image rapprochée d’une
surface automobile, si la peinture semble d’origine ou repeinte. Le résultat
reste indicatif et ne remplace pas l’expertise d’un professionnel.

## Contenu du projet

- `backend/` : API FastAPI, prétraitement d’image et modèle de classification.
- `frontend/` : interface web autonome pour envoyer une image et lire le résultat.
- `repainted model/` : notebooks, jeux de données et résultats d’entraînement.
- `docs/requirements/paint_defects/` : protocole et documentation de recherche.
- `tests/backend/` : tests du contrat de l’API.

## Prérequis

- Python 3.11
- Node.js 18 ou plus récent
- Git LFS pour récupérer le modèle `.keras` depuis GitHub

## Lancement local

À la racine du dépôt, ouvrir deux terminaux.

### 1. Installer et démarrer l’API

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Vérifier l’API sur [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) et consulter la documentation
interactive sur [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 2. Démarrer l’interface

```powershell
cd frontend
npm run dev
```

Ouvrir [http://127.0.0.1:3000](http://127.0.0.1:3000). L’interface utilise React et Babel depuis un
CDN, une connexion Internet est donc nécessaire lors du chargement de la page.

## API

`POST /paint/predict` attend un fichier multipart nommé `file` (JPEG ou PNG,
10 Mo maximum). La réponse inclut le verdict (`origine`, `repeint` ou
`incertain`), le niveau de confiance, les probabilités par classe et la version
du modèle.

La route `GET /health` permet de vérifier que l’API est démarrée.

## Configuration

Le modèle est chargé depuis
`backend/models/paint/efficientnet_binaire_phase2_best.keras`. Pour utiliser
un autre modèle, définir `PAINT_MODEL_PATH` avant de démarrer l’API.

Exemple PowerShell :

```powershell
$env:PAINT_MODEL_PATH = "C:\chemin\vers\mon_modele.keras"
$env:PAINT_ALLOWED_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Les origines autorisées par CORS sont configurables avec
`PAINT_ALLOWED_ORIGINS`, une liste séparée par des virgules. Par défaut,
l’interface locale sur les ports `localhost:3000` et `127.0.0.1:3000` est
autorisée.

## Tests

```powershell
python -m pip install -r backend/requirements-dev.txt
python -m pytest tests/backend/test_paint_predict_contract.py
```

## Données et publication

Les jeux d’images de recherche restent dans `repainted model/`. Avant de
publier le dépôt, vérifier que leur partage est autorisé. Le modèle est suivi
par Git LFS ; installer Git LFS puis exécuter `git lfs pull` après le clonage
pour récupérer son contenu.
