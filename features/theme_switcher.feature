@ui @theme
Feature: Omarchy Theme Switcher
  As a visitor to the website
  I want to toggle through different color themes
  So that I can customize the visual aesthetic to my preference and have it remembered

  Background:
    Given I visit the website homepage

  Scenario: Default theme is set on initial load
    Then the active theme attribute on html should be "tokyo-night"

  Scenario: Cycling through themes updates the DOM and local storage
    When I click the theme switcher button
    Then the active theme attribute on html should change from the initial theme
    And the local storage "omarchy-site-theme" should match the active theme

  Scenario: Selected theme persists across page reloads
    When I click the theme switcher button
    And I note the current active theme
    And I reload the webpage
    Then the active theme attribute on html should match the noted theme
