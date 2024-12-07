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

@app.route('/')
def hello():
	return render_template('index.html')


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
    phone_number = request.form['phone_number']

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
        
        # Insert into Customer_Phone_Number table
        ins_phone = '''
        INSERT INTO Customer_Phone_Number (
            email, customer_number
        ) VALUES (%s, %s)
        '''
        cursor.execute(ins_phone, (email, phone_number))
        
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
    email = request.form['email']
    phone_number = request.form['phone_number']

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
    ins_staff = '''
    INSERT INTO Airline_Staff (
        username, thepassword, airline_name, first_name, last_name, date_of_birth
    ) VALUES (%s, %s, %s, %s, %s, %s)
    '''
    try:
        cursor.execute(ins_staff, (
            username, hashed_password, airline_name, first_name, last_name, date_of_birth
        ))

        # Insert the staff email into the Staff_Email table
        ins_email = '''
        INSERT INTO Staff_Email (username, staff_mail)
        VALUES (%s, %s)
        '''
        cursor.execute(ins_email, (username, email))

        # Insert the staff phone number into the Staff_Phone_Number table
        ins_phone = '''
        INSERT INTO Staff_Phone_Number (username, staff_number)
        VALUES (%s, %s)
        '''
        cursor.execute(ins_phone, (username, phone_number))

        # Commit the transaction
        conn.commit()
    except Exception as e:
        conn.rollback()
        error = f"An error occurred: {e}"
        return render_template('staff_register.html', error=error)
    finally:
        cursor.close()

    return redirect(url_for('hello'))


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


@app.route('/search-flights1', methods=['GET'])
def searchFlights1():
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

        # Execute query to fetch departure flights
        cursor = conn.cursor()

        # Fetch departure flights
        departure_query = '''
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
            a2.city AS destination_city,
            ap.number_of_seats
        FROM 
            Flight AS f
        JOIN 
            Airport AS a1 ON f.departure_airport_code = a1.airport_code
        JOIN 
            Airport AS a2 ON f.arrival_airport_code = a2.airport_code
        JOIN 
            Airplane AS ap ON f.airplane_id = ap.airplane_id
        WHERE 
            a1.airport_name = %s
            AND a2.airport_name = %s
            AND DATE(f.departure_datetime) = %s
        '''
        cursor.execute(departure_query, (source_airport, destination_airport, departure_date))
        departure_flights = cursor.fetchall()

        # Calculate adjusted price for departure flights
        for flight in departure_flights:
            ticket_count_query = '''
            SELECT COUNT(*) AS tickets_sold
            FROM Ticket
            WHERE flight_number = %s AND departure_datetime = %s AND airline_name = %s
            '''
            cursor.execute(ticket_count_query, (flight['flight_number'], flight['departure_datetime'], flight['airline_name']))
            tickets_sold = cursor.fetchone()['tickets_sold']

            capacity = flight['number_of_seats']
            if tickets_sold >= 0.8 * capacity:
                flight['calculated_price'] = int(round(flight['base_price'] * 1.25, 2))
            else:
                flight['calculated_price'] = flight['base_price']

        # Fetch return flights if return_date is provided
        return_flights = []
        if return_date:
            return_query = '''
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
                a2.city AS destination_city,
                ap.number_of_seats
            FROM 
                Flight AS f
            JOIN 
                Airport AS a1 ON f.departure_airport_code = a1.airport_code
            JOIN 
                Airport AS a2 ON f.arrival_airport_code = a2.airport_code
            JOIN 
                Airplane AS ap ON f.airplane_id = ap.airplane_id
            WHERE 
                a1.airport_name = %s
                AND a2.airport_name = %s
                AND DATE(f.departure_datetime) = %s
            '''
            cursor.execute(return_query, (destination_airport, source_airport, return_date))
            return_flights = cursor.fetchall()

            # Calculate adjusted price for return flights
            for flight in return_flights:
                ticket_count_query = '''
                SELECT COUNT(*) AS tickets_sold
                FROM Ticket
                WHERE flight_number = %s AND departure_datetime = %s AND airline_name = %s
                '''
                cursor.execute(ticket_count_query, (flight['flight_number'], flight['departure_datetime'], flight['airline_name']))
                tickets_sold = cursor.fetchone()['tickets_sold']

                capacity = flight['number_of_seats']
                if tickets_sold >= 0.8 * capacity:
                    flight['calculated_price'] = int(round(flight['base_price'] * 1.25, 2))
                else:
                    flight['calculated_price'] = flight['base_price']

        cursor.close()

        return render_template(
            'search_results.html',
            departure_flights=departure_flights,
            return_flights=return_flights
        )

    except Exception as e:
        print(f"Error during flight search: {e}")
        return f"An error occurred during flight search: {e}", 500

