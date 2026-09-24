import requests
from flask import Flask, request, render_template , session
import psycopg2
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

load_dotenv()
database_url = os.environ.get("DATABASE_URL")
app.secret_key = os.environ.get("SECRET_KEY")

def is_logged_in():
    return "user_id" in session

@app.route("/register" , methods = ["POST"])
def register():
    check_if_exists = ["username" , "password"]
    data = request.json
    if all(key in data for key in check_if_exists):
        username = data["username"]
        password = data["password"]
        password_hash = generate_password_hash(password)
        
        try:
            connections = psycopg2.connect(database_url)
            cursor = connections.cursor()
            cursor.execute("INSERT INTO users (username , password_hash) VALUES(%s, %s);" , (username, password_hash))
            
            connections.commit()
            cursor.close()
            connections.close()
            
            return f"User {username} has been registered" , 200
        
        except psycopg2.OperationalError:
            return "Gateway Server Timeout", 504
    else:
        return "Missing required fields", 400
    
@app.route("/register-form", methods = ["GET"])
def register_form():
    return render_template("register.html")

@app.route("/submit-register-form", methods = ["POST"])
def submit_register_form():
    username = request.form["username"]
    password = request.form["password"]
    password_hash = generate_password_hash(password)
    
    try:
        connections = psycopg2.connect(database_url)
        cursor = connections.cursor()
        cursor.execute("INSERT INTO users (username , password_hash) VALUES(%s ,%s);" , (username , password_hash)) 
        
        connections.commit()
        cursor.close()
        connections.close()
        return "User registered"
    
    except psycopg2.OperationalError:
        return "Gateway Server Error", 500
    
    
@app.route("/login" , methods = ["POST"])
def login():
    data = request.json
    check_if_exist = ["username" , "password"]
    if all(key in data for key in check_if_exist):
        username = data["username"]
        password = data["password"]
        
        try:
            connections = psycopg2.connect(database_url)
            cursor = connections.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s ;" , (username,))
            
            result = cursor.fetchone()
            cursor.close()
            connections.close()
            
            if result:
                check = check_password_hash(result[2] , password)
                if check:
                    session["user_id"] = result[0]
                    return "login successful"
                else:
                    return "Invalid details", 401
            else:
                return "Not found"
            
        except psycopg2.OperationalError:
            return "Gateway Server Timeout",504
        
@app.route("/login-form" , methods = ["GET"])
def login_form():
    return render_template("user_login.html")
    
@app.route("/submit-login-form" , methods = ["POST"])
def submit_login_form():
    username = request.form["username"]
    password = request.form["password"]
    
    try:
                connections = psycopg2.connect(database_url)
                cursor = connections.cursor()
                cursor.execute("SELECT * FROM users WHERE username = %s ;" , (username,))
                
                result = cursor.fetchone()
                cursor.close()
                connections.close()
                
                if result:
                    check = check_password_hash(result[2] , password)
                    if check:
                        session["user_id"] = result[0]
                        return "login successful"
                    else:
                        return "Invalid details", 401
                else:
                    return "Username not found"    
    except psycopg2.OperationalError:
                return "Gateway Server Timeout",504
    
    

    
        
        
        

@app.route("/" , methods = ["GET"])
def index():
    if is_logged_in():
        try:
            connections = psycopg2.connect(database_url)
            cursor = connections.cursor()
            
            current_userid = session['user_id']
            cursor.execute(" SELECT id, habit, frequency, streak FROM habittracker WHERE userid = %s; " , (current_userid,))

            rows = cursor.fetchall()
            
            cursor.close()
            connections.close()
            
            lines = []
            for row in rows:
                id_habit = row[0]
                habit = row[1]
                frequency = row[2]
                streak = row[3]
                
                lines.append( f"{id_habit}. {habit} (frequency)={frequency} (streak)={streak}\n")

            return "\n".join(lines)
        except psycopg2.OperationalError:
                        return "Gateway Server Timeout",504
            
        
    else:
        return "Please log in", 401


@app.route("/add-habit", methods =["POST"])
def add_habit():
    if not is_logged_in():
        return "Please log in ", 401
    data = request.json
    
    habit = data["habit"]
    frequency = data["frequency"]
    streak = data["streak"]
    current_user_id = session['user_id']
    try:
        connections = psycopg2.connect(database_url)   
        cursor = connections.cursor()
        cursor.execute("""INSERT INTO habittracker
                       (habit, frequency, streak, userid) 
                       VALUES (%s, %s, %s, %s);""", 
                       (habit, frequency, streak, current_user_id))
        
        connections.commit()
        cursor.close()
        connections.close()
        
        return f'{habit} added'
    
    except psycopg2.OperationalError:
                    return "Gateway Server Timeout",504
        

@app.route("/add-habit-form" , methods = ['GET'])
def add_habit_form():
    return render_template('add_habit.html')

@app.route("/submit-habit" , methods = ["POST"])
def submit_habit():
    if not is_logged_in():
        return "Please log in",401
    
    habit = request.form['habit']
    frequency = request.form['frequency']
    streak = float(request.form['streak'])
    current_user_id = session['user_id']
    
    try:
        connections = psycopg2.connect(database_url)
        cursor = connections.cursor()
        cursor.execute("""
                       INSERT INTO habittracker (habit, frequency, streak, userid) 
                       VALUES(%s, %s, %s, %s);"""
                       , (habit, frequency, streak, current_user_id))

        connections.commit()
        cursor.close()
        connections.close()
        
        return f'{habit} submitted'
    
    except psycopg2.OperationalError:
                    return "Gateway Server Timeout",504
        

@app.route("/update-habit/<int:id>" , methods = ['PUT'])
def update_habit(id):
    if not is_logged_in():
        return "Please log in ", 401
    
    data = request.json
    habit = data["habit"]
    streak = data["streak"]
    frequency = data["frequency"]
    current_user_id  = session['user_id']
    
    try:
        connections = psycopg2.connect(database_url)
        cursor = connections.cursor()
        cursor.execute("UPDATE habittracker SET habit = %s, frequency = %s, streak = %s WHERE id =%s AND userid = %s ;" ,  (habit, frequency, streak, id , current_user_id))
        
        connections.commit()
        cursor.close()
        connections.close()
        
        return f'{habit} updated'
    
    except psycopg2.OperationalError:
                    return "Gateway Server Timeout",504
        


@app.route("/delete/<int:id>" , methods = ["DELETE"])
def delete(id):
    if not is_logged_in():
        return "Please log in", 401
    
    
    try:
        connections = psycopg2.connect(database_url)
        cursor = connections.cursor()
        
        current_user_id = session['user_id']
        cursor.execute("DELETE FROM habittracker WHERE id = %s  AND userid = %s;" , (id, current_user_id))
        connections.commit()
        cursor.close()
        connections.close()
        
        return f'{id} deleted'
    
    except psycopg2.OperationalError:
                    return "Gateway Server Timeout",504
        
    
if __name__ == "__main__":
    app.run(debug = True)
    
    

