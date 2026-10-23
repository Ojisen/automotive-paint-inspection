# Protocole expérimental — Acquisition des images automobiles

**Projet :** MALLOULINOVA / MALLOULIAUTO
**Référence :** MALL-STG-ETE-2026-PAINT-01
**Version :** 1.1 — protocole effectivement utilisé
**Dispositif :** Redmi Note 12 + module Apexel
**Périmètre :** étude exploratoire de faisabilité

---

## 1. Objectif

Ce protocole décrit les conditions utilisées pour acquérir des images macro de surfaces automobiles afin d'étudier la différence visuelle entre :

- `origine` : peinture d'origine confirmée ;
- `repeint` : peinture repeinte confirmée.

L'analyse porte principalement sur les variations de texture, les points visibles, les micro-irrégularités et les variations locales de brillance observées dans les images.

Ce protocole correspond à une campagne pilote et ne constitue pas encore une procédure industrielle définitive.

---

## 2. Matériel utilisé

- Smartphone : **Redmi Note 12** ;
- Module optique : **Apexel** ;
- Application caméra du smartphone en mode **Pro** ;
- Éclairage intégré au module Apexel ;
- Filtre cpl intégré au module Apexel.

---

## 3. Paramètres de capture réellement utilisés

Les paramètres suivants ont été utilisés pendant la campagne :

| Paramètre                | Valeur                                                  |
| ------------------------- | ------------------------------------------------------- |
| Smartphone                | Redmi Note 12                                           |
| Module                    | Apexel                                                  |
| Mode caméra              | Pro                                                     |
| Vitesse d'obturation      | **1/50 s**                                        |
| Balance des blancs        | **5600 K**                                        |
| Mise au point             | **Auto (F)**                                      |
| Sensibilité ISO          | **Auto (ISO)**                                    |
| Compensation d'exposition | **0 EV**                                          |
| Objectif utilisé         | **W (Wide)**                                      |
| Distance                  | Quasi nulle, selon la meilleure mise au point observée |
| Nombre de captures        | **2 à 3 captures par zone étudiée**            |

Le mode 50 MP n'est pas retenu comme mode principal lorsqu'il produit un cercle lumineux, un vignettage ou des bords assombris. Le mode Pro avec l'objectif **W** constitue la configuration documentée pour cette campagne.

---

## 4. Procédure de capture

Pour chaque zone automobile étudiée :

1. Positionner le smartphone Redmi Note 12 équipé du module Apexel.
2. Utiliser l'objectif **W** et ne pas utiliser l'objectif **UW**.
3. Régler la vitesse à **1/50 s**.
4. Régler la balance des blancs à **5600 K**.
5. Laisser la mise au point en mode **Auto (F)**.
6. Laisser la sensibilité ISO en mode **Auto (ISO)**.
7. Régler la compensation d'exposition à **0 EV**.
8. Positionner le module à une distance quasi nulle correspondant à la meilleure netteté observée.
9. Vérifier visuellement la netteté de la zone centrale.
10. Réaliser **2 à 3 captures de la même zone**.
11. Vérifier rapidement les images obtenues.
12. Enregistrer les images dans le dossier correspondant à leur label.

**La campagne expérimentale a été menée dans plusieurs environnements professionnels du secteur automobile** :
zones dédiées à l’application et au séchage de la peinture, entreprises automobiles disposant de véhicules neufs, ainsi que des ateliers spécialisés en tôlerie-carrosserie. Cette diversité de sites a permis de collecter des surfaces correspondant à différents états de peinture, tout en intégrant la variabilité des conditions réelles d’acquisition sur le terrain.

---

## 5. Organisation des fichiers

Les images sont organisées selon deux classes :

```text
dataset/
├── origine/
└── repeint/
```

Après la préparation du dataset, les images sont réparties dans :

```text
dataset_final_splits_v2/
├── train/
│   ├── origine/
│   └── repeint/
├── val/
│   ├── origine/
│   └── repeint/
└── test/
    ├── origine/
    └── repeint/
```

---

## 6. Métadonnées utilisées

Le fichier de métadonnées utilisé dans cette campagne contient uniquement les informations effectivement exploitées :

| Champ          | Rôle                                         |
| -------------- | --------------------------------------------- |
| `filename`   | Nom de l'image, par exemple`image_225.jpeg` |
| `filepath`   | Chemin vers l'image                           |
| `label`      | `origine` ou `repeint`                    |
| `session_id` | Identifiant de chaque voiture                 |
| `split`      | `train`, `val` ou `test`                |

---

## 7. Annotation des images

Chaque image est associée à l'une des deux classes :

```text
origine
repeint
```

L'annotation est basée sur les informations disponibles auprès de l'atelier et non uniquement sur l'apparence visuelle de l'image.

---

## 8. Contrôle qualité

Une capture est conservée si :

- la zone étudiée est visible ;
- la mise au point est suffisamment nette ;
- l'image n'est pas fortement surexposée ou sous-exposée ;
- la texture n'est pas masquée par un reflet important ;
- le cercle lumineux ne couvre pas la zone utile.

Les images très floues ou fortement dégradées peuvent être exclues du dataset final.

---

## 9. Préparation des données pour l'IA

Les images sont redimensionnées en :

```text
384 × 384 pixels
```

Un recadrage central fixe de 32 pixels par côté peut être appliqué afin de réduire l'influence des bords lumineux :

```text
Image initiale : 384 × 384
Zone conservée : 320 × 320
Entrée modèle : 384 × 384 après redimensionnement
```

Le même traitement doit être appliqué à Train, Validation et Test.

La data augmentation est appliquée uniquement au jeu Train.

---

## 10. Règles de séparation

- Les images d'une même session doivent rester dans le même sous-ensemble lorsque cela est possible.
- Les images d'un même véhicule ne doivent pas être réparties entre Train et Test si l'identifiant est disponible.
- Les images Validation et Test ne doivent pas subir de data augmentation.
- Le Test est utilisé uniquement pour l'évaluation finale.

---

## 11. Limites du protocole pilote

- Le smartphone utilisé est uniquement le Redmi Note 12.
- Le module utilisé est uniquement l'Apexel.
- La distance exacte de travail et le grossissement réel ne sont pas encore calibrés précisément.
- Le mode 50 MP peut produire un vignettage circulaire et des bords assombris.
- Les captures concernent des zones disponibles dans l'atelier, sans protocole imposant une pièce automobile déterminée.
- Deux à trois captures par zone ne constituent pas toujours des observations indépendantes.
- Le dataset pilote ne permet pas encore de valider une utilisation industrielle.
