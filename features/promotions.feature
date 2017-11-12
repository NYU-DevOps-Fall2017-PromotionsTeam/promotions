Feature: The Promotion service back-end
    As the Promotion Service
    I need a RESTful catalog service
    So that I can hold information about what Promotions are currently available.

Background:
    Given the following promotions
        | id | name       | promo_type | value | start_date        | end_date              | detail |
        |  0 | promo1     | $          | 10.0  | 2017-01-01 00:00:00 | 2018-01-01 00:00:00 | det_1  |
        |  1 | promo2     | $          | 25.25 | 2017-01-01 00:00:00 | 2019-01-01 00:00:00 | det_2  |
        |  2 | promo3     | %          | 5.0   | 2017-01-01 00:00:00 | 2020-01-01 00:00:00 | det_3  |

Scenario: Testing 1 2 3
    
