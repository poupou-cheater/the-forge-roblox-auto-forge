import keyboard
import time
import pyautogui
import random
import win32gui
import sys # Nécessaire pour sys.exit() en cas d'erreur ou d'arrêt
from typing import Tuple 

# =======================================================
# === 1. CONFIGURATION INTERNE (FACILE À MODIFIER) ===
# =======================================================

CONFIG_DATA = {
    # Coordonnées et limites
    'BOUTON_START_X': 738,
    'BOUTON_START_Y': 846,
    'Y_TOP': 704,
    'Y_DOWN': 1536,
    'X_MIN': 700,
    'X_MAX': 750,
    
    # Paramètres de l'application et de la vitesse
    'APP_TARGET': "Roblox",
    'DURATION_DOWN': 0.05, 
    'DURATION_UP': 0.01, 
    'TWEEN': None # Mettre 'None' (str) ou 'linear', 'easeInQuad', etc.
}

# =======================================================
# === 2. DÉCLARATION ET INITIALISATION DES VARIABLES ===
# =======================================================

# Récupération des variables à partir du dictionnaire (Conversion automatique des types)
APP_TARGET = CONFIG_DATA['APP_TARGET']

# Tuple de coordonnées
BOUTON_START = (CONFIG_DATA['BOUTON_START_X'], CONFIG_DATA['BOUTON_START_Y']) 

# Coordonnées simples
Y_TOP = CONFIG_DATA['Y_TOP']
Y_DOWN = CONFIG_DATA['Y_DOWN']
X_MIN = CONFIG_DATA['X_MIN']
X_MAX = CONFIG_DATA['X_MAX']

# Durées et transition
DURATION_DOWN = CONFIG_DATA['DURATION_DOWN']
DURATION_UP = CONFIG_DATA['DURATION_UP']
TWEEN = CONFIG_DATA['TWEEN'] # Python gère déjà le None si vous l'avez écrit comme tel.

# Nettoyage des imports inutiles pour cette méthode : configparser et os sont retirés.

# =======================================================
# === 3. LOGIQUE PRINCIPALE DU SCRIPT ===
# =======================================================

print("-" * 30)
print(f"Application cible : {APP_TARGET}")
print(f"Coordonnées de départ : {BOUTON_START}")
print("Hold G = CLICK MAINTENU & MOUVEMENT ACTIF, Release G = STOP")
print("Press Ctrl+C pour arrêter le script.")
print("-" * 30)


click_held = False 

try:
    while True:

        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        
        # Vérifie si la fenêtre cible est active
        if APP_TARGET in title:
            if keyboard.is_pressed("g"):

                if not click_held:
                    click_held = True
                    # Déplacement initial vers le bouton
                    pyautogui.moveTo(BOUTON_START[0], BOUTON_START[1], duration=0.1)
                    pyautogui.mouseDown(button='left') 
                    print("--- HOLD CLICK START & MOUVEMENT ACTIF ---")
                
                # Mouvement vers le bas
                random_x = random.randint(X_MIN, X_MAX)
                pyautogui.moveTo(random_x, Y_DOWN, 
                                 duration=DURATION_DOWN, 
                                 tween=TWEEN) 
                
                # Mouvement vers le haut
                random_x = random.randint(X_MIN, X_MAX) 
                pyautogui.moveTo(random_x, Y_TOP, 
                                 duration=DURATION_UP, 
                                 tween=TWEEN)

            else:
                # La touche 'g' n'est pas pressée
                if click_held:
                    click_held = False
                    pyautogui.mouseUp(button='left') 
                    print("--- HOLD CLICK STOP & MOUVEMENT ARRÊTÉ ---") 
        
        # Pause pour éviter de surcharger le CPU
        time.sleep(0.01)
        

except KeyboardInterrupt:
    print("\nScript arrêté par l'utilisateur.")
except Exception as e:
    print(f"\nUne erreur inattendue s'est produite: {e}")
finally:
    # S'assure de relâcher le clic en cas d'arrêt du script
    if click_held:
        pyautogui.mouseUp(button='left')

# L'appel à sys.exit(1) est nécessaire seulement dans la fonction load_config
# s'il y a des erreurs critiques. Dans le code principal, les exceptions gèrent l'arrêt.
