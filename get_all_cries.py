import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://play.pokemonshowdown.com/audio/cries/"
DOWNLOAD_DIR = "song/cries"

# 1. Crée le dossier s’il n’existe pas
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 2. Récupérer la page listant les fichiers
resp = requests.get(BASE_URL)
soup = BeautifulSoup(resp.text, 'html.parser')

# 3. Filtrer les liens vers les fichiers .mp3 ou .ogg
links = soup.find_all('a')
audio_files = [a['href'] for a in links if a['href'].endswith(('.mp3'))]

# 4. Télécharger chaque fichier
for filename in audio_files:
    url = BASE_URL + filename
    print(f"Téléchargement de : {filename}")
    r = requests.get(url)
    if r.status_code == 200:
        with open(os.path.join(DOWNLOAD_DIR, filename), 'wb') as f:
            f.write(r.content)
    else:
        print(f"Erreur lors du téléchargement de {filename}, statut : {r.status_code}")

print("Tous les fichiers sont téléchargés !")