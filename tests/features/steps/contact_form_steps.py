from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

@given('I am on the Contact Us page')
def step_open_page(context):
    context.driver = webdriver.Chrome()
    context.driver.get("http://localhost:8080")
    context.driver.maximize_window()

# =============================
# Positive Test Case
# =============================
@when('I fill out all fields correctly')
def step_fill_form(context):
    page = context.driver
    page.find_element(By.NAME, "title").send_keys("Ms")
    page.find_element(By.NAME, "firstName").send_keys("Jane")
    page.find_element(By.NAME, "email").send_keys("jane@example.com")
    Select(page.find_element(By.NAME, "age")).select_by_value("30")
    page.find_element(By.NAME, "feedback").send_keys("This is great!")

# =============================
# Negative Test Cases
# =============================
@when('I leave the first name blank')
def step_leave_first_name_blank(context):
    page = context.driver
    page.find_element(By.NAME, "title").send_keys("Mr")
    page.find_element(By.NAME, "firstName").clear()
    page.find_element(By.NAME, "email").send_keys("john@example.com")
    Select(page.find_element(By.NAME, "age")).select_by_value("25")
    page.find_element(By.NAME, "feedback").send_keys("Missing name test")

@when('I enter an invalid email address')
def step_invalid_email(context):
    page = context.driver
    page.find_element(By.NAME, "title").send_keys("Mr")
    page.find_element(By.NAME, "firstName").send_keys("John")
    page.find_element(By.NAME, "email").send_keys("invalidemail.com")
    Select(page.find_element(By.NAME, "age")).select_by_value("40")
    page.find_element(By.NAME, "feedback").send_keys("Bad email format")

@when('I leave the age dropdown unselected')
def step_leave_age_blank(context):
    page = context.driver
    page.find_element(By.NAME, "title").send_keys("Mr")
    page.find_element(By.NAME, "firstName").send_keys("John")
    page.find_element(By.NAME, "email").send_keys("john@example.com")
    page.find_element(By.NAME, "feedback").send_keys("Age not selected")

@when('I leave the feedback field blank')
def step_leave_feedback_blank(context):
    page = context.driver
    page.find_element(By.NAME, "title").send_keys("Ms")
    page.find_element(By.NAME, "firstName").send_keys("Sarah")
    page.find_element(By.NAME, "email").send_keys("sarah@example.com")
    Select(page.find_element(By.NAME, "age")).select_by_value("35")
    # feedback left empty

@when('I leave the email blank')
def step_leave_email_blank(context):
    page = context.driver
    page.find_element(By.NAME, "title").send_keys("Ms")
    page.find_element(By.NAME, "firstName").send_keys("Alex")
    page.find_element(By.NAME, "email").clear()
    Select(page.find_element(By.NAME, "age")).select_by_value("28")
    page.find_element(By.NAME, "feedback").send_keys("Missing email test")

# =============================
# Multiple fields empty scenario
# =============================
@when('I leave the first name blank and the email blank and the feedback field blank')
def step_multiple_fields_blank(context):
    page = context.driver
    page.find_element(By.NAME, "title").send_keys("Mr")
    page.find_element(By.NAME, "firstName").clear()
    page.find_element(By.NAME, "email").clear()
    Select(page.find_element(By.NAME, "age")).select_by_value("40")
    page.find_element(By.NAME, "feedback").clear()

# =============================
# Shared Action Step
# =============================
@when('I click the submit button')
def step_click_submit(context):
    context.driver.find_element(By.ID, "submitButton").click()
    time.sleep(1)

# =============================
# Validation / Then Steps
# =============================
@then('I should see a success message')
def step_check_success(context):
    message = context.driver.find_element(By.ID, "successMessage").text
    assert "thank you" in message.lower()
    context.driver.quit()

@then('I should see an error message for the first name field')
def step_check_firstname_error(context):
    error = context.driver.find_element(By.ID, "firstNameError").text
    assert "required" in error.lower()
    context.driver.quit()

@then('I should see an email validation error')
def step_check_email_error(context):
    error = context.driver.find_element(By.ID, "emailError").text
    assert "valid email" in error.lower()
    context.driver.quit()

@then('I should see an error message for the age field')
def step_check_age_error(context):
    error = context.driver.find_element(By.ID, "ageError").text
    assert "required" in error.lower()
    context.driver.quit()

@then('I should see an error message for the feedback field')
def step_check_feedback_error(context):
    error = context.driver.find_element(By.ID, "feedbackError").text
    assert "required" in error.lower()
    context.driver.quit()

@then('I should see error messages for the first name, email, and feedback fields')
def step_check_multiple_errors(context):
    first_error = context.driver.find_element(By.ID, "firstNameError").text
    email_error = context.driver.find_element(By.ID, "emailError").text
    feedback_error = context.driver.find_element(By.ID, "feedbackError").text
    assert "required" in first_error.lower()
    assert "required" in email_error.lower()
    assert "required" in feedback_error.lower()
    context.driver.quit()