@api @seo
Feature: Website SEO, Meta Tags, and Endpoint Health
  As a site administrator
  I want to ensure all core pages return 200 OK and critical SEO metadata is intact
  So that the site remains discoverable, indexed, and reliable

  Scenario Outline: Core site endpoints respond with HTTP 200
    When I perform an HTTP GET request to "<endpoint>"
    Then the response status code should be 200
    And the response content-type should be "text/html"

    Examples:
      | endpoint   |
      | /          |
      | /projects/ |
      | /blog/     |
      | /about/    |
      | /contact/  |
      | /resume/   |

  Scenario: Metadata and Open Graph tags on homepage
    Given I visit the website homepage
    Then the meta tag "author" should have content "Vrushabh Deshmukh"
    And the meta tag "description" should not be empty
    And the open graph tag "og:title" should contain "Vrushabh Deshmukh"
    And the link tag "canonical" should point to "https://itsvrushabh.github.io/"
