@api @performance
Feature: Critical Assets and Performance Budget
  As a website performance engineer
  I want to ensure all preloaded hero assets and core stylesheets are lightweight and healthy
  So that visitors experience fast page load speeds and no bandwidth waste

  Scenario Outline: Critical media assets are accessible and correctly typed
    When I request the static asset "<asset_path>"
    Then the asset status code should be 200
    And the asset content-type should be "<expected_content_type>"
    And the asset size should be less than <max_size_kb> kilobytes

    Examples:
      | asset_path                           | expected_content_type   | max_size_kb |
      | /assets/images/3D_helmat_model_v3.webp| image/webp              | 350         |
      | /assets/images/3D_model_v3.webp       | image/webp              | 300         |
      | /assets/css/omarchy-themes.css       | text/css                | 20          |
      | /assets/css/main.css                 | text/css                | 120         |
      | /site.webmanifest                    | application/manifest+json| 10          |

  Scenario: Homepage DOMContentLoaded timing is within budget
    Given I visit the website homepage
    Then the DOMContentLoaded duration should be under 3000 milliseconds
