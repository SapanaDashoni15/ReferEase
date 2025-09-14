import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Load connections from CSV ===
connections_df = pd.read_csv("connections.csv")
print(f"✅ Loaded {len(connections_df)} connections from CSV")

# === Setup Selenium ===
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # keep browser open
driver = webdriver.Chrome(options=options)

# Open LinkedIn login page
driver.get("https://www.linkedin.com/login")
print("👉 Please log in to LinkedIn manually in the browser window.")
input("✅ Press Enter here once you are logged in...")

# === Iterate over connections ===
for index, row in connections_df.iterrows():
    profile_url = row["ProfileURL"]
    name = row["Name"]
    
    try:
        print(f"\n👉 Opening profile: {name} ({profile_url})")
        driver.get(profile_url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Try to find Message button
        try:
            message_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Message')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", message_button)
            message_button.click()
            print("✅ Message button clicked.")
            
        except:
            # Fallback: Try Connect button if Message is not available
            try:
                connect_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Connect')]"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", connect_button)
                connect_button.click()
                print("⚡ Connect button clicked. Sending note...")
                
                # Click Add Note
                add_note_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Add a note')]"))
                )
                add_note_button.click()
                
                # Enter message
                message_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "custom-message"))
                )
                message_text = f"Hi {name}, this is just a test message to check my automation script 😊"
                message_box.send_keys(message_text)
                
                # Send the invitation
                send_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Send now')]")
                send_button.click()
                print(f"✅ Connect + Note sent successfully to {name}!")
                continue  # skip to next profile
                
            except:
                print("⚠️ Could not find Message or Connect button. Skipping profile.")
                continue
        
        # Wait for the message textarea after Message button
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "textarea"))
        )
        message_text = f"Hi {name}, this is just a test message to check my automation script 😊"
        message_box.send_keys(message_text)
        time.sleep(1)
        message_box.send_keys(Keys.RETURN)
        print(f"✅ Message sent successfully to {name}!")
        
    except Exception as e:
        print(f"❌ Error with {name}: {e}")

print("\n🎯 Task completed for all connections.")
