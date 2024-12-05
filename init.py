#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from hashlib import md5
import pymysql.cursors
from datetime import datetime, timedelta

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='127.0.0.1',
                       port=8889,
                       user='root',
                       password='root',
                       db='airline_ticket_db',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

# #Define route for login
# @app.route('/login')
# def login():
# 	return render_template('login.html')

#Define route for register
@app.route('/register1')
def register():
	return render_template('customer_register.html')

@app.route('/login1Auth', methods=['POST'])
def login1Auth():
    # Collect form data
    email = request.form['email']
    password = request.form['password']
    hashed_password = md5(password.encode()).hexdigest()

    cursor = conn.cursor()

    # Query for customer login
    query = 'SELECT * FROM Customer WHERE email = %s AND thepassword = %s'
    cursor.execute(query, (email, hashed_password))
    customer_data = cursor.fetchone()
    cursor.close()

    if customer_data:
        # Login successful
        session['username'] = email
        session['user_type'] = 'customer'
        return redirect(url_for('customer_page'))
    else:
        # Login failed
        error = "Invalid customer login credentials"
        return render_template('index.html', error=error)
    

@app.route('/login2Auth', methods=['POST'])
def login2Auth():
    # Collect form data
    username = request.form['username']
    password = request.form['password']
    hashed_password = md5(password.encode()).hexdigest()

    cursor = conn.cursor()

    # Query for staff login
    query = 'SELECT * FROM Airline_Staff WHERE username = %s AND thepassword = %s'
    cursor.execute(query, (username, hashed_password))
    staff_data = cursor.fetchone()
    cursor.close()

    if staff_data:
        # Login successful
        session['username'] = username
        session['user_type'] = 'staff'
        session['airline_name'] = staff_data['airline_name']  # Store airline name in session
        return render_template('staff_page.html')
    else:
        # Login failed
        error = "Invalid staff login credentials"
        return render_template('index.html', error=error)


