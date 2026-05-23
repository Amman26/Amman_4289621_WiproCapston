@regression
Feature: Apollo 247 Functionalities


  @smoke
  Scenario: Verify Website Launch

    Given User launches Apollo website
    Then Website should launch successfully


  @positive @authentication
  Scenario: Positive Login Test

    Given User launches Apollo website
    When User performs positive login
    Then User should login successfully


  @negative @authentication
  Scenario: Negative Login Test

    Given User launches Apollo website
    When User performs negative login
    Then Invalid login error should display


  @positive @search
  Scenario: Positive Medicine Search

    Given User opens Buy Medicines page
    When User performs positive medicine search
    Then Search results should display


  @negative @search
  Scenario: Negative Medicine Search

    Given User opens Buy Medicines page
    When User performs negative medicine search
    Then No valid results should display