# Rapport d'entraînement — Dataset propriétaire atelier

**Projet :** MALLOULINOVA / MALLOULIAUTO  
**Référence :** MALL-STG-ETE-2026-PAINT-01  
**Type d'étude :** preuve de faisabilité exploratoire  
**Dispositif :** Redmi Note 12 + module Apexel  
**Date de dernière exécution documentée :** 21 août 2026

---

## 1. Objectif

L'objectif de cette expérimentation est d'évaluer si des images macro-texturales acquises avec un smartphone Redmi Note 12 et un module Apexel contiennent un signal permettant de distinguer des surfaces automobiles :

- `origine` ;
- `repeint`.

L'étude porte principalement sur les variations de texture, les différences de brillance et les irrégularités de finition observables à courte distance.

Le résultat recherché est une première validation de faisabilité et non une validation industrielle du produit.

---

## 2. Dataset utilisé

Le dataset propriétaire pilote contient actuellement :

```text
Nombre total : 264 images
Origine      : environ 157 images
Repeint      : environ 107 images
```

Répartition utilisée pour l'entraînement :

| Sous-ensemble | Origine | Repeint | Total |
|---|---:|---:|---:|
| Train | 112 | 54 | 166 |
| Validation | 23 | 24 | 47 |
| Test | 22 | 29 | 51 |

Les images ont été réparties à l'aide des métadonnées de session. La séparation par véhicule doit continuer à être vérifiée lorsque les identifiants sont disponibles.

---

## 3. Prétraitement

Les étapes utilisées sont :

1. chargement des images depuis `dataset_final_splits_v2/` ;
2. redimensionnement en `384 × 384` pixels ;
3. recadrage central fixe de 32 pixels par côté pour réduire l'influence des bords lumineux ;
4. redimensionnement de la zone conservée vers `384 × 384` ;
5. normalisation attendue par EfficientNet-B0 ;
6. data augmentation modérée appliquée uniquement pendant l'entraînement.

Le recadrage central de 64 pixels par côté n'a pas été retenu, car il supprimait une partie trop importante de la texture utile.

---

## 4. Data augmentation

Les transformations utilisées sont modérées :

- retournement horizontal ;
- rotation légère ;
- translation légère ;
- zoom léger ;
- variation modérée du contraste ;
- variation modérée de la luminosité.

Les transformations ne sont pas appliquées aux jeux Validation et Test.

---

## 5. Modèle

Le modèle utilisé est un EfficientNet-B0 pré-entraîné sur ImageNet avec une tête de classification binaire.

Architecture :

```text
Image 384×384×3
      ↓
Crop central fixe
      ↓
Redimensionnement 384×384
      ↓
Data augmentation pendant Train
      ↓
EfficientNet-B0
      ↓
GlobalAveragePooling2D
      ↓
Dropout 0,5
      ↓
Dense 128
      ↓
Dropout 0,3
      ↓
Softmax 2 classes
      ↓
origine / repeint
```

### Phase 1

- backbone gelé ;
- learning rate : `1e-3` ;
- pondération des classes ;
- EarlyStopping ;
- ReduceLROnPlateau.

### Phase 2

- fine-tuning limité ;
- cinq dernières couches potentiellement entraînables ;
- BatchNorm conservées gelées ;
- learning rate : `1e-5` ;
- EarlyStopping ;
- sauvegarde du meilleur checkpoint.

---

## 6. Résultats du dernier entraînement

Le dernier entraînement documenté a produit les résultats suivants sur le jeu de test :

| Métrique | Résultat |
|---|---:|
| Test loss | 0,8098 |
| Accuracy | 0,6863 |
| Balanced accuracy | 0,7132 |
| F1 macro | 0,6832 |
| Precision Origine | 0,5882 |
| Recall Origine | 0,9091 |
| F1 Origine | 0,7143 |
| Precision Repeint | 0,8824 |
| Recall Repeint | 0,5172 |
| F1 Repeint | 0,6522 |
| AUC Repeint | 0,6755 |
| Nombre d'erreurs | 16 / 51 |

Matrice de confusion :

```text
                 Prédit origine   Prédit repeint
Vrai origine            20                 2
Vrai repeint            14                15
```

---

## 7. Interprétation

Le modèle reconnaît correctement une grande partie des surfaces d'origine :

```text
20/22 images Origine correctement classées
```

La classe `Repeint` est reconnue dans :

```text
15/29 images
```

La précision de la classe `Repeint` est élevée, mais son rappel reste limité. Le modèle manque donc encore plusieurs surfaces repeintes et les classe comme `Origine`.

L'AUC de `0,6755` indique une séparation probabiliste modérée. Le système contient donc un signal exploitable, mais ce signal n'est pas suffisamment stable pour une utilisation industrielle.

---

## 8. Seuils de décision

Le seuil exploratoire de classification de la classe `Repeint` a été recherché sur le jeu de validation. Une valeur proche de `0,52` a été observée dans cette expérience.

La règle de classification est :

```text
p(repeint) ≥ 0,52 → repeint
p(repeint) < 0,52 → origine
```

Un seuil de rejet séparé peut produire l'état `Incertain` :

```text
confiance maximale < 0,65 → Incertain
```

Ces seuils ne doivent pas être considérés comme définitifs. Ils doivent être confirmés sur un dataset plus représentatif.

---

## 9. Analyse de l'overfitting

Les courbes montrent généralement une amélioration plus rapide de l'accuracy d'entraînement que de l'accuracy de validation. La validation reste plus faible et la validation loss augmente après les premières époques.

Cela indique :

- un surapprentissage partiel ;
- une variabilité importante des images ;
- une différence entre les sessions d'acquisition ;
- un dataset encore petit pour un modèle de Deep Learning ;
- une possible influence de la couleur, de la pièce, de l'éclairage et du cadrage.

La régularisation, le crop central, la data augmentation modérée et le fine-tuning limité réduisent le risque, mais ne suppriment pas complètement l'overfitting.

---

## 10. Limites

- Dataset propriétaire encore limité.
- Classes déséquilibrées.
- Validation réalisée sur un petit nombre d'images.
- Variabilité entre véhicules, pièces, couleurs et sessions.
- L'Apexel présente un vignettage dans certains modes de capture.
- Les performances peuvent être influencées par les conditions d'acquisition.
- La validation par véhicule doit être renforcée.
- Aucun modèle industriel final n'est validé.

---

## 11. Conclusion

Le pipeline complet de classification a été exécuté sur un dataset automobile propriétaire acquis avec un Redmi Note 12 et un module Apexel. Les résultats obtenus montrent une possibilité d'exploiter les caractéristiques macro-texturales pour distinguer des surfaces d'origine et repeintes.

La performance actuelle constitue une preuve de faisabilité partielle. Elle ne permet toutefois pas de garantir une généralisation fiable à de nouveaux véhicules ou à de nouvelles sessions d'acquisition.

Les prochaines améliorations prioritaires sont :

1. augmenter la diversité des véhicules et des pièces ;
2. améliorer la représentation des surfaces repeintes dans Train ;
3. contrôler davantage l'éclairage et la mise au point ;
4. appliquer une séparation stricte par véhicule ;
5. évaluer plusieurs sessions indépendantes ;
6. analyser les erreurs avec l'expertise de l'atelier ;
7. optimiser le seuil `Incertain` sur un jeu de validation plus grand.
