import requests
from bs4 import BeautifulSoup
import json
import os
import time
base_URL = "https://www.lyoncampus.com/sortir/agenda"
json_file_path = "events.json"
if os.path.exists(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        try:
            activity_data = json.load(f)  
        except json.JSONDecodeError:
            activity_data = []  
else:
    activity_data = []  
def event_exists(event, data):
    for existing_event in data:
        if (existing_event["Date"] == event["Date"] and
            existing_event["Titre"] == event["Titre"] and
            existing_event["Lieu"] == event["Lieu"]):
            return True
    return False
def scrape_page(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="c651")
    activitys = results.find_all("div", class_="event col-md-6 mb-5")
    tmp_data=[]
    for activity in activitys:
        activity_info = {}
        date = activity.find("div", class_="event-date")
        if date:
            date_text = date.get_text(strip=True) 
            activity_info["Date"] = date_text
        image_div=activity.find("div",class_="event-photo col-9 col-md-12 col-lg-5 mb-3")
        if image_div:
            image_tag=image_div.find("img")
            if image_tag and image_tag.has_attr("src"):
                image=image_tag["src"]
                image="https://www.lyoncampus.com"+image
                activity_info["image"] = image
            else:
                activity_info["image"] = None
        
    
        link=activity.find("div",class_="event-excerpt d-none d-lg-block").find("a")
        if link:
            title=link.get_text(strip=True) 
            activity_info["Titre"] = title
        if link and link.has_attr("href"):
            link_href = link["href"]
            link_href="https://www.lyoncampus.com"+link_href
            event_page = requests.get(link_href)
            event_soup = BeautifulSoup(event_page.content, "html.parser")
            lieu_header=event_soup.find("h2",string="Lieu")
            if lieu_header:
                row_div=lieu_header.find_next("div",class_="row")
                if row_div:
                    lieu_div=row_div.find("div",class_="col-md-6")
                    if lieu_div:
                        lieu=lieu_div.find("p").get_text(strip=True)
                        if "lyon" in lieu.lower():
                            lieu=lieu.split("Lyon")[0].strip()
                            lieu+=" Lyon"
                            activity_info["Lieu"] = lieu            
            prix_header=event_soup.find("h2",string="Tarif")
            if prix_header:
                prix_div=lieu_header.find_next("div",class_="d-flex justify-content-center")
                if prix_div:
                    prix_svg=prix_div.find("svg",class_="mx-4 mb-4")
                    if prix_svg and prix_svg.has_attr("aria-label"):
                        arialabel=prix_svg["aria-label"]
                        if arialabel=="Cet événement est gratuit":
                            prix=0
                        elif arialabel=="Cet événement est éligible au Pass Culture":
                            prix="Pass Culture"
                        activity_info["Tarif"] = prix
                else:
                    prix=prix_header.find_next("p").get_text(strip=True)
                    if "libre"not in prix and prix!="Tarif selon l'événement":
                        if "euros" in prix.lower():
                            prix=prix.split("euros")[0].strip()   
                        elif "€" in prix:
                            prix=prix.split("€")[0].strip()
                            prix=int(prix)
                        activity_info["Tarif"] = prix

        activity_info["Type"]="Activité"        
        required_fields = ["Date", "Titre", "Lieu", "Tarif","Type","image"]
        if all(field in activity_info for field in required_fields):
            if not event_exists(activity_info, activity_data): 
                tmp_data.append(activity_info) 
    activity_data.extend(tmp_data)
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(activity_data, json_file, indent=4, ensure_ascii=False)
    next_page_link=soup.find("li",class_="next pagination-link pagination-link--next").find("a")["href"]
    if next_page_link :
        next_page_link="https://www.lyoncampus.com"+next_page_link
        return next_page_link
    else:
        return None
pages_to_scrape_first = 2 
current_page_link = base_URL

for _ in range(pages_to_scrape_first):
    if current_page_link:
        current_page_link = scrape_page(current_page_link)
    else:
        break
delay_seconds = 2  
while current_page_link:
    time.sleep(delay_seconds)
    current_page_link = scrape_page(current_page_link)

