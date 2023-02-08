-- Keep a log of any SQL queries you execute as you solve the mystery.
select * from  crime_scene_reports where day = "28" and month = "7";
select * from interviews where day = "28" and month = "7" and transcript like "%bakery%";
select name from bakery_security_logs, people where day = "28" and month = "7" and hour = "10" and minute > 15 and minute < 35 and people.license_plate = bakery_security_logs.license_plate;
+---------+
|  name   |
+---------+
| Vanessa |
| Bruce   |
| Barry   |
| Luca    |
| Sofia   |
| Iman    |
| Diana   |
| Kelsey  |
+---------+

select distinct people.name from atm_transactions, people,bank_accounts where atm_transactions.account_number =bank_accounts.account_number and people.id = bank_accounts.person_id and day = "28" and month = "7" and atm_location = "Leggett Street";
+---------+
|  name   |
+---------+
| Luca    |
| Kenny   |
| Taylor  |
| Bruce   |
| Brooke  |
| Kaelyn  |
| Iman    |
| Benista |
| Diana   |
+---------+

-- bruce, luca, imam, diana

sqlite> select name from  phone_calls ,people where caller =  phone_number and day ="28" and month="7" and duration < "60";
+---------+
|  name   |
+---------+
| Sofia   |
| Kelsey  |
| Bruce   |
| Kelsey  |
| Taylor  |
| Diana   |
| Carina  |
| Kenny   |
| Benista |
+---------+

-- bruce, diana

sqlite> select * from  flights ,airports where origin_airport_id=  airports.id and day ="29" and month="7" and city = "Fiftyville";
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+
| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | id | abbreviation |          full_name          |    city    |
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+
| 18 | 8                 | 6                      | 2021 | 7     | 29  | 16   | 0      | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
| 23 | 8                 | 11                     | 2021 | 7     | 29  | 12   | 15     | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
| 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
| 43 | 8                 | 1                      | 2021 | 7     | 29  | 9    | 30     | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
| 53 | 8                 | 9                      | 2021 | 7     | 29  | 15   | 20     | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+

--id = 36

--ruce, diana

sqlite> select name from  passengers ,people where passengers.passport_number = people.passport_number and passengers.flight_id = "36";
+--------+
|  name  |
+--------+
| Doris  |
| Sofia  |
| Bruce  |
| Edward |
| Kelsey |
| Taylor |
| Kenny  |
| Luca   |
+--------+

-- bruce
sqlite> select name, phone_number from  phone_calls ,people where caller =  phone_number and name ="Bruce";
+-------+----------------+
| name  |  phone_number  |
+-------+----------------+
| Bruce | (367) 555-5533 |

sqlite> select name from  phone_calls ,people where receiver =  phone_number and caller = "(367) 555-5533" and day = "28" and month ="7" and duration < "60";
+-------+
| name  |
+-------+
| Robin |
+-------+

-- bruce and robin

sqlite> select city from  flights ,airports where destination_airport_id=  airports.id and flights.id = "36";
+---------------+
|     city      |
+---------------+
| New York City |
+---------------+