#Authenticates the register
@app.route('/register1Auth', methods=['POST'])
def register1Auth():
    # Collect form data
    email = request.form['email']
    thepassword = request.form['thepassword']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    building_num = request.form['building_num']
    street_name = request.form['street_name']
    apt_num = request.form['apt_num']
    city = request.form['city']
    state_name = request.form['state_name']
    zip_code = request.form['zip_code']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    date_of_birth = request.form['date_of_birth']

    hashed_password = md5(thepassword.encode()).hexdigest()


    cursor = conn.cursor()
    query = 'SELECT * FROM Customer WHERE email = %s'
    cursor.execute(query, (email,))
    data = cursor.fetchone()
    error = None

    if data:
        error = "This customer already exists"
        return render_template('customer_register.html', error=error)
    else:
        ins = '''
        INSERT INTO Customer (
            email, thepassword, first_name, last_name, building_num, street_name, apt_num,
            city, state_name, zip_code, passport_number, passport_expiration,
            passport_country, date_of_birth
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(ins, (
            email, hashed_password, first_name, last_name, building_num, street_name, apt_num,
            city, state_name, zip_code, passport_number, passport_expiration,
            passport_country, date_of_birth
        ))
        conn.commit()
        cursor.close()
        return redirect(url_for('hello'))


@app.route('/register2Auth', methods=['POST'])
def register2Auth():
    # Collect form data
    username = request.form['username']
    thepassword = request.form['thepassword']
    airline_name = request.form['airline_name']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']

    # Hash the password
    hashed_password = md5(thepassword.encode()).hexdigest()

    cursor = conn.cursor()

    # Check if the username already exists
    query = 'SELECT * FROM Airline_Staff WHERE username = %s'
    cursor.execute(query, (username,))
    data = cursor.fetchone()
    error = None

    if data:
        error = "This staff already exists"
        return render_template('staff_register.html', error=error)
    
    # Ensure the airline exists
    query_airline = 'SELECT * FROM Airline WHERE airline_name = %s'
    cursor.execute(query_airline, (airline_name,))
    airline_data = cursor.fetchone()

    if not airline_data:
        error = "Airline does not exist"
        return render_template('staff_register.html', error=error)
    
    # Insert the new airline staff
    ins = '''
    INSERT INTO Airline_Staff (
        username, thepassword, airline_name, first_name, last_name, date_of_birth
    ) VALUES (%s, %s, %s, %s, %s, %s)
    '''
    try:
        cursor.execute(ins, (
            username, hashed_password, airline_name, first_name, last_name, date_of_birth
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        error = f"An error occurred: {e}"
        return render_template('staff_register.html', error=error)
    finally:
        cursor.close()

    return redirect(url_for('hello'))

@app.route('/home')
def home():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

	
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor()
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.route('/customerpage')
def customer_page():
    return render_template('customer_page.html')

@app.route('/staff_page')
def staff_page():
    return render_template('staff_page.html')

@app.route('/customer_register')
def customer_register():
    return render_template('customer_register.html')

@app.route('/staff_register')
def staff_register():
    return render_template('staff_register.html')

@app.route('/search-flights', methods=['GET'])
def searchFlights():
    # Validate required inputs
    source_airport = request.args.get('departure-airport')
    destination_airport = request.args.get('destination-airport')
    departure_date = request.args.get('departure-date')
    return_date = request.args.get('return-date')

    if not all([source_airport, destination_airport, departure_date]):
        return "Required fields are missing.", 400

    try:
        # Parse dates
        from datetime import datetime
        departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date() if return_date else None

        # Construct query and parameters
        query = '''
        SELECT 
            f.flight_number,
            f.airline_name,
            f.departure_datetime,
            f.arrival_datetime,
            f.base_price,
            f.flight_status,
            a1.airport_name AS departure_airport,
            a1.city AS departure_city,
            a2.airport_name AS destination_airport,
            a2.city AS destination_city
        FROM 
            Flight AS f
        JOIN 
            Airport AS a1 ON f.departure_airport_code = a1.airport_code
        JOIN 
            Airport AS a2 ON f.arrival_airport_code = a2.airport_code
        WHERE 
            a1.airport_name = %s
            AND a2.airport_name = %s
            AND DATE(f.departure_datetime) >= %s
        '''
        params = [source_airport, destination_airport, departure_date]

        if return_date:
            query += " AND DATE(f.departure_datetime) <= %s"
            params.append(return_date)

        # Execute query
        cursor = conn.cursor()
        cursor.execute(query, params)
        flights = cursor.fetchall()
        cursor.close()

        return render_template('search_results.html', flights=flights)

    except Exception as e:
        print(f"Error during flight search: {e}")
        return "An error occurred during flight search."

@app.route('/purchase-ticket', methods=['POST'])
def purchase_ticket():
    # Check if the user is logged in
    customer_email = session.get('username')  # Customer email is stored in the session
    if not customer_email:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Get flight details from the form
    flight_number = request.form['flight_number']
    departure_datetime = request.form['departure_datetime']
    base_price = request.form['base_price']

    # Insert the ticket into the database
    cursor = conn.cursor()
    try:
        # Check if the flight exists
        query = 'SELECT * FROM Flight WHERE flight_number = %s AND departure_datetime = %s'
        cursor.execute(query, (flight_number, departure_datetime))
        flight = cursor.fetchone()
        if not flight:
            return "Flight not found", 404

        # Insert ticket into the Ticket table
        insert_ticket_query = '''
        INSERT INTO Ticket (customer_email, flight_number, purchase_date, price)
        VALUES (%s, %s, NOW(), %s)
        '''
        cursor.execute(insert_ticket_query, (customer_email, flight_number, base_price))
        conn.commit()

        return render_template('purchase_success.html', flight=flight)
    except Exception as e:
        print("Error during ticket purchase:", e)
        return "An error occurred while purchasing the ticket.", 500
    finally:
        cursor.close()
  
# @app.route('/purchase-process', methods=['POST'])
# def purchase_process():
#     # Get flight details from the form
#     flight_details = {
#         'flight_number': request.form['flight_number'],
#         'departure_datetime': request.form['departure_datetime'],
#         'base_price': request.form['base_price'],
#         'airline_name': request.form['airline_name'],
#         'departure_airport': request.form['departure_airport'],
#         'destination_airport': request.form['destination_airport'],
#     }

#     # Ensure the user is logged in
#     customer_email = session.get('username')
#     if not customer_email:
#         return redirect(url_for('index'))  # Redirect to login if not logged in

#     # Pass flight details to the template
#     return render_template('purchase_process.html', flight_details=flight_details)

# @app.route('/purchase-process', methods=['POST'])
# def purchase_process():
#     # Ensure the user is logged in
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     # Get flight details from the form
#     flight_details = {
#         'flight_number': request.form['flight_number'],
#         'departure_datetime': request.form['departure_datetime'],
#         'base_price': request.form['base_price'],
#         'airline_name': request.form['airline_name'],
#         'departure_airport': request.form['departure_airport'],
#         'destination_airport': request.form['destination_airport'],
#     }

#     # Pass flight details to the template
#     return render_template('purchase_process.html', flight_details=flight_details)


@app.route('/purchase-process', methods=['POST'])
def purchase_process():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get flight details from the form (hidden inputs)
    flight_details = {
        'flight_number': request.form['flight_number'],
        'departure_datetime': request.form['departure_datetime'],
        'base_price': request.form['base_price'],
        'airline_name': request.form['airline_name'],
        'departure_airport': request.form['departure_airport'],
        'destination_airport': request.form['destination_airport'],
    }

    # Pass flight details to the purchase form
    return render_template('purchase_process.html', flight_details=flight_details)

# @app.route('/finalize-purchase', methods=['POST'])
# def finalize_purchase():
#     # Get purchase details from the form
#     flight_number = request.form['flight_number']
#     departure_datetime = request.form['departure_datetime']
#     base_price = request.form['base_price']
#     passenger_name = request.form['passenger_name']
#     payment_method = request.form['payment_method']

#     # Ensure the user is logged in
#     customer_email = session.get('username')
#     if not customer_email:
#         return redirect(url_for('login'))  # Redirect to login if not logged in

#     # Insert the ticket into the database
#     cursor = conn.cursor()
#     try:
#         # Check if the flight exists
#         query = 'SELECT * FROM Flight WHERE flight_number = %s AND departure_datetime = %s'
#         cursor.execute(query, (flight_number, departure_datetime))
#         flight = cursor.fetchone()
#         if not flight:
#             return "Flight not found", 404

#         # Insert ticket into the Ticket table
#         insert_ticket_query = '''
#         INSERT INTO PURCHASE (customer_email, flight_number, passenger_name, purchase_date, price, payment_method)
#         VALUES (%s, %s, %s, NOW(), %s, %s)
#         '''
#         cursor.execute(insert_ticket_query, (customer_email, flight_number, passenger_name, base_price, payment_method))
#         conn.commit()

