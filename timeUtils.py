import time
from datetime import datetime


def waitDate(dateStr: str):
    """
    Attend précisément jusqu'à une date et heure précises.

    :param date_cible: Date et heure de fin au format 'YYYY-MM-DD HH:MM:SS'.
    """
    # Convertir la date cible en objet datetime
    date_cible_datetime = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")

    # Obtenir l'heure actuelle
    now = datetime.now()

    # Calculer la durée restante en secondes
    remainingTime = (date_cible_datetime - now).total_seconds()

    # Vérifier si la date cible est dans le passé
    if remainingTime < 0:
        print(f"La date cible {dateStr} est déjà passée.")
        return

    print(f"Temps à attendre : {remainingTime} secondes.")

    # Attendre pendant le temps restant
    time.sleep(remainingTime)

    print(f"Date cible atteinte : {dateStr}")