@app.route('/purchase-process', methods=['POST'])
def purchase_process():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('/'))

    # Debug: Log form data received
    print("Form Data Received for Purchase Process:", request.form)

    # Extract and log flight details
    flight_details = {
        'flight_number': request.form.get('flight_number'),
        'departure_datetime': request.form.get('departure_datetime'),
        'calculated_price': request.form.get('calculated_price'),
        'airline_name': request.form.get('airline_name'),  # Make sure this is included
        'departure_airport': request.form.get('departure_airport'),
        'destination_airport': request.form.get('destination_airport'),
    }
    
    print("Flight Details Sent to Template:", flight_details)

    # Render the purchase form
    return render_template('purchase_process.html', flight_details=flight_details)

@app.route('/finalize-purchase', methods=['POST'])
def finalize_purchase():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        # Log incoming form data
        print("Form Data Received:", request.form)

        # Extract form data
        email = session.get('username')
        flight_number = request.form.get('flight_number')
        departure_datetime = request.form.get('departure_datetime')
        calculated_price = (request.form.get('calculated_price')) # here
        airline_name = request.form.get('airline_name')
        name_on_card = request.form.get('name_on_card')
        card_number = request.form.get('card_number')
        card_type = request.form.get('card_type')
        card_expiration_date = request.form.get('card_expiration_date')
        passenger_first_name = request.form.get('passenger_first_name')
        passenger_last_name = request.form.get('passenger_last_name')
        passenger_birth_date = request.form.get('passenger_birth_date')

        # Validate required fields
        required_fields = [flight_number, departure_datetime, calculated_price, airline_name,
                           name_on_card, card_number, card_type, card_expiration_date,
                           passenger_first_name, passenger_last_name, passenger_birth_date]
        if any(field is None for field in required_fields):
            return "Missing required fields. Please check your input.", 400

        # Parse date fields
        from datetime import datetime
        departure_datetime = datetime.strptime(departure_datetime, '%Y-%m-%d %H:%M:%S')
        card_expiration_date = datetime.strptime(card_expiration_date, '%Y-%m-%d').date()
        passenger_birth_date = datetime.strptime(passenger_birth_date, '%Y-%m-%d').date()

        # Check if flight exists
        cursor = conn.cursor()
        flight_check_query = '''
        SELECT f.*, a.number_of_seats
        FROM Flight f
        JOIN Airplane a ON f.airplane_id = a.airplane_id
        WHERE f.flight_number = %s AND f.departure_datetime = %s AND LOWER(f.airline_name) = LOWER(%s)
        '''
        cursor.execute(flight_check_query, (flight_number, departure_datetime, airline_name))
        flight = cursor.fetchone()
        if not flight:
            return "Flight does not exist. Please verify your input.", 400

        # Check seat availability
        ticket_count_query = '''
        SELECT COUNT(*) AS tickets_sold
        FROM Ticket
        WHERE flight_number = %s AND departure_datetime = %s AND LOWER(airline_name) = LOWER(%s)
        '''
        cursor.execute(ticket_count_query, (flight_number, departure_datetime, airline_name))
        tickets_sold = cursor.fetchone()['tickets_sold']
        if tickets_sold >= flight['number_of_seats']:
            return "No seats available for this flight.", 400

        # Insert ticket into Ticket table
        insert_ticket_query = '''
        INSERT INTO Ticket (
            flight_number, departure_datetime, airline_name, calculated_ticket_price
        ) VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(insert_ticket_query, (flight_number, departure_datetime, airline_name, calculated_price))

        # Retrieve the auto-generated ticket_id
        ticket_id = cursor.lastrowid

        # Insert purchase details into Purchases table
        insert_purchase_query = '''
        INSERT INTO Purchases (
            ticket_id, email, name_on_card, card_number, card_type, 
            purchase_datetime, card_expiration_date, passenger_first_name, 
            passenger_last_name, passenger_birthofdate
        ) VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s)
        '''
        cursor.execute(insert_purchase_query, (
            ticket_id, email, name_on_card, card_number, card_type,
            card_expiration_date, passenger_first_name, passenger_last_name, passenger_birth_date
        ))

        # Commit transaction
        conn.commit()

        # Prepare flight details for the success page
        flight_details = {
            "flight_number": flight_number,
            "airline_name": airline_name,
            "departure_airport": request.form.get('departure_airport', 'Unknown'),
            "destination_airport": request.form.get('destination_airport', 'Unknown'),
            "departure_datetime": departure_datetime,
            "calculated_price": calculated_price,
        }

        # Redirect to purchase success page
        return render_template(
            'purchase_success.html',
            flight=flight_details,
            passenger_name=f"{passenger_first_name} {passenger_last_name}",
            payment_method=card_type
        )

    except Exception as e:
        print(f"Error during finalize purchase: {e}")
        return f"An error occurred: {e}", 500

    finally:
        try:
            cursor.close()
        except Exception as close_error:
            print(f"Error closing cursor: {close_error}")
            
@app.route('/view-my-flights', methods=['GET'])
def view_my_flights():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    email = session['username']  # Retrieve the logged-in user's email
    try:
        cursor = conn.cursor()

        # Fetch the user's purchased flights that are in the future
        query = '''
        SELECT 
            t.flight_number,
            t.departure_datetime,
            t.airline_name,
            t.calculated_ticket_price,
            p.passenger_first_name,
            p.passenger_last_name,
            p.card_type,
            t.ticket_id
        FROM 
            Ticket AS t
        JOIN 
            Purchases AS p ON t.ticket_id = p.ticket_id
        WHERE 
            p.email = %s AND t.departure_datetime > NOW()
        ORDER BY 
            t.departure_datetime;
        '''
        cursor.execute(query, (email,))
        flights = cursor.fetchall()

        cursor.close()

        # Render the view_my_flights.html template with the fetched data
        return render_template('view_my_flights.html', flights=flights)

    except Exception as e:
        print(f"Error fetching flights: {e}")
        return "An error occurred while fetching your flights.", 500

@app.route('/cancel-trip', methods=['POST'])
def cancel_trip():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        cursor = conn.cursor()
        email = session['username']  # Logged-in user's email
        ticket_id = request.form['ticket_id']  # Ticket ID from the form

        # Step 1: Verify the ticket belongs to the logged-in user and is in the future
        verify_ticket_query = '''
        SELECT t.ticket_id, t.departure_datetime
        FROM Ticket t
        JOIN Purchases p ON t.ticket_id = p.ticket_id
        WHERE p.email = %s AND t.ticket_id = %s
        '''
        cursor.execute(verify_ticket_query, (email, ticket_id))
        ticket = cursor.fetchone()

        if not ticket:
            return "Invalid ticket or ticket does not belong to you.", 400

        from datetime import datetime, timedelta
        if ticket['departure_datetime'] <= datetime.now() + timedelta(hours=24):
            return "You cannot cancel a trip less than 24 hours before departure.", 400

        # Step 2: Remove ticket from `Purchases` and make it available again
        delete_purchase_query = 'DELETE FROM Purchases WHERE ticket_id = %s AND email = %s'
        cursor.execute(delete_purchase_query, (ticket_id, email))

        # Commit the changes
        conn.commit()

        return redirect(url_for('view_my_flights'))

    except Exception as e:
        print(f"Error during cancellation: {e}")
        return f"An error occurred while canceling the trip: {e}", 500

    finally:
        try:
            cursor.close()
        except Exception as e:
            print(f"Error closing cursor: {e}")


@app.route('/rate-flights', methods=['GET'])
def rate_flights():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    email = session['username']

    try:
        cursor = conn.cursor()

        # Fetch flights that the user has taken (past flights)
        query = '''
        SELECT 
            t.ticket_id,
            t.flight_number,
            t.airline_name,
            f.departure_datetime,
            f.arrival_datetime,
            t.calculated_ticket_price,
            f.flight_status
        FROM 
            Ticket AS t
        JOIN 
            Purchases AS p ON t.ticket_id = p.ticket_id
        JOIN 
            Flight AS f ON t.flight_number = f.flight_number AND t.departure_datetime = f.departure_datetime AND t.airline_name = f.airline_name
        WHERE 
            p.email = %s AND f.departure_datetime < NOW()
        '''
        cursor.execute(query, (email,))
        flights = cursor.fetchall()
        cursor.close()

        # Render the flights to a review page
        return render_template('rate_flights.html', flights=flights)

    except Exception as e:
        print(f"Error fetching completed flights for rating: {e}")
        return "An error occurred while fetching your completed flights.", 500

@app.route('/submit-rating', methods=['POST'])
def submit_rating():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        # Log incoming form data for debugging
        print("Form Data Received:", request.form)

        # Extract data from the form
        ticket_id = request.form.get('ticket_id')
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        # Validate inputs
        if not ticket_id or not rating or not comment:
            print("Missing required form fields.")
            return "Invalid input. Please ensure all fields are filled out.", 400

        # Log extracted data
        print(f"Ticket ID: {ticket_id}, Rating: {rating}, Comment: {comment}")

        cursor = conn.cursor()

        # Validate ticket exists and belongs to the logged-in user
        email = session['username']
        ticket_validation_query = '''
        SELECT t.flight_number, t.departure_datetime, t.airline_name
        FROM Ticket t
        JOIN Purchases p ON t.ticket_id = p.ticket_id
        WHERE t.ticket_id = %s AND p.email = %s
        '''
        cursor.execute(ticket_validation_query, (ticket_id, email))
        ticket = cursor.fetchone()

        if not ticket:
            print("Ticket validation failed: Ticket does not belong to the user or does not exist.")
            return "Invalid ticket. Please ensure the ticket belongs to you.", 400

        # Log ticket details for debugging
        print("Validated Ticket Details:", ticket)

        # Check if the rating already exists
        check_rating_query = '''
        SELECT *
        FROM Takes
        WHERE flight_number = %s AND departure_datetime = %s AND email = %s AND airline_name = %s
        '''
        cursor.execute(check_rating_query, (
            ticket['flight_number'], ticket['departure_datetime'], email, ticket['airline_name']
        ))
        existing_rating = cursor.fetchone()

        if existing_rating:
            print("Rating already exists. Updating instead of inserting.")
            # Update the existing rating
            update_rating_query = '''
            UPDATE Takes
            SET comment = %s, rating = %s
            WHERE flight_number = %s AND departure_datetime = %s AND email = %s AND airline_name = %s
            '''
            cursor.execute(update_rating_query, (
                comment, rating, ticket['flight_number'], ticket['departure_datetime'], email, ticket['airline_name']
            ))
        else:
            print("No existing rating. Inserting a new one.")
            # Insert a new rating
            insert_rating_query = '''
            INSERT INTO Takes (
                flight_number, departure_datetime, airline_name, email, comment, rating
            ) VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_rating_query, (
                ticket['flight_number'], ticket['departure_datetime'], ticket['airline_name'],
                email, comment, rating
            ))

        # Commit transaction
        conn.commit()

        # Log success message
        print("Rating submitted successfully.")
        return redirect(url_for('rate_flights'))

    except Exception as e:
        print(f"Error submitting rating: {e}")
        return f"An error occurred while submitting your rating: {e}", 500

    finally:
        try:
            cursor.close()
        except Exception as close_error:
            print(f"Error closing cursor: {close_error}")
            

