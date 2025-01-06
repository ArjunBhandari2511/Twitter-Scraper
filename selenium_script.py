import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Set up Firefox WebDriver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

try:
    # Step 1: Navigate to Twitter's login page
    print("Navigating to Twitter login page...")
    driver.get("https://x.com/login")
    time.sleep(3)  # Sleep for 3 seconds to observe the page load

    # Step 2: Log in to Twitter
    print("Entering username...")
    wait = WebDriverWait(driver, 20)
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    username_field.send_keys("Username")  # Replace with your Twitter username
    username_field.send_keys(Keys.RETURN)
    time.sleep(3)  # Wait for 3 seconds before entering the password

    # Step 3: Wait for the password field to load and enter password
    print("Entering password...")
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys("Password")  # Replace with your Twitter password
    password_field.send_keys(Keys.RETURN)
    time.sleep(3)  # Wait for 3 seconds after submitting the password

    driver.get("https://x.com/explore/tabs/for-you")
    time.sleep(3)

    # Step 4: Wait for the target elements to load (first 4 elements with the specified class)
    print("Waiting for the target elements...")
    target_elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "span.r-18u37iz")
        )
    )
    time.sleep(2)  # Sleep for 2 seconds to ensure elements are fully loaded

    # Step 5: Retrieve and print the text of the first 4 matching elements
    print("Following are the trending topics:")
    for i in range(min(10, len(target_elements))):  # Ensure we don't exceed available elements
        print(f"Trending On {i+1}: {target_elements[i].text}")
        time.sleep(1)  # Sleep for 1 second between prints for better visibility

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Step 6: Close the browser
    print("Closing the browser...")
    driver.quit()