#         return render_template('purchase_success.html', flight=flight, passenger_name=passenger_name)
#     except Exception as e:
#         print("Error during ticket purchase:", e)
#         return "An error occurred while purchasing the ticket.", 500
#     finally:
#         cursor.close()

# @app.route('/finalize-purchase', methods=['POST'])
# def finalize_purchase():
#     # Ensure the user is logged in
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     # Get data from the form
#     email = session['customer_email'] 
#     name_on_card = request.form['name_on_card']
#     card_number = request.form['card_number']
#     card_type = request.form['card_type']
#     card_expiration_date = request.form['card_expiration_date']
#     passenger_first_name = request.form['passenger_first_name']
#     passenger_last_name = request.form['passenger_last_name']
#     passenger_birth_date = request.form['passenger_birth_date']

#     try:
#         # Insert purchase data into the `purchase` table
#         cursor = conn.cursor()

#         # Construct the SQL INSERT query
#         insert_purchase_query = '''
#         INSERT INTO PURCHASE (
#             email, name_on_card, card_number, card_type, 
#             purchase_datetime, card_expiration_date, passenger_first_name, 
#             passenger_last_name, passenger_birthdate
#         )
#         VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s, %s)
#         '''

#         # Execute the query with provided data
#         cursor.execute(insert_purchase_query, (
#             email, name_on_card, card_number, card_type, 
#             card_expiration_date, passenger_first_name, 
#             passenger_last_name, passenger_birth_date
#         ))
#         # Commit the transaction
#         conn.commit()

#         # Redirect to the success page
#         return render_template('purchase_success.html', flight_number=flight_number)

#     except Exception as e:
#         print(f"Error during purchase: {e}")
#         return "An error occurred while processing your purchase.", 500

#     finally:
#         # Close the cursor
#         cursor.close()

