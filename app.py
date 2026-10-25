from binascii import Error
import uuid
import pymysql
from flask import Flask, jsonify, render_template, request
from flask import Flask, render_template, request, redirect, url_for, session ,flash
from dbconnection import get_db_connection
# import mysql.connector
import threading

import os




app = Flask(__name__)
app.secret_key = 'a8f5f167f44f4964e6c998dee827110c' 







@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template("signup.html")


#route for sign up user

@app.route('/signup_user', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Input validation
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return render_template('signup.html')

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if username or email already exists
            cursor.execute("SELECT * FROM users WHERE user_name = %s OR email = %s", (username, email))
            user_exists = cursor.fetchone()

            if user_exists:
                flash("Username already exists!", "error")
                return render_template('signup.html')
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email))
            user_email = cursor.fetchone()

            if user_email:
                flash("email aderss already exists!", "error")
                return render_template('signup.html')

            # Insert new user into the database
            query = "INSERT INTO users (name, email, user_name, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (fullname, email, username, password))
            connection.commit()

            flash("Account created successfully! Please log in.", "success")
            return redirect('/')  # Redirect to the login page

        except OSError as err:
            print(f"Error: {err}")
            flash("An error occurred. Please try again later.", "error")
            return render_template('signup.html')

        finally:
            cursor.close()
            connection.close()

    # Render the signup form for GET requests
    return render_template('login.html')



#route for user_login
@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username =='chetan@123' and password == 'Pass@1234':

            





            return render_template('admin.html')
            
        



        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # connection = get_db_connection()
            # cursor = connection.cursor(dictionary=True)

            # Query the database for the user by username
            cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
            user = cursor.fetchone()

            if user:
                # Check if the provided password matches the hashed password in the database
                # if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    # User is authenticated, create a session
                if  password == user[4]:
                    session['user_id'] = user[0]
                    session['username'] = user[3]
                    # "Login successful!", "success")
                    name = user[1]
                    return redirect('/home' )  # Redirect to the home page or a dashboard
                else:
                    flash("Incorrect password. Please try again.", "error")
                    return redirect('/')  # Reload login page
            else:
                flash("Username not found. Please try again.", "error")
                return redirect('/')  # Reload login page

        except OSError as err:
            print(f"Error: {err}")
            flash("An error occurred. Please try again later.", "error")
        
        finally:
            cursor.close()
            connection.close()

    return render_template('login.html')



# Route for the Home Page
@app.route('/home')
def home():

    # username= session['usersname'] 
    
    return render_template('home.html')







# Route for search results
@app.route('/search_buses', methods=['GET'])
def search():
    source = request.args.get('from')
    destination = request.args.get('to')
    date = request.args.get('date')
    
    
    connection = get_db_connection()
    cursor = connection.cursor()
    # sql = "SELECT * FROM buses WHERE source = %s AND destination = %s " 
    # val = ("pune", "mumbai")  
    
    query = "SELECT * FROM buses WHERE d_loction = %s AND a_location = %s AND d_dt >= %s  AND available_seats >= %s "
          
    cursor.execute(query, (source, destination, date, 0))
    
    try:
       
        
        buses = cursor.fetchall() 
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return e
          
    finally:
        cursor.close()
        connection.close()
    
    return render_template('search_results.html', buses=buses)




# @app.route('/booking1/<int:bus_id>')
# def booking1(bus_id):

    # username= session['usersname']

    connection = get_db_connection()
    cursor = connection.cursor()
    # sql = "SELECT * FROM buses WHERE source = %s AND destination = %s " 
    # val = ("pune", "mumbai")  
    
    query = "SELECT * FROM buses WHERE d_loction = %s AND a_location = %s AND d_dt >= %s  "
          
    cursor.execute(query, (source, destination, date))
    
    try:
       
        
        buses = cursor.fetchall() 
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return e
          
    finally:
        cursor.close()
        connection.close()
    
    return render_template('search_results.html', buses=buses)