@app.route('/track-spending', methods=['GET'])
def track_spending():
   if 'username' not in session:
       return redirect(url_for('login'))  # Ensure user is logged in


   email = session['username']  # Get logged-in user's email


   try:
       cursor = conn.cursor()


       # Query for total spending in the past year
       year_query = '''
       SELECT SUM(calculated_ticket_price) AS total_spent
       FROM Ticket
       JOIN Purchases ON Ticket.ticket_id = Purchases.ticket_id
       WHERE Purchases.email = %s AND Purchases.purchase_datetime >= DATE_SUB(NOW(), INTERVAL 1 YEAR);
       '''
       cursor.execute(year_query, (email,))
       total_spent_year = cursor.fetchone()['total_spent'] or 0


       # Query for month-wise spending in the last 6 months
       months_query = '''
       SELECT DATE_FORMAT(Purchases.purchase_datetime, '%%Y-%%m') AS month,
              SUM(calculated_ticket_price) AS total_spent
       FROM Ticket
       JOIN Purchases ON Ticket.ticket_id = Purchases.ticket_id
       WHERE Purchases.email = %s AND Purchases.purchase_datetime >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
       GROUP BY month
       ORDER BY month DESC;
       '''
       cursor.execute(months_query, (email,))
       month_data = cursor.fetchall()


       return render_template(
           'track_spending.html',
           total_spent_year=total_spent_year,
           month_data=month_data,
           total_spent_range=None,
           range_data=None,
           start_date=None,
           end_date=None
       )


   except Exception as e:
       print(f"Error in track_spending: {e}")
       return f"An error occurred while processing your request: {e}", 500


   finally:
       cursor.close()




