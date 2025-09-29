import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from database import fetch_employees_by_company

# ⚠️ LinkedIn login
LINKEDIN_EMAIL = "your_email@gmail.com"
LINKEDIN_PASSWORD = "your_password"

def send_referral_messages(company, referral_message):
    employees = fetch_employees_by_company(company)

    if not employees:
        print(f"No employees found for {company}")
        return

    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    # Login
    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

    # Go to each profile and send message
    for name, profile_url in employees:
        try:
            driver.get(profile_url)
            time.sleep(5)

            # Click on Message button
            message_button = driver.find_element(By.CLASS_NAME, "artdeco-button__text")
            message_button.click()
            time.sleep(3)

            # Type message
            textarea = driver.find_element(By.TAG_NAME, "textarea")
            textarea.send_keys(referral_message)
            time.sleep(1)

            # Send message
            send_button = driver.find_element(By.XPATH, "//button[contains(@class,'msg-form__send-button')]")
            send_button.click()
            time.sleep(2)

            print(f"✅ Message sent to {name}")
        except Exception as e:
            print(f"❌ Could not message {name}: {e}")

    driver.quit()

if __name__ == "__main__":
    company_name = input("Enter company name: ")
    referral_message = input("Enter referral message: ")
    send_referral_messages(company_name, referral_message)
