# Qualification des pièces repeintes par vision artificielle

Application expérimentale qui estime, à partir d'une image rapprochée d'une surface automobile, si la peinture semble d'origine ou repeinte. Le système repose sur un modèle **EfficientNet-B0** et une API **FastAPI**, appelée depuis une interface web **React**.

Le résultat est indicatif : il ne remplace ni l'inspection d'un professionnel ni une mesure instrumentale. Le projet vise à expérimenter la faisabilité de la classification de textures de peinture automobile, et non à fournir une certification industrielle.

## Fonctionnalités

- Sélection et prévisualisation d'une image JPEG ou PNG.
- Envoi de l'image à l'API avec le champ multipart `file`.
- Classification selon trois verdicts : `origine`, `repeint` ou `incertain`.
- Affichage de la confiance et des probabilités des classes `origine` et `repeint`.
- Affichage facultatif de la zone centrale utilisée pour l'analyse.
- Chargement du modèle côté backend : le navigateur ne charge pas directement les poids Keras.

## Structure du projet

```text
automotive-paint-inspection/
├── backend/
│   ├── main.py                         # Application FastAPI et configuration CORS
│   ├── paint_analysis.py               # Endpoint et logique d'inférence
│   ├── requirements.txt                # Dépendances du backend
│   └── models/
│       └── paint/
│           └── efficientnet_binaire_phase2_best.keras
├── frontend/
│   └── ...                             # Interface React et styles
├── repainted model/                    # Supports de recherche/entraînement, si autorisés
├── docs/
│   └── requirements/paint_defects/      # Documentation du projet
├── tests/
│   └── backend/
│       └── test_paint_predict_contract.py
├── .gitignore
└── README.md
```

La structure exacte peut varier selon les fichiers présents dans le dépôt. Ne publiez pas de jeux de données, de rapports internes ou de code provenant d'un autre projet sans avoir vérifié que leur diffusion est autorisée.

## Prérequis

- Python 3.11 recommandé.
- Node.js 18 ou plus récent et npm.
- Git.
- Git LFS, si le modèle Keras du dépôt est distribué avec Git LFS.

## Installation et lancement local

Depuis la racine du dépôt, ouvrez deux terminaux PowerShell.

### 1. Installer les dépendances du backend

Si l'environnement virtuel `venv` n'existe pas encore, créez-le à la racine du dépôt :

```powershell
py -3.11 -m venv venv
.\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Si le modèle est suivi par Git LFS, récupérez son contenu après le clonage :

```powershell
git lfs install
git lfs pull
```

### 2. Démarrer le backend

Dans le premier terminal :

```powershell
cd backend
..\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

L'API est disponible sur [http://127.0.0.1:8000](http://127.0.0.1:8000). La vérification de démarrage est [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) et la documentation interactive est [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Le modèle est chargé lors de la première prédiction. La première requête peut donc être plus lente que les suivantes.

### 3. Démarrer le frontend

Dans le deuxième terminal, depuis la racine du dépôt :

```powershell
cd frontend
npm install
npm run dev
```

Si PowerShell bloque la commande `npm` à cause de sa stratégie d'exécution, utilisez `npm.cmd` :

```powershell
npm.cmd run dev
```

