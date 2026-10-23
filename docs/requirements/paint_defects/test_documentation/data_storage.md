# Stockage des Datasets — MALLOULIAUTO WP3

Les datasets volumineux ne sont pas versionnés dans Git (limite 100 MB/fichier).
Ils sont accessibles via les liens suivants :

## Datasets de Test (Semaine 4)

| Dataset                     | Lien                                                                                                        | Taille | Usage                        |
| :-------------------------- | :---------------------------------------------------------------------------------------------------------- | :-----: | :--------------------------- |
| CarDD (zip)                 | [www.kaggle.com/datasets/issamjebnouni/cardd/data](https://www.kaggle.com/datasets/issamjebnouni/cardd/data) | ~500 MB | Test data augmentation       |
| CarDD (multiclass)          | Version structurée en classes par script à partir de CarDD (zip)                                          |  ~1 GB  | Version organisée 6 classes |
| Roboflow Paint Defects(zip) | [app.roboflow.com/amir-mwck6/1-ubhu1-5c4w6/1](https://app.roboflow.com/amir-mwck6/1-ubhu1-5c4w6/1)           | ~200 MB | Analyse préliminaire        |

## Dataset Propriétaire (Semaine 5)

| Dataset           | Lien          |     Taille     | Usage               |
| :---------------- | :------------ | :-------------: | :------------------ |
| MALLOULIAUTO v0.1 | À construire | ~500 MB estimé | Entraînement final |

## Téléchargement des Datasets Publics

### CarDD

```bash
kaggle datasets download -d issamjebnouni/cardd
```
