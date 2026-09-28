@api @crawler
Feature: Internal Link Integrity and 404 Detection
  As a website maintainer
  I want to crawl all internal navigation and blog links
  So that I ensure visitors never hit broken 404 error pages

  Scenario: Crawl homepage and verify all discovered internal links return 200
    When I crawl all internal links from the homepage
    Then none of the crawled internal links should return 404 or server errors

  Scenario Outline: Technical blog dispatches are live and accessible
    When I perform an HTTP GET request to "<post_path>"
    Then the response status code should be 200
    And the response content-type should be "text/html"

    Examples:
      | post_path                                                         |
      | /blog/architecting-modern-async-rust-microservices/               |
      | /blog/building-high-throughput-apis-in-rust/                      |
      | /blog/resilient-distributed-state-with-rabbitmq-and-redis/        |
