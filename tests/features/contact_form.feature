@high @regression
Feature: Contact Form Validation
  As a user
  I want to fill out the Contact Us form
  So that I can send feedback successfully

  Background:
    Given I am on the Contact Us page

  # Positive Test Case
  @positive @smoke @contact_form @test001
  Scenario: Successful form submission
    When I fill out all fields correctly
    And I click the submit button
    Then I should see a success message

  # Negative Test Cases
  @negative @regression @contact_form @test002
  Scenario: Missing required field - First Name
    When I leave the first name blank
    And I click the submit button
    Then I should see an error message saying "First name is required"

  @negative @regression @contact_form @test003
  Scenario: Invalid email format
    When I enter an invalid email address
    And I click the submit button
    Then I should see an error message saying "Please enter a valid email address"

  @negative @regression @contact_form @test004
  Scenario: Age not selected
    When I leave the age dropdown unselected
    And I click the submit button
    Then I should see an error message saying "Age is required"

  @negative @regression @contact_form @test005
  Scenario: Feedback field empty
    When I leave the feedback field blank
    And I click the submit button
    Then I should see an error message saying "Feedback is required"

  @negative @regression @contact_form @test006
  Scenario: Multiple required fields empty
    When I leave the title and first name and email and age and feedback field blank
    And I click the submit button
    Then I should see error messages saying:
      | First name is required |
      | Please enter a valid email address |
      | Feedback is required |