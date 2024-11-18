CREATE TABLE Airline (
airline_name VARCHAR(255) PRIMARY KEY
);


CREATE TABLE Airline_Staff (
username VARCHAR(255) PRIMARY KEY,
thepassword VARCHAR(255),
airline_name VARCHAR(255),
FOREIGN KEY (airline_name) REFERENCES Airline(airline_name)
);



CREATE TABLE Staff_Email (
username VARCHAR(255),
staff_mail VARCHAR(255) NOT NULL,
FOREIGN KEY (username) REFERENCES Airline_Staff(username),
PRIMARY KEY (username, staff_mail)
);


CREATE TABLE Staff_Phone_Number (
username VARCHAR(255),
staff_number CHAR(10),
FOREIGN KEY (username) REFERENCES Airline_Staff(username),
PRIMARY KEY (username, staff_number)
);

CREATE TABLE Works_For(
username VARCHAR(255),
airline_name VARCHAR(255),
FOREIGN KEY (airline_name) REFERENCES Airline(airline_name),
FOREIGN KEY (username) REFERENCES Airline_Staff(username),
PRIMARY KEY (airline_name, username)
);


CREATE TABLE Airplane (
airplane_id int,
airline_name VARCHAR(255),
manufacturing_company VARCHAR(255),
model_number int,
manufacturing_date DATE,
FOREIGN KEY (airline_name) REFERENCES Airline(airline_name),
PRIMARY KEY (airplane_id, airline_name)
);


CREATE TABLE Maintenance (
airplane_id int,
airline_name VARCHAR(255),
start_datetime DATETIME,
end_datetime DATETIME,
FOREIGN KEY (airplane_id) REFERENCES Airplane(airplane_id),
FOREIGN KEY (airline_name) REFERENCES Airline(airline_name),
PRIMARY KEY (airplane_id, airline_name, start_datetime, end_datetime)
);


CREATE TABLE Ticket (
ticket_id int,
calculated_ticket_price int,
PRIMARY KEY (ticket_id)
);



CREATE TABLE Airport(
airport_code int PRIMARY KEY,
airport_name VARCHAR(255),
city VARCHAR(255),
country VARCHAR(255),
num_of_terminals int,
airport_type VARCHAR(255)
);

CREATE TABLE Flight(
flight_number int,
departure_datetime DATETIME,
airline_name VARCHAR(255),
arrival_datetime DATETIME,
base_price int,
flight_status VARCHAR(255),
arrival_airport_code int,
departure_airport_code int,
FOREIGN KEY (arrival_airport_code) REFERENCES Airport(airport_code),
FOREIGN KEY (departure_airport_code) REFERENCES Airport(airport_code),
PRIMARY KEY(flight_number, departure_datetime, airline_name)
);


CREATE TABLE Takes(
flight_number int,
departure_datetime DATETIME,
airline_name VARCHAR(255),
email VARCHAR(255),
comment VARCHAR(255),
rating int,
FOREIGN KEY (flight_number, departure_datetime, airline_name) REFERENCES Flight(flight_number, departure_datetime, airline_name),
PRIMARY KEY (flight_number, departure_datetime, email, airline_name)
);

CREATE TABLE Customer(
email VARCHAR(255) REFERENCES Takes(email),
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


CREATE TABLE Purchases(
email VARCHAR(255),
ticket_id int,
name_on_card VARCHAR(255),
card_number VARCHAR(255),
card_type VARCHAR(255),
purchase_datetime DATETIME,
card_expiration_date DATE,
FOREIGN KEY (email) REFERENCES Customer(email),
PRIMARY KEY (email, ticket_id)
);

CREATE TABLE Customer_Phone_Number(
email VARCHAR(255),
customer_number int NOT NULL,
FOREIGN KEY (email) REFERENCES Customer(email),
PRIMARY KEY (email, customer_number)
);


CREATE TABLE Ticket_Of_Flight(
ticket_id int,
departure_datetime DATETIME,
flight_number int,
airline_name VARCHAR(255),
FOREIGN KEY (ticket_id) REFERENCES Ticket(ticket_id),
FOREIGN KEY (flight_number, departure_datetime, airline_name) REFERENCES Flight(flight_number, departure_datetime, airline_name),
PRIMARY KEY (ticket_id, departure_datetime, flight_number, airline_name)
);