@app.route('/track-spending-range', methods=['POST'])
def track_spending_range():
   if 'username' not in session:
       return redirect(url_for('login'))  # Ensure user is logged in


   email = session['username']  # Get logged-in user's email


   try:
       start_date = request.form.get('start_date')
       end_date = request.form.get('end_date')


       # Validate input dates
       if not start_date or not end_date:
           return "Invalid date range specified.", 400


       cursor = conn.cursor()


       # Query for total spending in the custom date range
       range_query = '''
       SELECT SUM(calculated_ticket_price) AS total_spent
       FROM Ticket
       JOIN Purchases ON Ticket.ticket_id = Purchases.ticket_id
       WHERE Purchases.email = %s AND Purchases.purchase_datetime BETWEEN %s AND %s;
       '''
       cursor.execute(range_query, (email, start_date, end_date))
       total_spent_range = cursor.fetchone()['total_spent'] or 0


       # Query for month-wise spending in the custom date range
       range_month_query = '''
       SELECT DATE_FORMAT(Purchases.purchase_datetime, '%%Y-%%m') AS month,
              SUM(calculated_ticket_price) AS total_spent
       FROM Ticket
       JOIN Purchases ON Ticket.ticket_id = Purchases.ticket_id
       WHERE Purchases.email = %s AND Purchases.purchase_datetime BETWEEN %s AND %s
       GROUP BY month
       ORDER BY month DESC;
       '''
       cursor.execute(range_month_query, (email, start_date, end_date))
       range_data = cursor.fetchall()


       # Return custom range results
       return render_template(
           'track_spending_range.html',
           total_spent_range=total_spent_range,
           range_data=range_data,
           start_date=start_date,
           end_date=end_date
       )


   except Exception as e:
       print(f"Error in track_spending_range: {e}")
       return f"An error occurred while processing your request: {e}", 500


   finally:
       cursor.close()
      



