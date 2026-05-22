@regression
Feature: Apollo 247 Functionalities


  Scenario: Verify Website Launch

    Given User launches Apollo website
    Then Website should launch successfully


  Scenario Outline: Positive Login Test

    Given User launches Apollo website
    When User enters mobile number "<mobile>"
    And User completes OTP verification
    Then User should login successfully

    Examples:
      | mobile     |
      | 9031388089 |


  Scenario Outline: Negative Login Test

    Given User launches Apollo website
    When User enters invalid mobile number "<mobile>"
    Then Invalid login error should display

    Examples:
      | mobile |
      | 1234   |


  Scenario Outline: Positive Medicine Search

    Given User opens Buy Medicines page
    When User searches medicine "<medicine>"
    Then Search results should display

    Examples:
      | medicine         |
      | Dolo 650         |
      | Paracetamol 500mg|
      | Vicks Vaporub    |


  Scenario Outline: Negative Medicine Search

    Given User opens Buy Medicines page
    When User searches invalid medicine "<medicine>"
    Then No valid results should display

    Examples:
      | medicine |
      | @#$$%^&* |