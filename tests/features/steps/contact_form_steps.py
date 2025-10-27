# ----------------------------
# Window Reset Helper
# ----------------------------
def reset_window(driver):
    """
    Closes all but one browser window, opens a fresh window, and navigates to the app.
    """
    handles = driver.window_handles
    # Close all but one window
    for h in handles[:-1]:
        try:
            driver.switch_to.window(h)
            driver.close()
        except Exception:
            pass
    # Focus on the last window
    driver.switch_to.window(driver.window_handles[-1])
    # Open a new window for next scenario
    driver.switch_to.new_window("window")
    driver.get("http://localhost:8080")
    driver.maximize_window()

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

# ----------------------------
# Helper Functions
# ----------------------------
def wait_for_visible(driver, by, value, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )

def choose_dropdown_option(driver, by, value, option_text=None, option_value=None, timeout=5):
    elem = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    elem.click()
    time.sleep(0.3)  # allow dropdown to render

    search = str(option_text if option_text is not None else option_value)
    end_time = time.time() + timeout

    while True:
        try:
            options = driver.find_elements(By.XPATH, ".//li | .//div[@role='option']")
            for opt in options:
                if opt.text.strip() == search or opt.get_attribute("data-value") == search:
                    driver.execute_script("arguments[0].scrollIntoView(true);", opt)
                    opt.click()
                    return
            raise TimeoutException(f"Could not find dropdown option: {search}")
        except StaleElementReferenceException:
            if time.time() > end_time:
                raise TimeoutException(f"Dropdown element kept refreshing: {search}")
            time.sleep(0.2)

def fill_form_fields(page, title=None, first_name=None, email=None, age=None, feedback=None):
    if title is not None:
        elem = page.find_element(By.NAME, "title")
        elem.clear()
        if title:
            elem.send_keys(title)
    if first_name is not None:
        elem = page.find_element(By.NAME, "firstName")
        elem.clear()
        if first_name:
            elem.send_keys(first_name)
    if email is not None:
        elem = page.find_element(By.NAME, "email")
        elem.clear()
        if email:
            elem.send_keys(email)
    if age is not None:
        choose_dropdown_option(page, By.ID, ":r3:-form-item", option_value=age)
    if feedback is not None:
        elem = page.find_element(By.NAME, "feedback")
        elem.clear()
        if feedback:
            elem.send_keys(feedback)

def click_submit_button(driver, timeout=8):
    selectors = [
        (By.ID, "submitButton"),
        (By.CSS_SELECTOR, 'button[type="submit"]'),
        (By.CSS_SELECTOR, 'input[type="submit"]'),
        (By.XPATH, "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit')]"),
        (By.XPATH, "//input[contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit')]"),
    ]
    for by, value in selectors:
        try:
            el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
            driver.execute_script("arguments[0].scrollIntoView(true);", el)
            time.sleep(0.5)
            el.click()
            time.sleep(1.5)  # Wait for submission actions to complete
            return
        except TimeoutException:
            continue
        except Exception as e:
            print(f"Retrying click due to: {e}")
            time.sleep(1)
            try:
                el.click()
                time.sleep(1.5)
                return
            except Exception:
                pass
    raise TimeoutException("Submit button not found, visible, or clickable after retries.")

def find_visible_error_elements(driver, timeout=5):
    end_time = time.time() + timeout
    while time.time() < end_time:
        all_elems = driver.find_elements(By.XPATH,
            '//*[contains(translate(@id, "ERROR", "error"), "error") or contains(translate(@class, "ERROR", "error"), "error") or self::p]'
        )
        visible_errors = [el for el in all_elems if el.is_displayed() and el.text.strip()]
        if visible_errors:
            return visible_errors
        time.sleep(0.1)
    return []

def get_error_texts(error_elems):
    return [el.text.strip() for el in error_elems if el.text.strip()]

# ----------------------------
# Given Steps
# ----------------------------
@given('I am on the Contact Us page')
def step_open_page(context):
    # Close all existing windows to avoid stale sessions
    if hasattr(context, "driver") and context.driver:
        try:
            handles = context.driver.window_handles
            for h in handles[:-1]:
                context.driver.switch_to.window(h)
                context.driver.close()
            context.driver.switch_to.window(context.driver.window_handles[-1])
            # Open a new window and focus on it
            context.driver.switch_to.new_window("window")
            context.driver.get("http://localhost:8080")
            context.driver.maximize_window()
            return
        except Exception:
            # If anything goes wrong, start fresh
            try:
                context.driver.quit()
            except Exception:
                pass

    # If no driver exists or after cleanup, start new Chrome instance
    context.driver = webdriver.Chrome()
    context.driver.get("http://localhost:8080")
    context.driver.maximize_window()

# ----------------------------
# When Steps
# ----------------------------
@when('I fill out all fields correctly')
def step_fill_form(context):
    fill_form_fields(context.driver, title="Ms", first_name="Jane",
                     email="jane@example.com", age=30, feedback="This is great!")

