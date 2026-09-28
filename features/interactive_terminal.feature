@ui @terminal
Feature: Interactive TUI Terminal Simulation
  As a developer visiting Vrushabh's website
  I want to interact with the embedded terminal emulator
  So that I can run commands like fastfetch, about, and skills directly in the browser

  Background:
    Given I visit the website homepage
    And I navigate to the interactive terminal section

  Scenario: Terminal window is rendered with titlebar and prompt
    Then the terminal window should be visible
    And the terminal prompt should show "vrushabh@omarchy:~$"

  Scenario Outline: Execute quick commands via buttons
    When I click the quick command button "<command>"
    Then the terminal output should contain "<expected_content>"

    Examples:
      | command    | expected_content |
      | fastfetch  | Arch Linux       |
      | about      | Vrushabh         |
      | skills     | Rust             |
      | shortcuts  | Shortcuts        |

  Scenario: Execute typed command via keyboard input
    When I type "fastfetch" into the terminal prompt and submit
    Then the terminal output should match either "OS: Omarchy Linux" or "Arch Linux"

  Scenario: Clear terminal output
    When I click the quick command button "about"
    Then the terminal output should not be empty
    When I click the quick command button "clear"
    Then the terminal output should be cleared
