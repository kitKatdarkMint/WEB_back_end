import re
import json
import requests
from bs4 import BeautifulSoup
URL = "https://lyon.citycrunch.fr/top-5-des-restaurants-pour-etudiants-a-lyon/2020/01/28/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# On vérifie que la page a été téléchargée avec succès
if page.status_code != 200:
    print("Error: ", page.status_code)
else:
    body = soup.find("section", class_="entry-content")
    titres = body.find_all("h2") #contient titre et prix
    images = body.find_all("img")
    lieus = [p for p in body.find_all("p") if "?" in p.get_text().lower()]
    
    with open("events.json", "r", encoding="utf-8") as f:
        dataBase = json.load(f)
    for i in range(len(titres)):

        # On extrait le titre et le prix avec Regex
        titre = titres[i].get_text()
        match = re.search(r"([\d]+(?:,[\d]+)?)\s?€", titre)
        if match:
            titre = re.sub(r"à\s(.+)€", "", titre).strip()
            prix = match.group(1)
            prix = float(prix.replace(",", "."))
        else:
            prix = None

        #On extrait le lieu avec split
        lieu = lieus[i].get_text()
        lieu = (lieu.split("Lyon")[0].strip() + " Lyon").replace("?", "")
        
        
        # print("Titre : ", titre)
        # print("Prix : ", prix)
        # print("Lieu : ", lieu)
        # print("Image : ", images[i]["src"])
        # print("\n")
        
        dataBase.append({
            "Date": None,
            "Titre": titre,
            "Lieu": lieu.strip(),
            "Tarif": prix,
            "Image": images[i]["src"],
            "Type": "Restaurant"
        })

    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(dataBase, f, indent=4, ensure_ascii=False)