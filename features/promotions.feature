Feature: The Promotion service back-end
    As the Promotion Service
    I need a RESTful catalog service
    So that I can hold information about what Promotions are currently available.

Background:
    Given the following promotions
        | name       | promo_type | value | start_date        | end_date | detail |
        | promo1     | $          | 10.0  | 01-01-17 00:00:00 |          | det_1  |
        | promo2     | $          | 25.25 | 11-09-17 00:00:00 | 12-31-25 | det_2  |
        | promo3     | %          | 5.0   | 01-01-99 00:00:00 | 01-01-18 | det_3  |