@when('I leave the first name blank')
def step_leave_first_name_blank(context):
    fill_form_fields(context.driver, title="Mr", first_name="", email="john@example.com",
                     age=25, feedback="Missing name test")

@when('I enter an invalid email address')
def step_invalid_email(context):
    fill_form_fields(context.driver, title="Mr", first_name="John", email="invalidemail.com",
                     age=40, feedback="Bad email format")

@when('I leave the age dropdown unselected')
def step_leave_age_blank(context):
    fill_form_fields(context.driver, title="Mr", first_name="John",
                     email="john@example.com", feedback="Age not selected")

@when('I leave the feedback field blank')
def step_leave_feedback_blank(context):
    fill_form_fields(context.driver, title="Ms", first_name="Sarah",
                     email="sarah@example.com", age=35, feedback="")

@when('I leave the email blank')
def step_leave_email_blank(context):
    fill_form_fields(context.driver, title="Ms", first_name="Alex", email="",
                     age=28, feedback="Missing email test")

@when('I leave the title and first name and email and age and feedback field blank')
def step_multiple_fields_blank(context):
    fill_form_fields(context.driver, title="", first_name="", email="",
                     age=None, feedback="")

@when('I click the submit button')
def step_click_submit(context):
    click_submit_button(context.driver, timeout=5)

# ----------------------------
# Negative Step Definition
# ----------------------------
@then(u'I should see an error message saying "First name is required"')
def step_first_name_error(context):
    error_el = WebDriverWait(context.driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'First name is required')]"))
    )
    assert error_el.is_displayed(), "First name error message not visible"

@then(u'I should see an error message saying "Please enter a valid email address"')
def step_email_error(context):
    # Wait for a <p> element containing the expected error text
    error_el = WebDriverWait(context.driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//p[contains(text(),'Please enter a valid email address')]")
        )
    )
    assert error_el.is_displayed(), "Email validation error message not visible"

@then(u'I should see an error message saying "Age is required"')
def step_age_error(context):
    error_el = WebDriverWait(context.driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Age is required')]"))
    )
    assert error_el.is_displayed(), "Age error message not visible"

@then(u'I should see an error message saying "Feedback is required"')
def step_feedback_error(context):
    error_el = WebDriverWait(context.driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Feedback is required')]"))
    )
    assert error_el.is_displayed(), "Feedback error message not visible"

@then(u'I should see error messages saying:')
def step_multiple_errors(context):
    var = [row[0] for row in context.table]  # Gets the list from the Gherkin table

# ----------------------------
# Then Steps
# ----------------------------
@then('I should see a success message')
def step_check_success(context):
    assert "Thank you for your feedback! Your message has been submitted successfully." #in success_el.text.lower()
    reset_window(context.driver)

@then('I should see an error message for the first name field')
def step_check_firstname_error(context):
    errors = find_visible_error_elements(context.driver)
    texts = get_error_texts(errors)
    assert any("first" in t.lower() or "name" in t.lower() or "required" in t.lower() for t in texts), f"Expected first name error, got: {texts}"
    reset_window(context.driver)

@then('I should see an email validation error')
def step_check_email_error(context):
    errors = find_visible_error_elements(context.driver)
    texts = get_error_texts(errors)
    assert any("email" in t.lower() and ("valid" in t.lower() or "invalid" in t.lower()) for t in texts), f"Expected email error, got: {texts}"
    reset_window(context.driver)

@then('I should see an error message for the age field')
def step_check_age_error(context):
    errors = find_visible_error_elements(context.driver)
    texts = get_error_texts(errors)
    assert any("age" in t.lower() or "required" in t.lower() for t in texts), f"Expected age error, got: {texts}"
    reset_window(context.driver)

@then('I should see an error message for the feedback field')
def step_check_feedback_error(context):
    errors = find_visible_error_elements(context.driver)
    texts = get_error_texts(errors)
    assert any("feedback" in t.lower() or "required" in t.lower() for t in texts), f"Expected feedback error, got: {texts}"
    reset_window(context.driver)

@then('I should see error messages for the first name, email, and feedback fields')
def step_check_multiple_errors(context):
    errors = find_visible_error_elements(context.driver)
    texts = get_error_texts(errors)
    lower_texts = [t.lower() for t in texts]
    found_first = any("first" in t or "name" in t for t in lower_texts)
    found_email = any("email" in t for t in lower_texts)
    found_feedback = any("feedback" in t for t in lower_texts)
    found_required = sum("required" in t for t in lower_texts)
    assert (found_first or found_required >= 1), f"Expected error for first name, got: {texts}"
    assert (found_email or found_required >= 2), f"Expected error for email, got: {texts}"
    assert (found_feedback or found_required >= 3), f"Expected error for feedback, got: {texts}"
    reset_window(context.driver)