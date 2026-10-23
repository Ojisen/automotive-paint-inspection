## ways to reduce overfitting

- Add more data
- Data Augmentation
- Dropout
- Batch Norm
- Reduce complexity

# Data Augmentation

![1784124287325](image/rapport_test_data_augmentation/1784124287325.png)

📊 TABLEAU COMPARATIF — Impact de la Data Augmentation

| Métrique                 | Sans Augmentation | Avec Augmentation |
| :------------------------ | :---------------: | :---------------: |
| **Best Epoch**      |        29        |        13        |
| **Train Accuracy**  |      0.6264      |      0.5156      |
| **Val Accuracy**    |      0.5790      |      0.5074      |
| **Train Loss**      |      0.8996      |      1.1192      |
| **Val Loss**        |      1.0357      |      1.1981      |
| **Overfitting Gap** |      0.0474      |      0.0082      |

---

### 💡 VERDICT

* **✅ Réduction drastique de l'overfitting (de 82.7%)**
  * *Gap sans augmentation :* 0.0474
  * *Gap avec augmentation :* 0.0082
* **⚠️ Diminution de la performance globale**
  * La *validation accuracy* subit une baisse de **-7.2 points**.

# Visualisation des Images Augmentées

![1784124465781](image/rapport_test_data_augmentation/1784124465781.png)

# Inférence (Test Final)

![1784124525086](image/rapport_test_data_augmentation/1784124525086.png)