#it goto passenger page
@app.route('/booking1/<int:bus_id>')
def booking1(bus_id):

    bus_id = bus_id

    connection = get_db_connection()
    cursor = connection.cursor()
    # sql = "SELECT * FROM buses WHERE source = %s AND destination = %s " 
    # val = ("pune", "mumbai")  
    
    query = "SELECT price FROM buses WHERE bus_id = %s  "
          
    cursor.execute(query,bus_id)
    
    try:
       
        
         result = cursor.fetchone() 
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return e
          
    finally:
        cursor.close()
        connection.close()

    
    price = float(result[0])
    print(price)
    
    return render_template('passenget.html', price = price, bus_id = bus_id)




# @app.route('/save_booking', methods=['POST'])
# def save_passenger_details():



    try:
        # Fetch data from the form
        data = request.json
        bus_id = data['bus_id']
        travel_date = data['travel_date']
        departure_time = data['departure_time']
        total_price = data['total_price']
        passengers = data['passengers']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert booking data
        cursor.execute("""
            INSERT INTO bookings (user_id, bus_id, travel_date, departure_time, total_price)
            VALUES (%s, %s, %s, %s, %s)
        """, (1, bus_id, travel_date, departure_time, total_price))
        booking_id = cursor.lastrowid

        # Insert passenger data
        for passenger in passengers:
            cursor.execute("""
                INSERT INTO passengers (booking_id, name, age, gender)
                VALUES (%s, %s, %s, %s)
            """, (booking_id, passenger['name'], passenger['age'], passenger['gender']))

        connection.commit()
        return jsonify({'status': 'success', 'booking_id': booking_id})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/save_booking', methods=['POST'])
def save_booking():
    # if 'user_id' not in session:
    #     return redirect(url_for('login'))  # Redirect to login if not logged in
    

    # data = request.json
    # tiprice = data.get('totalPriceEl')
    # print(tiprice)
    # submission_id = session.get('submission_id', str(uuid.uuid4()))

    if request.method == 'POST':
        # Process booking form submission
        user_id = session['user_id']
        bus_id = request.form.get('bus_id')
        passengers = []

        passenger_names = request.form.getlist('name')
        passenger_ages = request.form.getlist('age')
        passenger_genders = request.form.getlist('gender')

        for name, age, gender in zip(passenger_names, passenger_ages, passenger_genders):
            passengers.append({
                'name': name,
                'age': int(age),
                'gender': gender
            })

        # Save booking and passenger details in the database
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # qur2 = "select * from reload"
            # cursor.execute(qur)
            # res = cursor.fetchall()

            # if submission_id in res:

            # qur = "insert into reload values(%s)"
            # cursor.execute(qur, submission_id)

           


            # Insert booking record with bus_id
            booking_query = "INSERT INTO bookings (user_id, bus_id) VALUES (%s, %s)"
            cursor.execute(booking_query, (user_id, bus_id))
            booking_id = cursor.lastrowid
            # if booking_id not in data_store:

            seats_no_q = "select available_seats from buses WHERE bus_id = %s"
            cursor.execute(seats_no_q, bus_id)
            seats_no = cursor.fetchone() 
             
            seat =  44 - int(seats_no[0])



            seats_no_q1 = "select price from buses WHERE bus_id = %s"
            cursor.execute(seats_no_q1, bus_id)
            price22 = cursor.fetchone()

            price1 = price22[0]




            # Insert passenger records
            passenger_query = """
                INSERT INTO passengers (booking_id, user_id, name, age, gender, seat_no, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            for passenger in passengers:
                cursor.execute(passenger_query, (booking_id, user_id, passenger['name'], passenger['age'], passenger['gender'], seat, price1 ))

            # Update available seats for the bus
            update_seats_query = "UPDATE buses SET available_seats = available_seats - %s WHERE bus_id = %s"
            cursor.execute(update_seats_query, (len(passengers), bus_id))

            get_bus = "select * from buses where bus_id = %s"
            cursor.execute(get_bus, bus_id)
            bus = cursor.fetchone() 


            get_pa_q = "select * from passengers where booking_id = %s "
            cursor.execute(get_pa_q, booking_id)
            ipassengers = cursor.fetchall() 

            connection.commit()


            # session['booking_id'] = booking_id
            # session['bus'] = bus
            # session['passengers'] = passengers



            # return redirect(url_for('confirmation345'))


            # return redirect(url_for("confirmation.html",booking_id = booking_id, bus = bus, passengers = ipassengers))

            return render_template("confirmation.html",booking_id = booking_id, bus = bus, passengers = ipassengers)

        except Error as err:
            print(f"Database Error: {err}")
            return "An error occurred while processing your booking."
        finally:
            cursor.close()
            connection.close()

        return render_template("confirmation.html",booking_id = booking_id, bus = bus, passengers = ipassengers)

@app.route('/confirmation345')
def confirmation345():
    # booking_id = session.get('booking_id')
    # bus = session.get('bus')
    # passengers = session.get('passengers')
    
    return render_template('confirmation.html')




@app.route('/mybooking')
def mybooking():
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)  # Use DictCursor

        # Fetch user_id from session (assuming user is logged in)
        user_id = session.get('user_id')

        if not user_id:
            return "User not logged in.", 401

        # SQL query to fetch booking and passenger details
        query = """
        SELECT 
            b.booking_id,
            b.bus_id,
            b.travel_date,
            b.departure_time,
            b.total_price,
            b.status,
            b.created_at,
            p.passenger_id,
            p.name AS name,
            p.age AS age,
            p.gender AS gender,
            p.seat_no,
            p.price AS price
        FROM 
            bookings b
        LEFT JOIN 
            passengers p ON b.booking_id = p.booking_id
        WHERE 
            b.user_id = %s;
        """
        cursor.execute(query, (user_id,))
        bookings = cursor.fetchall()

        # Transform data for display
        booking_details = {}
        for row in bookings:
            booking_id = row['booking_id']
            if booking_id not in booking_details:
                booking_details[booking_id] = {
                    'bus_id': row['bus_id'],
                    'travel_date': row['travel_date'],
                    'departure_time': row['departure_time'],
                    'total_price': row['total_price'],
                    'status': row['status'],
                    'created_at': row['created_at'],
                    'passengers': []
                }
            booking_details[booking_id]['passengers'].append({
                'passenger_id': row['passenger_id'],
                'name': row['name'],
                'age': row['age'],
                'gender': row['gender'],
                'seat_no': row['seat_no'],
                'price': row['price']
            })

        return render_template('mybooking.html', bookings=booking_details)

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while fetching booking details."

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


    # return render_template("Mybooking.html",bookings = booking_id, passengers = ipassengers)

    return render_template("Mybooking.html" ,bookings=booking_details)






# @app.route('/payment')
# def payment():
#     booking_id = request.args.get('booking_id')
    
#     # Fetch booking details using booking_id
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("""
#         SELECT * FROM bookings WHERE booking_id = %s
#     """, (booking_id,))
#     booking = cursor.fetchone()

