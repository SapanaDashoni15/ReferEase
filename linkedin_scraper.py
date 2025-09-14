# linkedin_scraper.py
from config import email, password
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # <- NEW

# --- CONFIG ---
LINKEDIN_EMAIL = "email"
LINKEDIN_PASSWORD = "password"

# --- DATABASE SETUP ---
conn = sqlite3.connect("connections.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        company TEXT
    )
""")
conn.commit()

# --- SELENIUM SETUP ---
options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

# 🚀 webdriver-manager will handle ChromeDriver automatically
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# --- LOGIN ---
driver.get("https://www.linkedin.com/login")
time.sleep(2)

driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(5)

# --- GO TO CONNECTIONS PAGE ---
driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
time.sleep(5)


# --- SCRAPE CONNECTIONS ---
connections = driver.find_elements(By.CSS_SELECTOR, "li.mn-connection-card")

for person in connections:
    try:
        name = person.find_element(By.CSS_SELECTOR, "span.mn-connection-card__name").text.strip()
    except:
        name = "Unknown"

    try:
        company = person.find_element(By.CSS_SELECTOR, "span.mn-connection-card__occupation").text.strip()
    except:
        company = "Unknown"

    print(f"Name: {name}, Company: {company}")

    # Save into DB
    cursor.execute("INSERT INTO connections (name, company) VALUES (?, ?)", (name, company))
    conn.commit()
