from bs4 import BeautifulSoup
import csv

# --- READ THE DOWNLOADED HTML FILE ---
with open("connections.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# --- SCRAPE CONNECTIONS ---
connections = []
cards = soup.find_all("div", class_="mn-connection-card__details")

for card in cards:
    try:
        name = card.find("span", class_="mn-connection-card__name").get_text(strip=True)
    except:
        name = "Unknown"

    try:
        occupation = card.find("span", class_="mn-connection-card__occupation").get_text(strip=True)
    except:
        occupation = "Unknown"

    try:
        profile_link = card.find("a", class_="mn-connection-card__link")["href"]
    except:
        profile_link = "Unknown"

    connections.append([name, occupation, profile_link])

# --- SAVE TO CSV ---
with open("connections.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Occupation", "Profile Link"])  # Header
    writer.writerows(connections)

print("✅ Data saved into connections.csv")
