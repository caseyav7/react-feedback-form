Feature: Contact Form Validation
  As a user
  I want to fill out the Contact Us form
  So that I can send feedback successfully

  Background:
    Given I am on the Contact Us page

  # Positive Test Case
  @positive @contact-form @smoke @regression
  Scenario: Successful form submission
    When I fill out all fields correctly
    And I click the submit button
    Then I should see a success message

  # Negative Test Cases
  @negative @contact-form @regression
  Scenario: Missing required field - First Name
    When I leave the first name blank
    And I click the submit button
    Then I should see an error message for the first name field

  @negative @contact-form @regression
  Scenario: Invalid email format
    When I enter an invalid email address
    And I click the submit button
    Then I should see an email validation error

  @negative @contact-form @regression
  Scenario: Age not selected
    When I leave the age dropdown unselected
    And I click the submit button
    Then I should see an error message for the age field

  @negative @contact-form @regression
  Scenario: Feedback field empty
    When I leave the feedback field blank
    And I click the submit button
    Then I should see an error message for the feedback field

  @negative @contact-form @regression
  Scenario: Multiple required fields empty
    When I leave the first name blank
    And I leave the email blank
    And I leave the feedback field blank
    And I click the submit button
    Then I should see error messages for the first name, email, and feedback fields