@app.route('/finalize-purchase', methods=['POST'])
def finalize_purchase():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    # Extract purchase details
    email = session['customer_email'] 
    flight_number = request.form['flight_number']
    departure_datetime = request.form['departure_datetime']
    base_price = request.form['base_price']
    airline_name = request.form['airline_name']
    name_on_card = request.form['name_on_card']
    card_number = request.form['card_number']
    card_type = request.form['card_type']
    card_expiration_date = request.form['card_expiration_date']
    passenger_first_name = request.form['passenger_first_name']
    passenger_last_name = request.form['passenger_last_name']
    passenger_birth_date = request.form['passenger_birth_date']

    try:
        cursor = conn.cursor()

        # Step 1: Insert into the `Ticket` table
        insert_ticket_query = '''
        INSERT INTO Ticket (
            calculated_ticket_price, airline_name, departure_datetime, flight_number
        ) VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(insert_ticket_query, (base_price, airline_name, departure_datetime, flight_number))

        # Get the generated ticket_id
        ticket_id = cursor.lastrowid

        # Step 2: Insert into the `Purchases` table
        insert_purchase_query = '''
        INSERT INTO Purchases (
            ticket_id, email, name_on_card, card_number, card_type, 
            purchase_datetime, card_expiration_date, passenger_first_name, 
            passenger_last_name, passenger_birthofdate
        )
        VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s)
        '''
        cursor.execute(insert_purchase_query, (
            ticket_id, email, name_on_card, card_number, card_type,
            card_expiration_date, passenger_first_name, 
            passenger_last_name, passenger_birth_date
        ))

        # Commit the transaction
        conn.commit()

        # Redirect to the success page
        return render_template('purchase_success.html', ticket_id=ticket_id)

    except Exception as e:
        print(f"Error during purchase: {e}")
        return "An error occurred while processing your purchase.", 500

    finally:
        cursor.close()

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)



@app.route('/viewFlights', methods=['GET', 'POST'])
def viewFlights():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    airline_name = session.get('airline_name')  # Assume staff's airline name is stored in the session
    cursor = conn.cursor()

    # Default view: Next 30 days
    if request.method == 'GET':
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)

        query = '''
        SELECT f.*, a1.airport_name AS departure_airport, a2.airport_name AS arrival_airport
        FROM Flight AS f
        JOIN Airport AS a1 ON f.departure_airport_code = a1.airport_code
        JOIN Airport AS a2 ON f.arrival_airport_code = a2.airport_code
        WHERE f.airline_name = %s
        AND f.departure_datetime BETWEEN %s AND %s
        '''
        cursor.execute(query, (airline_name, start_date, end_date))
        flights = cursor.fetchall()
        cursor.close()

        return render_template('view_flights.html', flights=flights)

    # Custom filters
    elif request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        departure_airport = request.form.get('departure_airport', None)
        arrival_airport = request.form.get('arrival_airport', None)

        query = '''
        SELECT f.*, a1.airport_name AS departure_airport, a2.airport_name AS arrival_airport
        FROM Flight AS f
        JOIN Airport AS a1 ON f.departure_airport_code = a1.airport_code
        JOIN Airport AS a2 ON f.arrival_airport_code = a2.airport_code
        WHERE f.airline_name = %s
        AND f.departure_datetime BETWEEN %s AND %s
        '''
        params = [airline_name, start_date, end_date]

        if departure_airport:
            query += " AND a1.airport_name = %s"
            params.append(departure_airport)

        if arrival_airport:
            query += " AND a2.airport_name = %s"
            params.append(arrival_airport)

        cursor.execute(query, tuple(params))
        flights = cursor.fetchall()
        cursor.close()

        return render_template('view_flights.html', flights=flights)
    
@app.route('/createFlight', methods=['GET', 'POST'])
def createFlight():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    if request.method == 'POST':
        airline_name = session.get('airline_name')  # Get airline name from session
        flight_number = request.form['flight_number']
        departure_datetime = request.form['departure_datetime']
        arrival_datetime = request.form['arrival_datetime']
        departure_airport_code = request.form['departure_airport_code']
        arrival_airport_code = request.form['arrival_airport_code']
        airplane_id = request.form['airplane_id']
        base_price = request.form['base_price']
        status = "on-time"

        cursor = conn.cursor()

        # Check if the airplane belongs to the logged-in staff's airline
        airplane_query = '''
        SELECT * FROM Airplane WHERE airplane_id = %s AND airline_name = %s
        '''
        cursor.execute(airplane_query, (airplane_id, airline_name))
        airplane = cursor.fetchone()

        if not airplane:
            cursor.close()
            return render_template('create_flight.html', message="Error: The selected airplane does not belong to your airline.")

        # Check if the airplane is under maintenance during the flight period
        maintenance_query = '''
        SELECT * FROM Maintenance
        WHERE airplane_id = %s AND airline_name = %s
        AND (start_datetime <= %s AND end_datetime >= %s)
        '''
        cursor.execute(maintenance_query, (airplane_id, airline_name, arrival_datetime, departure_datetime))
        maintenance = cursor.fetchone()

        if maintenance:
            cursor.close()
            return render_template('create_flight.html', message="Error: The selected airplane is under maintenance during the specified flight period.")

        # Proceed to create the flight
        flight_query = '''
        INSERT INTO Flight (flight_number, departure_datetime, airline_name, airplane_id,
        base_price, flight_status, arrival_airport_code, departure_airport_code, arrival_datetime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        try:
            cursor.execute(flight_query, (
                flight_number, departure_datetime, airline_name, airplane_id, base_price,
                status, arrival_airport_code, departure_airport_code, arrival_datetime
            ))
            conn.commit()
            message = "Flight created successfully!"
        except Exception as e:
            conn.rollback()
            message = f"Error creating flight: {e}"
        finally:
            cursor.close()

        return render_template('create_flight.html', message=message)

    return render_template('create_flight.html')


@app.route('/staffHome')
def staffHome():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    return render_template('staff_page.html')



@app.route('/changeFlightStatus', methods=['GET', 'POST'])
def changeFlightStatus():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    if request.method == 'POST':
        flight_number = request.form['flight_number']
        new_status = request.form['new_status']
        airline_name = session.get('airline_name')  # Ensure airline name is retrieved from the session
        
        cursor = conn.cursor()

        # Handle delayed status with optional new departure time
        if new_status == "delayed":
            delay_minutes = int(request.form.get('delay_minutes', 0))  # Retrieve delay in minutes
            query = '''
            UPDATE Flight
            SET flight_status = %s, departure_datetime = DATE_ADD(departure_datetime, INTERVAL %s MINUTE)
            WHERE flight_number = %s AND airline_name = %s
            '''
            params = (new_status, delay_minutes, flight_number, airline_name)
        else:
            query = '''
            UPDATE Flight
            SET flight_status = %s
            WHERE flight_number = %s AND airline_name = %s
            '''
            params = (new_status, flight_number, airline_name)

        try:
            cursor.execute(query, params)
            conn.commit()
            message = "Flight status updated successfully!"
        except Exception as e:
            conn.rollback()
            message = f"Error updating flight status: {e}"
        finally:
            cursor.close()

        return render_template('change_flight_status.html', message=message)

    return render_template('change_flight_status.html')

@app.route('/addAirplane', methods=['GET', 'POST'])
def addAirplane():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    airline_name = session.get('airline_name')  # Retrieve airline name from session

    if request.method == 'POST':
        airplane_id = request.form['airplane_id']
        manufacturing_company = request.form['manufacturing_company']
        model_number = request.form['model_number']
        manufacturing_date = request.form['manufacturing_date']
        number_of_seats = request.form['number_of_seats']

        cursor = conn.cursor()

        # Insert new airplane
        insert_query = '''
        INSERT INTO Airplane (airplane_id, airline_name, manufacturing_company, model_number, manufacturing_date, number_of_seats)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        try:
            cursor.execute(insert_query, (airplane_id, airline_name, manufacturing_company, model_number, manufacturing_date, number_of_seats))
            conn.commit()
            message = "Airplane added successfully!"
        except Exception as e:
            conn.rollback()
            message = f"Error adding airplane: {e}"
        finally:
            cursor.close()

        # Redirect to confirmation page to display all airplanes
        return redirect(url_for('confirmAddAirplane', message=message))

    return render_template('add_airplane.html')

@app.route('/confirmAddAirplane')
def confirmAddAirplane():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    airline_name = session.get('airline_name')  # Retrieve airline name from session
    cursor = conn.cursor()

    # Fetch all airplanes owned by the airline
    query = '''
    SELECT * FROM Airplane WHERE airline_name = %s
    '''
    cursor.execute(query, (airline_name,))
    airplanes = cursor.fetchall()
    cursor.close()

    # Render confirmation page with all airplanes
    message = request.args.get('message', '')
    return render_template('confirm_add_airplane.html', airplanes=airplanes, message=message)

@app.route('/addAirport', methods=['GET', 'POST'])
def addAirport():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    if request.method == 'POST':
        airport_code = request.form['airport_code']
        airport_name = request.form['airport_name']
        city = request.form['city']
        country = request.form['country']
        num_of_terminals = request.form['num_of_terminals']
        airport_type = request.form['airport_type']

        cursor = conn.cursor()
        query = '''
        INSERT INTO Airport (airport_code, airport_name, city, country, num_of_terminals, airport_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        try:
            cursor.execute(query, (airport_code, airport_name, city, country, num_of_terminals, airport_type))
            conn.commit()
            message = "Airport added successfully!"
        except Exception as e:
            conn.rollback()
            message = f"Error adding airport: {e}"
        finally:
            cursor.close()

        return render_template('add_airport.html', message=message)

    return render_template('add_airport.html')


@app.route('/viewFlightRatings', methods=['GET'])
def viewFlightRatings():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    airline_name = session.get('airline_name')
    cursor = conn.cursor()
    query = '''
    SELECT f.flight_number, AVG(t.rating) AS average_rating, GROUP_CONCAT(t.comment SEPARATOR '; ') AS comments
    FROM Flight AS f
    LEFT JOIN Takes AS t ON f.flight_number = t.flight_number AND f.airline_name = t.airline_name
    WHERE f.airline_name = %s
    GROUP BY f.flight_number
    '''
    cursor.execute(query, (airline_name,))
    ratings = cursor.fetchall()
    cursor.close()

    return render_template('view_flight_ratings.html', ratings=ratings)


    
@app.route('/scheduleMaintenance', methods=['GET', 'POST'])
def scheduleMaintenance():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    if request.method == 'POST':
        airplane_id = request.form['airplane_id']
        start_datetime = request.form['start_datetime']
        end_datetime = request.form['end_datetime']
        airline_name = session.get('airline_name')

        cursor = conn.cursor()
        query = '''
        INSERT INTO Maintenance (airplane_id, airline_name, start_datetime, end_datetime)
        VALUES (%s, %s, %s, %s)
        '''
        try:
            cursor.execute(query, (airplane_id, airline_name, start_datetime, end_datetime))
            conn.commit()
            message = "Maintenance scheduled successfully!"
        except Exception as e:
            conn.rollback()
            message = f"Error scheduling maintenance: {e}"
        finally:
            cursor.close()

        return render_template('schedule_maintenance.html', message=message)

    return render_template('schedule_maintenance.html')



@app.route('/viewFrequentCustomers', methods=['GET'])
def viewFrequentCustomers():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    airline_name = session.get('airline_name')
    cursor = conn.cursor()
    query = '''
    SELECT t.email, COUNT(t.flight_number) AS flight_count
    FROM Takes AS t
    JOIN Flight AS f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name
    WHERE f.airline_name = %s AND t.departure_datetime > NOW() - INTERVAL 1 YEAR
    GROUP BY t.email
    ORDER BY flight_count DESC
    LIMIT 1
    '''
    cursor.execute(query, (airline_name,))
    frequent_customer = cursor.fetchone()
    cursor.close()

    return render_template('view_frequent_customers.html', frequent_customer=frequent_customer)


@app.route('/viewRevenue', methods=['GET'])
def viewRevenue():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    airline_name = session.get('airline_name')
    cursor = conn.cursor()

    # Query to calculate revenue for the last month
    query_month = '''
    SELECT SUM(t.calculated_ticket_price) AS revenue_last_month
    FROM Ticket AS t
    JOIN Purchases AS p ON t.ticket_id = p.ticket_id
    WHERE t.airline_name = %s
    AND p.purchase_datetime BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW()
    '''

    # Query to calculate revenue for the last year
    query_year = '''
    SELECT SUM(t.calculated_ticket_price) AS revenue_last_year
    FROM Ticket AS t
    JOIN Purchases AS p ON t.ticket_id = p.ticket_id
    WHERE t.airline_name = %s
    AND p.purchase_datetime BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()
    '''

    try:
        cursor.execute(query_month, (airline_name,))
        revenue_last_month = cursor.fetchone()['revenue_last_month'] or 0

        cursor.execute(query_year, (airline_name,))
        revenue_last_year = cursor.fetchone()['revenue_last_year'] or 0

    except Exception as e:
        cursor.close()
        return render_template('view_revenue.html', error=f"Error fetching revenue data: {e}")

    cursor.close()

    return render_template('view_revenue.html',
                           revenue_last_month=revenue_last_month,
                           revenue_last_year=revenue_last_year)