# Data Augmentation — Étude et Sélection des Techniques

**Référence :** MALL-STG-ETE-2026-PAINT-01  
**Semaine :** S4  
**Contexte :** Étude préparatoire à l'implémentation du pipeline Keras

---

## 1. Introduction

### 1.1. Qu'est-ce que la Data Augmentation ?

La data augmentation est une technique consistant à générer artificiellement de nouvelles images à partir d'un dataset existant, en appliquant des transformations qui préservent le label de l'image. Cette technique permet d'augmenter la diversité des données d'entraînement sans collecter de nouvelles images, améliorant ainsi la robustesse et la généralisation du modèle.

### 1.2. Pourquoi c'est important pour MALLOULIAUTO

Le dataset propriétaire MALLOULIAUTO v0.1 étant limité à 450-500 patches macroscopiques (voir §4 du planning), la data augmentation constitue un levier essentiel pour :

- Réduire le risque d'overfitting sur un petit dataset
- Simuler la variabilité des conditions terrain (luminosité, positionnement du module)
- Améliorer la robustesse inter-smartphones du modèle
- Augmenter virtuellement le volume d'entraînement sans coût matériel

---

## 2. Techniques Étudiées et Sélectionnées

Le tableau ci-dessous synthétise l'ensemble des techniques de data augmentation évaluées, leur principe, leur pertinence pour la détection macroscopique de la peau d'orange, et la configuration finale retenue pour le pipeline Keras du projet MALLOULIAUTO.

| Technique | Principe | Paramètre Keras | Analyse pour la peau d'orange (patches macroscopiques) | Décision | Configuration retenue |
|-----------|----------|-----------------|-------------------------------------------------------|:--------:|----------------------|
| **Rotation** | Rotation aléatoire de l'image dans une plage angulaire définie. Simule les légères variations d'angle de positionnement du module macroscopique sur la surface. | `RandomRotation` | La micro-texture du vernis est isotrope (pas de direction privilégiée), donc invariante à la rotation. Renforce la robustesse aux petites variations d'orientation du module Apexel lors du contact avec la carrosserie. Limiter à ±10-15° pour rester réaliste. | ✅ **Oui** | ±10 à 15° |
| **Flip horizontal** | Applique un effet miroir horizontal. Un patch d'aile gauche devient visuellement un patch d'aile droite. | `RandomFlip("horizontal")` | La texture macroscopique est identique quelle que soit son orientation spatiale. Double virtuellement le dataset sans introduire d'artefact. Utile car les pièces gauche/droite d'un véhicule ont la même signature texturale en macro. | ✅ **Oui** | Systématique |
| **Flip vertical** | Applique un effet miroir vertical. L'image est retournée haut-bas. | `RandomFlip("vertical")` | Physiquement irréaliste : les gouttes de peinture coulent vers le bas pendant le séchage, créant une direction privilégiée subtile visible en macro. Pourrait introduire des artefacts avec l'éclairage LED intégré au module qui a une orientation fixe. | ❌ **Non** | — |
| **Zoom** | Agrandissement ou réduction aléatoire de l'image. Simule les légères variations de distance entre le module et la surface. | `RandomZoom` | La peau d'orange macroscopique est un signal à échelle physique fixe (millimétrique). Un zoom trop important modifie artificiellement l'échelle de la texture et empêche la généralisation terrain. Zoom léger (±5-10%) acceptable pour simuler les petites variations de pression du module contre la carrosserie. | ⚠️ **Léger** | ±5 à 10% |
| **Translation** | Décalage aléatoire horizontal ou vertical de l'image. Simule un cadrage légèrement décalé de la zone cible. | `RandomTranslation` | La texture macroscopique étant homogène sur toute la zone capturée par le module Apexel, une translation ne change pas l'information utile. Renforce la robustesse au positionnement imprécis du module sur la carrosserie. | ✅ **Oui** | ±10% |
| **Luminosité** | Modification aléatoire de la luminosité globale. Simule les variations d'éclairage ambiant qui peuvent affecter le rendu même avec les LEDs intégrées. | `RandomBrightness` | Extrêmement utile pour simuler les différentes conditions lumineuses terrain (atelier, parking ombragé, lumière indirecte). Même avec les LEDs intégrées du module Apexel, la lumière ambiante influence légèrement le résultat. Éviter les valeurs extrêmes qui saturent ou sous-exposent. | ✅ **Oui** | ±10 à 20% |
| **Contraste** | Amplification ou atténuation des différences d'intensité entre pixels. Simule les variations de contraste liées à l'intensité de la lumière ambiante. | `RandomContrast` | Utile pour simuler les variations d'éclairage. Un contraste trop faible pourrait effacer les ombres révélatrices de la peau d'orange capturées par les LEDs du module. Un contraste trop élevé pourrait créer des artefacts. | ✅ **Oui** | ±10 à 15% |
| **Saturation** | Modification de la saturation des couleurs (couleurs plus vives ou plus pâles). | Custom (`tf.image`) | Le signal principal étant la texture macroscopique (pas la couleur), la saturation a peu d'impact direct. Peut néanmoins simuler les variations de rendu colorimétrique inter-smartphones (ISP) attendues lors des tests Semaine 7, renforçant la robustesse inter-marques. | ✅ **Oui** | ±10 à 15% |
| **Teinte (Hue)** | Décalage de la teinte globale (rouge → orange → jaune → vert...). Modifie la couleur perçue sans toucher à la texture. | Custom (`tf.image`) | Simule les variations de teinte entre différentes carrosseries (rouge, bleu, gris...). Force le modèle à apprendre la texture macroscopique indépendamment de la couleur de fond de la peinture. Décalage limité pour rester réaliste. | ✅ **Oui** | ±10 à 15° |
| **Bruit gaussien** | Ajout d'un bruit aléatoire à chaque pixel. Simule le bruit numérique du capteur smartphone (surtout à ISO élevé). | Custom (`GaussianNoise`) | Ambigu en mode macroscopique : le bruit peut être confondu avec la micro-texture fine de la peau d'orange révélée par le grossissement du module Apexel. Risque de dégrader la capacité du modèle à distinguer texture réelle vs bruit. En très faible quantité uniquement, peut renforcer la robustesse. | ⚠️ **Test** | σ < 0.02 |
| **Flou (Blur)** | Application d'un flou gaussien à l'image. Simule des captures légèrement floues (vibration, mise au point imparfaite). | Custom | Contre-productif : le flou détruit précisément la micro-texture macroscopique que le modèle doit apprendre. En mode macro, la netteté est critique pour capturer la peau d'orange en pixel-perfect. Rendrait le modèle moins discriminant sur les signaux texturaux fins. | ❌ **Non** | — |
| **Cutout / Random Erasing** | Masquage aléatoire d'une zone rectangulaire de l'image. Force le modèle à ne pas dépendre d'une seule région du patch. | Custom | Renforce la robustesse en obligeant le modèle à apprendre la texture macroscopique sur plusieurs zones du patch. Simule les cas où une partie du patch serait masquée par un reflet résiduel ou une poussière malgré le nettoyage préalable. Ne pas masquer plus de 15-20% de l'image. | ✅ **Oui** | 10-15% max |

