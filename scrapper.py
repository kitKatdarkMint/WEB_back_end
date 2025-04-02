import requests
from bs4 import BeautifulSoup
URL = "https://www.lyoncampus.com/sortir/agenda"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="c651")
activity_event = results.find_all("div", class_="event col-md-6 mb-5")
for activity in activity_event:
    date = activity.find("div", class_="event-date")
    if date:
        date_text = date.get_text(strip=True) 
        print(date_text)
    category= activity.find("div", class_="event-category")
    print(category)
    prix= activity.find("svg").find("title")
    if prix:
        prix_text = prix.get_text(strip=True)
        print(prix_text)
    link=activity.find("div",class_="event-excerpt d-none d-lg-block").find("a")
    if link and link.has_attr("href"):
        link_href = link["href"]
        print(link_href)

