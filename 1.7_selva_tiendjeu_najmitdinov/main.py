import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel

# --- 1. Génération de données synthétiques (Le "Ground Truth") ---
def target_function(x):
    """Une fonction sinusoïdale simple pour simuler un phénomène physique."""
    return x * np.sin(x)

# On génère des points d'entraînement aléatoires (observations bruitées)
rng = np.random.RandomState(42)
X_train = rng.uniform(0, 10, 20).reshape(-1, 1) 
y_train = target_function(X_train).ravel()
dy = 0.5 + 1.0 * rng.random(y_train.shape)
noise = rng.normal(0, dy)
y_train += noise

X_test = np.linspace(0, 15, 1000).reshape(-1, 1)

# RBF (Radial Basis Function) gère la "douceur" de la courbe.
# WhiteKernel gère le bruit des données (l'incertitude aléatoire).
kernel = 1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e2)) \
         + WhiteKernel(noise_level=1, noise_level_bounds=(1e-10, 1e+1))

gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

print("Entraînement du modèle...")
gp.fit(X_train, y_train)

# Prédiction : Le modèle renvoie la moyenne ET l'écart-type (sigma)
print("Calcul des prédictions et de l'incertitude...")
y_pred, sigma = gp.predict(X_test, return_std=True)

plt.figure(figsize=(12, 6))

plt.plot(X_test, target_function(X_test), 'r:', label=r'$f(x) = x \sin(x)$ (Vraie fonction)')

plt.errorbar(X_train.ravel(), y_train, dy, fmt='k.', markersize=10, label='Observations (Données)')

plt.plot(X_test, y_pred, 'b-', label='Prédiction (Moyenne GP)')

# On trace l'intervalle de confiance à 95% (1.96 * sigma)
plt.fill_between(X_test.ravel(), y_pred - 1.96 * sigma, y_pred + 1.96 * sigma,
                 alpha=0.2, color='blue', label='Incertitude (95% confidence)')

plt.title("Régression par Processus Gaussien : Quantification de l'Incertitude")
plt.xlabel("Input X")
plt.ylabel("Output f(X)")
plt.legend(loc='upper left')

filename = "resultat_gp.png"
plt.savefig(filename)
print(f"Graphique généré : {filename}")
plt.show()

print("\n--- Paramètres appris par le modèle ---")
print(f"Kernel final : {gp.kernel_}")
print(f"Log-marginal-likelihood : {gp.log_marginal_likelihood(gp.kernel_.theta):.3f}")