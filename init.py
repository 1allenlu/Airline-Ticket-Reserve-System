#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

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

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register1')
def register():
	return render_template('customer_register.html')

@app.route('/loginAuth', methods=['POST'])
def loginAuth():
    # Get the login type (customer or staff)
    login_type = request.form['login_type']
    password = request.form['password']
    cursor = conn.cursor()

    if login_type == 'customer':
        # Customer login uses 'email' field
        email = request.form['email']
        query = 'SELECT * FROM Customer WHERE email = %s AND thepassword = %s'
        cursor.execute(query, (email, password))
        data = cursor.fetchone()
        if data:
            session['username'] = email
            session['user_type'] = 'customer'
            return redirect(url_for('customer_page'))

    elif login_type == 'staff':
        # Airline staff login uses 'username' field
        username = request.form['username']
        query = 'SELECT * FROM Airline_Staff WHERE username = %s AND thepassword = %s'
        cursor.execute(query, (username, password))
        data = cursor.fetchone()
        if data:
            session['username'] = username
            session['user_type'] = 'staff'
            return redirect(url_for('staff_page'))

    cursor.close()

    # If login fails
    error = 'Invalid login credentials'
    return render_template('login.html', error=error)

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
            email, thepassword, first_name, last_name, building_num, street_name, apt_num,
            city, state_name, zip_code, passport_number, passport_expiration,
            passport_country, date_of_birth
        ))
        conn.commit()
        cursor.close()
        return redirect(url_for('hello'))

@app.route('/register2Auth', methods=['GET', 'POST'])
def register2Auth():
	#grabs information from the forms
	username = request.form['username']
	thepassword = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This customer already exists"
		return render_template('customer_register.html', error = error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, %s)'
		cursor.execute(ins, (username, thepassword))
		conn.commit()
		cursor.close()
		return render_template('index.html')

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
	session.pop('username')
	return redirect('/')

@app.route('/customerpage')
def customer_page():
    return render_template('customer_page.html')

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
