@ui @hero
Feature: Hero Section and Interactive Components
  As a visitor
  I want to view the hero overview, system driver specs, and quick install snippets
  So that I can quickly understand Vrushabh's background and copy setup commands

  Background:
    Given I visit the website homepage

  Scenario: Hero displays correct title, role, and description
    Then the hero title should be "VRUSHABH DESHMUKH"
    And the hero tagline should contain "Systems & Backend Engineer"
    And the hero lead description should mention "Rust"

  Scenario Outline: Switching snippet tabs updates the copyable command
    When I click the snippet tab "<snippet_mode>"
    Then the snippet command label should contain "<expected_snippet_text>"

    Examples:
      | snippet_mode | expected_snippet_text |
      | cargo        | cargo install         |
      | curl         | curl                  |
      | cli          | curl                  |

  Scenario: Hero action buttons have correct destination anchors
    Then the "Launch Terminal" button should link to "#terminal"
    And the "Explore Plugins & Code" button should link to "#projects"
