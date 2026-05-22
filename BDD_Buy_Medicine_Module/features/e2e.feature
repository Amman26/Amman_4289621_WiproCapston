@e2e
Feature: Apollo 24/7 End To End Journey

  Scenario: Login Add Multiple Medicines And Checkout

    Given User launches Apollo 24/7 website
    When User logs in with valid mobile number
    And User searches and adds multiple medicines to cart
    Then User proceeds to checkout successfully