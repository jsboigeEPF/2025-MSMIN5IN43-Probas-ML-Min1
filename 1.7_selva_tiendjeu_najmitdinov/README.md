# 📉 Projet 1.7 (Sujet B) : Processus Gaussiens & Quantification d'Incertitude

> **Projet :** MSMIN5IN43 - IA probabiliste, théorie de jeux et machine learning  
> **École :** EPF Engineering School  
> **Auteur :** Selva Vicram, Tiendjeu Yannick, Najmitdinov Alekseï

Ce projet explore l'utilisation des **Processus Gaussiens (Gaussian Processes)** pour la régression non-linéaire et, surtout, pour la **quantification rigoureuse de l'incertitude** dans les modèles d'IA.

---

## 🎯 Objectif du projet

Contrairement aux réseaux de neurones classiques qui donnent souvent une prédiction ponctuelle avec une fausse confiance (overconfidence), ce projet vise à construire un modèle "honnête" capable de dire "Je ne sais pas".

* **Modélisation Non-Linéaire :** Apprendre des fonctions complexes (ex: $x \sin(x)$) à partir de peu de données.
* **Quantification d'Incertitude :** Distinguer les zones de certitude (proches des données) des zones d'inconnu (extrapolation).
* **Gestion du Bruit :** Séparer le signal réel du bruit de mesure inhérent aux capteurs via un noyau composite.

### 💡 Cas d'usage
* 🏥 **Médecine :** Diagnostiquer une maladie seulement si la certitude est > 99%.
* 💰 **Finance :** Estimer non seulement le prix futur d'un actif, mais aussi le risque (volatilité) associé.
* 🤖 **Robotique :** Planification de trajectoire sûre (éviter les zones où le robot est "incertain" de l'environnement).

---

## 🏗️ Architecture du projet
```plaintext
gp-uncertainty-project/
├── src/
│   ├── main.py                 # 🚀 Script principal (Simulation & Visualisation)
│   └── presentation.ipynb      # 📓 Notebook Jupyter pour la démo interactive
├── results/
│   └── resultat_gp.png         # 📊 Graphique de sortie (Preuve de concept)
├── README.md                   # 📄 Ce fichier de documentation
└── requirements.txt            # ✅ Liste des dépendances
```

---

## 🧠 Concepts Mathématiques Clés

### 1. Le Processus Gaussien (GP)
Un GP n'apprend pas des paramètres (poids), il apprend une distribution sur des fonctions.

Pour tout ensemble de points $x$, la distribution des sorties $f(x)$ est une gaussienne multivariée :

$$ f(x) \sim \mathcal{GP}(m(x), k(x, x')) $$

### 2. Le Noyau (Kernel) RBF
C'est le cœur du modèle. Il définit la similarité entre deux points. Si deux points $x$ et $x'$ sont proches, leurs sorties $f(x)$ et $f(x')$ doivent être corrélées.

$$ k(x, x') = \sigma_f^2 \exp\left(-\frac{(x-x')^2}{2l^2}\right) $$

* $l$ (length_scale) : Contrôle la "douceur" de la fonction.
* $\sigma_f^2$ : Contrôle l'amplitude verticale.

### 3. Gestion du Bruit (White Kernel)
Pour gérer des données réelles (bruitées), nous ajoutons un terme de bruit blanc à la diagonale de la matrice de covariance :

$$ K_{y} = K_{f} + \sigma_n^2 I $$

Cela permet au modèle de ne pas sur-apprendre (overfit) le bruit des observations.

---

## ⚙️ Choix Techniques & Justification

Bien que le sujet suggère initialement l'utilisation de GPyTorch (orienté Deep Learning/GPU), nous avons fait un choix d'ingénierie différent pour ce cas d'usage précis.

| Critère | GPyTorch (Suggéré) | Scikit-Learn (Choisi) |
|---------|-------------------|----------------------|
| **Méthode de Calcul** | Approximation Variationnelle (VI) | Inférence Exacte (Algèbre Linéaire) |
| **Cible** | Big Data (> 100k points) | Small Data & Pédagogie (< 1k points) |
| **Précision** | Dépend de l'optimisation | Mathématiquement parfaite |
| **Complexité** | Élevée (Boucles d'optimisation manuelles) | Faible (API unifiée .fit()) |

**Verdict :** Pour une démonstration pédagogique sur la quantification d'incertitude, l'approche exacte de scikit-learn offre une visualisation plus rigoureuse et une meilleure explicabilité que les approximations nécessaires au passage à l'échelle.

---

## 🚀 Installation & Utilisation

### Prérequis : Python 3.8+

**Cloner le projet :**
```bash
git clone lien/du/projet
cd le-fichier
```

**Installer les dépendances :**
```bash
pip install numpy matplotlib scikit-learn
```

**Lancer la simulation :**
```bash
python src/main.py
```

Cela générera le graphique `resultat_gp.png` montrant la régression et le tube d'incertitude.

---

## 🛠️ Stack Technique

| Catégorie | Outils |
|-----------|--------|
| **Modélisation** | scikit-learn (GaussianProcessRegressor) |
| **Noyaux (Kernels)** | RBF, WhiteKernel |
| **Calcul Matriciel** | numpy |
| **Visualisation** | matplotlib |

---

## 📈 Résultats Obtenus

Le modèle parvient à :

1. **Apprendre le signal :** La moyenne prédictive (ligne bleue) suit fidèlement la fonction cible $x\sin(x)$.
2. **Ignorer le bruit :** Grâce au WhiteKernel, il ne "course" pas après chaque point aberrant.
3. **Quantifier l'inconnu :** L'intervalle de confiance (zone bleue) s'élargit drastiquement dans les zones sans données ($x > 10$), illustrant l'incertitude épistémique.

---

## 🎓 Contexte Académique

Ce projet est réalisé dans le cadre du cours **IA Probabiliste (2025-2026)**.

* **École :** EPF Engineering School
* **Date de rendu :** 5 Janvier 2026
* **Présentation :** 6 Janvier 2026

**Critères de réussite :**
* ✅ Compréhension des enjeux probabilistes.
* ✅ Justification pertinente des choix technologiques.
* ✅ Qualité de la visualisation de l'incertitude.

---

## 📝 Licence

MIT License.

Projet réalisé pour l'exploration des modèles génératifs et probabilistes.