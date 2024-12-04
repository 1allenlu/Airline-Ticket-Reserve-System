INSERT INTO Airline VALUES ('Jet Blue');
INSERT INTO Airline VALUES ('American Airlines');

INSERT INTO Airport VALUES (1, 'JFK', 'NYC', 'USA', 5, 'International');
INSERT INTO Airport VALUES (2, 'PVG', 'Shanghai', 'China', 2, 'International');


INSERT INTO Customer VALUES ('dante999@gmail.com', 'hahaha', 'Dante', 'Minasyan', 10, 'Jay Street', 55, 'Brooklyn', 'NY', 11201, 123456789, '2030-01-01', 'Armenia', '2004-12-08');
INSERT INTO Customer VALUES ('vivian0000@gmail.com', 'bibian', 'Vivian', 'Teo', 20, 'Gold Street', 30, 'Irvine', 'CA', 92617, 987654321, '2035-01-01', 'USA', '2005-09-05');
INSERT INTO Customer VALUES ('evannnnn@gmail.com', 'evanevan', 'Evan', 'Dworkin', 30, 'Ray Street', 999, 'San Jose', 'CA', 94088, 543216789, '2026-01-01', 'Taiwan', '2005-08-31');


INSERT INTO Airplane VALUES (123, 'Jet Blue', 'Boeing', '747', '2010-05-05', 100);
INSERT INTO Airplane VALUES (456, 'Jet Blue', 'Boeing', '747', '2015-05-05', 200);
INSERT INTO Airplane VALUES (789, 'Jet Blue', 'Airbus', '220', '2018-05-05', 300);
INSERT INTO Airplane VALUES (999, 'American Airlines', 'Airbus', '220', '2018-05-06', 200);



INSERT INTO Airline_Staff VALUES ('allenlu', 'hahahausofunny0101', 'Jet Blue', 'Allen', 'Lu', '2004-05-26');


INSERT INTO Flight VALUES (100, '2024-11-05 12:05:20', 'Jet Blue', 123, 500, 'On-time', 1, 2, '2024-11-05 14:05:20');
INSERT INTO Flight VALUES (200, '2024-11-12 12:05:20', 'Jet Blue', 123, 400, 'On-time', 1, 2, '2024-11-12 14:05:20');
INSERT INTO Flight VALUES (300, '2024-11-13 12:05:20', 'Jet Blue', 123, 300, 'Delayed', 2, 1, '2024-11-13 14:05:20');
INSERT INTO Flight VALUES (400, '2024-11-14 12:05:20', 'Jet Blue', 123, 300, 'Delayed', 2, 1, '2024-11-14 14:05:20');


INSERT INTO Ticket VALUES (100, 100, '2024-11-05 12:05:20', 'Jet Blue', 500);
INSERT INTO Ticket VALUES (101, 200, '2024-11-12 12:05:20', 'Jet Blue', 510);
INSERT INTO Ticket VALUES (102, 300, '2024-11-13 12:05:20', 'Jet Blue', 520);
INSERT INTO Ticket VALUES (103, 400, '2024-11-14 12:05:20', 'Jet Blue', 530);


INSERT INTO Purchases VALUES (100, 'evannnnn@gmail.com', 'Evan Dworkin', '123123', 'credit', '2024-09-09 10:00:00', '2025-10-10', 'evan', 'dworking', '2005-08-31');
INSERT INTO Purchases VALUES (101, 'dante999@gmail.com', 'Dante Minasyan', '456456', 'debit', '2024-09-09 10:00:00', '2025-10-10', 'dante', 'minas', '2005-12-08');

<!-- Customer's Test Cases -->
INSERT INTO Flight VALUES (300, '2024-12-10 10:00:00', 'Jet Blue', 123, 300, 'Delayed', 1, 2, '2024-12-10 14:00:00');
INSERT INTO Flight VALUES (500, '2024-12-10 08:00:00', 'Jet Blue', 123, 300, 'On-time', 1, 2, '2024-12-10 10:00:00');
INSERT INTO Flight VALUES (600, '2024-12-20 13:00:00', 'Jet Blue', 456, 450, 'Delayed', 2, 1, '2024-12-20 15:00:00');
INSERT INTO Flight VALUES (700, '2024-12-25 07:00:00', 'American Airlines', 999, 550, 'On-time', 1, 2, '2024-12-25 09:00:00');
INSERT INTO Flight VALUES (800, '2025-01-05 14:00:00', 'American Airlines', 999, 400, 'Cancelled', 2, 1, '2025-01-05 16:00:00');

ALTER TABLE Ticket ADD COLUMN is_canceled BOOLEAN DEFAULT FALSE;