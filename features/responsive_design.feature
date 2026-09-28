@ui @responsive
Feature: Responsive Viewport Compatibility
  As a visitor using various devices
  I want the website structure to load properly across mobile, tablet, and desktop viewports
  So that the site remains functional regardless of device form factor

  Scenario Outline: Site components adapt to screen sizes
    Given I set the browser viewport to <width> by <height>
    When I visit the website homepage
    Then the menubar header should be present
    And the terminal section should be present
    And the hero title should be visible

    Examples:
      | device        | width | height |
      | Mobile        | 375   | 812    |
      | Tablet        | 768   | 1024   |
      | Desktop HD    | 1280  | 720    |
      | Desktop Large | 1440  | 900    |