### Justification Globale de la Sélection

La configuration retenue privilégie les augmentations qui :

1. **Préservent le signal texture macroscopique** (rotation, flip horizontal, translation, cutout modéré).
2. **Simulent les conditions terrain** (luminosité, contraste, variations de positionnement du module).
3. **Renforcent la robustesse inter-smartphones** (saturation, teinte) en prévision des tests de Semaine 7.
4. **Évitent la destruction du signal principal** (exclusion du flou, bruit minimal, pas de flip vertical).

Cette configuration est cohérente avec la **stratégie macroscopique** définie dans le `revue_SOTA.md` (§4.6) et sera implémentée dans le fichier `pipeline_initial.py` en Semaine 4.

---

## 3. Implémentation Prévue en Keras

### 3.1. Structure du Code Prévue

```python
import tensorflow as tf
from tensorflow.keras import layers

# Data augmentation pipeline pour MALLOULIAUTO V0.1
# Adapté aux patches macroscopiques (module Apexel tout-en-un)
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.04),          # ~15°
    layers.RandomTranslation(0.1, 0.1),
    layers.RandomZoom(0.05),
    layers.RandomBrightness(0.15),
    layers.RandomContrast(0.1),
    # Saturation et Hue via tf.image (custom layer)
])
```

### 3.2. Points d'Attention pour l'Implémentation

- Appliquer la data augmentation **uniquement sur le train set** (jamais sur le validation ou test set)
- Utiliser `training=True` explicite lors de l'appel
- Intégrer dans `tf.data.Dataset` pipeline pour performance optimale
- Documenter les paramètres exacts dans `config.yaml`

---

## 4. Conclusion

Cette étude préparatoire a permis d'identifier les techniques de data augmentation les plus pertinentes pour le projet MALLOULIAUTO, en privilégiant celles qui préservent le signal texture macroscopique (peau d'orange capturée en pixel-perfect par le module Apexel tout-en-un) tout en simulant la variabilité des conditions terrain.

La configuration retenue sera implémentée en Semaine 4 dans le fichier `pipeline_initial.py` et validée empiriquement avant l'entraînement du modèle EfficientNet-B0 binaire (Origine / Repeint) en Semaine 6.

---

## 5. Références

- Vidéo YouTube "Day 8 : Data Augmentation" (Playlist Computer Vision for Developers)
- Documentation Keras : https://keras.io/api/layers/preprocessing_layers/image_augmentation/
- Documentation TensorFlow : https://www.tensorflow.org/tutorials/images/data_augmentation