#     # Fetch passenger details
#     cursor.execute("""
#         SELECT * FROM passengers WHERE booking_id = %s
#     """, (booking_id,))
#     passengers = cursor.fetchall()

#     return render_template('payment.html', booking=booking, passengers=passengers)











@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))







#adming



@app.route('/admin1')
def admin_home():



    return render_template('admin.html')





@app.route('/api/buses', methods=['GET'])
def get_buses():
    try:
            connection = get_db_connection()
            cursor = connection.cursor()


            q = "select * from buses"
            cursor.execute(q)
            buses = cursor.fetchall()
            
    except Error as err:
        print(f"Database Error: {err}")
        
    finally:
        cursor.close()
        connection.close()

    return jsonify(buses)



@app.route('/managebuses')
def manage_buses():
   



   try:
            connection = get_db_connection()
            cursor = connection.cursor()

            
            


            # Insert booking record with bus_id
            # query = "select * from bookings where user_id = %s  "
            # cursor.execute(query, id)
            # booking_id = cursor.fetchall() 


            query2 = "select * from passengers where user_id = %s "
            cursor.execute(query2, id)
            ipassengers = cursor.fetchall() 


            q = "select * from buses"
            cursor.execute(q)
            buses = cursor.fetchall()
            
   except Error as err:
        print(f"Database Error: {err}")
        return "An error occurred while processing your booking."
   finally:
        cursor.close()
        connection.close()


   return render_template('manag.html', buses = buses)



