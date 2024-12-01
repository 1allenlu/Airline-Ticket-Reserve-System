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

#Authenticates the login
# @app.route('/loginAuth', methods=['GET', 'POST'])
# def loginAuth():
# 	#grabs information from the forms
# 	username = request.form['username']
# 	password = request.form['password']

# 	#cursor used to send queries
# 	cursor = conn.cursor()
# 	#executes query
# 	query = 'SELECT * FROM Customer WHERE email = %s AND thepassword = %s'
# 	cursor.execute(query, (username, password))
# 	#stores the results in a variable
# 	data = cursor.fetchone()
# 	#use fetchall() if you are expecting more than 1 data row
# 	cursor.close()
# 	error = None
# 	if(data):
# 		#creates a session for the the user
# 		#session is a built in
# 		session['username'] = username
# 		return redirect(url_for('customer_page'))
# 	else:
# 		#returns an error message to the html page
# 		error = 'Invalid login or username'
# 		return render_template('login.html', error=error)

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
    # Get form data
    source_city = request.args.get('source-city')
    source_airport = request.args.get('departure-airport')
    destination_city = request.args.get('destination-city')
    destination_airport = request.args.get('destination-airport')
    departure_date = request.args.get('departure-date')
    return_date = request.args.get('return-date')

    # Construct the query
    cursor = conn.cursor()
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
    FROM l
        Flight AS f
    JOIN 
        Airport AS a1 ON f.departure_airport_code = a1.airport_code
    JOIN 
        Airport AS a2 ON f.arrival_airport_code = a2.airport_code
    WHERE 
        a1.city = %s AND a1.airport_name = %s
        AND a2.city = %s AND a2.airport_name = %s
        AND f.departure_datetime >= %s
    '''
    # If return date is provided, add it to the query (optional)
    params = [source_city, source_airport, destination_city, destination_airport, departure_date]
    if return_date:
        query += " AND return_date = %s"
        params.append(return_date)

    # Execute the query
    cursor.execute(query, params)
    flights = cursor.fetchall()
    cursor.close()

    # Pass results to the template
    return render_template('search_results.html', flights=flights)
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
