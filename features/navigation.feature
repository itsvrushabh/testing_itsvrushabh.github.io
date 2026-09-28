@ui @navigation
Feature: Website Navigation and Workspaces
  As a visitor to Vrushabh Deshmukh's portfolio website
  I want to navigate through the menubar and workspace links
  So that I can explore his projects, dispatches, manual, contact, and resume

  Background:
    Given I visit the website homepage

  Scenario: Homepage loads with correct branding and title
    Then the page title should contain "Vrushabh Deshmukh"
    And the menubar should be visible
    And the home workspace icon should be active

  Scenario Outline: Navigate to topbar workspaces
    When I click on the workspace "<workspace_name>"
    Then the current URL path should be "<expected_path>"
    And the page title should contain "<title_keyword>"

    Examples:
      | workspace_name   | expected_path | title_keyword |
      | Plugins & Code   | /projects/    | Projects      |
      | Dispatches       | /blog/        | Blog          |
      | Manual           | /about/       | Manual        |
      | Contact          | /contact/     | Contact       |
      | Resume           | /resume/      | Resume        |

  Scenario: GitHub link points to user profile
    Then the GitHub profile link should point to "https://github.com/itsvrushabh"
    And the GitHub profile link should open in a new tab

  Scenario: System calendar popover can be toggled from topbar
    When I click the datetime clock in the menubar
    Then the terminal calendar popover should be displayed
    When I click the datetime clock in the menubar again
    Then the terminal calendar popover should be closed