Ouvrez [http://localhost:3000/paint-inspection](http://localhost:3000/paint-inspection).

L'interface fournie charge React et Babel depuis un CDN ; une connexion Internet est donc nécessaire si ces bibliothèques ne sont pas servies localement.

Le serveur de développement sert l'application sur cette adresse et renvoie la page principale pour `/paint-inspection`.

## API d'inspection peinture

### `POST /paint/predict`

Envoie une image au modèle pour obtenir une prédiction.

- Type de requête : `multipart/form-data`.
- Nom du champ fichier : `file`.
- Formats acceptés : JPEG et PNG (`image/jpeg`, `image/png`).
- Taille maximale : 10 MiB (environ 10,5 Mo décimaux).

Exemple PowerShell avec `curl.exe` :

```powershell
curl.exe -X POST "http://127.0.0.1:8000/paint/predict" -F "file=@C:/chemin/vers/image.jpg"
```

La réponse JSON comprend notamment :

- `verdict` : `origine`, `repeint` ou `incertain` ;
- `confidence` : confiance associée à la prédiction, entre 0 et 1 ;
- `probabilities.origine` et `probabilities.repeint` : probabilités retournées pour les deux classes ;
- `model_version` : identifiant de la version du modèle ;
- `is_experimental` : indique que le résultat est expérimental ;
- `cropped_image` : image centrale encodée en data URL, si elle a pu être générée.

Les probabilités et le verdict sont des sorties du modèle et de la règle de décision actuelle ; elles ne constituent pas une preuve absolue qu'une pièce a été repeinte.

### `GET /health`

Retourne `{"status":"ok"}` pour confirmer que le service est démarré.

## Configuration

### Chemin du modèle

Par défaut, le backend recherche le modèle à cet emplacement :

```text
backend/models/paint/efficientnet_binaire_phase2_best.keras
```

La variable `PAINT_MODEL_PATH` permet de choisir un autre fichier. Un chemin relatif est résolu à partir du dossier `backend/` ; un chemin absolu peut aussi être fourni.

Exemple PowerShell :

```powershell
$env:PAINT_MODEL_PATH = "C:/models/mon_modele.keras"
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Le modèle attendu doit être compatible avec le code d'inférence, notamment avec l'ordre des classes : indice 0 pour `origine` et indice 1 pour `repeint`. Le backend vérifie également la présence des couches de prétraitement attendues lors du chargement du modèle.

### CORS (origines du frontend autorisées)

Le backend utilise `PAINT_ALLOWED_ORIGINS`, une liste d'origines séparées par des virgules. Lorsqu'elle est définie avec une valeur non vide, cette liste remplace les origines par défaut.

Par défaut, le code actuel autorise les origines frontend suivantes :

- `http://localhost:3000`
- `http://127.0.0.1:3000`

Pour le développement local, le frontend utilise l'une de ces deux origines sur le port `3000`.

Exemple PowerShell pour autoriser uniquement les deux origines locales du frontend :

```powershell
$env:PAINT_ALLOWED_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

**CORS et URL de l'API sont deux configurations différentes.** Dans `PaintInspection.jsx`, `PAINT_API_BASES` contient actuellement `http://127.0.0.1:8000` et `http://localhost:8000`. Pour un déploiement, il faudra également adapter cette liste ou la rendre configurable afin qu'elle pointe vers l'API réellement déployée.

## Tests

Depuis la racine du dépôt :

```powershell
python -m pip install -r backend/requirements-dev.txt
python -m pytest tests/backend/test_paint_predict_contract.py
```

Ces commandes supposent que `backend/requirements-dev.txt` et le fichier de test indiqué sont présents dans le dépôt.

## Dépannage

### L'API ne démarre pas

- Vérifiez que l'environnement virtuel est activé et que les dépendances de `backend/requirements.txt` sont installées.
- Lancez Uvicorn depuis la racine du dépôt avec `backend.main:app`, comme dans les commandes ci-dessus.
- Vérifiez que le port 8000 n'est pas déjà utilisé.

### Erreur indiquant que le modèle est introuvable ou illisible

- Vérifiez le chemin du fichier `.keras`.
- Si le modèle est géré par Git LFS, exécutez `git lfs pull` et vérifiez que le fichier téléchargé est le modèle complet, et non un simple fichier pointeur LFS.
- Vérifiez que le modèle correspond à l'architecture et aux couches de prétraitement attendues par `paint_analysis.py`.

### Le navigateur bloque l'appel à l'API

- Vérifiez que le backend écoute sur le port 8000.
- Ouvrez le frontend depuis une origine autorisée par `PAINT_ALLOWED_ORIGINS`.
- Vérifiez les adresses dans `PAINT_API_BASES` dans `PaintInspection.jsx`.
- Consultez la console du navigateur et les journaux du backend pour distinguer une erreur CORS d'une erreur réseau ou d'une réponse HTTP.

### Le frontend ne charge pas les bibliothèques React/Babel

Le frontend fourni les charge depuis un CDN. Vérifiez la connexion Internet ou configurez le frontend pour servir ces dépendances localement.

## Données, confidentialité et publication

Les données de recherche peuvent contenir des images de véhicules et des informations provenant de collectes sur le terrain. Avant toute publication publique :

- vérifiez l'autorisation de diffuser le code, le modèle, les poids, les notebooks, les résultats et les images ;
- retirez les images confidentielles, les données clients et toute information permettant d'identifier un véhicule ou une personne ;
- ne publiez pas de clés API, fichiers `.env`, identifiants ou secrets ;
- contrôlez également l'historique Git, car supprimer un fichier du dernier commit ne l'efface pas forcément de l'historique ;
- vérifiez que `.gitignore` exclut les secrets, environnements virtuels, caches et données qui ne doivent pas être partagées.

Le modèle est géré par Git LFS. Vérifiez les droits de redistribution avant de le rendre accessible publiquement.

## Limites

Ce système est expérimental et dépend du jeu de données, des conditions de capture, de l'éclairage, de la mise au point et des surfaces observées. Une prédiction `origine` ou `repeint` doit être interprétée comme une estimation du modèle, pas comme une certification. Une prédiction `incertain` invite à une vérification complémentaire.
