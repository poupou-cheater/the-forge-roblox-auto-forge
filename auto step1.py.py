import keyboard
import time
import pyautogui
import random
import win32gui
import configparser
import os  # <-- NOUVEL IMPORT NÉCESSAIRE
from typing import Tuple 

# --- FONCTION DE CHARGEMENT DE CONFIGURATION ---
def load_config(filename: str = 'config.cfg') -> Tuple:
    """Charge les données de configuration depuis un fichier CFG et retourne les variables."""
    config = configparser.ConfigParser()
    
    # 1. DÉTERMINER LE CHEMIN ABSOLU DU FICHIER DE CONFIGURATION
    # os.path.dirname(__file__) donne le répertoire où se trouve le script Python actuel.
    # os.path.join construit le chemin complet.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, filename)

    # 2. Tenter de lire le fichier en utilisant le chemin absolu
    if not config.read(config_path):
        # Affiche le chemin exact où il a cherché, ce qui est très utile pour le débogage.
        print(f"Erreur: Le fichier de configuration '{filename}' est introuvable ou vide au chemin: {config_path}")
        print("Veuillez créer un fichier 'config.cfg' avec les sections [COORDINATES] et [SETTINGS] DANS LE MÊME DOSSIER QUE LE SCRIPT.")
        exit() 

    # --- Lecture des coordonnées (le reste est inchangé) ---
    try:
        coords = config['COORDINATES']
        
        BOUTON_START = (coords.getint('BOUTON_START_X'), coords.getint('BOUTON_START_Y')) 
        Y_TOP = coords.getint('Y_TOP')
        Y_DOWN = coords.getint('Y_DOWN')
        X_MIN = coords.getint('X_MIN')
        X_MAX = coords.getint('X_MAX')
    except Exception as e:
        print(f"Erreur lors de la lecture des coordonnées: {e}. Vérifiez la section [COORDINATES].")
        exit()

    # --- Lecture des paramètres (le reste est inchangé) ---
    try:
        settings = config['SETTINGS']
        
        DURATION_DOWN = settings.getfloat('DURATION_DOWN')
        DURATION_UP = settings.getfloat('DURATION_UP')
        TWEEN = settings.get('TWEEN')
        if TWEEN and TWEEN.lower() == 'none':
            TWEEN = None
            
        APP_TARGET = settings.get('APP_TARGET')
    except Exception as e:
        print(f"Erreur lors de la lecture des paramètres: {e}. Vérifiez la section [SETTINGS].")
        exit()

    print(f"Configuration chargée avec succès depuis {config_path}.")
    return APP_TARGET, BOUTON_START, Y_TOP, Y_DOWN, X_MIN, X_MAX, DURATION_DOWN, DURATION_UP, TWEEN

# ... (le reste de votre script principal) ...

# --- CHARGEMENT DES VARIABLES AU DÉBUT DU SCRIPT ---
APP_TARGET, BOUTON_START, Y_TOP, Y_DOWN, X_MIN, X_MAX, DURATION_DOWN, DURATION_UP, TWEEN = load_config()

# Début de la logique principale
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