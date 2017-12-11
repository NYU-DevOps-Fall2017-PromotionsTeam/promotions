Feature: The Promotion service back-end
    As the Promotion Service
    I need a RESTful catalog service
    So that I can hold information about what Promotions are currently available.

Background:
    Given the following promotions
        | id | name       | promo_type | value | start_date          | end_date            | detail |
        |  0 | promo1     | $          | 10.0  | 2017-01-01 00:00:00 | 2018-01-01 00:00:00 | det_1  |
        |  1 | promo2     | $          | 25.25 | 2017-01-01 00:00:00 | 2019-01-01 00:00:00 | det_2  |
        |  2 | promo3     | %          | 5.0   | 2017-01-01 00:00:00 | 2020-01-01 00:00:00 | det_3  |

Scenario: List All Promotions
    When I visit "promotions"
    Then I should get a response code "200"
    And I should see "promo1"
    And I should see "promo2"
    And I should see "promo3"

Scenario: List promotions with conditions
    When I visit "promotions?promo_type=$"
    Then I should get a response code "200"
    And I should see "promo1"
    And I should see "promo2"
    And I should not see "promo3"
    When I visit "promotions?promo_type=%"
    Then I should get a response code "200"
    And I should not see "promo1"
    And I should not see "promo2"
    And I should see "promo3"
    When I visit "promotions?available_on=2018-06-01 00:00:00"
    Then I should get a response code "200"
    And I should not see "promo1"
    And I should see "promo2"
    And I should see "promo3"
    When I visit "promotions?available_on=2018-06-01 00:00:00&promo_type=%"
    Then I should get a response code "200"
    And I should not see "promo1"
    And I should not see "promo2"
    And I should see "promo3"

Scenario: Get promotion with id
    When I retrieve "promotions" with id "2"
    Then I should get a response code "200"
    And I should see "promo3"

Scenario: Get Or Update promotion with invalid id
    When I retrieve "promotions" with id "42"
    Then I should get a response code "404"
    When I visit "promotions"
    Then I will not see a promotion with "id" as "42"

Scenario: Update a promotion's value
    When I retrieve "promotions" with id "1"
    And I change "value" to "100.0"
    And I update "promotions" with id "1"
    Then I will see "promo2" with "value" as "100.0"

Scenario: Update a promotion's promo_type
    When I retrieve "promotions" with id "0"
    And I change "promo_type" to "%"
    And I update "promotions" with id "0"
    Then I will see "promo2" with "promo_type" as "%"

Scenario: Delete a promotion with valid id
    When I visit "promotions"
    Then I should see "promo1"
    When I delete "promotions" with id "0"
    Then I should get a response code "204"
    When I visit "promotions"
    Then I should see "promo2"
    And I should see "promo3"
    And I should not see "promo1"
    And There should be "2" promotions

Scenario: Delete a promotion with an invalid id
    When I delete "promotions" with id "99"
    Then I should get a response code "204"

Scenario: Create a promotion with default characteristics
    When I create a promotion
    Then I should get a response code "201"
    When I visit "promotions"
    Then I should get a response code "200"
    And I should see "promo1"
    And I should see "promo2"
    And I should see "promo3"
    And I should see "default"
    Then I reset the server db for further tests

Scenario: Create a Promotion using Incorrect Header
    When I call POST with Incorrect content-type
    Then I should get a response code "415"

Scenario: Action-Delete all promotions in service
    When I send a PUT request to '/promotions/delete-all'
    Then I should get a response code "204"
    When I visit "promotions"
    Then There should be "0" promotions

Scenario: Visiting the home page
    When I visit the root url
    Then I should get a response code "200"