# @app.route('/api/buses', methods=['POST'])
# def add_bus():
#     # Add a new bus to the list
#     new_bus = request.json
#     new_bus['id'] = max(bus['id'] for bus in buses) + 1 if buses else 1
#     buses.append(new_bus)
#     return jsonify(new_bus), 201

# @app.route('/api/buses/<int:bus_id>', methods=['PUT'])
# def update_bus(bus_id):
#     # Update bus details
#     updated_data = request.json
#     for bus in buses:
#         if bus['id'] == bus_id:
#             bus.update(updated_data)
#             return jsonify(bus)
#     return jsonify({"error": "Bus not found"}), 404

@app.route('/Delete/<int:bus_id>')
def delete_bus(bus_id):


    


   try:
            connection = get_db_connection()
            cursor = connection.cursor()

            d = "delete from buses where bus_id = %s"
            cursor.execute(d, bus_id)
            connection.commit() 
            




            # q = "select * from buses"
            # cursor.execute(q)
            # buses = cursor.fetchall()
            cursor.execute("select * from buses")
            buses = cursor.fetchall()

            flash('Bus deleted successfully!', 'success')
            return redirect(url_for('manage_buses',buses = buses))  # Redirect to the manage buses page
  
            
   except Error as err:
        print(f"Database Error: {err}")
        return "An error occurred while processing your booking."
   finally:
        cursor.close()
        connection.close()


   return render_template('manag.html', buses = buses)
    



@app.route('/edit/<int:bus_id>')
def update_bus(bus_id):

   try:
            connection = get_db_connection()
            cursor = connection.cursor()

            q = "select * from buses where bus_id = %s"
            cursor.execute(q,bus_id)
            bus = cursor.fetchone()
            
   except Error as err:
        print(f"Database Error: {err}")
        return "An error occurred while processing your booking."
   finally:
        cursor.close()
        connection.close()



   return render_template('edit.html', bus = bus)





# Update bus details
@app.route('/update', methods=['POST'])
def update():

    
    
    id = request.form.get('bus_id')  # Assuming `bus_id` is passed as a hidden field in the form
    bus_name = request.form.get('bus_name')
    from_route = request.form.get('from')
    to_route = request.form.get('to')
    travel_date = request.form.get('date')
    arrival_date = request.form.get('date2')
    seats = request.form.get('seats')
    price = request.form.get('price')

    print(id)
    print("bus id printed...")


    
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        
        # Update bus details
        update_query = " UPDATE buses SET  d_loction = %s, a_location = %s, available_seats = %s, price = %s, d_dt = %s, a_d = %s, bus_name = %s WHERE bus_id = %s "
        cursor.execute(update_query, (from_route, to_route,  seats, price, travel_date, arrival_date , bus_name,id))
        connection.commit()


        q = "select * from buses"
        cursor.execute(q)
        buses = cursor.fetchall()


        
        flash('Bus updated successfully!', 'success')
        return redirect(url_for('manage_buses',buses = buses))  # Redirect to the manage buses page
    except Exception as e:
        connection.rollback()
        return f"An error occurred: {str(e)}", 500
    finally:
        cursor.close()
        connection.close()

    return render_template('manag.html',buses = buses)

@app.route('/addBus1')
def add_bus1():

    return render_template('addBus.html')






@app.route('/addBus', methods=['GET', 'POST'])
def add_bus():
    if request.method == 'POST':
        try:
            # Get form data
            bus_name = request.form['bus_name']
            from_route = request.form['from']
            to_route = request.form['to']
            travel_date = request.form['date']
            arrival_date = request.form['date2']
            seats = int(request.form['seats'])
            price = float(request.form['price'])

            # Connect to MySQL
            connection = get_db_connection()
            cursor = connection.cursor()
           

            # Insert data into database  - , d_dt, a_d, seats, price
            insert_query = "INSERT INTO buses (bus_name, d_loction, a_location) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (bus_name, from_route, to_route))
            connection.commit()
            cursor.execute("select * from buses")
            buses = cursor.fetchall()

            # q = "select * from buses"
            
            
            

            flash('Bus added successfully!', 'success')
            # return render_template('manag.html',buses = buses)
            return redirect(url_for('manage_buses',buses = buses))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('manag.html',buses = buses)




if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
   