from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup ---
driver = webdriver.Chrome()  # or webdriver.Firefox()
driver.get("http://localhost:8080")  # Your React app URL

wait = WebDriverWait(driver, 10)

# --- Locate input fields ---
first_name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id, ':r0:')]")))
email_input = driver.find_element(By.XPATH, "//input[contains(@id, ':r1:')]")
feedback_textarea = driver.find_element(By.XPATH, "//textarea[contains(@id, ':r5:')]")
submit_button = driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]")

# --- Leave fields blank and submit ---
submit_button.click()

# --- Wait a short moment for errors to render ---
wait.until(lambda d: True)  # can replace with a small sleep if needed

# --- Collect visible error messages dynamically ---
error_elements = driver.find_elements(By.XPATH, "//*")
print("=== Detected Potential Error Messages ===")
for el in error_elements:
    if el.is_displayed() and el.text.strip():
        text = el.text.strip()
        # Filter for keywords that indicate errors
        if any(keyword in text.lower() for keyword in ["first", "email", "feedback", "required", "error"]):
            print(f"{el.tag_name} -> Text: {text}")

# --- Clean up ---
driver.quit()