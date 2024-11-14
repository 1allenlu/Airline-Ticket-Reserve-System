SELECT *
FROM Flight
WHERE departure_datetime > NOW();


SELECT *
FROM Flight
WHERE flight_status = 'Delayed';


SELECT DISTINCT Customer.first_name, Customer.last_name
FROM Customer NATURAL JOIN Purchases;


SELECT * 
FROM Airplane
WHERE airline_name = 'Jet Blue';


/*
RESULTS

Query 1
+-----------------+----------------------+--------------------+---------------------+---------------+---------------+----------------------+------------------------+
| flight_number   | departure_datetime   | airline_name       | arrival_datetime    | base_price    | flight_status | arrival_airport_code | departure_airport_code |
+-----------------+----------------------+--------------------+---------------------+---------------+---------------+----------------------+------------------------+
|       200       |  2024-11-12 12:05:20 | Jet Blue           | 2024-11-12 14:05:20 |      300      | On-Time       |          1           |            2           |
+-----------------+----------------------+--------------------+---------------------+---------------+---------------+----------------------+------------------------+
|       300       |  2024-11-13 12:05:20 | Jet Blue           | 2024-11-13 14:05:20 |      300      | Delayed       |          1           |            2           |
+-----------------+----------------------+--------------------+---------------------+---------------+---------------+----------------------+------------------------+
|       400       |  2024-11-14 12:05:20 | Jet Blue           | 2024-11-14 14:05:20 |      300      | Delayed       |          1           |            2           |
+-----------------+----------------------+--------------------+---------------------+---------------+---------------+----------------------+------------------------+


Query 2
+-----------------+----------------------+--------------------+---------------------+---------------+---------------+----------------------+------------------------+
| flight_number   | departure_datetime   | airline_name       | arrival_datetime    | base_price    | flight_status | arrival_airport_code | departure_airport_code |
+-----------------+----------------------+--------------------+---------------------+---------------+---------------+----------------------+------------------------+
|       300       |  2024-11-13 12:05:20 | Jet Blue           | 2024-11-13 14:05:20 |      300      | Delayed       |          1           |            2           |
+-----------------+----------------------+--------------------+---------------------+---------------+---------------+----------------------+------------------------+
|       400       |  2024-11-14 12:05:20 | Jet Blue           | 2024-11-14 14:05:20 |      300      | Delayed       |          1           |            2           |
+-----------------+----------------------+--------------------+---------------------+---------------+---------------+----------------------+------------------------+


Query 3
+------------+-----+-----+
| fist_name  | last_name |
+------------+-----+-----+
| Dante      | Minasyan  |
| Evan       | Dworkin   |
+------------+-----+-----+


Query 4
+--------------+--------------+-----------------------+--------------+--------------------+
| airplane_id  | airline_name | manufacturing_company | model_number | manufacturing_date |
+--------------+--------------+-----------------------+--------------+--------------------+
|     123      |    Jet Blue  |         Boeing        |     747      |     2010-05-05     |
|     456      |    Jet Blue  |         Boeing        |     747      |     2015-05-05     |
|    789       |    Jet Blue  |         Airbus        |     747      |     2018-05-05     |
+--------------+--------------+-----------------------+--------------+--------------------+


*/