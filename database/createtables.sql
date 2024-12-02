CREATE TABLE Airline (
airline_name VARCHAR(255) PRIMARY KEY
);


CREATE TABLE Airline_Staff (
username VARCHAR(255),
thepassword VARCHAR(255),
airline_name VARCHAR(255), 
first_name VARCHAR(255), 
last_name VARCHAR(255), 
date_of_birth DATE,
FOREIGN KEY (airline_name) REFERENCES Airline(airline_name),
PRIMARY KEY (username)
);


CREATE TABLE Staff_Email (
username VARCHAR(255),
staff_mail VARCHAR(255),
FOREIGN KEY (username) REFERENCES Airline_Staff(username),
PRIMARY KEY (username, staff_mail)
);


CREATE TABLE Staff_Phone_Number (
username VARCHAR(255),
staff_number CHAR(10),
FOREIGN KEY (username) REFERENCES Airline_Staff(username),
PRIMARY KEY (username, staff_number)
);


CREATE TABLE Airplane (
airplane_id int,
airline_name VARCHAR(255),
manufacturing_company VARCHAR(255),
model_number int,
manufacturing_date DATE,
number_of_seats int,
FOREIGN KEY (airline_name) REFERENCES Airline(airline_name),
PRIMARY KEY (airplane_id, airline_name)
);


CREATE TABLE Maintenance (
airplane_id int,
airline_name VARCHAR(255),
start_datetime DATETIME,
end_datetime DATETIME,
FOREIGN KEY (airplane_id, airline_name) REFERENCES Airplane(airplane_id, airline_name),
PRIMARY KEY (airplane_id, airline_name, start_datetime, end_datetime)
);





CREATE TABLE Airport(
airport_code int,
airport_name VARCHAR(255),
city VARCHAR(255),
country VARCHAR(255),
num_of_terminals int,
airport_type VARCHAR(255), 
PRIMARY KEY (airport_code)
);

CREATE TABLE Flight(
flight_number int,
departure_datetime DATETIME,
airline_name VARCHAR(255),
airplane_id int,
base_price int,
flight_status VARCHAR(255),
arrival_airport_code int,
departure_airport_code int,
arrival_datetime DATETIME,
FOREIGN KEY (arrival_airport_code) REFERENCES Airport(airport_code),
FOREIGN KEY (departure_airport_code) REFERENCES Airport(airport_code),
FOREIGN KEY (airplane_id) REFERENCES Airplane(airplane_id),
FOREIGN KEY (airline_name) REFERENCES Airline (airline_name), 
PRIMARY KEY(flight_number, departure_datetime, airline_name)
);

CREATE TABLE Ticket (
ticket_id int,
flight_number int,
departure_datetime DATETIME, 
airline_name VARCHAR(255), 
calculated_ticket_price int,
FOREIGN KEY (flight_number, departure_datetime, airline_name) REFERENCES Flight(flight_number, departure_datetime, airline_name), 
PRIMARY KEY (ticket_id)
);

CREATE TABLE Customer(
email VARCHAR(255),
thepassword VARCHAR(255),
first_name VARCHAR(255),
last_name VARCHAR(255),
building_num int,
street_name VARCHAR(255),
apt_num int,
city VARCHAR(255),
state_name VARCHAR(255),
zip_code int,
passport_number int,
passport_expiration DATE,
passport_country VARCHAR(255),
date_of_birth DATE,
PRIMARY KEY(email)
);

CREATE TABLE Takes(
flight_number int,
departure_datetime DATETIME,
airline_name VARCHAR(255),
email VARCHAR(255),
comment VARCHAR(255),
rating int,
FOREIGN KEY (flight_number, departure_datetime, airline_name) REFERENCES Flight(flight_number, departure_datetime, airline_name),
FOREIGN KEY (email) REFERENCES Customer(email),
PRIMARY KEY (flight_number, departure_datetime, email, airline_name)
);

CREATE TABLE Purchases(
ticket_id int,
email VARCHAR(255),
name_on_card VARCHAR(255),
card_number VARCHAR(255),
card_type VARCHAR(255),
purchase_datetime DATETIME,
card_expiration_date DATE,
passenger_first_name VARCHAR(255), 
passenger_last_name VARCHAR(255), 
passenger_birthofdate DATETIME,
FOREIGN KEY (email) REFERENCES Customer(email),
FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id), 
PRIMARY KEY (ticket_id)
);

CREATE TABLE Customer_Phone_Number(
email VARCHAR(255),
customer_number int,
FOREIGN KEY (email) REFERENCES Customer(email),
PRIMARY KEY (email, customer_number)
);
