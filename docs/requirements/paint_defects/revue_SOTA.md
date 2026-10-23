# MALLOULINOVA – Stage Été 2026

## R&D — Qualification fiable des pièces repeintes vs peinture d'origine sur véhicule par vision artificielle

**Référence :** MALL-STG-ETE-2026-PAINT-01
**Livrable :** Mission 1 — Revue SOTA & Cadrage du Projet

---

## 1. Cadrage Scientifique & Problématique

L'objectif de ce stage est d'étudier la faisabilité d'un système de vision artificielle capable de distinguer automatiquement une peinture d'origine d'une pièce repeinte, à partir d'images acquises avec un smartphone.

Dans le domaine automobile, cette opération est généralement réalisée par un expert qui combine plusieurs indices visuels et son expérience. Une pièce repeinte peut présenter des différences plus ou moins marquées selon la qualité de la réparation, ce qui rend une détection automatique particulièrement difficile.

Les principaux indices pouvant révéler une opération de repeinture sont notamment :

-la micro-texture du vernis (effet peau d'orange) ;

-les variations locales de brillance ;

-les différences de réflexion de la lumière ;

-les légères dérives colorimétriques ;

-les défauts de finition (poussières, inclusions, traces de polissage, etc.).

Cependant, ces indices ne sont pas systématiquement présents et leur visibilité dépend fortement des conditions d'éclairage, du type de peinture, de la couleur du véhicule et de la qualité de la réparation.

Dans le cadre de ce stage, l'étude se concentre principalement sur l'observation de **la micro-texture de surface**, car elle constitue un indice physique directement lié au procédé d'application et au comportement du vernis lors du séchage. Cette texture devient plus facilement observable grâce à une acquisition macroscopique réalisée avec un smartphone équipé d'un module optique dédié.

L'objectif n'est pas de démontrer que la micro-texture est l'unique critère permettant d'identifier une repeinture, mais d'évaluer si cette information, exploitée par un modèle de Deep Learning, est suffisante pour obtenir une première classification fiable dans des conditions d'acquisition compatibles avec une utilisation mobile.

---

## 2. Axe SOTA — Synthèse des techniques candidates

La revue SOTA compare ici les principales techniques candidates pour améliorer la qualité du signal destiné à l'IA, en tenant compte des contraintes de portabilité et de coût du projet.

### Tableau 1 — Synthèse des techniques SOTA

| Technique                                           | Principe                                                                                                                 | Signal exploité par l'IA                                                   | Avantage principal                                                                                        | Limite principale                                                                                               | Maturité | Statut                               |
| :-------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- | :-------- | :----------------------------------- |
| **RGB smartphone**                            | Capture classique par caméra mobile.                                                                                    | Image RGB.                                                                  | Simplicité maximale et disponibilité du matériel.                                                      | Sensibilité aux reflets, à l'éclairage et aux traitements ISP.                                               | Élevée  | Baseline de référence              |
| **Module macroscopique clip-on tout-en-un**   | Adaptation optique portable intégrant grossissement macro, LED d'éclairage et filtre polarisant CPL sur le smartphone. | RGB haute résolution effective (~1300 pixels/mm) avec reflets contrôlés. | Solution tout-en-un : grossissement, éclairage et polarisation intégrés dans un même module portable. | Champ de vision réduit (~6 mm), nécessite multi-patches par véhicule.                                        | Élevée  | 🟢**Retenu (Setup principal)** |
| **Éclairage LED rasant externe**             | Éclairage contrôlé sur la zone observée avec incidence rasante (15-25°).                                            | RGB avec micro-relief révélé par ombres portées.                        | Révèle la texture par ombres portées, stabilise l'acquisition.                                         | Positionnement précis requis, complexité opérationnelle, accessoire séparé à manipuler.                   | Élevée  | Écarté (intégré au module macro) |
| **Filtre CPL séparé**                       | Polarisation circulaire montée sur clip smartphone.                                                                     | RGB filtré optiquement.                                                    | Supprime les reflets spéculaires du vernis.                                                              | Réglage optique manuel nécessaire, accessoire séparé à manipuler.                                          | Élevée  | Écarté (intégré au module macro) |
| **Caméra monochrome USB**                    | Capteur CMOS sans filtre Bayer, sensibilité +30%, résolution effective doublée.                                       | Signal monochrome à contraste maximal.                                     | Meilleur rapport signal/bruit en basse lumière.                                                          | Résolution nominale faible (1-5 MP vs 48 MP smartphone), nécessite PC portable, non portable au sens terrain. | Moyenne   | Écarté (perspective V2 poste fixe) |
| **Spectrophotométrie portable**              | Mesure locale des propriétés colorimétriques en espace L\*a\*b\*.                                                     | Signature spectrale / valeurs Lab.                                          | Mesure colorimétrique précise (ΔE < 0.5).                                                              | Ne fournit pas une image 2D complète, coût utilisateur élevé, temps de capture long.                        | Moyenne   | Écarté du produit                  |
| **Calibration ColorChecker (charte Macbeth)** | Référence physique étalonnée à 24 patchs pour étalonnage colorimétrique.                                          | RGB corrigé par matrice CCM.                                               | Référence colorimétrique fiable et reproductible.                                                      | Contrainte UX et manipulation terrain.                                                                          | Élevée  | Référence laboratoire              |
| **Déflectométrie d'apparence**              | Analyse des réflexions de motifs structurés projetés sur la surface.                                                  | Signature géométrique de surface (waviness, DOI, haze).                   | Très riche pour l'étude du vernis et des micro-défauts.                                                | Acquisition lourde et peu mobile, coût prohibitif (25 000-150 000 €).                                         | Élevée  | Référence industrielle             |

---

## 3. Configurations expérimentales

Les configurations expérimentales servent à comparer des combinaisons concrètes de capture afin d'identifier le meilleur compromis pour le terrain, en tenant compte des contraintes de coût, portabilité et faisabilité dans le cadre du stage.

### Tableau 1 — Benchmark des setups

| Setup             | Composition                                                                              | Objectif                                                                                                                 | Coût indicatif   | Temps           | Contraintes                           | Performance estimée                                                          | Portabilité terrain     | Décision                        |
| :---------------- | :--------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- | :---------------- | :-------------- | :------------------------------------ | :---------------------------------------------------------------------------- | :----------------------- | :------------------------------- |
| **Setup A** | Smartphone RGB seul à 40 cm.                                                            | Baseline minimale.                                                                                                       | 0 DT              | Très court     | Très faibles                         | Faible (~40 pixels/mm)                                                        | Très élevée           | Écarté                         |
| **Setup B** | Spectrophotomètre portable (Spectro 1 Mobile).                                          | Mesure spectrale ponctuelle de référence.                                                                              | 1008 DT           | Long            | Moyennes                              | Élevée sur la couleur, faible sur l'image 2D                                | Moyenne                  | Écarté du produit              |
| **Setup C** | Smartphone + LED NEEWER + Filtre CPL séparé à 40 cm (accessoires séparés).          | Amélioration texture par éclairage rasant et polarisation.                                                             | 242 DT            | Court           | Moyennes (3 accessoires à manipuler) | Moyenne (~40 pixels/mm, résolution limitée à 40 cm)                        | Élevée                 | Écarté (macro plus efficace)   |
| **Setup D** | Calibrite ColorChecker Classic Mini.                                                     | Référence colorimétrique labo.                                                                                        | 290 DT            | Moyen           | Élevées                             | Très élevée en calibration, faible en usage terrain                        | Faible                   | Écarté du produit              |
| **Setup E** | Rhopoint TAMS - Total Appearance Measurement System.                                     | Déflectométrie d'apparence industrielle.                                                                               | 63000 DT          | Long            | Très élevées                       | Très élevée en signal géométrique                                        | Faible                   | Référence industrielle         |
| **Setup F** | **Module macroscopique Apexel tout-en-un (grossissement + LED + CPL intégrés).** | **Analyse macroscopique haute résolution du signal texture avec accessoires intégrés dans un seul dispositif.** | **~180 DT** | **Court** | **Faibles (1 seul module)**     | **Élevée (~1300 pixels/mm, résolution ~30x supérieure au Setup C)** | **Très élevée** | 🟢**Choix optimal retenu** |

---

## 4. Guide Méthodologique du Benchmark

L'évaluation comparative des configurations optiques a été révisée en Semaine 4 suite à l'identification du module macroscopique Apexel tout-en-un comme solution optimale. Ce module intègre dans un seul dispositif le grossissement macro, l'éclairage LED et le filtre polarisant CPL, éliminant ainsi la nécessité d'accessoires séparés (Setup C initialement envisagé).

Cette réorientation permet de figer la trajectoire technique et de consacrer exclusivement les semaines suivantes à la collecte du dataset propriétaire terrain (450 à 500 patches macroscopiques en V0.1, objectif à long terme de 1 000 patches inscrit en roadmap V1, classes *Origine / Repeint*) et à l'entraînement du modèle d'IA sur cette configuration unique.

### 4.1. Variables contrôlées et variables testées

#### Tableau 1 — Variables contrôlées (stabilisées strictement par le protocole)

| Variable contrôlée                      | Règle opérationnelle appliquée                                                                                                                                        | Objectif méthodologique                                                                                                         |
| :---------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| **Véhicule & zone**                | Même véhicule, plusieurs pièces (capot, ailes, portières, toit, coffre) durant une session.                                                                          | Documenter l'ensemble des zones significatives par véhicule pour l'agrégation multi-patches.                                   |
| **Distance module-surface**         | Contact quasi-direct (5-10 mm) avec la surface, guidé par la butée physique du module Apexel.                                                                          | Garantir le grossissement optimal et la mise au point automatique du module macro.                                               |
| **Nombre de patches par pièce**    | 2 patches par pièce sur les zones planes principales.                                                                                                                   | Statistiquement significatif pour classification et agrégation multi-patches.                                                   |
| **Nombre de pièces par véhicule** | 6 à 8 pièces (capot, aile G, aile D, portière G, portière D, portière arrière G, portière arrière D, coffre).                                                    | Représentativité du véhicule pour verdict global fiable.                                                                      |
| **Éclairage**                      | LEDs intégrées au module Apexel systématiquement activées.                                                                                                           | Standardiser l'éclairage indépendamment des conditions ambiantes.                                                              |
| **Polarisation**                    | Filtre CPL intégré au module Apexel actif en permanence.                                                                                                               | Éliminer les reflets spéculaires directement au niveau du module, sans manipulation externe.                                   |
| **Mise au point**                   | Automatique via optique fixe du module macro (distance de travail 5-10 mm).                                                                                              | Garantir la netteté du signal texture à l'échelle microscopique.                                                              |
| **Modes de traitement smartphone**  | Utilisation obligatoire du mode Pro/Manuel avec désactivation explicite du HDR automatique, mode Portrait et filtres artistiques. Documentation dans les métadonnées. | Éliminer les biais introduits par les traitements ISP algorithmiques qui altèrent artificiellement la micro-texture du vernis. |
| **Résolution smartphone**          | 12.5 MP                                                                                                                                                                  | Exploiter la résolution native maximale du capteur pour capturer tous les détails.                                             |
| **Format d'enregistrement**         | JPEG qualité maximale.                                                                                                                                                  | Préserver l'information haute fréquence contenant la signature texturale.                                                      |
| **Résolution & IA**                | Format strict de ** 384×384 pixels ** sur backbone**EfficientNet-B0**.                                                                                            | Uniformiser la dimension d'entrée du réseau.                                                                                   |

#### Tableau 2 — Variables testées (facteurs d'évaluation de la performance)

| Variable testée                         | Objectif scientifique de la mesure                                                                                           |
| :--------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Couleur carrosserie**            | Évaluer la robustesse du signal texture sur teintes claires réfléchissantes, sombres et métallisées.                    |
| **Marque et modèle de véhicule** | Évaluer la généralisation du modèle sur diverses marques automobiles.                                                    |
| **État de peinture**              | Comparer les signatures macroscopiques de peintures d'origine, repeintes en concession et repeintes en atelier indépendant. |

### 4.2 Prétraitement des images

| Étape                                              | Rôle                                                                        | Objectif                                                                                       |
| :-------------------------------------------------- | :--------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| Redimensionnement (384 × 384) pixels               | Adapte l'image macroscopique au format d'entrée du modèle EfficientNet-B0. | Réduire le coût de calcul et standardiser l'entrée.                                         |
| Normalisation Keras (preprocess_input EfficientNet) | Applique la normalisation standard attendue par le backbone pré-entraîné. | Assurer la compatibilité des statistiques d'entrée avec les poids ImageNet.                  |
| Finalité globale                                   | Limite les variations non pertinentes tout en préservant le signal texture. | Permettre au modèle de se concentrer sur les caractéristiques discriminantes de la peinture. |

### 4.3. Matrice multicritère de sélection du setup optimal

La sélection du setup final repose sur une analyse multicritère combinant :

- les performances attendues selon l'état de l'art ;
- les contraintes industrielles ;
- les premiers résultats expérimentaux disponibles.

> **Note méthodologique** : Les scores ci-dessous constituent une aide à la décision d'ingénierie (analyse multicritère pondérée), et non un benchmark expérimental. Les critères "Qualité du signal texture" et "Performance IA attendue" sont des estimations issues de la littérature et des spécifications constructeur pour les setups non testés (C, B, D, E), et de tests terrain préliminaires pour les setups A et F. Les scores seront complétés par des mesures expérimentales en Semaine 4.

Cette approche permet de comparer des configurations de complexité différente sans nécessiter l'acquisition immédiate de tous les équipements.

Le choix final est effectué selon un score global :

$$
Score_{setup} = \sum_{i=1}^{n} W_i \times S_i
$$

avec $W_i$ : poids du critère, $S_i$ : score attribué au setup pour ce critère (1 = faible → 5 = excellent).

#### Tableau 1 — Évaluation pondérée des setups

*Notation : 1 (faible) → 5 (excellent). Les scores des Setups B, C, D et E sont des estimations basées sur la littérature et les spécifications constructeur (non mesurés expérimentalement) ; les Setups A et F font l'objet de tests terrain réels.*

| Critère d'arbitrage évalué          | Poids ($W_i$) |         Setup A*(Smartphone seul)*         |         Setup B*(Spectrophotométrie)*         |      Setup C*(LED + CPL séparé)*      |       Setup D*(ColorChecker)*       |          Setup E*(Rhopoint TAMS)*          | **Setup F [Choix cible]** *(Module Macro tout-en-un)* |
| :------------------------------------- | :-------------: | :-------------------------------------------: | :----------------------------------------------: | :----------------------------------------: | :------------------------------------: | :-------------------------------------------: | :-----------------------------------------------------------: |
| **Qualité du signal texture**   |       25       |                       1                       |                        1                        |                     2                     |                   3                   |                       5                       |                          **5**                          |
| **Performance IA attendue**      |       25       |                       2                       |                        3                        |                     3                     |                   4                   |                       5                       |                          **5**                          |
| **Gestion des reflets**          |       15       |                       1                       |                        2                        |                     5                     |                   4                   |                       5                       |                          **5**                          |
| **Temps de capture (<90s)**      |       10       |                       5                       |                        2                        |                     4                     |                   3                   |                       1                       |                          **5**                          |
| **Coût (contrainte ≤ 250 DT)** |       10       |                       5                       |                        2                        |                     4                     |                   3                   |                       1                       |                          **4**                          |
| **Portabilité**                 |       10       |                       5                       |                        3                        |                     4                     |                   2                   |                       1                       |                          **5**                          |
| **Disponibilité**               |        5        |                       5                       |                        1                        |                     4                     |                   1                   |                       1                       |                          **5**                          |
| **SCORE TOTAL / 5**              | **100%** |              **2.55 / 5**              |                **2.20 / 5**                |             **3.25 / 5**             |           **3.30 / 5**           |              **3.50 / 5**              |                     **🟢 4.85 / 5**                     |
| **INTERPRÉTATION & DÉCISION**  |       —       | ❌ Baseline simple (résolution insuffisante) | ❌ Ne fournit pas d'image 2D compatible avec CNN | ❌ Résolution effective limitée à 40 cm | ❌ Précis (trop contraignant terrain) | ❌ Fort potentiel (trop complexe et coûteux) |         🟢**Meilleur compromis (Setup Retenu)**         |

### 4.5. Gestion des données et vérité terrain

Chaque acquisition est associée à des métadonnées permettant d'assurer la traçabilité du dataset.

| Information             | Exemple                                                   |
| :---------------------- | :-------------------------------------------------------- |
| Setup utilisé          | A / F                                                     |
| Smartphone              | Xiaomi Redmi Note 12 (référence dataset)                |
| Véhicule               | Marque, modèle, année                                   |
| Pièce inspectée       | Capot, aile, portière, toit, coffre                      |
| Position du patch       | Numéro (1 ou 2) et zone approximative (centre, latéral) |
| Couleur peinture        | Claire, sombre, métallisée                              |
| Conditions extérieures | Soleil, ombre, météo, intérieur atelier                |
| Annotation              | Origine / Repeint                                         |

La vérité terrain est définie à partir des informations disponibles (historique véhicule, expertise humaine ou mesure externe si nécessaire).

| Classe  | Description                         |
| :------ | :---------------------------------- |
| Origine | Peinture d'usine confirmée         |
| Repeint | Modification de peinture confirmée |

Le dataset propriétaire constitue la référence finale pour l'entraînement et l'évaluation.

#### Tableau 1 — Stratégie de classification et gestion de l'état Incertain

> **Décision architecturale** : Le modèle est entraîné sur **2 classes** uniquement (Origine / Repeint). L'état "Incertain" n'est pas une classe entraînée — c'est un état de sortie produit automatiquement en post-traitement lorsque la confiance maximale du modèle est inférieure à un seuil à déterminer expérimentalement (valeur initiale : 0.65). Cette approche est cohérente avec les pratiques industrielles de classification binaire avec seuil de rejet.

| Phase du Pipeline                               | Action Opérationnelle Terrain / Code                                                                                                                                                                                                                  | Objectif Méthodologique & Impact IA                                                                 |
| :---------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| **1. Capture Initiale**                   | - Capture d'environ**200 patches macroscopiques** certifiés d'usine (*Origine*).- Capture d'environ **200 patches macroscopiques** certifiés retravaillés (*Repeint*).- Les cas sans confirmation fiable sont écartés du dataset. | Constituer une base de données v0.1 propre sur 2 classes uniquement, quantitativement équilibrée. |
| **2. Filtrage qualité post-acquisition** | Exclusion des patches flous, mal exposés ou avec un mauvais contact module-surface.                                                                                                                                                                   | Éliminer les données techniquement non fiables.                                                    |
| **3. Entraînement**                      | EfficientNet-B0 entraîné sur**2 classes binaires** : Origine et Repeint. Aucune troisième classe.                                                                                                                                             | Modèle binaire propre, sans bruit de classe ambiguë.                                               |
| **4. Post-traitement à l'inférence**    | Si`max(softmax_output) ≥ seuil` → classe prédite (Origine ou Repeint).Si `max(softmax_output) < seuil` → état "Incertain" (flag de rejet).                                                                                                    | Produire un verdict avec niveau de confiance contrôlé.                                             |
| **5. Optimisation du seuil**              | Le seuil de rejet sera optimisé sur le jeu de validation (grid search sur la courbe précision/recall). Valeur initiale : 0.65.                                                                                                                       | Trouver le meilleur équilibre faux positifs / cas rejetés.                                         |

---

### 4.6. Architecture du modèle IA

L'objectif est de classer automatiquement une pièce de carrosserie selon deux catégories principales :

- Origine ;
- Repeint.

Avec un état "Incertain" produit en post-traitement lorsque la confiance du modèle est insuffisante.

Le modèle exploite comme information principale la micro-texture de surface (peau d'orange) capturée par le Setup F (module macroscopique Apexel tout-en-un). L'architecture repose sur une approche patch par patch avec agrégation multi-patches pour établir un verdict au niveau du véhicule.

| Signal                                          | Rôle dans le système                                                                                                              |
| :---------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| **Texture macroscopique (peau d'orange)** | Signal physique principal, exploité via EfficientNet-B0 sur patches RGB haute résolution acquis avec le module Apexel tout-en-un. |
| **Couleur (implicite)**                   | Information secondaire apprise automatiquement par les couches profondes du CNN, sans traitement colorimétrique dédié.           |

Pipeline général :

```text
               Acquisition de l'image
      (smartphone + Module Apexel tout-en-un)
      [LED intégrées + CPL intégré activés]
                      │
                      ▼
        Acquisition avec le Setup F
     (Grossissement + LED rasant + CPL intégrés)
                      │
                      ▼
        15-20 patches par véhicule
     (2 patches par pièce sur 6-8 pièces)
                      │
                      ▼
           Prétraitement OpenCV
     • Redimensionnement (384×384)
     • Normalisation Keras (preprocess_input)
                      │
                      ▼
          Modèle IA EfficientNet-B0
      (Transfer Learning - Classification binaire)
                      │
                      ▼
      Prédiction par patch + Score de confiance
                      │
                      ▼
      Filtrage par seuil de rejet (initial : 0.65)
      - Confiance ≥ seuil → Origine ou Repeint
      - Confiance < seuil → Incertain (flag)
                      │
                      ▼
      Agrégation par vote pondéré par la confiance
                      │
                      ▼
      Verdict véhicule + Rapport détaillé par pièce
```

Le pipeline repose sur une acquisition macroscopique à contact quasi-direct avec la surface via le Setup F, suivie d'un prétraitement OpenCV minimaliste (redimensionnement et normalisation Keras), puis d'une inférence par patch via EfficientNet-B0. Un système de filtrage par seuil de confiance produit l'état "Incertain" pour les patches ambigus, et une couche d'agrégation par vote pondéré par la confiance produit le verdict final au niveau du véhicule ainsi qu'un diagnostic par pièce. La simplicité du pipeline est un choix méthodologique délibéré : en déplaçant la maîtrise du signal vers l'acquisition matérielle (Setup F), la chaîne de traitement d'image reste courte et robuste, réduisant les risques d'introduction de biais artificiels.

## Principe d'architecture : division des rôles entre acquisition, prétraitement et IA

La performance du système ne repose pas uniquement sur le modèle d'intelligence artificielle. Chaque bloc du pipeline possède une fonction spécifique permettant de réduire la complexité globale du problème.

| Élément du système                              | Mission principale                                                                    | Rôle dans la réduction de complexité                                                                                                                                                             |
| :------------------------------------------------- | :------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Setup F (Module Macro Apexel tout-en-un)** | Révéler le micro-relief en pixel-perfect avec éclairage et polarisation intégrés | Optimiser physiquement l'acquisition en fournissant une résolution effective largement supérieure à une capture standard, avec tous les accessoires intégrés dans un seul dispositif portable. |
| **Prétraitement OpenCV (minimal)**          | Adapter les images au format d'entrée du modèle                                     | Standardiser sans altérer le signal texture ; complexité volontairement réduite.                                                                                                                 |
| **Modèle IA (EfficientNet-B0)**             | Extraire automatiquement les caractéristiques discriminantes de texture par patch    | Classifier chaque patch en Origine ou Repeint avec score de confiance.                                                                                                                              |
| **Seuil de rejet de confiance**              | Produire l'état "Incertain" pour les prédictions ambiguës                          | Éviter les décisions à faible confiance en levant explicitement l'ambiguïté.                                                                                                                   |
| **Couche d'agrégation par vote pondéré**  | Consolider les prédictions par véhicule via vote pondéré par la confiance         | Produire un verdict global fiable et un diagnostic détaillé par zone, sans règles arbitraires.                                                                                                   |

### Conclusion architecturale

Cette approche suit un principe classique des systèmes de vision industrielle :

**améliorer le signal avant d'augmenter la complexité du modèle.**

En déplaçant la maîtrise de la difficulté vers l'acquisition (Setup F macroscopique tout-en-un) et une approche patch par patch avec agrégation par vote pondéré par la confiance, il devient possible d'utiliser une architecture légère adaptée à un déploiement mobile, avec un pipeline logiciel volontairement court et robuste.

### 4.7 Choix du modèle Deep Learning

| Modèle                                | Avantages                                                                                                    | Inconvénients / Limites                                                                                                     | Décision R&D                       |
| :------------------------------------- | :----------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- | :---------------------------------- |
| **ResNet-50**                    | Backbone de référence en vision industrielle carrosserie*(cf. Semitela et al., 2025)*.                   | Volume de paramètres élevé (25M), lourd en calcul Edge et risque de surapprentissage (*overfitting*) sur petit dataset. | ❌**Non retenu**              |
| **ViT** *(Vision Transformer)* | Excellente capacité d'attention et de corrélation contextuelle globale sur les formes.                     | Nécessite un volume massif de données d'entraînement pour converger (absence de biais inductif).                          | ❌**Non retenu**              |
| **ConvNeXt**                     | Architecture moderne, hautement performante sur les tâches de segmentation complexes.                       | Coût computationnel élevé, empreinte mémoire et vitesse d'inférence défavorables pour le mobile.                       | ❌**Non retenu**              |
| **EfficientNet-B0**              | **Ultra-léger (5M de paramètres), précis, optimisé pour l'embarqué via le *Compound Scaling*.** | Sensible à la qualité géométrique du redimensionnement initial (exige un format strict 224×224).                        | 🟢**RETENU (Backbone Cible)** |

**Justification du choix d'EfficientNet-B0 :**

- **Optimisation Edge AI** : Volume de paramètres divisé par 5 (5M vs 25M pour ResNet-50), minimisant l'empreinte mémoire RAM et la consommation de batterie sur smartphone.
- **Vitesse d'inférence** : Vitesse de calcul jusqu'à 4 fois plus rapide sur processeur mobile, garantissant le respect strict de l'objectif expérimental cible de temps de cycle ($\le$ 90 secondes).
- **Adaptation au Transfer Learning** : Architecture idéale pour converger rapidement sans surapprentissage (overfitting) sur notre volume cible de 450 à 500 patches macroscopiques en V0.1.
- **Compatibilité TensorFlow Lite** : Conversion native vers format mobile via l'API `keras.applications`, cohérente avec le framework Keras / TensorFlow retenu pour le pipeline.

### 4.8. Stratégie données et robustesse

Le modèle sera testé sur :

| Facteur                           | But                                                            |
| :-------------------------------- | :------------------------------------------------------------- |
| **Plusieurs couleurs**      | Généralisation aux teintes claires, sombres et métallisées |
| **Différents véhicules**  | Généralisation aux différentes marques et modèles          |
| **Différentes conditions** | Robustesse ombre / atelier / lumière indirecte                |

Le tableau ci-dessous synthétise la cartographie des données exploitées pour initialiser et entraîner l'architecture **EfficientNet-B0** :

| Dataset / Jeu de données                                                                  | Taille / Contenu                                                                                                                                                                                    | Pertinence pour ce stage                                                                                                                                                                                                                                                         | Usage recommandé & Intégration                                                                                                                                                                                             |
| :----------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **MVTec AD**                                                                         | 5 354 images, 15 catégories d'objets, anomalies industrielles de surface.                                                                                                                          | **Moyenne** : Excellent proxy temporaire pour l'apprentissage des micro-textures et des irrégularités de vernis, mais non spécifique au domaine automobile macroscopique.                                                                                               | Écarté : Non adapté à l'échelle macroscopique du Setup F.                                                                                                                                                               |
| **Roboflow Paint Defects** *(BuildwellAI)*                                         | 467 images de défauts de peinture automobile (vue globale à distance).                                                                                                                            | **Risque critique d'overfitting :** L'analyse montre que les distributions statistiques sont trop divergentes (vue globale contextuelle vs texture macroscopique *pixel-perfect* de l'APEXEL). Un transfert direct provoquerait un surapprentissage sur le faux domaine. | **Conservé uniquement pour tester techniquement le pipeline** (vérifier le bon fonctionnement du code, du chargement et de l'inférence à blanc) et pour la documentation SOTA. Aucun entraînement de performance. |
| **CarDD**                                                                            | 4 000 images haute résolution, > 9 000 instances de défauts annotées.                                                                                                                            | **Moyenne** : Utile pour la validation du pipeline technique, mais éloignée du signal cible (dommages mécaniques vs texture de peinture macroscopique).                                                                                                                 | Écarté du pipeline principal.                                                                                                                                                                                              |
| **Curacel Car Damage**                                                               | 6 839 images de véhicules accidentés ou endommagés sur le terrain.                                                                                                                               | **Moyenne à Élevée** : Utile pour confronter l'IA à la diversité chromatique des constructeurs et aux environnements extérieurs complexes.                                                                                                                           | Écarté du pipeline principal.                                                                                                                                                                                              |
| **Dataset Propriétaire MALLOULIAUTO v0.1** *(À construire — première version)* | 450-500 patches macroscopiques haute résolution avec métadonnées complètes et labels*Origine / Repeint*, capturés avec Setup F. Les cas sans vérité terrain fiable sont exclus du dataset. | **Maximale** : Cible métier unique et cœur de la R&D du produit **MALLOULIAUTO**.                                                                                                                                                                                  | **Dataset d'entraînement principal (Semaine 5)**. Cette première version sera enrichie si les résultats de validation révèlent un manque de représentativité ou un surapprentissage.                            |

Les datasets publics servent uniquement pour tester le pipeline.

Cette découverte confirme scientifiquement la nécessité de constituer un dataset propriétaire cohérent avec le setup d'acquisition final, sans mélange de sources hétérogènes.

### 4.9. Stratégie d'entraînement progressive

Le développement du modèle est organisé en deux étapes.

La première étape établit une baseline exploitant le signal texture (peau d'orange), signal physique principal du projet.

La seconde étape ajuste le seuil de rejet de confiance et développe le système d'agrégation multi-patches.

---

#### Phase 1 — Entraînement de la tête de classification (Backbone gelé)

Cette phase adapte rapidement le modèle au domaine spécifique de la peau d'orange en gelant les poids pré-entraînés d'ImageNet. Le modèle est entraîné sur **2 classes binaires** (Origine / Repeint) uniquement.

Pipeline :

```text
        Capture Macroscopique
    (smartphone + Module Apexel tout-en-un)
               │
               ▼
     Prétraitement OpenCV minimal
    (Redimensionnement 384 ×384 )
               │
               ▼
    Normalisation Keras
    (preprocess_input EfficientNet)
               │
               ▼
        EfficientNet-B0 Backbone (Gelé)
        (Poids ImageNet préservés)
               │
               ▼
        Tête de classification personnalisée
        (Dense + Softmax 2 classes)
               │
               ▼
        Origine / Repeint (avec score de confiance)
```

Configuration Phase 1 :

- **Epochs** : 15-20
- **Learning rate** : 1e-3
- **Batch size** : 32
- **Optimiseur** : Adam
- **Loss** : Categorical crossentropy
- **Nombre de classes** : 2 (Origine / Repeint)

Objectifs :

- obtenir une première mesure de performance sur le signal texture ;
- calculer les KPI du benchmark ;
- évaluer la robustesse du modèle dans les conditions d'acquisition retenues ;
- identifier les principales erreurs du modèle.

Métriques évaluées :

| Métrique         | Objectif                      |
| :---------------- | :---------------------------- |
| AUC               | Séparation Origine / Repeint |
| Recall Repeint    | Réduction des faux négatifs |
| F1-score          | Équilibre précision/rappel  |
| Matrice confusion | Analyse des erreurs           |

---

#### Phase 2 — Fine-tuning des dernières couches + Optimisation du seuil de rejet

Cette phase affine les représentations spécifiques au signal texture macroscopique en dégelant les dernières couches du backbone. Le seuil de rejet de confiance est ensuite optimisé sur le jeu de validation.

Configuration Phase 2 :

- **Epochs** : 10-15 supplémentaires
- **Learning rate** : 1e-5 (réduit)
- **Couches dégelées** : Dernières 30 couches d'EfficientNet-B0
- **Régularisation** : Dropout 0.3, Early stopping
- **Optimisation du seuil de rejet** : Grid search sur le jeu de validation (valeur initiale : 0.65)

---

#### Système d'Agrégation Multi-Patches par Vote Pondéré

Après classification individuelle de chaque patch et application du seuil de rejet, une couche d'agrégation simple produit le verdict au niveau du véhicule par **vote majoritaire pondéré par la confiance**.

**Méthode d'agrégation** :

```text
Pour chaque véhicule :
    1. Récupérer les prédictions des 15-20 patches (classe prédite + score de confiance)
    2. Exclure les patches dont la confiance < seuil de rejet (état Incertain)
    3. Sur les patches retenus, calculer le vote pondéré :
       - Score global "Repeint" = Σ (confiance des patches classés Repeint)
       - Score global "Origine" = Σ (confiance des patches classés Origine)
    4. Verdict du véhicule = classe avec le score global le plus élevé
    5. Si aucun patch retenu (tous rejetés par le seuil) → Véhicule INCERTAIN
```

**Justification méthodologique** :

Le vote majoritaire pondéré par la confiance est une approche **statistiquement justifiable** et **cohérente avec le paradigme Deep Learning** du projet. Elle évite l'introduction de règles arbitraires (seuils fixés manuellement) et laisse le modèle exprimer sa confiance globale via l'accumulation des scores. Cette approche est standard en classification par patches en vision industrielle.

Cette méthode présente trois avantages :

1. **Simplicité** : Aucun hyperparamètre arbitraire à optimiser au niveau de l'agrégation.
2. **Cohérence** : Respecte le principe "le modèle apprend seul", sans règles manuelles.
3. **Robustesse** : Un patch très confiant (0.95) pèse plus qu'un patch peu confiant (0.55), ce qui est statistiquement justifié.

Le seul paramètre à optimiser reste le **seuil de rejet de confiance** (valeur initiale 0.65), déterminé par grid search sur le jeu de validation.

---

## 5. Protocole Benchmark v0

| Composante du Protocole               | Valeur de Référence Expérimentale & Spécifications R&D                                                                                                                                                                                                            |
| :------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Configuration Retenue**       | Setup F (Xiaomi Redmi Note 12 + Module Macroscopique Apexel tout-en-un)                                                                                                                                                                                               |
| **Signal Principal Exploité**  | Micro-texture macroscopique de surface (peau d'orange)                                                                                                                                                                                                                |
| **Classes Entraînées**        | Origine / Repeint (binaire)                                                                                                                                                                                                                                           |
| **État de Sortie Additionnel** | Incertain (généré par seuil de rejet de confiance)                                                                                                                                                                                                                 |
| **Résolution d'Entrée**       | Format strict et standardisé de**(384×384) pixels**                                                                                                                                                                                                           |
| **Modèle / Backbone**          | Architecture cible**EfficientNet-B0** *(Transfer Learning)*                                                                                                                                                                                                   |
| **Framework**                   | **Keras / TensorFlow** *(compatibilité TensorFlow Lite pour déploiement mobile futur)*                                                                                                                                                                      |
| **Approche**                    | Classification par patch + Seuil de rejet + Agrégation par vote pondéré par confiance                                                                                                                                                                              |
| **Variables Contrôlées**      | Véhicule, pièce, zone de carrosserie, distance module-surface (contact 5-10 mm), éclairage LED intégré, Xiaomi Redmi Note 12 en mode Pro, 2 patches par pièce sur 6-8 pièces par véhicule.                                                                    |
| **Variables Testées**          | Marque/modèle de véhicule, couleur de carrosserie, conditions lumineuses résiduelles.                                                                                                                                                                              |
| **Critères d'Inclusion**       | Patch parfaitement net, contact effectif module-surface, matrice de métadonnées contextuelles complète, capture réalisée avec paramètres ISP contrôlés manuellement.                                                                                          |
| **Critères d'Exclusion**       | Flou, mauvais contact module-surface, éclairage LED défaillant, patch avec confiance modèle inférieure au seuil (marqué Incertain), annotation incertaine non marquée.                                                                                          |
| **Sorties Attendues (KPI)**     | **AUC** *(Séparation)*, **Recall Repeint** *(Sensibilité)*, **F1-score inter-smartphones** *(Robustesse ISP)*, **Accuracy véhicule** *(Verdict global après agrégation)*, **Taux d'Incertain** *(Proportion de rejets)*. |

---

## 6. Livrables et Objectifs Expérimentaux Cibles

> **Note** : Les valeurs ci-dessous sont des **objectifs expérimentaux cibles** et non des seuils de réussite garantis. Ils seront évalués et discutés à la lumière des résultats réels obtenus. En cas de non-atteinte, une analyse des causes racines et des propositions d'amélioration constitueront un livrable à part entière.

Le projet doit impérativement produire :

- une matrice de benchmark ;
- un dataset macroscopique v0.1 documenté ;
- un prototype IA de classification patch + seuil + agrégation ;
- un rapport d'évaluation ;
- des recommandations produit ;
- une roadmap d'industrialisation.

Les objectifs expérimentaux cibles sont fixés à :

- **AUC par patch** $\ge$ 0,85.
- **Recall Repeint par patch** $\ge$ 0,90.
- **Accuracy véhicule** $\ge$ 0,80 après agrégation multi-patches.
- **Temps de traitement** $\le$ 90 secondes par véhicule (capture + inférence).
- **Analyse d'erreurs** : au moins 5 causes racines identifiées et expliquées.

## 7. Perspectives d'évolution

* **Développement d'une application mobile dédiée** : Le déploiement final du produit MALLOULIAUTO nécessitera le développement d'une application mobile native (Android et iOS) qui remplacera l'application caméra générique du smartphone. Cette application accédera directement au capteur photographique via les APIs bas-niveau du système d'exploitation (**CameraX** sur Android, **AVFoundation** sur iOS) pour contrôler programmatiquement l'ensemble des paramètres de capture : désactivation forcée du Beauty Mode, du HDR automatique, du mode Portrait et de tous les filtres computationnels ; verrouillage de l'exposition, de la balance des blancs et de la mise au point ; imposition de la résolution maximale et du format RAW/DNG lorsque supporté. L'utilisateur final n'aurait aucune manipulation technique à effectuer, garantissant la reproductibilité des captures inter-utilisateurs et inter-smartphones. L'application intégrerait également un masque graphique à l'écran, un verrouillage par **gyroscope** bloqué à 45° et une analyse de l'histogramme RGB en temps réel pour intercepter et rejeter les clichés aberrants (*hard cases*) avant l'inférence. Le développement de cette application est **hors périmètre du stage actuel** (contraintes de temps sur les 8 semaines) et constitue la première étape prioritaire de la roadmap V1 pour le déploiement industriel.
* **Extension colorimétrique par comparaison intra-véhicule** : Pour renforcer la sensibilité du modèle sur les cas de réparations partielles haut de gamme où la signature texturale seule serait insuffisante, une évolution future du produit pourrait exploiter une référence colorimétrique interne au véhicule (typiquement le toit, statistiquement rarement repeint). Cette approche calculerait un écart colorimétrique (ΔE, espace CIELAB) entre le panneau de référence et la pièce inspectée, directement à partir du Setup F existant sans matériel supplémentaire. Elle nécessiterait une calibration empirique préalable du seuil de décision, les valeurs ΔE issues d'une capture smartphone terrain n'étant pas comparables aux seuils spectrophotométriques de laboratoire (typiquement ΔE > 2.0 sous éclairage D65 standardisé).
* **Filtrage de la luminance (Double espace)** : L'espace sRGB natif mélange la couleur et l'intensité lumineuse sur ses canaux, ce qui rend l'analyse sensible à la météo du parking. Une évolution possible consisterait à passer temporairement en espace **CIELAB** pour normaliser la brillance sur le canal de luminance ($L$), puis à repasser en sRGB. L'utilité serait de neutraliser les biais d'éclairement tout en conservant le format 3 canaux sRGB requis pour le **Transfer Learning** d'EfficientNet-B0.
* **Extension avec descripteurs de texture classiques** : Si les résultats du stage révèlent des cas difficiles où EfficientNet-B0 confond systématiquement Origine et Repeint sur certaines textures, une approche hybride combinant les prédictions du CNN avec des descripteurs de texture classiques (filtres de Gabor, Laplacien, Local Binary Patterns) pourrait être explorée. Cette piste reste **hors périmètre du stage actuel** car elle contredirait le principe méthodologique d'apprentissage automatique par le modèle, mais constitue une évolution potentielle en cas de plafonnement des performances.
* **Enrichissement du dataset v0.1** : Si les résultats du stage révèlent un manque de représentativité (surapprentissage sur certaines marques, couleurs ou conditions), une session de collecte élargie sera planifiée en post-stage pour construire une version v0.2 avec 1000+ patches diversifiés.

---

## 8. Limites de l'étude

Une démarche scientifique rigoureuse exige d'identifier explicitement les limites de ce travail. Les limites suivantes sont reconnues dès le cadrage du projet.

| Limite                                                        | Description                                                                                                                                                                                                                         | Impact potentiel                                                                                                                                       |
| :------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Volume limité du dataset v0.1**                      | 450-500 patches issus de 30-50 véhicules constituent une première version exploratoire.                                                                                                                                           | Risque de surapprentissage sur les marques et couleurs sur-représentées dans le dataset. Nécessitera un enrichissement pour une version production. |
| **Un seul module macro testé**                         | Le Setup F (Apexel tout-en-un) est le seul dispositif d'acquisition macroscopique évalué expérimentalement. D'autres modules (Sandmarc 40x, Moment Macro) pourraient offrir des performances différentes.                       | Le choix du setup optimal est conditionné à la disponibilité matérielle, pas à une comparaison exhaustive de l'ensemble des modules du marché.   |
| **Absence de validation multi-saisons**                 | Toutes les captures sont réalisées durant l'été 2026 (Juillet-Août). Les performances pourraient varier en conditions hivernales (humidité, givre, éclairage différent).                                                    | Le système n'a pas été validé sur des conditions climatiques diversifiées.                                                                        |
| **Absence de validation inter-pays**                    | Le dataset est constitué uniquement sur des véhicules disponibles en Tunisie. Les standards de peinture, les marques dominantes et les pratiques de carrosserie varient selon les marchés.                                       | La généralisation à d'autres marchés géographiques n'est pas garantie sans adaptation du dataset.                                                 |
| **Grossissement réel non certifié**                   | Le grossissement réel du module Apexel n'est pas celui annoncé par le fabricant (~10x mesuré vs 200x revendiqué). La résolution effective est une estimation préliminaire à confirmer par mesure avec règle de calibration. | Les chiffres de résolution effective cités dans ce document sont des estimations à valider expérimentalement en Semaine 4.                         |
| **Vérité terrain dépendante de l'expertise humaine** | L'annotation Origine/Repeint repose sur l'historique d'atelier ou l'expertise visuelle d'un carrossier, avec une incertitude inhérente sur les cas frontières.                                                                    | Une mauvaise annotation de quelques images peut réduire la performance du modèle de manière non traçable.                                          |
| **Application mobile hors périmètre**                 | Ce stage produit un pipeline de classification, pas une application mobile déployée. Le comportement en conditions d'utilisation réelle (opérateur non expert, pression de l'environnement) n'est pas évalué.                 | Les résultats du stage servent à valider la faisabilité technique, pas la robustesse en usage terrain non supervisé.                               |

---

## 9. Références & Matériel Validé

- **[Dong et al., AAAI 2024]** — *Exploiting Polarized Material Cues for Robust Car Detection* — [https://arxiv.org](https://arxiv.org)
- **[Code associé PCDNet]** — *Framework de détection polarisée* — [https://github.com](https://github.com)
- **[ISRA Vision]** — *Car Paint Vision Systems for Industrial Automation* — [https://isravision.com](https://isravision.com)
- **[Micro-Epsilon]** — *reflectCONTROL Automotive Defect Detection* — [https://micro-epsilon.com](https://micro-epsilon.com)
- **[Semitela et al., Sensors 2025]** — *Combining Deflectometry and Deep Learning (ResNet-50) for Car Body Paint Inspection* — [https://doi.org](https://doi.org)
- **[OpenCV Documentation]** — *Color Constancy Framework (xphoto::GrayworldWB)* — [https://opencv.org](https://opencv.org)
- **[Université de Helsinki]** — *Computer Vision Combined with Smartphone Helps See Colours Accurately* — [https://helsinki.fi](https://helsinki.fi)
- **[DeFelsko]** — *Automotive Paint Inspection (Paint Meters)* — [https://defelsko.com](https://defelsko.com)
- **[CarVertical]** — *Guide jauge d'épaisseur de peinture automobile* — [https://carvertical.com](https://carvertical.com)
- **[Apexel]** — *Smartphone Macro Lens Documentation* — [https://apexeloptic.com](https://apexeloptic.com)

---

### Spécifications Matériel Validées pour Commande (Setup F Retenu)

- **Module Macroscopique Smartphone Tout-en-Un (Priorité Haute)** : *Apexel Macro Microscope with integrated LEDs and CPL Filter* (37 €). Module clip-on universel offrant un grossissement macro avec LEDs intégrées et filtre polarisant CPL intégré, compatible avec la majorité des smartphones. Étui de transport inclus.
  - https://www.amazon.fr/Microscope-200X-smartphone-microscope-num%C3%A9rique/dp/B09QGQYG39?th=1

---

### Matériel étudié mais non commandé (Références SOTA)

- **NEEWER NL-36AI + Filtre CPL séparé (Setup C initialement envisagé)** : Approche par éclairage rasant et polarisation avec accessoires séparés. Écartée car résolution effective insuffisante à 40 cm comparée au Setup F macroscopique, et complexité opérationnelle liée à la gestion d'accessoires séparés (LED + CPL + trépied).
- **ColorChecker Classic Mini (Priorité Optionnelle)** : Mire physique étalonnée à 24 patchs pour l'étalonnage scientifique témoin en cas de dérive labo (Setup D). (£74.00)

  - [Lien Officiel : Calibrite.com](https://calibrite.com/product/colorchecker-classic-mini/)
- **Spectro 1 Mobile Spectrophotometer (Setup B)** : Appareil de captation spectrale ponctuelle multi-bandes pour l'extraction de signatures pigmentaires pures. Écarté du produit V1 car il fournit une mesure locale isolée et non une image 2D complète, le rendant incompatible avec un modèle CNN. ($299.99)

  - [Lien Commercial : Amazon.com](https://www.amazon.com/Spectro-Spectrophotometer-Matching-Analysis-Quality/dp/B0B4TWMRDJ)
- **Rhopoint TAMS - Total Appearance Measurement System (Setup E)** : Équipement industriel lourd de déflectométrie mesurant la distorsion des reflets de motifs structurés (waviness, DOI, défauts). Écarté car il s'agit d'un système de métrologie fixe au coût prohibitif, impossible à transposer pour un déploiement embarqué autonome de poche.

  - [Lien Constructeur : RhopointAmericas.com](https://www.rhopointamericas.com/product/rhopoint-tams-total-appearance-measurement-system/)
- **Caméras industrielles USB (Basler, IDS, FLIR)** : Solutions professionnelles évaluées mais écartées du stage pour trois raisons : (1) coût prohibitif (500-3000€), (2) nécessité d'un ordinateur portable en permanence, (3) résolution nominale inférieure au smartphone (1-5 MP contre 48 MP). Positionnées en perspective V2 pour un poste fixe d'inspection.