#STAFF

@app.route('/viewFlights', methods=['GET', 'POST'])
def viewFlights():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('hello'))

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
        return redirect(url_for('hello'))

    return render_template('staff_page.html')



@app.route('/changeFlightStatus', methods=['GET', 'POST'])
def changeFlightStatus():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('hello'))

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
        return render_template('index.html')

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



@app.route('/viewFrequentCustomers', methods=['GET', 'POST'])
def viewFrequentCustomers():
    if 'username' not in session or session['user_type'] != 'staff':
        return redirect(url_for('loginStaff'))

    airline_name = session.get('airline_name')  # Get airline name from session
    cursor = conn.cursor()

    if request.method == 'GET':
        # Query to find the most frequent customer in the last year
        query_frequent_customer = '''
        SELECT t.email, COUNT(t.flight_number) AS flight_count
        FROM Takes AS t
        JOIN Flight AS f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name
        WHERE f.airline_name = %s AND t.departure_datetime > DATE_SUB(NOW(), INTERVAL 1 YEAR)
        GROUP BY t.email
        ORDER BY flight_count DESC
        LIMIT 1
        '''
        cursor.execute(query_frequent_customer, (airline_name,))
        frequent_customer = cursor.fetchone()

        return render_template('view_frequent_customers.html', frequent_customer=frequent_customer)

    elif request.method == 'POST':
        # Retrieve the email of the customer from the form
        customer_email = request.form['customer_email']

        # Query to list all flights taken by the specific customer on this airline
        query_customer_flights = '''
        SELECT f.flight_number, f.departure_datetime, f.arrival_datetime, 
               a1.airport_name AS departure_airport, a2.airport_name AS arrival_airport
        FROM Takes AS t
        JOIN Flight AS f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name
        JOIN Airport AS a1 ON f.departure_airport_code = a1.airport_code
        JOIN Airport AS a2 ON f.arrival_airport_code = a2.airport_code
        WHERE t.email = %s AND f.airline_name = %s
        ORDER BY f.departure_datetime DESC
        '''
        cursor.execute(query_customer_flights, (customer_email, airline_name))
        customer_flights = cursor.fetchall()

        return render_template('customer_flights.html', customer_email=customer_email, flights=customer_flights)

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



app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)